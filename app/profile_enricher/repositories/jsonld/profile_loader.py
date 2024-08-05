import json
import logging
import os
from functools import cache
from pathlib import Path
from typing import Optional
from urllib.error import URLError
from urllib.request import urlopen

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

    @cache
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
        logger.debug(f"Load profile: {group_name}")

        # First, download the profile file if not exists or read it
        file_path = self.base_path.joinpath(f"{group_name}.jsonld")
        if file_path.is_file():
            profile_json = self.read_profile_file(file_path=file_path)
        else:
            profile_json = self.download_profile(group_name=group_name)

        # Next, validate & build the profile on the Pydantic model
        profile = self.build_profile_model(profile_json=profile_json)

        # If validation passed and the file doesn't exist, save it
        if not file_path.is_file():
            self.save_profile_file(file_path, profile_json)

        logger.info(f"Profile '{group_name}' loaded'")

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

        logger.info(f"Template '{template_name}' found'")

        return template

    @staticmethod
    def read_profile_file(file_path: Path) -> JsonType:
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
    def download_profile(group_name: str) -> JsonType:
        """
        Download a profile file for a given group.

        :param group_name: The name of the group whose profile is to be downloaded.
        :param destination_path: The path where the downloaded profile should be saved.
        :return: The contents of the downloaded profile as a dictionary.
        :raises ProfileNotFoundException: If the profile cannot be downloaded or the URL is not found.
        :raises InvalidJsonException: If the downloaded content is not valid JSON.

        :Environment Variables:
            - PROFILE_{GROUP_NAME}_URL: The URL from which to download the profile.
        """
        url = os.getenv(f"PROFILE_{group_name.upper()}_URL")
        if not url:
            raise ProfileNotFoundException(f"URL not found for profile: {group_name}")

        try:
            with urlopen(url) as response:
                content = response.read()
            return json.loads(content)
        except URLError as e:
            logger.error(f"Failed to download profile for {group_name}: {e}")
            raise ProfileNotFoundException(
                f"Failed to download profile for {group_name}: {e}"
            ) from e
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in downloaded profile for {group_name}: {e}")
            raise InvalidJsonException(
                f"Invalid JSON in downloaded profile for {group_name}: {e}"
            ) from e

    @staticmethod
    def save_profile_file(file_path: Path, profile_json: JsonType):
        """
        Save a profile file to the file system.

        :param file_path: The file path where to save the profile
        :param profile_json: The profile data to save
        :raises IOError: If there's an error writing the file to the specified path.
        """
        try:
            json_string = json.dumps(profile_json, ensure_ascii=False, indent=2)
            file_path.write_text(json_string, encoding='utf-8')
            logger.info(f"Profile saved to {file_path}")
        except IOError as e:
            logger.error(f"Failed to save profile to {file_path}: {e}")
            raise

    @staticmethod
    def build_profile_model(profile_json: JsonType) -> Profile:
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
