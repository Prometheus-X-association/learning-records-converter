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
from typing import Annotated, Any, Literal, Union, get_args, get_origin

from pydantic import (
    AnyUrl,
    BaseModel,
    Field,
    ValidationInfo,
    field_validator,
    model_validator,
)

# Constants
PROFILE_CONTEXT_URL = "https://w3id.org/xapi/profiles/context"
ACTIVITY_CONTEXT_URL = "https://w3id.org/xapi/profiles/activity-context"
PROFILE_CONFORMS_TO_URL = "https://w3id.org/xapi/profiles#1.0"
LOCATION_PATTERN = r"^[\$@]([.\[].*)?$"


class CustomBaseModel(BaseModel):
    @model_validator(mode="before")
    @classmethod
    def allow_empty_string_for_anyurl(cls, values):
        for field_name, field_info in cls.model_fields.items():
            field_type = field_info.annotation
            field_alias = field_info.alias or field_name

            # If the field is an Optional AnyUrl (= Union of AnyUrl and None)
            if (
                values.get(field_alias) == ""
                and get_origin(field_type) is Union
                and AnyUrl in get_args(field_type)
                and type(None) in get_args(field_type)
            ):
                values[field_alias] = None

        return values


# Enums
class AuthorTypeEnum(StrEnum):
    """Enumeration of types of authors for profiles."""

    ORGANIZATION = "Organization"
    PERSON = "Person"


class ConceptTypeEnum(StrEnum):
    """Enumeration of types of concepts in a profile."""

    VERB = "Verb"
    ACTIVITY_TYPE = "ActivityType"
    ATTACHMENT_USAGE_TYPE = "AttachmentUsageType"


class ExtensionTypeEnum(StrEnum):
    """Enumeration of types of extensions in a profile."""

    CONTEXT = "ContextExtension"
    RESULT = "ResultExtension"
    ACTIVITY = "ActivityExtension"


class DocumentResourceTypeEnum(StrEnum):
    """Enumeration of types of document resources in a profile."""

    STATE = "StateResource"
    AGENT_PROFILE = "AgentProfileResource"
    ACTIVITY_PROFILE = "ActivityProfileResource"


class PresenceTypeEnum(StrEnum):
    """Enumeration of presence types for rules in statement templates."""

    INCLUDED = "included"
    EXCLUDED = "excluded"
    RECOMMENDED = "recommended"


class ActivityTypeEnum(StrEnum):
    """Enumeration of types of activities."""

    ACTIVITY = "Activity"


class ProfileTypeEnum(StrEnum):
    """Enumeration of profile types."""

    PROFILE = "Profile"


class StatementTemplateTypeEnum(StrEnum):
    """Enumeration of types of statement templates."""

    STATEMENTTEMPLATE = "StatementTemplate"


class PatternTypeEnum(StrEnum):
    """Enumeration of pattern types in a profile."""

    PATTERN = "Pattern"


# Models
class LanguageMap(CustomBaseModel):
    """A model representing a language map for multilingual labels and definitions."""

    en: str


class ProfileVersion(CustomBaseModel):
    """A model representing a version of a profile."""

    id: AnyUrl
    was_revision_of: list[AnyUrl] | None = Field(None, alias="wasRevisionOf")
    generated_at_time: datetime = Field(..., alias="generatedAtTime")


class Author(CustomBaseModel):
    """A model representing an author of a profile."""

    type: AuthorTypeEnum
    name: str
    url: AnyUrl | None = None


class ProfileElement(BaseModel, ABC):
    """Abstract base model for elements of a profile, including concepts, extensions, and document resources."""

    id: AnyUrl
    type: str
    in_scheme: AnyUrl = Field(..., alias="inScheme")
    pref_label: LanguageMap = Field(..., alias="prefLabel")
    definition: LanguageMap
    deprecated: bool = Field(default=False)


class Concept(ProfileElement):
    """A model representing a concept in a profile."""

    type: ConceptTypeEnum
    broader: list[AnyUrl] | None = None
    broad_match: list[AnyUrl] | None = Field(None, alias="broadMatch")
    narrower: list[AnyUrl] | None = None
    narrow_match: list[AnyUrl] | None = Field(None, alias="narrowMatch")
    related: list[AnyUrl] | None = None
    related_match: list[AnyUrl] | None = Field(None, alias="relatedMatch")
    exact_match: list[AnyUrl] | None = Field(None, alias="exactMatch")

    @field_validator("related")
    @staticmethod
    def related_only_for_deprecated(
        value: list[AnyUrl] | None,
        info: ValidationInfo,
    ) -> list[AnyUrl] | None:
        """Validator to ensure 'related' field is used only for deprecated concepts."""
        if value and not info.data.get("deprecated"):
            raise ValueError(
                "'related' MUST only be used on Concepts that are deprecated",
            )
        return value


class Extension(ProfileElement):
    """A model representing an extension in a profile."""

    type: ExtensionTypeEnum
    recommended_activity_types: list[AnyUrl] | None = Field(
        None,
        alias="recommendedActivityTypes",
    )
    recommended_verbs: list[AnyUrl] | None = Field(None, alias="recommendedVerbs")
    context: AnyUrl | None = None
    iri_schema: AnyUrl | None = Field(None, alias="schema")
    inline_schema: str | dict | None = Field(None, alias="inlineSchema")

    @field_validator("recommended_activity_types")
    @staticmethod
    def validate_recommended_activity_types(
        value: list[AnyUrl] | None,
        info: ValidationInfo,
    ) -> list[AnyUrl] | None:
        """Validator to ensure 'recommendedActivityTypes' is only allowed on ActivityExtension types."""
        if value is not None and info.data.get("type") != ExtensionTypeEnum.ACTIVITY:
            raise ValueError(
                "recommendedActivityTypes is only allowed on an ActivityExtension",
            )
        return value

    @field_validator("recommended_verbs")
    @staticmethod
    def validate_recommended_verbs(
        value: list[AnyUrl] | None,
        info: ValidationInfo,
    ) -> list[AnyUrl] | None:
        """Validator to ensure 'recommendedVerbs' is only allowed on ContextExtension or ResultExtension types."""
        if value is not None and info.data.get("type") not in [
            ExtensionTypeEnum.CONTEXT,
            ExtensionTypeEnum.RESULT,
        ]:
            raise ValueError(
                "recommendedVerbs is only allowed on a ContextExtension or a ResultExtension",
            )
        return value

    @model_validator(mode="after")
    def validate_schema_fields(self) -> "Extension":
        """Validator to ensure that only one of 'iriSchema' or 'inlineSchema' is used."""
        if self.iri_schema is not None and self.inline_schema is not None:
            raise ValueError(
                "Profiles MUST use at most one of schema and inlineSchema for Extensions",
            )
        return self


class DocumentResource(ProfileElement):
    """A model representing a document resource in a profile."""

    type: DocumentResourceTypeEnum
    content_type: str = Field(..., alias="contentType")
    context: AnyUrl | None = None
    iri_schema: AnyUrl | None = Field(None, alias="schema")
    inline_schema: str | dict | None = Field(None, alias="inlineSchema")

    @model_validator(mode="after")
    def validate_schema_fields(self) -> "DocumentResource":
        """Validator to ensure that only one of 'iriSchema' or 'inlineSchema' is used."""
        if self.iri_schema is not None and self.inline_schema is not None:
            raise ValueError(
                "Profiles MUST use at most one of schema and inlineSchema for Document Resources",
            )
        return self


class ActivityDefinition(CustomBaseModel):
    """A model defining the properties of an activity."""

    context: Annotated[AnyUrl, Literal[ACTIVITY_CONTEXT_URL]] = Field(
        default=ACTIVITY_CONTEXT_URL,
        alias="@context",
    )
    type: AnyUrl | None = None
    name: LanguageMap | None = None
    description: LanguageMap | None = None
    more_info: AnyUrl | None = Field(None, alias="moreInfo")
    extensions: dict[AnyUrl, Any] | None = None


class Activity(CustomBaseModel):
    """A model representing an activity in a profile."""

    id: AnyUrl
    type: ActivityTypeEnum
    in_scheme: AnyUrl = Field(..., alias="inScheme")
    activity_definition: ActivityDefinition = Field(..., alias="activityDefinition")
    deprecated: bool = Field(default=False)


class StatementTemplateRule(CustomBaseModel):
    """A model representing a rule for statement templates."""

    location: str = Field(pattern=LOCATION_PATTERN)
    selector: str = Field(pattern=LOCATION_PATTERN, default=None)
    presence: PresenceTypeEnum | None = None
    any: list[str] | None = None
    all: list[str] | None = None
    none: list[str] | None = None
    scope_note: LanguageMap | None = Field(None, alias="scopeNote")

    @field_validator("location", "selector")
    @staticmethod
    def validate_jsonpath(value: str | None) -> str | None:
        """Validator to ensure that filter and script expressions are not used in JSONPath."""
        if re.search(r"\(.*\)", value):
            raise ValueError(
                "Filter and script expressions MUST NOT be used in JSONPath",
            )
        return value

    @model_validator(mode="after")
    def at_least_one_rule(self) -> "StatementTemplateRule":
        """Validator to ensure that at least one of 'presence', 'any', 'all', or 'none' is specified."""
        if not any([self.presence, self.any, self.all, self.none]):
            raise ValueError(
                "A Statement Template Rule MUST include one or more of presence, any, all, or none",
            )
        return self


class StatementTemplate(ProfileElement):
    """A model representing a statement template in a profile."""

    type: StatementTemplateTypeEnum
    verb: AnyUrl | None = None
    object_activity_type: AnyUrl | None = Field(None, alias="objectActivityType")
    context_grouping_activity_type: list[AnyUrl] | None = Field(
        None,
        alias="contextGroupingActivityType",
    )
    context_parent_activity_type: list[AnyUrl] | None = Field(
        None,
        alias="contextParentActivityType",
    )
    context_other_activity_type: list[AnyUrl] | None = Field(
        None,
        alias="contextOtherActivityType",
    )
    context_category_activity_type: list[AnyUrl] | None = Field(
        None,
        alias="contextCategoryActivityType",
    )
    attachment_usage_type: list[AnyUrl] | None = Field(
        None,
        alias="attachmentUsageType",
    )
    object_statement_ref_template: list[AnyUrl] | None = Field(
        None,
        alias="objectStatementRefTemplate",
    )
    context_statement_ref_template: list[AnyUrl] | None = Field(
        None,
        alias="contextStatementRefTemplate",
    )
    rules: list[StatementTemplateRule] | None = None

    @model_validator(mode="after")
    def not_both_object_ref_and_activity_type(self) -> "StatementTemplate":
        """Validator to ensure that 'objectStatementRefTemplate' and 'objectActivityType' are not both present."""
        if (
            self.object_statement_ref_template is not None
            and self.object_activity_type is not None
        ):
            raise ValueError(
                "A Statement Template MUST NOT have both objectStatementRefTemplate and objectActivityType",
            )
        return self


class Pattern(ProfileElement):
    """A model representing a pattern in a profile."""

    type: PatternTypeEnum
    primary: bool = Field(default=False)
    alternates: list[AnyUrl] | None = None
    optional: AnyUrl | None = None
    one_or_more: AnyUrl | None = Field(None, alias="oneOrMore")
    sequence: list[AnyUrl] | None = None
    zero_or_more: AnyUrl | None = Field(None, alias="zeroOrMore")

    @field_validator("pref_label", "definition")
    @staticmethod
    def primary_must_have_label_and_definition(
        value: LanguageMap | None,
        info: ValidationInfo,
    ) -> LanguageMap | None:
        """Validator to ensure that primary patterns include both 'prefLabel' and 'definition'."""
        if info.data.get("primary") and value is None:
            raise ValueError("A primary Pattern MUST include prefLabel and definition")
        return value

    @field_validator("alternates")
    @staticmethod
    def validate_alternates(value: list[AnyUrl] | None) -> list[AnyUrl] | None:
        """Validator to ensure that 'alternates' does not directly contain 'optional' or 'zeroOrMore'."""
        if value is not None and any(
            str(x).endswith("/optional") or str(x).endswith("/zeroOrMore")
            for x in value
        ):
            raise ValueError(
                "MUST NOT put optional or zeroOrMore directly inside alternates",
            )
        return value

    @field_validator("sequence")
    @staticmethod
    def validate_sequence(
        value: list[AnyUrl] | None,
        info: ValidationInfo,
    ) -> list[AnyUrl] | None:
        """Validator to ensure that sequences include at least two members, unless specific conditions apply."""
        if (
            value is not None
            and len(value) < 2
            and not (info.data.get("primary") and not info.data.get("inScheme"))
        ):
            raise ValueError(
                "MUST include at least two members in sequence, unless sequence is in a primary Pattern that is not used elsewhere and the member of sequence is a single Statement Template",
            )
        return value

    @model_validator(mode="after")
    def exactly_one_pattern_type(self) -> "Pattern":
        """Validator to ensure that exactly one pattern type is specified."""
        pattern_types = [
            "alternates",
            "optional",
            "oneOrMore",
            "sequence",
            "zeroOrMore",
        ]
        if sum(1 for pt in pattern_types if getattr(self, pt) is not None) != 1:
            raise ValueError(
                "A Pattern MUST contain exactly one of alternates, optional, oneOrMore, sequence, and zeroOrMore",
            )
        return self

    @model_validator(mode="after")
    def no_self_reference(self) -> "Pattern":
        """Validator to ensure that patterns do not reference themselves, either directly or indirectly."""

        def check_self_reference(pattern_id, pattern_list) -> None:
            if pattern_id in pattern_list:
                raise ValueError(
                    "MUST NOT include any Pattern within itself, or within any Pattern within itself, or at any depth",
                )

        for field in [
            "alternates",
            "optional",
            "one_or_more",
            "sequence",
            "zero_or_more",
        ]:
            value = getattr(self, field)
            if value:
                check_self_reference(
                    self.id,
                    value if isinstance(value, list) else [value],
                )
        return self


class Profile(CustomBaseModel):
    """A model representing a profile in the system."""

    id: AnyUrl
    context: Annotated[AnyUrl, Literal[PROFILE_CONTEXT_URL]] = Field(
        default=PROFILE_CONTEXT_URL,
        alias="@context",
    )
    type: ProfileTypeEnum
    conforms_to: Annotated[AnyUrl, Literal[PROFILE_CONFORMS_TO_URL]] = Field(
        default=PROFILE_CONFORMS_TO_URL,
        alias="conformsTo",
    )
    pref_label: LanguageMap = Field(..., alias="prefLabel")
    definition: LanguageMap
    see_also: AnyUrl | None = Field(None, alias="seeAlso")
    versions: list[ProfileVersion]
    author: Author
    concepts: list[Concept | Extension | DocumentResource | Activity] | None = None
    templates: list[StatementTemplate] | None = None
    patterns: list[Pattern] | None = None

    @model_validator(mode="after")
    def unique_pattern_ids(self) -> "Profile":
        """Validator to ensure that all pattern IDs are unique and not the same as the profile ID."""
        pattern_ids = set()
        for pattern in self.patterns or []:
            if pattern.id in pattern_ids or pattern.id == self.id:
                raise ValueError(
                    f"Pattern id {pattern.id} is not unique or is the same as the Profile id",
                )
            pattern_ids.add(pattern.id)
        return self

    @model_validator(mode="after")
    def check_version_consistency(self) -> "Profile":
        """Validator to ensure that 'wasRevisionOf' references existing versions."""
        all_ids = {v.id for v in self.versions}
        for version in self.versions:
            if version.was_revision_of:
                for revision in version.was_revision_of:
                    if revision not in all_ids:
                        raise ValueError(
                            f"wasRevisionOf {revision} does not refer to an existing version",
                        )
        return self

    @model_validator(mode="after")
    def validate_concept_references(self) -> "Profile":
        """Validator to ensure that all concept references are valid within the profile."""
        concept_ids = {c.id for c in self.concepts or []}
        for concept in self.concepts or []:
            if isinstance(concept, Concept):
                for field in [
                    "broader",
                    "broad_match",
                    "narrower",
                    "narrow_match",
                    "related",
                    "related_match",
                    "exact_match",
                ]:
                    refs = getattr(concept, field, None)
                    if refs:
                        for ref in refs:
                            if ref not in concept_ids:
                                raise ValueError(
                                    f"Concept {concept.id} references non-existent concept {ref} in {field}",
                                )
        return self
