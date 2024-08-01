from abc import ABC, abstractmethod

from ..types import JsonType


class ProfileRepository(ABC):
    @abstractmethod
    def enrich_profile(self, group_name: str, template_name: str) -> JsonType:
        """Enrich a profile based on its group and template name."""
        ...
