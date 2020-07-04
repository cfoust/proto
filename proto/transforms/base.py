"""
Transformations are an abstraction for running some computation on inputs and
returning some output. Think of them like functions, but we allow them to have
state.
"""

from functools import reduce
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
    overload,
)

from proto.field import FieldResult

Data = TypeVar("Data")


class Transform(Generic[Data]):
    def __init__(self):
        pass

    def call(self, data: Data) -> FieldResult:
        raise Exception("`call` is not implemented in base class")


def wrap_class(instance: Transform[Data],) -> Callable[[Data], FieldResult]:
    """
    Wrap a class instance into a transform function.
    """
    return lambda data: instance.call(data)


_A = TypeVar("_A")
_B = TypeVar("_B")
_C = TypeVar("_C")
_D = TypeVar("_D")
_E = TypeVar("_E")
_F = TypeVar("_F")
_G = TypeVar("_G")
_H = TypeVar("_H")

# One
@overload
def pipe(steps: Tuple[Callable[[_A], _B]]) -> Callable[[_A], _B]:
    ...


# Two
@overload
def pipe(steps: Tuple[Callable[[_A], _B], Callable[[_B], _C]]) -> Callable[[_A], _C]:
    ...


# Three
@overload
def pipe(
    steps: Tuple[Callable[[_A], _B], Callable[[_B], _C], Callable[[_C], _D],]
) -> Callable[[_A], _D]:
    ...


# Four
@overload
def pipe(
    steps: Tuple[
        Callable[[_A], _B], Callable[[_B], _C], Callable[[_C], _D], Callable[[_D], _E]
    ]
) -> Callable[[_A], _E]:
    ...


# Five
@overload
def pipe(
    steps: Tuple[
        Callable[[_A], _B],
        Callable[[_B], _C],
        Callable[[_C], _D],
        Callable[[_D], _E],
        Callable[[_E], _F],
    ]
) -> Callable[[_A], _F]:
    ...


# Six
@overload
def pipe(
    steps: Tuple[
        Callable[[_A], _B],
        Callable[[_B], _C],
        Callable[[_C], _D],
        Callable[[_D], _E],
        Callable[[_E], _F],
        Callable[[_F], _G],
    ]
) -> Callable[[_A], _G]:
    ...


def pipe(steps):
    return lambda input: reduce(lambda a, b: b(a), steps, input)
