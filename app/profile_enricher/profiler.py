from .exceptions import ProfilerException
from .repositories.repository import ProfileRepository
from .types import JsonType


class Profiler:
    def __init__(self, repository: ProfileRepository):
        self.repository = repository

    def enrich(self, profile: str) -> JsonType:
        """
        Enrich a profile based on its name and group.

        Args:
            profile (str): The profile name in the format 'group.template_name'.

        Returns:
            JsonType: Enriched profile data.

        Raises:
            ProfileException: If there's an error during enrichment.
        """
        try:
            group_name, template_name = profile.split('.', 1)
        except ValueError as e:
            raise ProfilerException(f"Invalid profile format: {str(e)}")

        return self.repository.enrich_profile(
            group_name=group_name,
            template_name=template_name,
        )
