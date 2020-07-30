from .card import Card as Card
from .util import guid_for as guid_for
from typing import Any, Optional

class _TagList(list):
    def __init__(self, tags: Any = ...) -> None: ...
    def __setitem__(self, key: Any, val: Any) -> None: ...
    def append(self, tag: Any) -> None: ...
    def extend(self, tags: Any) -> None: ...
    def insert(self, i: Any, tag: Any) -> None: ...

class Note:
    model: Any = ...
    fields: Any = ...
    def __init__(self, model: Optional[Any] = ..., fields: Optional[Any] = ..., sort_field: Optional[Any] = ..., tags: Optional[Any] = ..., guid: Optional[Any] = ...) -> None: ...
    @property
    def sort_field(self): ...
    @sort_field.setter
    def sort_field(self, val: Any) -> None: ...
    @property
    def tags(self): ...
    @tags.setter
    def tags(self, val: Any) -> None: ...
    def cards(self): ...
    @property
    def guid(self): ...
    @guid.setter
    def guid(self, val: Any) -> None: ...
    def write_to_db(self, cursor: Any, now_ts: Any, deck_id: Any) -> None: ...