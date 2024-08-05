from abc import ABC, abstractmethod

from ..types import JsonType


class ProfileRepository(ABC):
    """
    Abstract base class for profile repositories.
    Defines the interface for enriching and validating traces based on profiles.
    """

    @abstractmethod
    def enrich_trace(self, group_name: str, template_name: str, trace: JsonType):
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
    ) -> bool:
        """
        Validate a trace against its profile rules.

        :param group_name: The group name of the profile
        :param template_name: The template name within the profile
        :param trace: The trace to validate
        :return: True if the trace is valid according to the profile, False otherwise
        """
        ...
