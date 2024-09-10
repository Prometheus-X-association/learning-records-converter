from utils.utils_dict import deep_merge

from app.common.models.trace import Trace
from app.infrastructure.config.contract import ConfigContract
from app.infrastructure.logging.contract import LoggerContract
from app.profile_enricher.repositories.contracts.repository import ProfileRepository
from app.profile_enricher.types import ValidationError, ValidationRecommendation

from .profile_loader import ProfileLoader
from .trace_enricher import TraceEnricher
from .trace_validator import TraceValidator


class JsonLdProfileRepository(ProfileRepository):
    """
    A repository for handling JSON-LD profiles.
    """

    def __init__(self, logger: LoggerContract, config: ConfigContract):
        """
        Initialize the JsonLdProfileRepository.

        :param logger: LoggerContract implementation for logging
        :param config: ConfigContract implementation for config
        """
        self.logger = logger
        self.profile_loader = ProfileLoader(logger=logger, config=config)
        self.trace_enricher = TraceEnricher(logger=logger)
        self.trace_validator = TraceValidator(logger=logger)

    def enrich_trace(self, group_name: str, template_name: str, trace: Trace) -> None:
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
        try:
            template = self.profile_loader.load_template(
                group_name=group_name,
                template_name=template_name,
            )
        except Exception:
            self.logger.error("Error while loading template")
            return

        # Build enriched data with template data
        enriched_data = self.trace_enricher.get_enriched_data(
            group_name=group_name,
            template=template,
            trace=trace,
        )

        # Merge recursively the original trace with enriched data
        deep_merge(target_dict=trace.data, merge_dct=enriched_data)
        self.logger.info("Trace enriched successfully", {"template": template_name})

    def validate_trace(
        self, group_name: str, template_name: str, trace: Trace,
    ) -> list[ValidationError]:
        """
        Validate a trace against its profile rules.

        :param group_name: The group name of the profile
        :param template_name: The template name within the profile
        :param trace: The trace to validate
        :return: A list of ValidationError objects. An empty list indicates a valid trace
        :raises TemplateNotFoundException: If the specified template is not found
        :raises ProfileNotFoundException: If the profile is not found
        :raises InvalidJsonException: If the profile JSON is invalid
        :raises ProfileValidationError: If the profile fails validation
        """
        # Get the correct template model depending on group and template names
        try:
            template = self.profile_loader.load_template(
                group_name=group_name,
                template_name=template_name,
            )
        except Exception:
            self.logger.error("Error while loading template")
            return []

        return self.trace_validator.validate_trace(template=template, trace=trace)

    def get_recommendations(
        self, group_name: str, template_name: str, trace: Trace,
    ) -> list[ValidationRecommendation]:
        """
        Generate recommendations for a trace based on a specific template

        :param group_name: The group name of the profile
        :param template_name: The template name within the profile
        :param trace: The trace data to generate recommendations for
        :return: A list of ValidationRecommendation objects
        :raises TemplateNotFoundException: If the specified template is not found
        :raises ProfileNotFoundException: If the specified group (profile) is not found
        :raises InvalidJsonException: If the profile JSON is invalid
        """
        # Get the correct template model depending on group and template names
        try:
            template = self.profile_loader.load_template(
                group_name=group_name,
                template_name=template_name,
            )
        except Exception:
            self.logger.error("Error while loading template")
            return []

        return self.trace_validator.get_recommendations(template=template, trace=trace)
