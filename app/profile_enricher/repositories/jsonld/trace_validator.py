import logging
from typing import Any, Callable

from app.profile_enricher.profiles.jsonld import (PresenceTypeEnum, StatementTemplate,
                                                  StatementTemplateRule)
from app.profile_enricher.types import (JsonType, ValidationError,
                                        ValidationRecommendation)
from app.profile_enricher.utils.jsonpath import JSONPathUtils

logger = logging.getLogger(__name__)


class TraceValidator:
    """Class responsible for validating traces against templates."""

    def __init__(self):
        self.rule_checks: dict[str, Callable[[list[Any], list[Any]], bool]] = {
            "any": self._check_any,
            "all": self._check_all,
            "none": self._check_none,
        }

    def validate_trace(
        self, template: StatementTemplate, trace: JsonType
    ) -> list[ValidationError]:
        """
        Validate a trace against a given template.

        :param template: The template to validate against
        :param trace: The trace to validate
        :return: A list of ValidationError objects. An empty list indicates a valid trace
        """
        errors: list[ValidationError] = []

        if template.rules:
            for rule in template.rules:
                # Apply the JSONPath to retrieve the field values to check
                values = self._get_values_for_rule(rule=rule, trace=trace)

                rule_errors = self._validate_rule(rule=rule, values=values)
                if rule_errors:
                    logger.debug(f"Trace validation failed for rule: {rule}")
                    errors.extend(rule_errors)
        if not errors:
            logger.debug(
                f"Trace validated successfully against template '{template.id}'"
            )

        return errors

    def get_recommendations(
        self, template: StatementTemplate, trace: JsonType
    ) -> list[ValidationRecommendation]:
        """
        Generate recommendations for a trace based on a given template.

        This method checks the trace against the rules defined in the template
        and generates recommendations for fields that are marked as recommended
        but do not meet the specified criteria.

        :param template: The template to validate against
        :param trace: The trace to validate
        :return: A list of ValidationRecommendation objects
        """
        recommendations: list[ValidationRecommendation] = []

        if template.rules:
            for rule in template.rules:
                # Apply the JSONPath to retrieve the field values to check
                values = self._get_values_for_rule(rule=rule, trace=trace)

                recommendations.extend(
                    self._get_rule_recommendations(rule=rule, values=values)
                )

        return recommendations

    def _validate_rule(
        self, rule: StatementTemplateRule, values: list[Any]
    ) -> list[ValidationError]:
        """
        Check if a trace follows a specific rule.
        See: https://adlnet.github.io/xapi-profiles/xapi-profiles-communication.html#statement-template-valid

        :param rule: The rule to check against
        :param values: The extracted values relevant to the rule
        :return: List of errors
        """
        if rule.presence not in [PresenceTypeEnum.INCLUDED, PresenceTypeEnum.EXCLUDED]:
            return []

        errors: list[ValidationError] = []

        # Check the "included" and "excluded" rules
        if rule.presence == PresenceTypeEnum.INCLUDED and not values:
            errors.append(
                ValidationError(
                    rule="presence",
                    path=rule.location,
                    expected="included",
                    actual="missing",
                )
            )
        elif rule.presence == PresenceTypeEnum.EXCLUDED and values:
            errors.append(
                ValidationError(
                    rule="presence",
                    path=rule.location,
                    expected="excluded",
                    actual="present",
                )
            )

        # Check the "any" / "all" / "none" rules
        for check_type, check_method in self.rule_checks.items():
            rule_values = getattr(rule, check_type)
            if rule_values and not check_method(rule_values, values):
                errors.append(
                    ValidationError(
                        rule=check_type,
                        path=rule.location,
                        expected=(
                            f"no values from {rule.none}"
                            if check_type == "none"
                            else rule_values
                        ),
                        actual=values,
                    )
                )

        return errors

    def _get_rule_recommendations(
        self, rule: StatementTemplateRule, values: list[Any]
    ) -> list[ValidationRecommendation]:
        """
        Generate recommendations for a specific rule based on the extracted values.

        This method checks if the rule is recommended and if the values meet
        the criteria specified by the rule. It generates appropriate
        recommendations if the criteria are not met.

        :param rule: The rule to check against
        :param values: The extracted values relevant to the rule
        :return: A list of ValidationRecommendation objects
        """
        if rule.presence != PresenceTypeEnum.RECOMMENDED:
            return []

        recommendations: list[ValidationRecommendation] = []

        if not values:
            recommendations.append(
                ValidationRecommendation(
                    rule="presence",
                    path=rule.location,
                    expected="included",
                    actual="missing",
                )
            )
        else:
            for check_type, check_method in self.rule_checks.items():
                rule_values = getattr(rule, check_type)
                if rule_values and not check_method(rule_values, values):
                    recommendations.append(
                        ValidationRecommendation(
                            rule=check_type,
                            path=rule.location,
                            expected=(
                                f"no values from {rule.none}"
                                if check_type == "none"
                                else rule_values
                            ),
                            actual=values,
                        )
                    )

        return recommendations

    @staticmethod
    def _check_any(any_values: list[Any], values: list[Any]) -> bool:
        """
        Check if any of the required values are present.

        :param any_values: The required values
        :param values: The values to check
        :return: True if any required value is present, False otherwise
        """
        return any(v in any_values for v in values)

    @staticmethod
    def _check_all(all_values: list[Any], values: list[Any]) -> bool:
        """
        Check if all the required values are present.

        :param all_values: The required values
        :param values: The values to check
        :return: True if all required values are present, False otherwise
        """
        return all(v in values for v in all_values)

    @staticmethod
    def _check_none(none_values: list[Any], values: list[Any]) -> bool:
        """
        Check if none of the prohibited values are present.

        :param none_values: The prohibited values
        :param values: The values to check
        :return: True if no prohibited value is present, False otherwise
        """
        return not any(v in none_values for v in values)

    def _get_values_for_rule(
        self, rule: StatementTemplateRule, trace: JsonType
    ) -> list[Any]:
        """
        Extract values from the trace that are relevant to a specific rule.

        This method applies the JSONPath specified in the rule to the trace,
        and if a selector is present, further refines the extracted values.

        :param trace: The trace data to extract values from
        :param rule: The StatementTemplateRule specifying how to extract values
        :return: A list of extracted values relevant to the rule
        """
        values = self._apply_jsonpath(data=trace, path=rule.location)
        if rule.selector:
            values = self._apply_selector(values=values, selector=rule.selector)
        return values

    @staticmethod
    def _apply_jsonpath(data: JsonType, path: str) -> list[Any]:
        """
        Apply a JSONPath expression to data and return the results.

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

    def _apply_selector(self, values: list[Any], selector: str) -> list[Any]:
        """
        Apply a selector to a list of values and return the results.

        :param values: The values to apply the selector to
        :param selector: The selector to apply
        :return: The results of applying the selector
        """
        result = []
        for value in values:
            if isinstance(value, dict):
                result.extend(self._apply_jsonpath(data=value, path=selector))
        return result
