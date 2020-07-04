from mypy_extensions import TypedDict

from typing import (
    Callable,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    TypeVar,
    Union,
    Tuple,
)

Data = TypeVar("Data")

# This is the type all fields must return.
Media = TypedDict("Media", {"filename": str, "data": bytes, "field": str,})
FieldData = Union[str, Media]
FieldResult = Optional[FieldData]
FieldFunction = Callable[[Data], FieldResult]


class Field(Generic[Data]):
    """
    Base class that manages transforming card data for a field.
    """

    def __init__(self, name: str, transform: Callable[[Data], FieldResult]) -> None:
        self.name = name
        self.transform = transform

    def run(self, data: Data) -> FieldResult:
        return self.transform(data)
