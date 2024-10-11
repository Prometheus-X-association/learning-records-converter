from abc import ABC, abstractmethod

from app.common.models.trace import Trace
from app.profile_enricher.profiler_types import (
    ValidationError,
    ValidationRecommendation,
)


class ProfileRepository(ABC):
    """
    Abstract base class for profile repositories.

    Defines the interface for enriching and validating traces based on profiles.
    """

    @abstractmethod
    def enrich_trace(self, group_name: str, template_name: str, trace: Trace) -> None:
        """
        Enrich a trace based on its profile.

        :param group_name: The group name of the profile
        :param template_name: The template name within the profile
        :param trace: The original trace to enrich
        """
        raise NotImplementedError

    @abstractmethod
    def validate_trace(
        self,
        group_name: str,
        template_name: str,
        trace: Trace,
    ) -> list[ValidationError]:
        """
        Validate a trace against its profile rules.

        :param group_name: The group name of the profile
        :param template_name: The template name within the profile
        :param trace: The trace to validate
        :return: A list of ValidationError objects. An empty list indicates a valid trace
        """
        raise NotImplementedError

    @abstractmethod
    def get_recommendations(
        self,
        group_name: str,
        template_name: str,
        trace: Trace,
    ) -> list[ValidationRecommendation]:
        """
        Generate recommendations for a trace based on a specific template.

        :param group_name: The group name of the profile
        :param template_name: The template name within the profile
        :param trace: The trace data to generate recommendations for
        :return: A list of ValidationRecommendation objects
        """
        raise NotImplementedError
