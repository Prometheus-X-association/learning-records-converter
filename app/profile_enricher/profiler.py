from .exceptions import ProfilerException
from .repositories.repository import ProfileRepository
from .types import JsonType


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

    def enrich_trace(self, profile: str, trace: JsonType):
        """
        Enrich a trace based on the specified profile.

        :param profile: The profile identifier in the format 'group_name.template_name'
        :param trace: The original trace to enrich
        :raises ProfilerException: If enrichment fails
        """
        group_name, template_name = self._parse_profile(profile=profile)

        try:
            enriched_trace = self.repository.enrich_trace(
                group_name=group_name,
                template_name=template_name,
                trace=trace,
            )
            return enriched_trace
        except Exception as e:
            raise ProfilerException(f"Failed to enrich trace: {str(e)}") from e

    def validate_trace(self, profile: str, trace: JsonType):
        """
        Validate a trace against the specified profile.

        :param profile: The profile identifier in the format 'group_name.template_name'
        :param trace: The trace to validate
        :raises ProfilerException: If validation fails
        """
        group_name, template_name = self._parse_profile(profile=profile)

        try:
            is_valid = self.repository.validate_trace(
                group_name=group_name,
                template_name=template_name,
                trace=trace,
            )
            return is_valid
        except Exception as e:
            raise ProfilerException("Failed to validate trace") from e

    def _parse_profile(self, profile: str) -> tuple[str, str]:
        """
        Parse a profile identifier in the format 'group_name.template_name'
        :param profile: The profile identifier
        :return: The group_name and the template_name
        """
        try:
            group_name, template_name = profile.split(".", 1)
        except ValueError as e:
            raise ProfilerException(
                f"Invalid profile format : {str(e)}. Expected 'group_name.template_name', got: {profile}"
            ) from e
        return group_name, template_name
