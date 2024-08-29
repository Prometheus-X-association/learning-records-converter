from dataclasses import dataclass
from typing import Any, TypeAlias

JsonType: TypeAlias = dict[str, Any]


@dataclass(frozen=True)
class ValidationResult:
    """
    Represents a result of trace validation against a profile rule.

    This class encapsulates information about a validation result, which can be
    either an error or an unmet recommendation.

    :param rule: The type of rule that was checked (e.g., "presence", "any", "all", "none")
    :param path: The JSONPath location in the trace where the result occurred
    :param expected: The expected value or condition as defined by the rule
    :param actual: The actual value found in the trace
    """

    rule: str
    path: str
    expected: Any
    actual: Any


class ValidationError(ValidationResult):
    """
    Represents an error that occurred during trace validation against a profile rule.
    """


class ValidationRecommendation(ValidationResult):
    """
    Represents a recommended rule in a profile that was not met by the trace.
    """
