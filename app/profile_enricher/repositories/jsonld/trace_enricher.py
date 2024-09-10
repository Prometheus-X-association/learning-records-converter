from app.common.models.trace import Trace
from app.common.type.types import JsonType
from app.common.utils.utils_dict import deep_merge, get_nested_from_flat
from app.infrastructure.logging.contract import LoggerContract
from app.profile_enricher.profiles.jsonld import PresenceTypeEnum, StatementTemplate
from app.profile_enricher.utils.jsonpath import JSONPathUtils

# Constants
CONTEXT_ACTIVITIES_CATEGORY_ID = "https://w3id.org/xapi"
CONTEXT_ACTIVITIES_CATEGORY_DEFINITION_TYPE = (
    "http://adlnet.gov/expapi/activities/profile"
)


class TraceEnricher:
    """Class responsible for enriching traces based on templates."""

    def __init__(self, logger: LoggerContract):
        self.logger = logger

    def get_enriched_data(
        self, group_name: str, template: StatementTemplate, trace: Trace,
    ) -> JsonType:
        """
        Get enriched data based on the given template.

        :param group_name: The group name of the template
        :param template: The template to use for enrichment
        :param trace: The trace that needs to be enriched
        :return: The enriched data
        """
        log_context = {
            "group": group_name,
            "template": template.id,
        }
        self.logger.debug("Start enrich trace", log_context)

        # Build enriched data with template data
        enriched_data = {
            "verb.id": str(template.verb),
            "verb.display.en-US": template.pref_label.en,
            "object.definition.type": str(template.object_activity_type),
            "context.contextActivities.category.0": {
                "id": f"{CONTEXT_ACTIVITIES_CATEGORY_ID}/{group_name}",
                "definition": {
                    "type": {CONTEXT_ACTIVITIES_CATEGORY_DEFINITION_TYPE},
                },
            },
        }

        # Enriched more for rules with only one value
        if template.rules:
            enriched_data.update(
                self._enrich_with_rules(template=template, trace=trace),
            )

        return get_nested_from_flat(flat_field=enriched_data)

    def _enrich_with_rules(self, template: StatementTemplate, trace: Trace) -> JsonType:
        """
        Get enriched data based on the template's rules than contain only one value

        :param template: The template to use for enrichment.
        :param trace: The trace that needs to be enriched.
        :return: The enriched data.
        """
        enriched_data = {}
        for rule in template.rules:
            if (
                rule.presence
                in {PresenceTypeEnum.RECOMMENDED, PresenceTypeEnum.INCLUDED}
                and rule.location
                and not JSONPathUtils.path_exists(path=rule.location, data=trace.data)
            ):
                value = None
                if rule.any and len(rule.any) == 1:
                    value = rule.any[0]
                elif rule.all and len(rule.all) == 1:
                    value = rule.all[0]

                if value:
                    self.logger.debug("1-value rule found", {"rule": rule.location})
                    rule_data = JSONPathUtils.path_to_dict(rule.location, value)
                    deep_merge(target_dict=enriched_data, merge_dct=rule_data)
        return enriched_data
