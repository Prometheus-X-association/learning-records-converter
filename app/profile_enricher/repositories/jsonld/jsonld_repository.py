import logging

from app.profile_enricher.repositories.repository import ProfileRepository
from app.profile_enricher.types import JsonType
from .profile_loader import ProfileLoader
from .trace_enricher import TraceEnricher
from .trace_validator import TraceValidator

from utils.utils_dict import deep_merge, get_nested_from_flat

logger = logging.getLogger(__name__)


class JsonLdProfileRepository(ProfileRepository):
    """
    A repository for handling JSON-LD profiles.
    """

    def __init__(self, base_path: str):
        """
        Initialize the JsonLdProfileRepository.

        :param base_path: Base path for profile files
        """
        self.profile_loader = ProfileLoader(base_path)
        self.trace_enricher = TraceEnricher()
        self.trace_validator = TraceValidator()

    def enrich_trace(self, group_name: str, template_name: str, trace: JsonType):
        """
        Enrich a trace based on its profile.

        :param group_name: The group name of the profile
        :param template_name: The template name within the profile
        :param trace: The trace to enrich
        :raises TemplateNotFoundException: If the specified template is not found
        :raises ProfileNotFoundException: If the profile is not found
        :raises InvalidJsonException: If the profile JSON is invalid
        :raises ProfileValidationError: If the profile fails validation
        """
        # Get the correct template model depending on group and template names
        template = self.profile_loader.load_template(
            group_name=group_name,
            template_name=template_name,
        )

        # Build enriched data with template data
        enriched_data = self.trace_enricher.get_enriched_data(template=template)

        # Merge recursively the original trace with enriched data
        deep_merge(target_dict=trace, merge_dct=get_nested_from_flat(enriched_data))
        logger.debug(f"Trace enriched successfully for template: {template_name}")

    def validate_trace(self, group_name: str, template_name: str, trace: JsonType) -> bool:
        """
        Validate a trace against its profile rules.

        :param group_name: The group name of the profile
        :param template_name: The template name within the profile
        :param trace: The trace to validate
        :return: True if the trace is valid according to the profile, False otherwise
        :raises TemplateNotFoundException: If the specified template is not found
        :raises ProfileNotFoundException: If the profile is not found
        :raises InvalidJsonException: If the profile JSON is invalid
        :raises ProfileValidationError: If the profile fails validation
        """
        # Get the correct template model depending on group and template names
        template = self.profile_loader.load_template(
            group_name=group_name,
            template_name=template_name,
        )

        return self.trace_validator.validate_trace(template=template, trace=trace)
