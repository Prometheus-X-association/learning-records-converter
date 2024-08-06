import re

from utils.utils_dict import get_nested_from_flat

from app.profile_enricher.profiles.jsonld import PresenceTypeEnum, StatementTemplate
from app.profile_enricher.types import JsonType

# Constants
VERB_ID = "verb.id"
VERB_DISPLAY = "verb.display.en-US"
OBJECT_DEFINITION_TYPE = "object.definition.type"


class TraceEnricher:
    """Class responsible for enriching traces based on templates."""

    def get_enriched_data(self, template: StatementTemplate) -> JsonType:
        """
        Get enriched data based on the given template.

        :param template: The template to use for enrichment.
        :return: The enriched data.
        """
        # Build enriched data with template data
        enriched_data = {
            VERB_ID: str(template.verb),
            VERB_DISPLAY: template.prefLabel.en,
            OBJECT_DEFINITION_TYPE: str(template.objectActivityType),
        }

        # Enriched more for rules with only one value
        if template.rules:
            for rule in template.rules:
                if (
                    rule.presence in [PresenceTypeEnum.RECOMMENDED, PresenceTypeEnum.INCLUDED]
                    and rule.location
                ):
                    if rule.any and len(rule.any) == 1:
                        enriched_data.update(
                            self._transform_rule(rule.location, rule.any[0])
                        )
                    elif rule.all and len(rule.all) == 1:
                        enriched_data.update(
                            self._transform_rule(rule.location, rule.all[0])
                        )

        return get_nested_from_flat(flat_field=enriched_data)

    @staticmethod
    def _transform_rule(path: str, value: str) -> JsonType:
        """
        Transform a rule path and value into a JSON-LD compatible format.

        :param path: The JSON path of the rule
        :param value: The value to be set at the specified path
        :return: A dictionary representing the transformed rule
        """
        # Remove the initial '$.' if present
        path = path.removeprefix("$.")

        # Split the main path and the part in brackets
        # Example : $.object.definition.extensions['https://w3id.org/xapi/acrossx/extensions/type']
        main_path, _, bracket_part = path.partition("[")

        if bracket_part:
            # Extract the key between single quotes
            key_match = re.search(r"'([^']*)'", bracket_part)
            if key_match:
                return {main_path: {key_match.group(1): value}}

        # If there's no part in brackets, set the value directly
        return {path: value}
