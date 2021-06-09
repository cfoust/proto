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


def default_empty_check(data: Optional[FieldResult]) -> bool:
    """
    Return whether a field appears to be empty.
    """
    return data is None or data == ""


class Field(Generic[Data]):
    """
    Base class that manages transforming card data for a field.
    """

    def __init__(
        self,
        name: str,
        transform: Callable[[Data], FieldResult],
        is_empty: Callable[[Optional[FieldResult]], bool] = default_empty_check,
    ) -> None:
        self.name = name
        self.transform = transform
        self.is_empty = is_empty

    def run(self, data: Data) -> Tuple[FieldResult, bool]:
        result = self.transform(data)
        return (result, self.is_empty(result))
