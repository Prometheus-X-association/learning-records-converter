import logging
from typing import Any

import jsonpath_ng

from app.profile_enricher.profiles.jsonld import (PresenceTypeEnum, StatementTemplate,
                                                  StatementTemplateRule)
from app.profile_enricher.types import JsonType, ValidationError

logger = logging.getLogger(__name__)


class TraceValidator:
    """Class responsible for validating traces against templates."""

    def validate_trace(
        self, template: StatementTemplate, trace: JsonType
    ) -> list[ValidationError]:
        """
        Validate a trace against a given template.

        :param template: The template to validate against.
        :param trace: The trace to validate.
        :return: A list of ValidationError objects. An empty list indicates a valid trace.
        """
        errors: list[ValidationError] = []
        if template.rules:
            for rule in template.rules:
                rule_errors = self._follows_rule(trace=trace, rule=rule)
                if rule_errors:
                    logger.debug(f"Trace validation failed for rule: {rule}")
                    errors.extend(rule_errors)

        if not errors:
            logger.debug(
                f"Trace validated successfully against template '{template.id}'"
            )

        return errors

    def _follows_rule(
        self, trace: JsonType, rule: StatementTemplateRule
    ) -> list[ValidationError]:
        """
        Check if a trace follows a specific rule.
        See: https://adlnet.github.io/xapi-profiles/xapi-profiles-communication.html#statement-template-valid

        :param trace: The trace to check
        :param rule: The rule to check against
        :return: List of errors
        """
        errors = []

        # Apply the JSONPath to retrieve the field to check
        values = self._apply_jsonpath(data=trace, path=rule.location)
        if rule.selector:
            values = self._apply_selector(values=values, selector=rule.selector)

        # Check the "included" and "excluded" rules
        if rule.presence:
            if rule.presence == PresenceTypeEnum.INCLUDED and not values:
                errors.append(
                    ValidationError(
                        rule="presence",
                        expected="included",
                        actual="missing",
                        path=rule.location,
                    )
                )
            elif rule.presence == PresenceTypeEnum.EXCLUDED and values:
                errors.append(
                    ValidationError(
                        rule="presence",
                        expected="excluded",
                        actual="present",
                        path=rule.location,
                    )
                )

        # Check the "any" / "all" / "none" rules
        if rule.presence != PresenceTypeEnum.RECOMMENDED or values:
            if rule.any and not self._check_any(any_values=rule.any, values=values):
                errors.append(
                    ValidationError(
                        rule="any", expected=rule.any, actual=values, path=rule.location
                    )
                )
            if rule.all and not self._check_all(all_values=rule.all, values=values):
                errors.append(
                    ValidationError(
                        rule="all", expected=rule.all, actual=values, path=rule.location
                    )
                )
            if rule.none and not self._check_none(none_values=rule.none, values=values):
                errors.append(
                    ValidationError(
                        rule="none",
                        expected=f"no values from {rule.none}",
                        actual=values,
                        path=rule.location,
                    )
                )

        return errors

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

    @staticmethod
    def _apply_jsonpath(data: JsonType, path: str) -> list[Any]:
        """
        Apply a JSONPath expression to data and return the results.

        :param data: The data to apply the JSONPath to
        :param path: The JSONPath expression
        :return: The results of applying the JSONPath
        :raises ValueError: If the JSONPath is invalid
        """
        try:
            results = jsonpath_ng.parse(path).find(data)
            # Flatten the list if the result is a list of lists
            return [
                item
                for result in results
                for item in (
                    result.value if isinstance(result.value, list) else [result.value]
                )
            ]
        except Exception as e:
            logger.error(f"Invalid JSONPath: {path}")
            raise ValueError(f"Invalid JSONPath: {path}") from e

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
