import json
import logging
from pathlib import Path
from typing import Optional

from pydantic import ValidationError

from app.profile_enricher.exceptions import (InvalidJsonException,
                                             ProfileNotFoundException,
                                             ProfileValidationError,
                                             TemplateNotFoundException)
from app.profile_enricher.profiles.jsonld import Profile, StatementTemplate
from app.profile_enricher.types import JsonType

logger = logging.getLogger(__name__)


class ProfileLoader:
    """Class responsible for loading profile's file."""

    def __init__(self, base_path: str):
        self.base_path: Path = Path(base_path)
        self.profiles_cache: dict[str, Profile] = {}

    def load_template(self, group_name: str, template_name: str) -> StatementTemplate:
        """
        Load a template from cache or from file if not cached.

        :param group_name: The group name of the profile
        :param template_name: The template name within the profile
        :return: The loaded StatementTemplate
        :raises TemplateNotFoundException: If the specified template is not found
        :raises ProfileNotFoundException: If the profile is not found
        :raises InvalidJsonException: If the profile JSON is invalid
        :raises ProfileValidationError: If the profile fails validation
        """
        # We use a cache to avoid reading the file multiple times
        cache_key = f"{group_name}"
        if cache_key not in self.profiles_cache:
            logger.debug(f"Load profile: {group_name}")

            # First, read the profile file
            file_path = self.base_path.joinpath(f"{group_name}.jsonld")
            profile_json = self._read_profile_file(file_path=file_path)

            # Next, validate the profile with the Pydantic model
            profile = self._validate_profile(profile_json=profile_json)

            self.profiles_cache[cache_key] = profile
            logger.info(f"Profile '{group_name}' loaded and cached'")
        else:
            profile = self.profiles_cache.get(cache_key)
            logger.debug(f"Profile in cache: {cache_key}")

        # Then, retrieve the correct template in the profile
        template = self._get_template_in_profile(
            profile=profile,
            template_name=template_name,
        )

        if template is None:
            logger.error(
                f"Template '{template_name}' not found in profile '{group_name}'"
            )
            raise TemplateNotFoundException(
                f"Template '{template_name}' not found in profile '{group_name}'"
            )

        return template

    @staticmethod
    def _read_profile_file(file_path: Path) -> JsonType:
        """
        Load a profile file from the file system.

        :param file_path: The file path of the profile
        :return: The loaded profile data
        :raises ProfileNotFoundException: If the profile file is not found
        :raises InvalidJsonException: If the profile JSON is invalid
        """
        try:
            file_content = file_path.read_text(encoding="utf8")
            return json.loads(file_content)
        except FileNotFoundError as e:
            logger.error(f"Profile file not found: {file_path}")
            raise ProfileNotFoundException(
                f"Profile file not found: {file_path} {e}"
            ) from e
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in profile file: {file_path}")
            raise InvalidJsonException(
                f"Invalid JSON in profile file: {file_path} {e}"
            ) from e

    @staticmethod
    def _validate_profile(profile_json: JsonType) -> Profile:
        """
        Validate the profile JSON against the Profile model.

        :param profile_json: The profile data in JSON format
        :return: A validated pydantic Profile instance
        :raises ProfileValidationError: If the profile data is invalid
        """
        try:
            return Profile(**profile_json)
        except ValidationError as e:
            logger.error(f"Profile validation failed: {e}")
            raise ProfileValidationError(f"Profile validation failed: {e}") from e
        except TypeError as e:
            logger.error(f"Invalid data type in profile: {e}")
            raise ProfileValidationError(f"Invalid data type in profile: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error during profile validation: {e}")
            raise ProfileValidationError(
                f"Unexpected error during profile validation: {e}"
            ) from e

    @staticmethod
    def _get_template_in_profile(
        profile: Profile, template_name: str
    ) -> Optional[StatementTemplate]:
        """
        Get a specific template from a profile.

        :param profile: The profile containing templates
        :param template_name: The name of the template to retrieve
        :return: The found template, or None if not found
        """
        if profile.templates is None:
            return None
        for profile_template in profile.templates:
            # Example: accessed-page in http://schema.dases.eu/xapi/profile/common/templates/accessed-page
            if template_name in str(profile_template.id):
                return profile_template
        return None
