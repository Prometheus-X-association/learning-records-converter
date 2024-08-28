"""
This module defines models and enums for xAPI profiles, including concepts, extensions, document resources, and statement templates.

It uses Pydantic for validation and includes:
- Enums for profile element types.
- Models for profile elements like concepts, extensions, and statements.
- Validation logic to enforce profile constraints and ensure consistency.

Constants are also provided for standard URLs used in profiles.
"""

import re
from abc import ABC
from datetime import datetime
from enum import StrEnum
from typing import Annotated, Any, Dict, Literal, Optional

from pydantic import (AnyUrl, BaseModel, Field, ValidationInfo, field_validator,
                      model_validator)

# Constants
PROFILE_CONTEXT_URL = "https://w3id.org/xapi/profiles/context"
ACTIVITY_CONTEXT_URL = "https://w3id.org/xapi/profiles/activity-context"
PROFILE_CONFORMS_TO_URL = "https://w3id.org/xapi/profiles#1.0"
LOCATION_PATTERN = r"^[\$@]([.\[].*)?$"


# Enums
class AuthorTypeEnum(StrEnum):
    """
    Enumeration of types of authors for profiles.
    """

    ORGANIZATION = "Organization"
    PERSON = "Person"


class ConceptTypeEnum(StrEnum):
    """
    Enumeration of types of concepts in a profile.
    """

    VERB = "Verb"
    ACTIVITY_TYPE = "ActivityType"
    ATTACHMENT_USAGE_TYPE = "AttachmentUsageType"


class ExtensionTypeEnum(StrEnum):
    """
    Enumeration of types of extensions in a profile.
    """

    CONTEXT = "ContextExtension"
    RESULT = "ResultExtension"
    ACTIVITY = "ActivityExtension"


class DocumentResourceTypeEnum(StrEnum):
    """
    Enumeration of types of document resources in a profile.
    """

    STATE = "StateResource"
    AGENT_PROFILE = "AgentProfileResource"
    ACTIVITY_PROFILE = "ActivityProfileResource"


class PresenceTypeEnum(StrEnum):
    """
    Enumeration of presence types for rules in statement templates.
    """

    INCLUDED = "included"
    EXCLUDED = "excluded"
    RECOMMENDED = "recommended"


class ActivityTypeEnum(StrEnum):
    """
    Enumeration of types of activities.
    """

    ACTIVITY = "Activity"


class ProfileTypeEnum(StrEnum):
    """
    Enumeration of profile types.
    """

    PROFILE = "Profile"


class StatementTemplateTypeEnum(StrEnum):
    """
    Enumeration of types of statement templates.
    """

    STATEMENTTEMPLATE = "StatementTemplate"


class PatternTypeEnum(StrEnum):
    """
    Enumeration of pattern types in a profile.
    """

    PATTERN = "Pattern"


# Models
class LanguageMap(BaseModel):
    """
    A model representing a language map for multilingual labels and definitions.
    """

    en: str


class ProfileVersion(BaseModel):
    """
    A model representing a version of a profile.
    """

    id: AnyUrl
    wasRevisionOf: Optional[list[AnyUrl]] = None
    generatedAtTime: datetime


class Author(BaseModel):
    """
    A model representing an author of a profile.
    """

    type: AuthorTypeEnum
    name: str
    url: Optional[AnyUrl] = None


class ProfileElement(BaseModel, ABC):
    """
    Abstract base model for elements of a profile, including concepts, extensions, and document resources.
    """

    id: AnyUrl
    type: str
    inScheme: AnyUrl
    prefLabel: LanguageMap
    definition: LanguageMap
    deprecated: bool = Field(default=False)


class Concept(ProfileElement):
    """
    A model representing a concept in a profile.
    """

    type: ConceptTypeEnum
    broader: Optional[list[AnyUrl]] = None
    broadMatch: Optional[list[AnyUrl]] = None
    narrower: Optional[list[AnyUrl]] = None
    narrowMatch: Optional[list[AnyUrl]] = None
    related: Optional[list[AnyUrl]] = None
    relatedMatch: Optional[list[AnyUrl]] = None
    exactMatch: Optional[list[AnyUrl]] = None

    @field_validator("related")
    @staticmethod
    def related_only_for_deprecated(
        value: Optional[list[AnyUrl]], info: ValidationInfo
    ) -> Optional[list[AnyUrl]]:
        """
        Validator to ensure 'related' field is used only for deprecated concepts.
        """
        if value and not info.data.get("deprecated"):
            raise ValueError(
                "'related' MUST only be used on Concepts that are deprecated"
            )
        return value


class Extension(ProfileElement):
    """
    A model representing an extension in a profile.
    """

    type: ExtensionTypeEnum
    recommendedActivityTypes: Optional[list[AnyUrl]] = None
    recommendedVerbs: Optional[list[AnyUrl]] = None
    context: Optional[AnyUrl] = None
    iriSchema: Optional[AnyUrl] = Field(
        default=None, alias="schema"
    )  # Rename internal Pydantic field
    inlineSchema: Optional[str] = None

    @field_validator("recommendedActivityTypes")
    @staticmethod
    def validate_recommended_activity_types(
        value: Optional[list[AnyUrl]], info: ValidationInfo
    ) -> Optional[list[AnyUrl]]:
        """
        Validator to ensure 'recommendedActivityTypes' is only allowed on ActivityExtension types.
        """
        if value is not None and info.data.get("type") != ExtensionTypeEnum.ACTIVITY:
            raise ValueError(
                "recommendedActivityTypes is only allowed on an ActivityExtension"
            )
        return value

    @field_validator("recommendedVerbs")
    @staticmethod
    def validate_recommended_verbs(
        value: Optional[list[AnyUrl]], info: ValidationInfo
    ) -> Optional[list[AnyUrl]]:
        """
        Validator to ensure 'recommendedVerbs' is only allowed on ContextExtension or ResultExtension types.
        """
        if value is not None and info.data.get("type") not in [
            ExtensionTypeEnum.CONTEXT,
            ExtensionTypeEnum.RESULT,
        ]:
            raise ValueError(
                "recommendedVerbs is only allowed on a ContextExtension or a ResultExtension"
            )
        return value

    @model_validator(mode="after")
    def validate_schema_fields(self) -> "Extension":
        """
        Validator to ensure that only one of 'iriSchema' or 'inlineSchema' is used.
        """
        if self.iriSchema is not None and self.inlineSchema is not None:
            raise ValueError(
                "Profiles MUST use at most one of schema and inlineSchema for Extensions"
            )
        return self


class DocumentResource(ProfileElement):
    """
    A model representing a document resource in a profile.
    """

    type: DocumentResourceTypeEnum
    contentType: str
    context: Optional[AnyUrl] = None
    iriSchema: Optional[AnyUrl] = Field(
        default=None, alias="schema"
    )  # Rename internal Pydantic field
    inlineSchema: Optional[str] = None

    @model_validator(mode="after")
    def validate_schema_fields(self) -> "DocumentResource":
        """
        Validator to ensure that only one of 'iriSchema' or 'inlineSchema' is used.
        """
        if self.iriSchema is not None and self.inlineSchema is not None:
            raise ValueError(
                "Profiles MUST use at most one of schema and inlineSchema for Document Resources"
            )
        return self


class ActivityDefinition(BaseModel):
    """
    A model defining the properties of an activity.
    """

    context: Annotated[AnyUrl, Literal[ACTIVITY_CONTEXT_URL]] = Field(
        default=ACTIVITY_CONTEXT_URL, alias="@context"
    )
    type: Optional[AnyUrl] = None
    name: Optional[LanguageMap] = None
    description: Optional[LanguageMap] = None
    moreInfo: Optional[AnyUrl] = None
    extensions: Optional[Dict[AnyUrl, Any]] = None


class Activity(BaseModel):
    """
    A model representing an activity in a profile.
    """

    id: AnyUrl
    type: ActivityTypeEnum
    inScheme: AnyUrl
    activityDefinition: ActivityDefinition
    deprecated: bool = Field(default=False)


class StatementTemplateRule(BaseModel):
    """
    A model representing a rule for statement templates.
    """

    location: str = Field(pattern=LOCATION_PATTERN)
    selector: str = Field(pattern=LOCATION_PATTERN, default=None)
    presence: Optional[PresenceTypeEnum] = None
    any: Optional[list[str]] = None
    all: Optional[list[str]] = None
    none: Optional[list[str]] = None
    scopeNote: Optional[LanguageMap] = None

    @field_validator("location", "selector")
    @staticmethod
    def validate_jsonpath(value: Optional[str]) -> Optional[str]:
        """
        Validator to ensure that filter and script expressions are not used in JSONPath.
        """
        if re.search(r"\(.*\)", value):
            raise ValueError(
                "Filter and script expressions MUST NOT be used in JSONPath"
            )
        return value

    @model_validator(mode="after")
    def at_least_one_rule(self) -> "StatementTemplateRule":
        """
        Validator to ensure that at least one of 'presence', 'any', 'all', or 'none' is specified.
        """
        if not any([self.presence, self.any, self.all, self.none]):
            raise ValueError(
                "A Statement Template Rule MUST include one or more of presence, any, all, or none"
            )
        return self


class StatementTemplate(ProfileElement):
    """
    A model representing a statement template in a profile.
    """

    type: StatementTemplateTypeEnum
    verb: Optional[AnyUrl] = None
    objectActivityType: Optional[AnyUrl] = None
    contextGroupingActivityType: Optional[list[AnyUrl]] = None
    contextParentActivityType: Optional[list[AnyUrl]] = None
    contextOtherActivityType: Optional[list[AnyUrl]] = None
    contextCategoryActivityType: Optional[list[AnyUrl]] = None
    attachmentUsageType: Optional[list[AnyUrl]] = None
    objectStatementRefTemplate: Optional[list[AnyUrl]] = None
    contextStatementRefTemplate: Optional[list[AnyUrl]] = None
    rules: Optional[list[StatementTemplateRule]] = None

    @model_validator(mode="after")
    def not_both_object_ref_and_activity_type(self) -> "StatementTemplate":
        """
        Validator to ensure that 'objectStatementRefTemplate' and 'objectActivityType' are not both present.
        """
        if (
            self.objectStatementRefTemplate is not None
            and self.objectActivityType is not None
        ):
            raise ValueError(
                "A Statement Template MUST NOT have both objectStatementRefTemplate and objectActivityType"
            )
        return self


class Pattern(ProfileElement):
    """
    A model representing a pattern in a profile.
    """

    type: PatternTypeEnum
    primary: bool = Field(default=False)
    alternates: Optional[list[AnyUrl]] = None
    optional: Optional[AnyUrl] = None
    oneOrMore: Optional[AnyUrl] = None
    sequence: Optional[list[AnyUrl]] = None
    zeroOrMore: Optional[AnyUrl] = None

    @field_validator("prefLabel", "definition")
    @staticmethod
    def primary_must_have_label_and_definition(
        value: Optional[LanguageMap], info: ValidationInfo
    ) -> Optional[LanguageMap]:
        """
        Validator to ensure that primary patterns include both 'prefLabel' and 'definition'.
        """
        if info.data.get("primary") and value is None:
            raise ValueError("A primary Pattern MUST include prefLabel and definition")
        return value

    @field_validator("alternates")
    @staticmethod
    def validate_alternates(value: Optional[list[AnyUrl]]) -> Optional[list[AnyUrl]]:
        """
        Validator to ensure that 'alternates' does not directly contain 'optional' or 'zeroOrMore'.
        """
        if value is not None:
            if any(x.endsWith("/optional") or x.endsWith("/zeroOrMore") for x in value):
                raise ValueError(
                    "MUST NOT put optional or zeroOrMore directly inside alternates"
                )
        return value

    @field_validator("sequence")
    @staticmethod
    def validate_sequence(
        value: Optional[list[AnyUrl]], info: ValidationInfo
    ) -> Optional[list[AnyUrl]]:
        """
        Validator to ensure that sequences include at least two members, unless specific conditions apply.
        """
        if value is not None:
            if len(value) < 2 and not (
                info.data.get("primary") and not info.data.get("inScheme")
            ):
                raise ValueError(
                    "MUST include at least two members in sequence, unless sequence is in a primary Pattern that is not used elsewhere and the member of sequence is a single Statement Template"
                )
        return value

    @model_validator(mode="after")
    def exactly_one_pattern_type(self) -> "Pattern":
        """
        Validator to ensure that exactly one pattern type is specified.
        """
        pattern_types = [
            "alternates",
            "optional",
            "oneOrMore",
            "sequence",
            "zeroOrMore",
        ]
        if sum(1 for pt in pattern_types if getattr(self, pt) is not None) != 1:
            raise ValueError(
                "A Pattern MUST contain exactly one of alternates, optional, oneOrMore, sequence, and zeroOrMore"
            )
        return self

    @model_validator(mode="after")
    def no_self_reference(self) -> "Pattern":
        """
        Validator to ensure that patterns do not reference themselves, either directly or indirectly.
        """

        def check_self_reference(pattern_id, pattern_list):
            if pattern_id in pattern_list:
                raise ValueError(
                    "MUST NOT include any Pattern within itself, or within any Pattern within itself, or at any depth"
                )

        for field in ["alternates", "optional", "oneOrMore", "sequence", "zeroOrMore"]:
            value = getattr(self, field)
            if value:
                check_self_reference(
                    self.id, value if isinstance(value, list) else [value]
                )
        return self


class Profile(BaseModel):
    """
    A model representing a profile in the system.
    """

    id: AnyUrl
    context: Annotated[AnyUrl, Literal[PROFILE_CONTEXT_URL]] = Field(
        default=PROFILE_CONTEXT_URL, alias="@context"
    )
    type: ProfileTypeEnum
    conformsTo: Annotated[AnyUrl, Literal[PROFILE_CONFORMS_TO_URL]] = Field(
        default=PROFILE_CONFORMS_TO_URL
    )
    prefLabel: LanguageMap
    definition: LanguageMap
    seeAlso: Optional[AnyUrl] = None
    versions: list[ProfileVersion]
    author: Author
    concepts: Optional[list[Concept | Extension | DocumentResource | Activity]] = None
    templates: Optional[list[StatementTemplate]] = None
    patterns: Optional[list[Pattern]] = None

    @model_validator(mode="after")
    def unique_pattern_ids(self) -> "Profile":
        """
        Validator to ensure that all pattern IDs are unique and not the same as the profile ID.
        """
        pattern_ids = set()
        for pattern in self.patterns or []:
            if pattern.id in pattern_ids or pattern.id == self.id:
                raise ValueError(
                    f"Pattern id {pattern.id} is not unique or is the same as the Profile id"
                )
            pattern_ids.add(pattern.id)
        return self

    @model_validator(mode="after")
    def check_version_consistency(self) -> "Profile":
        """
        Validator to ensure that 'wasRevisionOf' references existing versions.
        """
        all_ids = {v.id for v in self.versions}
        for version in self.versions:
            if version.wasRevisionOf:
                for revision in version.wasRevisionOf:
                    if revision not in all_ids:
                        raise ValueError(
                            f"wasRevisionOf {revision} does not refer to an existing version"
                        )
        return self

    @model_validator(mode="after")
    def validate_concept_references(self) -> "Profile":
        """
        Validator to ensure that all concept references are valid within the profile.
        """
        concept_ids = {c.id for c in self.concepts or []}
        for concept in self.concepts or []:
            if isinstance(concept, Concept):
                for field in [
                    "broader",
                    "broadMatch",
                    "narrower",
                    "narrowMatch",
                    "related",
                    "relatedMatch",
                    "exactMatch",
                ]:
                    refs = getattr(concept, field, None)
                    if refs:
                        for ref in refs:
                            if ref not in concept_ids:
                                raise ValueError(
                                    f"Concept {concept.id} references non-existent concept {ref} in {field}"
                                )
        return self
