from typing import List, Optional, Generic, TypeVar, Callable, Tuple
import genanki

from mypy_extensions import TypedDict
import progressbar


from proto.field import Field, FieldResult, Media
from proto.transforms import pipe

Data = TypeVar("Data")

Template = TypedDict("Template", {"name": str, "front": str, "back": str,})


def default_guid(value: str) -> str:
    return genanki.util.guid_for(value)


def use_first_guid(value: List[str]) -> str:
    return default_guid(value[0])


def normalize(data: FieldResult) -> Optional[str]:
    if data is None:
        return None

    if isinstance(data, str):
        return data

    # media
    return data["field"]


def filter_rows(
    discard_none: bool,
) -> Callable[[List[List[Optional[str]]]], List[List[Optional[str]]]]:
    return lambda rows: list(
        filter(
            lambda row: not any(map(lambda field: field is None, row))
            or not discard_none,
            rows,
        )
    )


def stringify_rows(rows: List[List[Optional[str]]]) -> List[List[str]]:
    return list(
        map(
            lambda row: list(map(lambda col: col if col is not None else "", row)),
            rows,
        )
    )


ModelReport = List[Tuple[Field[Data], int]]


class Model(Generic[Data]):
    """
    Represents an individual Anki card model.
    """

    def __init__(
        self,
        _id: int,
        name: str,
        guid: Callable[[Data], str],
        fields: Optional[List[Field[Data]]] = None,
        templates: Optional[List[Template]] = None,
        css: Optional[str] = None,
    ):
        self.id = _id
        self.name = name
        self.guid = guid
        self.fields = fields or []
        self.templates = templates or []
        self.css = css

    def build(self, data: List[Data]) -> List[List[Tuple[FieldResult, bool]]]:
        """
        Calculate the values of each field for each row of data.
        """
        fields = self.fields or []
        result = []

        for row in progressbar.progressbar(data):
            result.append(list(map(lambda field: field.run(row), fields)))

        return result

    def to_genanki(
        self, data: List[Data], discard_empty: bool = False
    ) -> Tuple[List[genanki.Note], List[Media], ModelReport]:
        """
        Build this model's cards for the data and translate it into genanki's
        structures.

        Return a list of:
        * genanki.Notes
        * Media files
        * A zipped list of fields and the number of their values that were empty
        """
        results = self.build(data)

        # Need to transform all Media to their normal, string format
        normalized: List[List[Optional[str]]] = []
        media: List[Media] = []

        # Also collect information on empty fields
        nones = [0 for field in self.fields]

        for note in results:
            note_data = [data for data, is_empty in note]
            fixed_note = list(map(normalize, note_data))
            normalized.append(fixed_note)

            nones = [
                a + b
                for a, b in zip(nones, [1 if is_empty else 0 for _, is_empty in note])
            ]

            # Grab all the media
            for field in note_data:
                if field is None or isinstance(field, str):
                    continue
                media.append(field)

        report = list(zip(self.fields, nones))

        # Coerce all fields to strings, filtering out any that came back None
        # (if `discard_empty` is true)
        stringified: List[List[str]] = pipe(
            (filter_rows(discard_empty), stringify_rows,)
        )(normalized)

        model = genanki.Model(
            self.id,
            self.name,
            fields=list(map(lambda v: {"name": v.name}, self.fields)),
            templates=list(
                map(
                    lambda v: {
                        "name": v["name"],
                        "qfmt": v["front"],
                        "afmt": v["back"],
                    },
                    self.templates,
                )
            ),
        )

        if self.css:
            model.css = self.css

        notes: List[genanki.Note] = [
            genanki.Note(model=model, fields=v, due=i)
            for i, v in enumerate(stringified)
        ]

        # To keep guids stable
        for n, value in zip(notes, data):
            n.guid = self.guid(value)

        return (
            notes,
            media,
            report,
        )
