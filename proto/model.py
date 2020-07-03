from typing import List, Optional, Generic, TypeVar, Callable

from mypy_extensions import TypedDict

from proto.field import Field

Data = TypeVar("Data")

Template = TypedDict('Template', {
    "name": str,
    "front": str,
    "back": str,
})

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
        self.fields = fields
        self.templates = templates
