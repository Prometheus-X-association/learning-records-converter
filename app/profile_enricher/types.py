from dataclasses import dataclass
from typing import Any, TypeAlias

JsonType: TypeAlias = dict[str, Any]


@dataclass
class ValidationError:
    rule: str
    path: str
    expected: Any
    actual: Any
