from typing import Any, Optional

class Model:
    FRONT_BACK: int = ...
    CLOZE: int = ...
    model_id: Any = ...
    name: Any = ...
    css: Any = ...
    model_type: Any = ...
    def __init__(self, model_id: Optional[Any] = ..., name: Optional[Any] = ..., fields: Optional[Any] = ..., templates: Optional[Any] = ..., css: str = ..., model_type: Any = ...) -> None: ...
    fields: Any = ...
    def set_fields(self, fields: Any) -> None: ...
    templates: Any = ...
    def set_templates(self, templates: Any) -> None: ...
    def to_json(self, now_ts: Any, deck_id: Any): ...