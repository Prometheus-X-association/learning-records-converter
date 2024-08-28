from utils.utils_dict import get_nested_from_flat

from app.profile_enricher.profiles.jsonld import PresenceTypeEnum, StatementTemplate
from app.profile_enricher.types import JsonType
from app.profile_enricher.utils.jsonpath import JSONPathUtils

# Constants
CONTEXT_ACTIVITIES_CATEGORY_ID = "https://w3id.org/xapi"
CONTEXT_ACTIVITIES_CATEGORY_DEFINITION_TYPE = (
    "http://adlnet.gov/expapi/activities/profile"
)


class TraceEnricher:
    """Class responsible for enriching traces based on templates."""

    def get_enriched_data(
        self, group_name: str, template: StatementTemplate, trace: JsonType
    ) -> JsonType:
        """
        Get enriched data based on the given template.

        :param group_name: The group name of the template
        :param template: The template to use for enrichment
        :param trace: The trace that needs to be enriched
        :return: The enriched data
        """
        # Build enriched data with template data
        enriched_data = {
            "verb.id": str(template.verb),
            "verb.display.en-US": template.prefLabel.en,
            "object.definition.type": str(template.objectActivityType),
            "context.contextActivities.category.0": {
                "id": f"{CONTEXT_ACTIVITIES_CATEGORY_ID}/{group_name}",
                "definition": {
                    "type": {CONTEXT_ACTIVITIES_CATEGORY_DEFINITION_TYPE},
                },
            },
        }

        # Enriched more for rules with only one value
        if template.rules:
            for rule in template.rules:
                if (
                    rule.presence
                    in [PresenceTypeEnum.RECOMMENDED, PresenceTypeEnum.INCLUDED]
                    and rule.location
                    and not JSONPathUtils.path_exists(path=rule.location, data=trace)
                ):
                    value = None
                    if rule.any and len(rule.any) == 1:
                        value = rule.any[0]
                    elif rule.all and len(rule.all) == 1:
                        value = rule.all[0]

                    if value:
                        enriched_data.update(
                            JSONPathUtils.path_to_dict(path=rule.location, value=value)
                        )

        return get_nested_from_flat(flat_field=enriched_data)
