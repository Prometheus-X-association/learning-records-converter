import json
import os
import re
from typing import Optional

from pydantic import ValidationError

from .repository import ProfileRepository
from ..exceptions import InvalidJsonException, ProfileNotFoundException, ProfileValidationError, TemplateNotFoundException
from ..profiles.jsonld import PresenceTypeEnum, Profile, StatementTemplate
from ..types import JsonType


class JsonLdProfileRepository(ProfileRepository):
    def __init__(self, base_path: str):
        self.base_path = base_path

    def enrich_profile(self, group_name: str, template_name: str) -> JsonType:
        """
        Enrich a profile based on its group and template name.

        Args:
            group_name (str): The group name of the profile.
            template_name (str): The template name within the profile.

        Returns:
            JsonType: Enriched profile data.

        Raises:
            ProfileNotFoundException: If the profile file is not found.
            InvalidJsonException: If the profile JSON is invalid.
            ProfileValidationError: If the profile fails validation.
            TemplateNotFoundException: If the specified template is not found in the profile.
        """
        profile_json = self._load_profile_file(group=group_name)
        profile = self._validate_profile(profile_json=profile_json)
        template = self._get_template(profile=profile, template_name=template_name)

        if template is None:
            raise TemplateNotFoundException(f"Template '{template_name}' not found in profile '{group_name}'")

        enriched_data = {
            'verb.id': str(template.verb),
            'verb.display.en-US': template.prefLabel.en,
            'object.definition.type': str(template.objectActivityType),
        }

        if template.rules:
            for rule in template.rules:
                if rule.presence in [PresenceTypeEnum.RECOMMENDED.value, PresenceTypeEnum.INCLUDED.value] and rule.location:
                    if rule.any and len(rule.any) == 1:
                        enriched_data.update(self._transform_rule(rule.location, rule.any[0]))
                    elif rule.all and len(rule.all) == 1:
                        enriched_data.update(self._transform_rule(rule.location, rule.all[0]))

        return enriched_data

    def _load_profile_file(self, group: str) -> JsonType:
        file = os.path.join(self.base_path, f'{group}.jsonld')
        try:
            with open(file=file, mode='r', encoding="utf8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise ProfileNotFoundException(f"Profile file not found: {file}")
        except json.JSONDecodeError:
            raise InvalidJsonException(f"Invalid JSON in profile file: {file}")

    @staticmethod
    def _validate_profile(profile_json: JsonType) -> Profile:
        try:
            return Profile(**profile_json)
        except ValidationError as e:
            raise ProfileValidationError(f"Profile validation failed: {e}")
        except TypeError as e:
            raise ProfileValidationError(f"Invalid data type in profile: {e}")
        except Exception as e:
            raise ProfileValidationError(f"Unexpected error during profile validation: {e}")

    @staticmethod
    def _get_template(profile: Profile, template_name: str) -> Optional[StatementTemplate]:
        if profile.templates is None:
            return None
        for profile_template in profile.templates:
            if template_name in str(profile_template.id):
                return profile_template
        return None

    @staticmethod
    def _transform_rule(path: str, value: str) -> JsonType:
        # Remove the initial '$.' if present
        if path.startswith('$.'):
            path = path[2:]

        # Split the main path and the part in brackets
        # Exemple : $.object.definition.extensions['https://w3id.org/xapi/acrossx/extensions/type']
        main_path, _, bracket_part = path.partition('[')

        if bracket_part:
            # Extract the key between single quotes
            key_match = re.search(r"'([^']*)'", bracket_part)
            if key_match:
                return {main_path: {key_match.group(1): value}}

        # If there's no part in brackets, set the value directly
        return {path: value}
