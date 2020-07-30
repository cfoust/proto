from typing import List, Optional, Generic, TypeVar, Callable, Tuple
import genanki

from mypy_extensions import TypedDict


from proto.field import Field, FieldResult, Media

Data = TypeVar("Data")

Template = TypedDict("Template", {"name": str, "front": str, "back": str,})


def normalize(data: FieldResult) -> Optional[str]:
    if data is None:
        return None

    if isinstance(data, str):
        return data

    # media
    return data["field"]


class Model(Generic[Data]):
    """
    Represents an individual Anki card model.
    """

    def __init__(
        self,
        id: int,
        name: str,
        guid: Optional[Callable[[Data], str]] = None,
        fields: Optional[List[Field[Data]]] = None,
        templates: Optional[List[Template]] = None,
    ):
        self.id = int
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

    def to_genanki(self, data: List[Data]) -> Tuple[List[genanki.Note], List[Media]]:
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

        return (
            list(map(lambda v: genanki.Note(model=model, fields=v), normalized)),
            media,
        )
