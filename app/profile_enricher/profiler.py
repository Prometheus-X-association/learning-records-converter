from app.common.models.trace import Trace

from .exceptions import ProfilerException
from .repositories.contracts.repository import ProfileRepository
from .types import ValidationError, ValidationRecommendation


class Profiler:
    """
    A class to manage profile-based operations on traces.
    """

    def __init__(self, repository: ProfileRepository):
        """
        Initialize the Profiler with a ProfileRepository.

        :param repository: The repository to use for profile operations
        """
        self.repository = repository

    def enrich_trace(self, trace: Trace) -> None:
        """
        Enrich a trace.

        :param trace: The original trace to enrich
        :raises ProfilerException: If enrichment fails
        """
        if not trace.profile:
            raise ProfilerException("No profile associated with the trace")
        group_name, template_name = self._parse_profile(profile=trace.profile)

        try:
            enriched_trace = self.repository.enrich_trace(
                group_name=group_name,
                template_name=template_name,
                trace=trace,
            )
            return enriched_trace
        except Exception as e:
            raise ProfilerException(f"Failed to enrich trace: {str(e)}") from e

    def validate_trace(self, trace: Trace) -> list[ValidationError]:
        """
        Validate a trace.

        :param trace: The trace to validate
        :return: A list of ValidationError objects
        :raises ProfilerException: If validation fails
        """
        if not trace.profile:
            return []
        group_name, template_name = self._parse_profile(profile=trace.profile)

        try:
            errors = self.repository.validate_trace(
                group_name=group_name,
                template_name=template_name,
                trace=trace,
            )
            return errors
        except Exception as e:
            raise ProfilerException("Failed to validate trace") from e

    def get_recommendations(self, trace: Trace) -> list[ValidationRecommendation]:
        """
        Generate recommendations for a trace.

        :param trace: The trace data to generate recommendations for
        :return: A list of ValidationRecommendation objects
        :raises ProfilerException: If recommendation generation fails
        """
        if not trace.profile:
            return []

        group_name, template_name = self._parse_profile(profile=trace.profile)

        recommendations = self.repository.get_recommendations(
            group_name=group_name,
            template_name=template_name,
            trace=trace,
        )
        return recommendations

    @staticmethod
    def _parse_profile(profile: str) -> tuple[str, str]:
        """
        Parse a profile identifier in the format 'group_name.template_name'
        :param profile: The profile identifier
        :return: The group_name and the template_name
        :raises ProfilerException: If the profile format is invalid
        """
        try:
            group_name, template_name = profile.split(".", 1)
            if not group_name or not template_name:
                raise ValueError("Group name and template name cannot be empty")
        except ValueError as e:
            raise ProfilerException(
                f"Invalid profile format: {str(e)}. Expected 'group_name.template_name', got: {profile}"
            ) from e
        return group_name, template_name
