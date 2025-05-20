from collections.abc import Iterable, Mapping, Sequence
from typing import TYPE_CHECKING, Any

from app.common.common_types import JsonType
from app.common.models.trace import Trace
from app.infrastructure.logging.contract import LoggerContract
from app.profile_enricher.profiler_types import (
    ValidationError,
    ValidationRecommendation,
    ValidationResult,
)
from app.profile_enricher.profiles.jsonld import (
    PresenceTypeEnum,
    StatementTemplate,
    StatementTemplateRule,
)
from app.profile_enricher.utils.jsonpath import JSONPathUtils

if TYPE_CHECKING:
    from collections.abc import Callable


class TraceValidator:
    """Class responsible for validating traces against templates."""

    def __init__(self, logger: LoggerContract) -> None:
        """Initialize the TraceValidator.

        :param logger: The logger instance for logging operations.
        """
        self.logger = logger
        self.rule_checks: dict[str, Callable[[Iterable[Any], Iterable[Any]], bool]] = {
            "any": self._check_any,
            "all": self._check_all,
            "none": self._check_none,
        }

    def validate_trace(
        self,
        template: StatementTemplate,
        trace: Trace,
    ) -> list[ValidationError]:
        """Validate a trace against a given template.

        :param template: The template to validate against
        :param trace: The trace to validate
        :return: A list of ValidationError objects. An empty list indicates a valid trace
        """
        log_context = {"template": template.id}
        self.logger.debug("Start trace validation", log_context)

        validation_results = self._apply_rules(
            template=template,
            trace=trace,
            rule_types={PresenceTypeEnum.INCLUDED, PresenceTypeEnum.EXCLUDED},
        )
        if not validation_results:
            self.logger.debug("Trace validated successfully", log_context)

        return [ValidationError(**result.__dict__) for result in validation_results]

    def get_recommendations(
        self,
        template: StatementTemplate,
        trace: Trace,
    ) -> list[ValidationRecommendation]:
        """Generate recommendations for a trace based on a given template.

        This method checks the trace against the rules defined in the template
        and generates recommendations for fields that are marked as recommended
        but do not meet the specified criteria.

        :param template: The template to validate against
        :param trace: The trace to validate
        :return: A list of ValidationRecommendation objects
        """
        log_context = {"template": template.id}
        self.logger.debug("Start trace recommendations", log_context)

        validation_results = self._apply_rules(
            template=template,
            trace=trace,
            rule_types={PresenceTypeEnum.RECOMMENDED},
        )

        if not validation_results:
            self.logger.debug("No trace recommendations", log_context)

        return [
            ValidationRecommendation(**result.__dict__) for result in validation_results
        ]

    def _apply_rules(
        self,
        template: StatementTemplate,
        trace: Trace,
        rule_types: set[PresenceTypeEnum],
    ) -> list[ValidationResult]:
        """Apply validation rules to a trace based on a given template and rule types.

        :param template: The StatementTemplate containing the rules to apply
        :param trace: The trace data to validate
        :param rule_types: A set of PresenceTypeEnum values indicating which types of rules to apply
        :return: A list of ValidationResult objects representing the outcome of applying the rules
        """
        if not template.rules:
            return []

        validation_results: list[ValidationResult] = []

        for rule in template.rules:
            # Apply the JSONPath to retrieve the field values to check
            values = self._get_values_for_rule(rule=rule, trace=trace)

            # Validate the rule
            validation_results.extend(
                self._validate_rule(rule=rule, values=values, rule_types=rule_types),
            )

        return validation_results

    def _validate_rule(
        self,
        rule: StatementTemplateRule,
        values: Sequence[Any],
        rule_types: set[PresenceTypeEnum],
    ) -> list[ValidationResult]:
        """Check if a trace follows a specific rule.

        See: https://adlnet.github.io/xapi-profiles/xapi-profiles-communication.html#statement-template-valid.

        :param rule: The rule to check against
        :param values: The extracted values relevant to the rule
        :param rule_types: A set of rule types to check
        :return: List of validation results
        """
        if rule.presence not in rule_types:
            return []

        validation_results: list[ValidationResult] = []
        log_context = {"rule": rule.location, "presence": rule.presence}

        # Check the "included", "excluded" and "recommended" rules
        if (
            rule.presence in {PresenceTypeEnum.INCLUDED, PresenceTypeEnum.RECOMMENDED}
            and not values
        ):
            self.logger.debug("Found rule presence validation", log_context)
            validation_results.append(
                ValidationResult(
                    rule="presence",
                    path=rule.location,
                    expected="included",
                    actual="missing",
                ),
            )
        elif rule.presence == PresenceTypeEnum.EXCLUDED and values:
            self.logger.debug("Found rule presence validation", log_context)
            validation_results.append(
                ValidationResult(
                    rule="presence",
                    path=rule.location,
                    expected="excluded",
                    actual="present",
                ),
            )

        # Check the "any" / "all" / "none" rules
        for check_type, check_method in self.rule_checks.items():
            rule_values = getattr(rule, check_type)
            if rule_values and not check_method(rule_values, values):
                self.logger.debug(
                    "Found rule presence validation",
                    {**log_context, "type": check_type},
                )

                validation_results.append(
                    ValidationResult(
                        rule=check_type,
                        path=rule.location,
                        expected=(
                            f"no values from {rule.none}"
                            if check_type == "none"
                            else rule_values
                        ),
                        actual=values,
                    ),
                )

        return validation_results

    @staticmethod
    def _check_any(any_values: Iterable[Any], values: Iterable[Any]) -> bool:
        """Check if any of the required values are present.

        :param any_values: The required values
        :param values: The values to check
        :return: True if any required value is present, False otherwise
        """
        return any(v in any_values for v in values)

    @staticmethod
    def _check_all(all_values: Iterable[Any], values: Iterable[Any]) -> bool:
        """Check if all the required values are present.

        :param all_values: The required values
        :param values: The values to check
        :return: True if all required values are present, False otherwise
        """
        return all(v in values for v in all_values)

    @staticmethod
    def _check_none(none_values: Iterable[Any], values: Iterable[Any]) -> bool:
        """Check if none of the prohibited values are present.

        :param none_values: The prohibited values
        :param values: The values to check
        :return: True if no prohibited value is present, False otherwise
        """
        return not any(v in none_values for v in values)

    def _get_values_for_rule(
        self,
        rule: StatementTemplateRule,
        trace: Trace,
    ) -> list[Any]:
        """Extract values from the trace that are relevant to a specific rule.

        This method applies the JSONPath specified in the rule to the trace,
        and if a selector is present, further refines the extracted values.

        :param trace: The trace data to extract values from
        :param rule: The StatementTemplateRule specifying how to extract values
        :return: A list of extracted values relevant to the rule
        """
        values = self._apply_jsonpath(data=trace.data, path=rule.location)
        if rule.selector:
            values = self._apply_selector(values=values, selector=rule.selector)
        return values

    @staticmethod
    def _apply_jsonpath(data: JsonType, path: str) -> list[Any]:
        """Apply a JSONPath expression to data and return the results.

        :param data: The data to apply the JSONPath to
        :param path: The JSONPath expression
        :return: The results of applying the JSONPath
        :raises ValueError: If the JSONPath is invalid
        """
        results = JSONPathUtils.parse_jsonpath(path).find(data)
        # Flatten the list if the result is a list of lists
        return [
            item
            for result in results
            for item in (
                result.value if isinstance(result.value, list) else [result.value]
            )
        ]

    def _apply_selector(self, values: Sequence[Any], selector: str) -> list[Any]:
        """Apply a selector to a sequence of values and return the results.

        :param values: The values to apply the selector to
        :param selector: The selector to apply
        :return: The results of applying the selector
        """
        result = []
        for value in values:
            if isinstance(value, Mapping):
                result.extend(self._apply_jsonpath(data=value, path=selector))
        return result
