from typing import List, Optional, Generic, TypeVar, Callable, Tuple
import genanki

from mypy_extensions import TypedDict


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
    ):
        self.id = _id
        self.name = name
        self.guid = guid
        self.fields = fields or []
        self.templates = templates or []

    def build(self, data: List[Data]) -> Optional[List[List[FieldResult]]]:
        fields = self.fields
        if not fields:
            return None

        return list(
            map(lambda row: list(map(lambda field: field.run(row), fields or [])), data)
        )

    def to_genanki(
        self, data: List[Data], discard_none: bool = True
    ) -> Tuple[List[genanki.Note], List[Media]]:
        results = self.build(data)

        if not results:
            return ([], [])

        # Need to transform all Media to their normal, string format
        normalized: List[List[Optional[str]]] = []
        media: List[Media] = []
        for note in results:
            fixed_note = list(map(normalize, note))
            normalized.append(fixed_note)

            # Grab all the media
            for field in note:
                if field is None or isinstance(field, str):
                    continue
                media.append(field)

        # Coerce all fields to strings, filtering out any that came back None
        # (if `discard_none` is true)
        stringified: List[List[str]] = pipe(
            (filter_rows(discard_none), stringify_rows,)
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

        notes: List[genanki.Note] = list(
            map(lambda v: genanki.Note(model=model, fields=v), stringified)
        )

        # To keep guids stable
        for n, value in zip(notes, data):
            n.guid = self.guid(value)

        return (
            notes,
            media,
        )
