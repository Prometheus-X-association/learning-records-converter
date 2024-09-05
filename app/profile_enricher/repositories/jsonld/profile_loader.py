import json
from functools import cache
from pathlib import Path
from typing import Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from pydantic import ValidationError

from app.common.type.types import JsonType
from app.infrastructure.config.contract import ConfigContract
from app.infrastructure.logging.contract import LoggerContract
from app.profile_enricher.exceptions import (BasePathException, InvalidJsonException,
                                             ProfileNotFoundException,
                                             ProfileValidationError,
                                             TemplateNotFoundException)
from app.profile_enricher.profiles.jsonld import Profile, StatementTemplate


class ProfileLoader:
    """Class responsible for loading profile's file."""

    def __init__(self, logger: LoggerContract, config: ConfigContract):
        self.logger = logger
        self.config = config

        try:
            self.base_path: Path = Path(config.get_and_create_profiles_base_path())
        except BasePathException as e:
            self.logger.exception("Failed to create or access profiles directory", e)
            raise

        self.download_timeout = config.get_download_timeout()

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
        # First, download the profile file if not exists or read it
        file_path = self.base_path.joinpath(f"{group_name}.jsonld")
        log_context = {
            "group": group_name,
            "template": template_name,
            "file": file_path,
        }
        self.logger.debug("Load profile file", log_context)

        if file_path.is_file():
            profile_json = self.read_profile_file(file_path=file_path)
        else:
            profile_json = self.download_profile(group_name=group_name)

        # Next, validate & build the profile on the Pydantic model
        profile = self.build_profile_model(profile_json=profile_json)

        # If validation passed and the file doesn't exist, save it
        if not file_path.is_file():
            self.save_profile_file(file_path, profile_json)

        self.logger.info("Profile loaded", log_context)

        # Then, retrieve the correct template in the profile
        template = self._get_template_in_profile(
            profile=profile,
            template_name=template_name,
        )
        if template is None:
            self.logger.warning("Template not found", log_context)
            raise TemplateNotFoundException(
                f"Template '{template_name}' not found in profile '{group_name}'"
            )

        self.logger.info("Template found", log_context)
        return template

    def read_profile_file(self, file_path: Path) -> JsonType:
        """
        Load a profile file from the file system.

        :param file_path: The file path of the profile
        :return: The loaded profile data
        :raises ProfileNotFoundException: If the profile file is not found
        :raises InvalidJsonException: If the profile JSON is invalid
        """
        log_context = {"path": file_path}
        self.logger.debug("Read profile file", log_context)
        try:
            file_content = file_path.read_text(encoding="utf8")
            return json.loads(file_content)
        except FileNotFoundError as e:
            self.logger.exception("Profile file not found", e, log_context)
            raise ProfileNotFoundException(
                f"Profile file not found: {file_path}"
            ) from e
        except json.JSONDecodeError as e:
            self.logger.exception("Invalid JSON in profile file", e, log_context)
            raise InvalidJsonException(
                f"Invalid JSON in profile file: {file_path}"
            ) from e

    def download_profile(self, group_name: str) -> JsonType:
        """
        Download a profile file for a given group.

        :param group_name: The name of the group whose profile is to be downloaded
        :return: The contents of the downloaded profile as a dictionary
        :raises ProfileNotFoundException: If the profile cannot be downloaded or the URL is not found
        :raises InvalidJsonException: If the downloaded content is not valid JSON
        """
        url = self.config.get_profile_url(profile_name=group_name)

        log_context = {"group": group_name, "url": url}
        self.logger.debug("Profile file downloading", log_context)

        if not url:
            self.logger.warning("URL not found for profile", log_context)
            raise ProfileNotFoundException(f"URL not found for profile: {group_name}")

        try:
            request = Request(url=url)
            with urlopen(request, timeout=self.download_timeout) as response:
                if response.status != 200:
                    self.logger.error("Failed to download profile", log_context)
                    raise ProfileNotFoundException(
                        f"Failed to download profile for {group_name}: HTTP status {response.status}"
                    )

                content = response.read().decode("utf-8")
            return json.loads(content)
        except HTTPError as e:
            self.logger.exception(
                "HTTP error occurred while downloading profile", e, log_context
            )
            raise ProfileNotFoundException(
                f"Failed to download profile for {group_name}: HTTP error {e.code}"
            ) from e
        except URLError as e:
            self.logger.exception("Failed to download profile", e, log_context)
            raise ProfileNotFoundException(
                f"Failed to download profile for {group_name}"
            ) from e
        except json.JSONDecodeError as e:
            self.logger.exception("Invalid JSON in downloaded profile", e, log_context)
            raise InvalidJsonException(
                f"Invalid JSON in downloaded profile for {group_name}"
            ) from e

    def save_profile_file(self, file_path: Path, profile_json: JsonType):
        """
        Save a profile file to the file system.

        :param file_path: The file path where to save the profile
        :param profile_json: The profile data to save
        :raises IOError: If there's an error writing the file to the specified path
        """
        log_context = {"file_path": file_path}
        try:
            json_string = json.dumps(profile_json, ensure_ascii=False, indent=2)
            file_path.write_text(json_string, encoding="utf-8")
            self.logger.info("Profile saved", log_context)
        except IOError as e:
            self.logger.exception("Failed to save profile", e, log_context)
            raise

    def build_profile_model(self, profile_json: JsonType) -> Profile:
        """
        Validate the profile JSON against the Profile model.

        :param profile_json: The profile data in JSON format
        :return: A validated pydantic Profile instance
        :raises ProfileValidationError: If the profile data is invalid
        """
        try:
            return Profile(**profile_json)
        except ValidationError as e:
            self.logger.exception("Profile validation failed", e)
            raise ProfileValidationError("Profile validation failed") from e
        except TypeError as e:
            self.logger.exception("Invalid data type in profile", e)
            raise ProfileValidationError("Invalid data type in profile") from e
        except Exception as e:
            self.logger.exception("Unexpected error during profile validation", e)
            raise ProfileValidationError(
                "Unexpected error during profile validation"
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
            if (
                str(profile_template.id)
                .rstrip("/")
                .casefold()
                .endswith(template_name.casefold())
            ):
                return profile_template
        return None
