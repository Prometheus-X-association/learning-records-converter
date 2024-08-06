from abc import ABC, abstractmethod

from app.profile_enricher.types import JsonType, ValidationError


class ProfileRepository(ABC):
    """
    Abstract base class for profile repositories.
    Defines the interface for enriching and validating traces based on profiles.
    """

    @abstractmethod
    def enrich_trace(
        self, group_name: str, template_name: str, trace: JsonType
    ) -> None:
        """
        Enrich a trace based on its profile.

        :param group_name: The group name of the profile
        :param template_name: The template name within the profile
        :param trace: The original trace to enrich
        """
        ...

    @abstractmethod
    def validate_trace(
        self, group_name: str, template_name: str, trace: JsonType
    ) -> list[ValidationError]:
        """
        Validate a trace against its profile rules.

        :param group_name: The group name of the profile
        :param template_name: The template name within the profile
        :param trace: The trace to validate
        :return: A list of ValidationError objects. An empty list indicates a valid trace.
        """
        ...
