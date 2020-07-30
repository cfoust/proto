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
import datetime

from proto.field import FieldResult
from proto.caching import Cache

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


class CachedTransformer(Transform[Data]):
    def __init__(
        self,
        # The database file to use
        database: str,
        # The `type` field that isolates transformers from each other
        identifier: str,
        # The underlying transformer that will be cached
        transformer: Transform[Data],
        # Given Data, gives a unique string key for the input
        key: Callable[[Data], str],
        # If this is set, the cache will be cleared after this amount of time
        # and we will re-pull
        retry_timeout: Optional[datetime.timedelta] = None,
        # Whether to only retry if the outcome was None
        retry_only_on_none: bool = True,
    ) -> None:
        self.transformer = transformer
        self.key = key
        self.cache = Cache(database, identifier)
        self.retry_timeout = retry_timeout
        self.retry_only_on_none = retry_only_on_none

    def call(self, data: Data) -> FieldResult:
        key = self.key(data)
        result = self.cache.retrieve(key)

        if result:
            time, stored = result

            if (
                self.retry_timeout is not None
                and (time + self.retry_timeout) < datetime.datetime.now()
            ):
                if stored is not None and self.retry_only_on_none:
                    return stored

                self.cache.delete(key)
                return self.call(data)

            return stored

        computed = self.transformer.call(data)
        self.cache.store(key, computed)
        return computed


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
