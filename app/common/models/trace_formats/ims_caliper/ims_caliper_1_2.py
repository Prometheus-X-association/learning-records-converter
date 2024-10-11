from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING, Literal, get_args, get_origin

from models.trace_formats.base import ExtendedTypeBaseModel
from models.trace_formats.ims_caliper.ims_caliper_1_1 import (
    RoleTermEnum,
    StatusTermEnum,
)
from pydantic import BaseModel, Field, field_validator
from pydantic.fields import FieldInfo

if TYPE_CHECKING:
    from pydantic_core.core_schema import ValidationInfo


#############################################################
##################### ENUMS/TERMS/TYPES #####################
#############################################################
class LtiMessageTypesEnum(StrEnum):
    LTIDEEPLINKINGREQUEST = "LtiDeepLinkingRequest"
    LTIRESOURCELINKREQUEST = "LtiResourceLinkRequest"


class MetricEnum(StrEnum):
    ASSESSMENTSPASSED = "AssessmentsPassed"
    ASSESSMENTSSUBMITTED = "AssessmentsSubmitted"
    MINUTESONTASK = "MinutesOnTask"
    SKILLSMASTERED = "SkillsMastered"
    STANDARDSMASTERED = "StandardsMastered"
    UNITSCOMPLETED = "UnitsCompleted"
    UNITSPASSED = "UnitsPassed"
    WORDSREAD = "WordsRead"


class SystemIdentifierTypeEnum(StrEnum):
    ACCOUNTUSERNAME = "AccountUserName"
    EMAILADDRESS = "EmailAddress"
    LISSOURCEDID = "LisSourcedId"
    LTICONTEXTID = "LtiContextId"
    LTIDEPLOYMENTID = "LtiDeploymentId"
    LTIPLATFORMID = "LtiPlatformId"
    LTITOOLID = "LtiToolId"
    LTIUSERID = "LtiUserId"
    ONEROSTERSOURCEDID = "OneRosterSourcedId"
    OTHER = "Other"
    SISSOURCEDID = "SisSourcedId"
    SYSTEMID = "SystemId"


class ActionTermEnum(StrEnum):
    ABANDONED = "Abandoned"
    ACCEPTED = "Accepted"
    ACTIVATED = "Activated"
    ADDED = "Added"
    ARCHIVED = "Archived"
    ATTACHED = "Attached"
    BOOKMARKED = "Bookmarked"
    CHANGEDRESOLUTION = "ChangedResolution"
    CHANGEDSIZE = "ChangedSize"
    CHANGEDSPEED = "ChangedSpeed"
    CHANGEDVOLUME = "ChangedVolume"
    CLASSIFIED = "Classified"
    CLOSEDPOPOUT = "ClosedPopout"
    COMMENTED = "Commented"
    COMPLETED = "Completed"
    COPIED = "Copied"
    CREATED = "Created"
    DEACTIVATED = "Deactivated"
    DECLINED = "Declined"
    DELETED = "Deleted"
    DESCRIBED = "Described"
    DISABLEDCLOSEDCAPTIONING = "DisabledClosedCaptioning"
    DISLIKED = "Disliked"
    DOWNLOADED = "Downloaded"
    ENABLEDCLOSEDCAPTIONING = "EnabledClosedCaptioning"
    ENDED = "Ended"
    ENTEREDFULLSCREEN = "EnteredFullScreen"
    EXITEDFULLSCREEN = "ExitedFullScreen"
    FORWARDEDTO = "ForwardedTo"
    GRADED = "Graded"
    HID = "Hid"
    HIGHLIGHTED = "Highlighted"
    IDENTIFIED = "Identified"
    JUMPEDTO = "JumpedTo"
    LAUNCHED = "Launched"
    LIKED = "Liked"
    LINKED = "Linked"
    LOGGEDIN = "LoggedIn"
    LOGGEDOUT = "LoggedOut"
    MARKEDASREAD = "MarkedAsRead"
    MARKEDASUNREAD = "MarkedAsUnread"
    MODIFIED = "Modified"
    MUTED = "Muted"
    NAVIGATEDTO = "NavigatedTo"
    OPENEDPOPOUT = "OpenedPopout"
    OPTEDIN = "OptedIn"
    OPTEDOUT = "OptedOut"
    PAUSED = "Paused"
    POSTED = "Posted"
    PRINTED = "Printed"
    PUBLISHED = "Published"
    QUESTIONED = "Questioned"
    RANKED = "Ranked"
    RECOMMENDED = "Recommended"
    REMOVED = "Removed"
    RESET = "Reset"
    RESTARTED = "Restarted"
    RESTORED = "Restored"
    RESUMED = "Resumed"
    RETRIEVED = "Retrieved"
    RETURNED = "Returned"
    REVIEWED = "Reviewed"
    REWOUND = "Rewound"
    SAVED = "Saved"
    SEARCHED = "Searched"
    SENT = "Sent"
    SHARED = "Shared"
    SHOWED = "Showed"
    SKIPPED = "Skipped"
    STARTED = "Started"
    SUBMITTED = "Submitted"
    SUBSCRIBED = "Subscribed"
    TAGGED = "Tagged"
    TIMEDOUT = "TimedOut"
    UNMUTED = "Unmuted"
    UNPUBLISHED = "Unpublished"
    UNSUBSCRIBED = "Unsubscribed"
    UPLOADED = "Uploaded"
    USED = "Used"
    VIEWED = "Viewed"


class ProfileTermEnum(StrEnum):
    ANNOTATIONPROFILE = "AnnotationProfile"
    ASSESSMENTPROFILE = "AssessmentProfile"
    ASSIGNABLEPROFILE = "AssignableProfile"
    FEEDBACKPROFILE = "FeedbackProfile"
    FORUMPROFILE = "ForumProfile"
    GENERALPROFILE = "GeneralProfile"
    GRADINGPROFILE = "GradingProfile"
    MEDIAPROFILE = "MediaProfile"
    READINGPROFILE = "ReadingProfile"
    RESOURCEMANAGEMENTPROFILE = "ResourceManagementProfile"
    SEARCHPROFILE = "SearchProfile"
    SESSIONPROFILE = "SessionProfile"
    SURVEYPROFILE = "SurveyProfile"
    TOOLLAUNCHPROFILE = "ToolLaunchProfile"
    TOOLUSEPROFILE = "ToolUseProfile"


class TypeTermEnum(StrEnum):
    AGENT = "Agent"
    AGGREGATEMEASURE = "AggregateMeasure"
    AGGREGATEMEASURECOLLECTION = "AggregateMeasureCollection"
    ANNOTATION = "Annotation"
    ANNOTATIONEVENT = "AnnotationEvent"
    ASSESSMENT = "Assessment"
    ASSESSMENTEVENT = "AssessmentEvent"
    ASSESSMENTITEM = "AssessmentItem"
    ASSESSMENTITEMEVENT = "AssessmentItemEvent"
    ASSIGNABLEDIGITALRESOURCE = "AssignableDigitalResource"
    ASSIGNABLEEVENT = "AssignableEvent"
    ATTEMPT = "Attempt"
    AUDIOOBJECT = "AudioObject"
    BOOKMARKANNOTATION = "BookmarkAnnotation"
    CHAPTER = "Chapter"
    COLLECTION = "Collection"
    COMMENT = "Comment"
    COURSEOFFERING = "CourseOffering"
    COURSESECTION = "CourseSection"
    DATETIMEQUESTION = "DateTimeQuestion"
    DATETIMERESPONSE = "DateTimeResponse"
    DIGITALRESOURCE = "DigitalResource"
    DIGITALRESOURCECOLLECTION = "DigitalResourceCollection"
    DOCUMENT = "Document"
    ENTITY = "Entity"
    EVENT = "Event"
    FEEDBACKEVENT = "FeedbackEvent"
    FILLINBLANKRESPONSE = "FillinBlankResponse"
    FORUM = "Forum"
    FORUMEVENT = "ForumEvent"
    FRAME = "Frame"
    GRADEEVENT = "GradeEvent"
    GROUP = "Group"
    HIGHLIGHTANNOTATION = "HighlightAnnotation"
    IMAGEOBJECT = "ImageObject"
    LEARNINGOBJECTIVE = "LearningObjective"
    LIKERTSCALE = "LikertScale"
    LINK = "Link"
    LTILINK = "LtiLink"
    LTISESSION = "LtiSession"
    MEDIAEVENT = "MediaEvent"
    MEDIALOCATION = "MediaLocation"
    MEDIAOBJECT = "MediaObject"
    MEMBERSHIP = "Membership"
    MESSAGE = "Message"
    MESSAGEEVENT = "MessageEvent"
    MULTIPLECHOICERESPONSE = "MultipleChoiceResponse"
    MULTIPLERESPONSERESPONSE = "MultipleResponseResponse"
    MULTISELECTQUESTION = "MultiselectQuestion"
    MULTISELECTRESPONSE = "MultiselectResponse"
    MULTISELECTSCALE = "MultiselectScale"
    NAVIGATIONEVENT = "NavigationEvent"
    NUMERICSCALE = "NumericScale"
    OPENENDEDQUESTION = "OpenEndedQuestion"
    OPENENDEDRESPONSE = "OpenEndedResponse"
    ORGANIZATION = "Organization"
    PAGE = "Page"
    PERSON = "Person"
    QUERY = "Query"
    QUESTION = "Question"
    QUESTIONNAIRE = "Questionnaire"
    QUESTIONNAIREEVENT = "QuestionnaireEvent"
    QUESTIONNAIREITEM = "QuestionnaireItem"
    QUESTIONNAIREITEMEVENT = "QuestionnaireItemEvent"
    RATING = "Rating"
    RATINGSCALEQUESTION = "RatingScaleQuestion"
    RATINGSCALERESPONSE = "RatingScaleResponse"
    RESOURCEMANAGEMENTEVENT = "ResourceManagementEvent"
    RESPONSE = "Response"
    RESULT = "Result"
    SCALE = "Scale"
    SCORE = "Score"
    SEARCHEVENT = "SearchEvent"
    SEARCHRESPONSE = "SearchResponse"
    SELECTTEXTRESPONSE = "SelectTextResponse"
    SESSION = "Session"
    SESSIONEVENT = "SessionEvent"
    SHAREDANNOTATION = "SharedAnnotation"
    SOFTWAREAPPLICATION = "SoftwareApplication"
    SURVEY = "Survey"
    SURVEYEVENT = "SurveyEvent"
    SURVEYINVITATION = "SurveyInvitation"
    SURVEYINVITATIONEVENT = "SurveyInvitationEvent"
    SYSTEMIDENTIFIER = "SystemIdentifier"
    TAGANNOTATION = "TagAnnotation"
    TEXTPOSITIONSELECTOR = "TextPositionSelector"
    THREAD = "Thread"
    THREADEVENT = "ThreadEvent"
    TOOLLAUNCHEVENT = "ToolLaunchEvent"
    TOOLUSEEVENT = "ToolUseEvent"
    TRUEFALSERESPONSE = "TrueFalseResponse"
    VIDEOOBJECT = "VideoObject"
    VIEWEVENT = "ViewEvent"
    WEBPAGE = "WebPage"


##############################################################
##################### INFORMATION MODELS #####################
##############################################################
class TextPositionSelectorModel(ExtendedTypeBaseModel):
    type: Literal[TypeTermEnum.TEXTPOSITIONSELECTOR] = Field(
        alias="type",
        examples=[TypeTermEnum.TEXTPOSITIONSELECTOR.value],
    )
    start: int = Field(
        alias="start",
        description="The starting position of the selected text MUST be specified. The first character in the full text is character position 0.",
    )
    end: int = Field(
        alias="end",
        description="The end position of the selected text MUST be specified.",
    )


class SystemIdentifierModel(ExtendedTypeBaseModel):
    type: Literal[TypeTermEnum.SYSTEMIDENTIFIER] = Field(
        alias="type",
        examples=[TypeTermEnum.SYSTEMIDENTIFIER.value],
    )
    identifier_type: SystemIdentifierTypeEnum = Field(alias="identifierType")
    identifier: str = Field(alias="identifier")
    source: SoftwareApplicationModel | str = Field(default=None, alias="source")
    extensions: dict = Field(default=None, alias="extensions")


####################################################
##################### ENTITIES #####################
####################################################
class EntityModel(ExtendedTypeBaseModel):
    context: Literal["http://purl.imsglobal.org/ctx/caliper/v1p2"] = Field(
        default=None,
        alias="@context",
        examples=["http://purl.imsglobal.org/ctx/caliper/v1p2"],
    )
    id: str = Field(
        alias="id",
        examples=["urn:instructure:canvas:user:21070000000000001"],
    )
    type: Literal[TypeTermEnum.ENTITY] = Field(
        alias="type",
        examples=[TypeTermEnum.PERSON.value],
    )
    name: str = Field(default=None, alias="name")
    description: str = Field(default=None, alias="description")
    date_created: str = Field(default=None, alias="dateCreated")  # Datetime
    date_modified: str = Field(default=None, alias="dateModified")  # Datetime
    other_identifiers: list[SystemIdentifierModel | str] = Field(
        default=None,
        alias="otherIdentifiers",
    )
    extensions: dict = Field(default=None, alias="extensions")


class AgentModel(EntityModel):
    type: Literal[TypeTermEnum.AGENT] = Field(
        alias="type",
        examples=[TypeTermEnum.AGENT.value],
    )


class PersonModel(AgentModel):
    type: Literal[TypeTermEnum.PERSON] = Field(
        alias="type",
        examples=[TypeTermEnum.PERSON.value],
    )


class SoftwareApplicationModel(AgentModel):
    type: Literal[TypeTermEnum.SOFTWAREAPPLICATION] = Field(
        alias="type",
        examples=[TypeTermEnum.SOFTWAREAPPLICATION.value],
    )
    host: str = Field(default=None, alias="host")
    ip_address: str = Field(default=None, alias="ipAddress")
    user_agent: str = Field(default=None, alias="userAgent")
    version: str = Field(default=None, alias="version")


class LearningObjectiveModel(EntityModel):
    type: Literal[TypeTermEnum.LEARNINGOBJECTIVE] = Field(
        alias="type",
        examples=[TypeTermEnum.LEARNINGOBJECTIVE.value],
    )


class AggregateMeasureModel(EntityModel):
    type: Literal[TypeTermEnum.AGGREGATEMEASURE] = Field(
        alias="type",
        examples=[TypeTermEnum.AGGREGATEMEASURE.value],
    )
    metric_value: float = Field(alias="metricValue")
    max_metric_value: float = Field(default=None, alias="maxMetricValue")
    metric: MetricEnum = Field(alias="metric")
    started_at_time: str = Field(default=None, alias="startedAtTime")  # Datetime
    ended_at_time: str = Field(default=None, alias="endedAtTime")  # Datetime


class OrganizationModel(AgentModel):
    type: Literal[TypeTermEnum.ORGANIZATION] = Field(
        alias="type",
        examples=[TypeTermEnum.ORGANIZATION.value],
    )
    sub_organization_of: OrganizationModel | str = Field(
        default=None,
        alias="subOrganizationOf",
    )
    members: list[AgentModel | str] = Field(default=None, alias="members")


class DigitalResourceModel(EntityModel):
    type: Literal[TypeTermEnum.DIGITALRESOURCE] = Field(
        alias="type",
        examples=[TypeTermEnum.DIGITALRESOURCE.value],
    )
    storage_name: str = Field(
        default=None,
        alias="storageName",
        description="The name of resource when stored in a file system.",
    )
    creators: list[AgentModel | str] = Field(
        default=None,
        alias="creators",
        description="An ordered collection of Agent entities, typically of type Person, that are responsible for bringing resource into being. Each array item MUST be expressed either as an object or as a string corresponding to the item's IRI.",
    )
    media_type: str = Field(
        default=None,
        alias="mediaType",
        description="A string value drawn from the list of IANA approved media types and subtypes that identifies the file format of the resource.",
    )
    keywords: list[str] = Field(
        default=None,
        alias="keywords",
        description="An ordered collection of one or more string values that represent tags or labels used to identify the resource.",
    )
    learning_objectives: list[LearningObjectiveModel | str] = Field(
        default=None,
        alias="learningObjectives",
        description="An ordered collection of one or more LearningObjective entities that describe what a learner is expected to comprehend or accomplish after engaging with the resource. Each array item MUST be expressed either as an object or as a string corresponding to the item's IRI.",
    )
    is_part_of: EntityModel | str = Field(
        default=None,
        alias="isPartOf",
        description="A related Entity that includes or incorporates the resource as a part of its whole. The isPartOf value MUST be expressed either as an object or as a string corresponding to the associated entity's IRI.",
    )
    date_published: str = Field(
        default=None,
        alias="datePublished",
        description="An ISO 8601 date and time value expressed with millisecond precision that provides the publication date of the resource. The value MUST be expressed using the format YYYY-MM-DDTHH:mm:ss.SSSZ set to UTC with no offset specified.",
    )  # DateTime
    version: str = Field(
        default=None,
        alias="version",
        description="A string value that designates the current form or version of the resource.",
    )


class QuestionModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.QUESTION] = Field(
        alias="type",
        examples=[TypeTermEnum.QUESTION.value],
    )
    question_posed: str = Field(
        default=None,
        alias="questionPosed",
        description="A string value comprising the question posed.",
    )


class AnnotationModel(EntityModel):
    type: Literal[TypeTermEnum.ANNOTATION] = Field(
        alias="type",
        examples=[TypeTermEnum.ANNOTATION.value],
    )
    annotator: PersonModel | str = Field(
        default=None,
        alias="annotator",
        description="The Person who created the Annotation. The annotator value MUST be expressed either as an object or as a string corresponding to the annotator's IRI.",
    )
    annotated: DigitalResourceModel | str = Field(
        default=None,
        alias="annotated",
        description="The DigitalResource that was annotated by the annotator. The annotated value MUST be expressed either as an object or as a string corresponding to the annotated resource's IRI.",
    )


class AttemptModel(EntityModel):
    type: Literal[TypeTermEnum.ATTEMPT] = Field(
        alias="type",
        examples=[TypeTermEnum.ATTEMPT.value],
    )
    assignee: PersonModel | str = Field(
        default=None,
        alias="assignee",
        description="The Person who initiated the Attempt. The assignee value MUST be expressed either as an object or as a string corresponding to the assignee's IRI.",
    )
    assignable: DigitalResourceModel | str = Field(
        default=None,
        alias="assignable",
        description="The DigitalResource that constitutes the object of the assignment. The assignable value MUST be expressed either as an object or as a string corresponding to the assigned resource's IRI.",
    )
    count: int = Field(
        default=None,
        alias="count",
        description="The total number of attempts inclusive of the current attempt that have been registered against the assigned DigitalResource.",
    )
    started_at_time: str = Field(
        default=None,
        alias="startedAtTime",
        description="An ISO 8601 date and time value expressed with millisecond precision that describes when the  Attempt was commenced. The value MUST be expressed using the format YYYY-MM-DDTHH:mm:ss.SSSZ set to UTC with no offset specified.",
    )  # DateTime
    ended_at_time: str = Field(
        default=None,
        alias="endedAtTime",
        description="An ISO 8601 date and time value expressed with millisecond precision that describes when the  Attempt was completed or terminated. The value MUST be expressed using the format YYYY-MM-DDTHH:mm:ss.SSSZ set to UTC with no offset specified.",
    )  # DateTime
    duration: str = Field(
        default=None,
        alias="duration",
        description="A time interval that represents the time taken to complete the Attempt. If a duration is specified the value MUST conform to the ISO 8601 duration format.",
    )  # Duration


class CollectionModel(EntityModel):
    type: Literal[TypeTermEnum.COLLECTION] = Field(
        alias="type",
        examples=[TypeTermEnum.COLLECTION.value],
    )
    items: list[EntityModel | str] = Field(
        default=None,
        alias="items",
        description="An ordered collection of entities. Each array item MUST be expressed either as an object or as a string corresponding to the resource's IRI.",
    )


class CommentModel(EntityModel):
    type: Literal[TypeTermEnum.COMMENT] = Field(
        alias="type",
        examples=[TypeTermEnum.COMMENT.value],
    )
    commenter: PersonModel | str = Field(
        default=None,
        alias="commenter",
        description="The Person who provided the comment. The commenter value MUST be expressed either as an object or as a string corresponding to the commenter's IRI.",
    )
    commented_on: EntityModel | str = Field(
        default=None,
        alias="commentedOn",
        description="The Entity which received the comment. The commentedOn value MUST be expressed either as an object or as a string corresponding to the IRI of the resource that was commented on.",
    )
    value: str = Field(
        default=None,
        alias="value",
        description="A string value representing the comment's textual value.",
    )


class LinkModel(EntityModel):
    type: Literal[TypeTermEnum.LINK] = Field(
        alias="type",
        examples=[TypeTermEnum.LINK.value],
    )


class MembershipModel(EntityModel):
    type: Literal[TypeTermEnum.MEMBERSHIP] = Field(
        alias="type",
        examples=[TypeTermEnum.MEMBERSHIP.value],
    )
    organization: OrganizationModel | str = Field(
        default=None,
        alias="organization",
    )
    member: PersonModel | str = Field(default=None, alias="member")
    roles: list[RoleTermEnum] = Field(
        default=None,
        alias="roles",
        examples=[["Learner"]],
    )
    status: StatusTermEnum = Field(default=None, alias="status")


class QueryModel(EntityModel):
    type: Literal[TypeTermEnum.QUERY] = Field(
        alias="type",
        examples=[TypeTermEnum.QUERY.value],
    )
    creator: PersonModel | str = Field(
        default=None,
        alias="creator",
        description="The Person who devised the search terms comprising this Query. The creator value MUST be expressed either as an object or as a string corresponding to the creator's IRI.",
    )
    search_target: EntityModel | str = Field(
        default=None,
        alias="searchTarget",
        description="The Entity, typically a DigitalResource or SoftwareApplication, that is the target of the Query. The resourceSearched value MUST be expressed either as an object or as a string corresponding to the resources's IRI.",
    )
    search_terms: str = Field(
        default=None,
        alias="searchTerms",
        description="The search terms employed by the creator of this Query.",
    )


class RatingModel(EntityModel):
    type: Literal[TypeTermEnum.RATING] = Field(
        alias="type",
        examples=[TypeTermEnum.RATING.value],
    )
    rater: PersonModel | str = Field(
        default=None,
        alias="rater",
        description="The Person who provided the Rating. The rater value MUST be expressed either as an object or as a string corresponding to the rater's IRI.",
    )
    rated: EntityModel | str = Field(
        default=None,
        alias="rated",
        description="The Entity which received the rating. The rated value MUST be expressed either as an object or as a string corresponding to the rated object's IRI.",
    )
    question: QuestionModel | str = Field(
        default=None,
        alias="question",
        description="The Question used for the Rating. The question value MUST be expressed either as an object or as a string corresponding to the question's IRI.",
    )
    selections: list[str] = Field(
        default=None,
        alias="selections",
        description="An array of the values representing the rater's selected response.",
    )
    rating_comment: CommentModel | str = Field(
        default=None,
        alias="ratingComment",
        description="The Comment left with the Rating. The ratingComment value MUST be expressed either as an object or as a string corresponding to the comment's IRI.",
    )


class ResponseModel(EntityModel):
    type: Literal[TypeTermEnum.RESPONSE] = Field(
        alias="type",
        examples=[TypeTermEnum.RESPONSE.value],
    )
    attempt: AttemptModel | str = Field(
        default=None,
        alias="attempt",
        description="The associated Attempt. The attempt value MUST be expressed either as an object or as a string corresponding to the attempt's IRI. If an object representation is provided, the Attempt SHOULD reference both the Person who initiated the Response and the relevant DigitalResource such as an AssessmentItem or QuestionnaireItem.",
    )
    started_at_time: str = Field(
        default=None,
        alias="startedAtTime",
        description="An ISO 8601 date and time value expressed with millisecond precision that describes when the  Response was commenced. The value MUST be expressed using the format YYYY-MM-DDTHH:mm:ss.SSSZ set to UTC with no offset specified.",
    )  # DateTime
    ended_at_time: str = Field(
        default=None,
        alias="endedAtTime",
        description="An ISO 8601 date and time value expressed with millisecond precision that describes when the  Response was completed or terminated. The value MUST be expressed using the format YYYY-MM-DDTHH:mm:ss.SSSZ set to UTC with no offset specified.",
    )  # DateTime
    duration: str = Field(
        default=None,
        alias="duration",
        description="A time interval that represents the time taken to complete the Response. If a duration is specified the value MUST conform to the ISO 8601 duration format.",
    )  # Duration


class SessionModel(EntityModel):
    type: Literal[TypeTermEnum.SESSION] = Field(
        alias="type",
        examples=[TypeTermEnum.SESSION.value],
    )
    user: PersonModel | str = Field(default=None, alias="user")
    client: SoftwareApplicationModel = Field(default=None, alias="client")
    started_at_time: str = Field(default=None, alias="startedAtTime")  # Datetime
    ended_at_time: str = Field(default=None, alias="endedAtTime")  # Datetime
    duration: str = Field(default=None, alias="duration")  # Duration ISO 8601


class ResultModel(EntityModel):
    type: Literal[TypeTermEnum.RESULT] = Field(
        alias="type",
        examples=[TypeTermEnum.RESULT.value],
    )
    attempt: AttemptModel | str = Field(
        default=None,
        alias="attempt",
        description="The associated Attempt. The attempt value MUST be expressed either as an object or as a string corresponding to the attempt's IRI. If an object representation is provided, the Attempt SHOULD reference both the Person making the Attempt and the assigned DigitalResource.",
    )
    max_result_score: float = Field(
        default=None,
        alias="maxResultScore",
        description="A number with a fractional part denoted by a decimal separator that designates the maximum result score permitted.",
    )
    result_score: float = Field(
        default=None,
        alias="resultScore",
        description="A number with a fractional part denoted by a decimal separator that designates the actual result score awarded.",
    )
    scored_by: AgentModel | str = Field(
        default=None,
        alias="scoredBy",
        description="The Agent who scored or graded the Attempt. The  scoredBy value MUST be expressed either as an object or as a string corresponding to the scorer's IRI.",
    )
    comment: str = Field(
        default=None,
        alias="comment",
        description="Plain text feedback provided by the scorer.",
    )


class ScaleModel(EntityModel):
    type: Literal[TypeTermEnum.SCALE] = Field(
        alias="type",
        examples=[TypeTermEnum.SCALE.value],
    )


class ScoreModel(EntityModel):
    type: Literal[TypeTermEnum.SCORE] = Field(
        alias="type",
        examples=[TypeTermEnum.SCORE.value],
    )
    attempt: AttemptModel | str = Field(
        default=None,
        alias="attempt",
        description="The associated Attempt. The attempt value MUST be expressed either as an object or as a string corresponding to the attempt's IRI. If an object representation is provided, the Attempt SHOULD reference both the Person who generated the Attempt and the assigned DigitalResource.",
    )
    max_score: float = Field(
        default=None,
        alias="maxScore",
        description="A number with a fractional part denoted by a decimal separator that designates the maximum score permitted.",
    )
    score_given: float = Field(
        default=None,
        alias="scoreGiven",
        description="A number with a fractional part denoted by a decimal separator that designates the actual score awarded.",
    )
    scored_by: AgentModel | str = Field(
        default=None,
        alias="scoredBy",
        description="The Agent who scored or graded the Attempt. The  scoredBy value MUST be expressed either as an object or as a string corresponding to the scorer's IRI.",
    )
    comment: str = Field(
        default=None,
        alias="comment",
        description="Plain text feedback provided by the scorer.",
    )


class SearchResponseModel(EntityModel):
    type: Literal[TypeTermEnum.SEARCHRESPONSE] = Field(
        alias="type",
        examples=[TypeTermEnum.SEARCHRESPONSE.value],
    )
    search_provider: SoftwareApplicationModel | str = Field(
        default=None,
        alias="searchProvider",
        description="The SoftwareApplication that is the provider of this  SearchResponse. The searchProvider value MUST be expressed either as an object or as a string corresponding to the resources's IRI.",
    )
    search_target: EntityModel | str = Field(
        default=None,
        alias="searchTarget",
        description="The Entity, typically a DigitalResource or  SoftwareApplication, that is the target of the search. The resourceSearched value MUST be expressed either as an object or as a string corresponding to the resources's IRI.",
    )
    query: QueryModel | str = Field(
        default=None,
        alias="query",
        description="The Query submitted by the actor.",
    )
    search_results_item_count: int = Field(
        default=None,
        alias="searchResultsItemCount",
        description="A total count of searchResults returned. If the Query submitted returned no results the count equal to zero (0).",
    )


class PageModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.PAGE] = Field(
        alias="type",
        examples=[TypeTermEnum.PAGE.value],
    )


class LtiSessionModel(SessionModel):
    type: Literal[TypeTermEnum.LTISESSION] = Field(
        alias="type",
        examples=[TypeTermEnum.LTISESSION.value],
    )
    message_parameters: dict = Field(
        default=None,
        alias="messageParameters",
        description="A map of LTI-specified message parameters that provide platform-related contextual information",
    )


class AssignableDigitalResourceModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.ASSIGNABLEDIGITALRESOURCE] = Field(
        alias="type",
        examples=[TypeTermEnum.ASSIGNABLEDIGITALRESOURCE.value],
    )
    date_to_activate: str = Field(
        default=None,
        alias="dateToActivate",
        description="An ISO 8601 date and time value expressed with millisecond precision that describes when the resource was activated. The value MUST be expressed using the format YYYY-MM-DDTHH:mm:ss.SSSZ set to UTC with no offset specified.",
    )  # DateTime
    date_to_show: str = Field(
        default=None,
        alias="dateToShow",
        description="An ISO 8601 date and time value expressed with millisecond precision that describes when the resource should be shown or made available to learners. The value MUST be expressed using the format YYYY-MM-DDTHH:mm:ss.SSSZ set to UTC with no offset specified.",
    )  # DateTime
    date_to_start_on: str = Field(
        default=None,
        alias="dateToStartOn",
        description="An ISO 8601 date and time value expressed with millisecond precision that describes when the resource can be started. The value MUST be expressed using the format YYYY-MM-DDTHH:mm:ss.SSSZ set to UTC with no offset specified.",
    )  # DateTime
    date_to_submit: str = Field(
        default=None,
        alias="dateToSubmit",
        description="An ISO 8601 date and time value expressed with millisecond precision that describes when the resource is to be submitted for evaluation. The value MUST be expressed using the format YYYY-MM-DDTHH:mm:ss.SSSZ set to UTC with no offset specified.",
    )  # DateTime
    max_attempts: int = Field(
        default=None,
        alias="maxAttempts",
        description="A non-negative integer that designates the number of permitted attempts.",
    )
    max_submits: int = Field(
        default=None,
        alias="maxSubmits",
        description="A non-negative integer that designates the number of permitted submissions.",
    )
    max_score: float = Field(
        default=None,
        alias="maxScore",
        description="A number with a fractional part denoted by a decimal separator that designates the maximum score permitted.",
    )


class AssessmentItemModel(AssignableDigitalResourceModel):
    type: Literal[TypeTermEnum.ASSESSMENTITEM] = Field(
        alias="type",
        examples=[TypeTermEnum.ASSESSMENTITEM.value],
    )
    is_time_dependent: bool = Field(
        default=None,
        alias="isTimeDependent",
        description="A boolean value indicating whether or not interacting with the item is time dependent.",
    )


class DigitalResourceCollectionModel(CollectionModel, DigitalResourceModel):
    type: Literal[TypeTermEnum.DIGITALRESOURCECOLLECTION] = Field(
        alias="type",
        examples=[TypeTermEnum.DIGITALRESOURCECOLLECTION.value],
    )
    items: list[DigitalResourceModel | str] = Field(
        default=None,
        alias="items",
        description="An ordered collection of DigitalResource entities. Each array item MUST be expressed either as an object or as a string corresponding to the item's IRI.",
    )


class AggregateMeasureCollectionModel(CollectionModel):
    type: Literal[TypeTermEnum.AGGREGATEMEASURECOLLECTION] = Field(
        alias="type",
        examples=[TypeTermEnum.AGGREGATEMEASURECOLLECTION.value],
    )
    items: list[AggregateMeasureModel | str] = Field(
        default=None,
        alias="items",
        description="An ordered collection of AggregateMeasure entities. Each array item MUST be expressed either as an object or as a string corresponding to the item's IRI.",
    )


class AssessmentModel(AssignableDigitalResourceModel, DigitalResourceCollectionModel):
    type: Literal[TypeTermEnum.ASSESSMENT] = Field(
        alias="type",
        examples=[TypeTermEnum.ASSESSMENT.value],
    )
    items: list[AssessmentItemModel | str] = Field(
        default=None,
        alias="items",
        description="An ordered collection of AssessmentItem entities. Each array item MUST be expressed either as an object or as a string corresponding to the item's IRI.",
    )


class MediaObjectModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.MEDIAOBJECT] = Field(
        alias="type",
        examples=[TypeTermEnum.MEDIAOBJECT.value],
    )
    duration: str = Field(
        default=None,
        alias="duration",
        description="An optional time interval that represents the total time required to view and/or listen to the  MediaObject at normal speed. If a duration is specified the value MUST conform to the ISO 8601 duration format.",
    )  # Duration


class AudioObjectModel(MediaObjectModel):
    type: Literal[TypeTermEnum.AUDIOOBJECT] = Field(
        alias="type",
        examples=[TypeTermEnum.AUDIOOBJECT.value],
    )
    volume_level: str = Field(
        default=None,
        alias="volumeLevel",
        description="A string value indicating the current volume level.",
    )
    volume_min: str = Field(
        default=None,
        alias="volumeMin",
        description="A string value indicating the minimum volume level permitted.",
    )
    volume_max: str = Field(
        default=None,
        alias="volumeMax",
        description="A string value indicating the maximum volume level permitted.",
    )
    muted: bool = Field(
        default=None,
        alias="muted",
        description="An optional boolean value indicating whether or not the AudioObject has been muted.",
    )


class BookmarkAnnotationModel(AnnotationModel):
    type: Literal[TypeTermEnum.BOOKMARKANNOTATION] = Field(
        alias="type",
        examples=[TypeTermEnum.BOOKMARKANNOTATION.value],
    )
    bookmark_notes: str = Field(
        default=None,
        alias="bookmarkNotes",
        description="A string value comprising a plain text rendering of the note that accompanies the bookmark.",
    )


class ChapterModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.CHAPTER] = Field(
        alias="type",
        examples=[TypeTermEnum.CHAPTER.value],
    )


class CourseOfferingModel(OrganizationModel):
    type: Literal[TypeTermEnum.COURSEOFFERING] = Field(
        alias="type",
        examples=[TypeTermEnum.COURSEOFFERING.value],
    )
    course_number: str = Field(
        default=None,
        alias="courseNumber",
        description="A string value that constitutes a human-readable identifier for the CourseOffering.",
    )
    academic_session: str = Field(
        default=None,
        alias="academicSession",
        description="A string value that constitutes a human-readable identifier of the designated period in which this  CourseOffering occurs.",
    )


class CourseSectionModel(CourseOfferingModel):
    type: Literal[TypeTermEnum.COURSESECTION] = Field(
        alias="type",
        examples=[TypeTermEnum.COURSESECTION.value],
    )
    category: str = Field(
        default=None,
        alias="category",
        description="A string value that characterizes the purpose of the section such as lecture, lab or seminar.",
    )


class DateTimeQuestionModel(QuestionModel):
    type: Literal[TypeTermEnum.DATETIMEQUESTION] = Field(
        alias="type",
        examples=[TypeTermEnum.DATETIMEQUESTION.value],
    )
    min_date_time: str = Field(
        default=None,
        alias="minDateTime",
        description="A DateTime value used to determine the minimum value allowed.",
    )  # DateTime
    min_label: str = Field(
        default=None,
        alias="minLabel",
        description="The label for the minimum DateTime.",
    )
    max_date_time: str = Field(
        default=None,
        alias="maxDateTime",
        description="A DateTime value used to determine the maximum value allowed.",
    )  # DateTime
    max_label: str = Field(
        default=None,
        alias="maxLabel",
        description="The label for the maximum value.",
    )


class DateTimeResponseModel(ResponseModel):
    type: Literal[TypeTermEnum.DATETIMERESPONSE] = Field(
        alias="type",
        examples=[TypeTermEnum.DATETIMERESPONSE.value],
    )
    date_time_selected: str = Field(
        default=None,
        alias="dateTimeSelected",
        description="The DateTime selected in response to the question.",
    )  # DateTime


class DocumentModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.DOCUMENT] = Field(
        alias="type",
        examples=[TypeTermEnum.DOCUMENT.value],
    )


class FillinBlankResponseModel(ResponseModel):
    type: Literal[TypeTermEnum.FILLINBLANKRESPONSE] = Field(
        alias="type",
        examples=[TypeTermEnum.FILLINBLANKRESPONSE.value],
    )
    values: list[str] = Field(
        default=None,
        alias="values",
        description="An ordered collection of one or more string values representing words, expressions or short phrases that constitute the 'fill in the blank' response.",
    )


class MessageModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.MESSAGE] = Field(
        alias="type",
        examples=[TypeTermEnum.MESSAGE.value],
    )
    reply_to: MessageModel | str = Field(
        default=None,
        alias="replyTo",
        description="A Message that represents the post to which this Message is directed in reply. The replyTo value MUST be expressed either as an object or as a string corresponding to the associated message's IRI.",
    )
    body: str = Field(
        default=None,
        alias="body",
        description="A string value comprising a plain-text rendering of the body content of the  Message.",
    )
    attachments: list[DigitalResourceModel | str] = Field(
        default=None,
        alias="attachments",
        description="An ordered collection of one or more DigitalResource entities attached to this Message. Each array item MUST be expressed either as an object or as a string corresponding to the item's IRI.",
    )


class ThreadModel(DigitalResourceCollectionModel):
    type: Literal[TypeTermEnum.THREAD] = Field(
        alias="type",
        examples=[TypeTermEnum.THREAD.value],
    )
    items: list[MessageModel | str] = Field(
        default=None,
        alias="items",
        description="An ordered collection of Message entities. Each array item MUST be expressed either as an object or as a string corresponding to the item's IRI.",
    )


class ForumModel(DigitalResourceCollectionModel):
    type: Literal[TypeTermEnum.FORUM] = Field(
        alias="type",
        examples=[TypeTermEnum.FORUM.value],
    )
    items: list[ThreadModel | str] = Field(
        default=None,
        alias="items",
        description="An ordered collection of Thread entities. Each array item MUST be expressed either as an object or as a string corresponding to the item's IRI.",
    )


class FrameModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.FRAME] = Field(
        alias="type",
        examples=[TypeTermEnum.FRAME.value],
    )
    index: int = Field(
        default=None,
        alias="index",
        description="A non-negative integer that represents the position of the Frame.",
    )


class GroupModel(OrganizationModel):
    type: Literal[TypeTermEnum.GROUP] = Field(
        alias="type",
        examples=[TypeTermEnum.GROUP.value],
    )


class HighlightAnnotationModel(AnnotationModel):
    type: Literal[TypeTermEnum.HIGHLIGHTANNOTATION] = Field(
        alias="type",
        examples=[TypeTermEnum.HIGHLIGHTANNOTATION.value],
    )
    selection_text: str = Field(
        default=None,
        alias="selectionText",
        description="A string value representing a plain-text rendering of the highlighted segment of the annotated DigitalResource.",
    )


class ImageObjectModel(MediaObjectModel):
    type: Literal[TypeTermEnum.IMAGEOBJECT] = Field(
        alias="type",
        examples=[TypeTermEnum.IMAGEOBJECT.value],
    )


class LikertScaleModel(ScaleModel):
    type: Literal[TypeTermEnum.LIKERTSCALE] = Field(
        alias="type",
        examples=[TypeTermEnum.LIKERTSCALE.value],
    )
    scale_points: int = Field(
        default=None,
        alias="scalePoints",
        description="A integer value used to determine the amount of points on the LikertScale.",
    )
    item_labels: list[str] = Field(
        default=None,
        alias="itemLabels",
        description="The ordered list of labels for each point on the scale. The values MUST be cast as strings.",
    )
    item_values: list[str] = Field(
        default=None,
        alias="itemValues",
        description="The ordered list of values for each point on the scale. The values MUST be cast as strings.",
    )


class LtiLinkModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.LTILINK] = Field(
        alias="type",
        examples=[TypeTermEnum.LTILINK.value],
    )
    message_type: LtiMessageTypesEnum = Field(
        default=None,
        alias="messageType",
        description="If present, the string value MUST be set to the term name of the LTI message type used to gain access to this LTI resource link (including but not limited to, LtiResourceLinkRequest or LtiDeepLinkingRequest, LtiDeepLinkingResponse).",
    )


class MediaLocationModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.MEDIALOCATION] = Field(
        alias="type",
        examples=[TypeTermEnum.MEDIALOCATION.value],
    )
    current_time: str = Field(
        default=None,
        alias="currentTime",
        description="A time interval or duration that represents the current playback position measured from the beginning of an AudioObject or VideoObject. If a  currentTime is specified the value MUST conform to the ISO 8601 duration format.",
    )  # Duration


class MultipleChoiceResponseModel(ResponseModel):
    type: Literal[TypeTermEnum.MULTIPLECHOICERESPONSE] = Field(
        alias="type",
        examples=[TypeTermEnum.MULTIPLECHOICERESPONSE.value],
    )
    value: str = Field(
        default=None,
        alias="value",
        description="A string value that represents the selected option.",
    )


class MultipleResponseResponseModel(ResponseModel):
    type: Literal[TypeTermEnum.MULTIPLERESPONSERESPONSE] = Field(
        alias="type",
        examples=[TypeTermEnum.MULTIPLERESPONSERESPONSE.value],
    )
    values: list[str] = Field(
        default=None,
        alias="values",
        description="An ordered collection of one or more selected options MAY be specified",
    )


class MultiselectQuestionModel(QuestionModel):
    type: Literal[TypeTermEnum.MULTISELECTQUESTION] = Field(
        alias="type",
        examples=[TypeTermEnum.MULTISELECTQUESTION.value],
    )
    points: int = Field(
        default=None,
        alias="points",
        description="A integer value used to determine the amount of points on the MultiselectQuestion.",
    )
    item_labels: list[str] = Field(
        default=None,
        alias="itemLabels",
        description="The list of labels that describe the set of selectable question options. Each label MUST be cast as a string.",
    )
    item_values: list[str] = Field(
        default=None,
        alias="itemValues",
        description="The list of values associated with the set of selectable question options. Each value MUST be cast as a string.",
    )


class MultiselectResponseModel(ResponseModel):
    type: Literal[TypeTermEnum.MULTISELECTRESPONSE] = Field(
        alias="type",
        examples=[TypeTermEnum.MULTISELECTRESPONSE.value],
    )
    selections: list[str] = Field(
        default=None,
        alias="selections",
        description="An array of the values representing the rater's selected responses.",
    )


class MultiselectScaleModel(ScaleModel):
    type: Literal[TypeTermEnum.MULTISELECTSCALE] = Field(
        alias="type",
        examples=[TypeTermEnum.MULTISELECTSCALE.value],
    )
    scale_points: int = Field(
        default=None,
        alias="scalePoints",
        description="A integer value used to determine the amount of points on the MultiselectScale.",
    )
    item_labels: list[str] = Field(
        default=None,
        alias="itemLabels",
        description="The ordered list of labels for each point on the scale. The values MUST be cast as strings.",
    )
    item_values: list[str] = Field(
        default=None,
        alias="itemValues",
        description="The ordered list of values for each point on the scale. The values MUST be cast as strings.",
    )
    is_ordered_selection: bool = Field(
        default=None,
        alias="isOrderedSelection",
        description="Indicates whether the order of the selected items is important.",
    )
    min_selections: int = Field(
        default=None,
        alias="minSelections",
        description="Indicates the minimum number of selections that can be chosen.",
    )
    max_selections: int = Field(
        default=None,
        alias="maxSelections",
        description="Indicates the maximum number of selections that can be chosen.",
    )


class NumericScaleModel(ScaleModel):
    type: Literal[TypeTermEnum.NUMERICSCALE] = Field(
        alias="type",
        examples=[TypeTermEnum.NUMERICSCALE.value],
    )
    min_value: float = Field(
        default=None,
        alias="minValue",
        description="A decimal value used to determine the minimum value of the NumericScale.",
    )
    min_label: str = Field(
        default=None,
        alias="minLabel",
        description="The label for the minimum value.",
    )
    max_value: float = Field(
        default=None,
        alias="maxValue",
        description="A decimal value used to determine the maximum value of the NumericScale.",
    )
    max_label: str = Field(
        default=None,
        alias="maxLabel",
        description="The label for the maximum value.",
    )
    step: float = Field(
        default=None,
        alias="step",
        description="Indicates the decimal step used for determining the options between the minimum and maximum values.",
    )


class OpenEndedQuestionModel(QuestionModel):
    type: Literal[TypeTermEnum.OPENENDEDQUESTION] = Field(
        alias="type",
        examples=[TypeTermEnum.OPENENDEDQUESTION.value],
    )


class OpenEndedResponseModel(ResponseModel):
    type: Literal[TypeTermEnum.OPENENDEDRESPONSE] = Field(
        alias="type",
        examples=[TypeTermEnum.OPENENDEDRESPONSE.value],
    )
    value: str = Field(
        default=None,
        alias="value",
        description="the textual value of the response.",
    )


class QuestionnaireItemModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.QUESTIONNAIREITEM] = Field(
        alias="type",
        examples=[TypeTermEnum.QUESTIONNAIREITEM.value],
    )
    question: QuestionModel | str = Field(
        default=None,
        alias="question",
        description="The Question entity posed by the QuestionnaireItem. The Question value MUST be expressed either as an object or as a string corresponding to the question's IRI.",
    )
    categories: list[str] = Field(
        default=None,
        alias="categories",
        description="An array of category items comprising the categories the QuestionnaireItem encompasses. Each category item MUST be cast as a string.",
    )
    weight: float = Field(
        default=None,
        alias="weight",
        description="A decimal value used to determine the weight of the QuestionnaireItem.",
    )


class QuestionnaireModel(DigitalResourceCollectionModel):
    type: Literal[TypeTermEnum.QUESTIONNAIRE] = Field(
        alias="type",
        examples=[TypeTermEnum.QUESTIONNAIRE.value],
    )
    items: list[QuestionnaireItemModel | str] = Field(
        alias="items",
        description="An array of one or more QuestionnaireItem entities that together comprise the Questionnaire. The object value MUST be expressed either as an object or as a string corresponding to the resource's IRI.",
    )


class RatingScaleQuestionModel(QuestionModel):
    type: Literal[TypeTermEnum.RATINGSCALEQUESTION] = Field(
        alias="type",
        examples=[TypeTermEnum.RATINGSCALEQUESTION.value],
    )
    scale: ScaleModel | str = Field(
        default=None,
        alias="scale",
        description="The Scale used in the question. The scale value MUST be expressed either as an object or as a string corresponding to the scale's IRI.",
    )


class RatingScaleResponseModel(ResponseModel):
    type: Literal[TypeTermEnum.RATINGSCALERESPONSE] = Field(
        alias="type",
        examples=[TypeTermEnum.RATINGSCALERESPONSE.value],
    )
    selections: list[str] = Field(
        default=None,
        alias="selections",
        description="An array of the values representing the rater's selected responses.",
    )


class SelectTextResponseModel(ResponseModel):
    type: Literal[TypeTermEnum.SELECTTEXTRESPONSE] = Field(
        alias="type",
        examples=[TypeTermEnum.SELECTTEXTRESPONSE.value],
    )
    values: list[str] = Field(
        default=None,
        alias="values",
        description="An ordered collection of one or more selected options.",
    )


class SharedAnnotationModel(AnnotationModel):
    type: Literal[TypeTermEnum.SHAREDANNOTATION] = Field(
        alias="type",
        examples=[TypeTermEnum.SHAREDANNOTATION.value],
    )
    with_agents: list[AgentModel | PersonModel | str] = Field(
        default=None,
        alias="withAgents",
        description="An ordered collection of one or more Agent entities, typically of type Person, with whom the annotated DigitalResource has been shared. Each array item MUST be expressed either as an object or as a string corresponding to the item's IRI.",
    )


class SurveyModel(CollectionModel):
    type: Literal[TypeTermEnum.SURVEY] = Field(
        alias="type",
        examples=[TypeTermEnum.SURVEY.value],
    )
    items: list[QuestionnaireModel | str] = Field(
        default=None,
        alias="items",
        description="An array of one or more Questionnaire entities that together comprise the Survey. Each array item MUST be expressed either as an object or as a string corresponding to the Questionnaire resource's IRI.",
    )


class SurveyInvitationModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.SURVEYINVITATION] = Field(
        alias="type",
        examples=[TypeTermEnum.SURVEYINVITATION.value],
    )
    rater: PersonModel | str = Field(
        default=None,
        alias="rater",
        description="The Person which will rate the Survey. The rater value MUST be expressed either as an object or as a string corresponding to the rater resource's IRI.",
    )
    survey: SurveyModel | str = Field(
        default=None,
        alias="survey",
        description="The Survey that the invitation is for. The survey value MUST be expressed either as an object or as a string corresponding to the rater resource's IRI.",
    )
    sent_count: int = Field(
        default=None,
        alias="sentCount",
        description="An integer value used to determine the amount of times the invitation was sent to the rater.",
    )
    date_sent: str = Field(
        default=None,
        alias="dateSent",
        description="An ISO 8601 date and time value expressed with millisecond precision that describes when the  SurveyInvitation was sent. The value MUST be expressed using the format YYYY-MM-DDTHH:mm:ss.SSSZ set to UTC with no offset specified.",
    )  # DateTime


class TagAnnotationModel(AnnotationModel):
    type: Literal[TypeTermEnum.TAGANNOTATION] = Field(
        alias="type",
        examples=[TypeTermEnum.TAGANNOTATION.value],
    )
    tags: list[str] = Field(
        default=None,
        alias="tags",
        description="An ordered collection of one or more string values that represent the tags associated with the annotated DigitalResource.",
    )


class TrueFalseResponseModel(ResponseModel):
    type: Literal[TypeTermEnum.TRUEFALSERESPONSE] = Field(
        alias="type",
        examples=[TypeTermEnum.TRUEFALSERESPONSE.value],
    )
    value: str = Field(
        default=None,
        alias="value",
        description="A string value that provides the true/false, yes/no binary selection SHOULD be provided.",
    )


class VideoObjectModel(MediaObjectModel):
    type: Literal[TypeTermEnum.VIDEOOBJECT] = Field(
        alias="type",
        examples=[TypeTermEnum.VIDEOOBJECT.value],
    )


class WebPageModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.WEBPAGE] = Field(
        alias="type",
        examples=[TypeTermEnum.WEBPAGE.value],
    )


##################################################
##################### EVENTS #####################
##################################################
class EventModel(ExtendedTypeBaseModel):
    context: Literal["http://purl.imsglobal.org/ctx/caliper/v1p2"] = Field(
        default=None,
        alias="@context",
        examples=["http://purl.imsglobal.org/ctx/caliper/v1p2"],
    )
    id: str = Field(
        alias="id",
        description="The emitting application MUST provision the Event with a UUID. A version 4 UUID SHOULD be generated. The UUID MUST be expressed as a URN using the form 'urn:uuid:<UUID>' per [RFC4122].",
        examples=["urn:uuid:cf6e0f3b-3511-4254-86c5-6936ff33f267"],
    )
    type: Literal[TypeTermEnum.EVENT] = Field(
        alias="type",
        description="A string value corresponding to the Term defined for the Event in the external 1EdTech Caliper JSON-LD context document. For a generic Event set the type to the string value Event. If a subtype of Entity is created, set the type to the Term corresponding to the subtype utilized, e.g., NavigationEvent.",
        examples=[TypeTermEnum.NAVIGATIONEVENT.value],
    )
    profile: ProfileTermEnum = Field(
        default=None,
        alias="profile",
        description="A string value corresponding to the Profile Term value defined for the Profile that governs the rules of interpretation for this Event. The range of Profile values is limited to the set of profiles described in this specification and any profile extension specifications extending this specification. Only one Profile Term value may be specified per Event. For a generic Event set the profile property value to the string term GeneralProfile.",
        examples=[ProfileTermEnum.GENERALPROFILE.value],
    )
    actor: AgentModel | str = Field(
        alias="actor",
        description="The Agent who initiated the Event, typically though not always a Person. The action value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: ActionTermEnum = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The action range is limited to the set of actions described in this specification or associated profiles and may be further constrained by the chosen Event type. Only one action Term may be specified per Event.",
        examples=[ActionTermEnum.NAVIGATEDTO.value],
    )
    object: EntityModel | str = Field(
        alias="object",
        description="The Entity that comprises the object of the interaction. The object value MUST be expressed either as an object or as a string corresponding to the object's IRI.",
    )
    event_time: str = Field(
        alias="eventTime",
        description="An ISO 8601 date and time value expressed with millisecond precision that indicates when the Event occurred. The value MUST be expressed using the format YYYY-MM-DDTHH:mm:ss.SSSZ set to UTC with no offset specified.",
        examples=["2019-11-01T00:09:06.878Z"],
    )  # Datetime
    ed_app: SoftwareApplicationModel | str = Field(
        default=None,
        alias="edApp",
        description="A SoftwareApplication that constitutes the application context. The edApp value MUST be expressed either as an object or as a string corresponding to the edApp's IRI.",
    )
    generated: EntityModel | str = Field(
        default=None,
        alias="generated",
        description="An Entity created or generated as a result of the interaction. The  generated value MUST be expressed either as an object or as a string corresponding to the generated entity's IRI.",
    )
    target: EntityModel | str = Field(
        default=None,
        alias="target",
        description="An Entity that represents a particular segment or location within the  object. The target value MUST be expressed either as an object or as a string corresponding to the target entity's IRI.",
    )
    referrer: EntityModel | str = Field(
        default=None,
        alias="referrer",
        description="An Entity that represents the referring context. A SoftwareApplication or DigitalResource will typically constitute the referring context. The referrer value MUST be expressed either as an object or as a string corresponding to the referrer's IRI.",
        examples=[
            "https://oxana.instructure.com/courses/565/discussion_topics/1072925?module_item_id=4635201",
        ],
    )
    group: CourseSectionModel | OrganizationModel | str = Field(
        default=None,
        alias="group",
        description="An Organization that represents the group context. The group value MUST be expressed either as an object or as a string corresponding to the group's IRI.",
    )
    membership: MembershipModel | str = Field(
        default=None,
        alias="membership",
        description="The relationship between the action and the group in terms of roles assigned and current status. The membership value MUST be expressed either as an object or as a string corresponding to the membership entity's IRI.",
    )
    session: SessionModel | str = Field(
        default=None,
        alias="session",
        description="The current user Session. The session value MUST be expressed either as an object or as a string corresponding to the session's IRI.",
    )
    federated_session: LtiSessionModel | str = Field(
        default=None,
        alias="federatedSession",
        description="If the Event occurs within the context of an LTI platform launch, the tool's LtiSession MAY be referenced. The federatedSession value MUST be expressed either as an object or as a string corresponding to the federated session's IRI.",
    )
    extensions: dict = Field(
        default=None,
        alias="extensions",
        description="A map of additional attributes not defined by the model MAY be specified for a more concise representation of the Event.",
    )


class AnnotationEventModel(EventModel):
    type: Literal[TypeTermEnum.ANNOTATIONEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.ANNOTATIONEVENT.value],
    )
    actor: PersonModel | str = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: Literal[
        ActionTermEnum.BOOKMARKED,
        ActionTermEnum.HIGHLIGHTED,
        ActionTermEnum.SHARED,
        ActionTermEnum.TAGGED,
    ] = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the Bookmarked, Highlighted, Shared, and Tagged actions only.",
    )
    object: DigitalResourceModel | str = Field(
        alias="object",
        description="The annotated DigitalResource that constitutes the object of the interaction. The object value MUST be expressed either as an object or as a string corresponding to the object's IRI.",
    )
    target: FrameModel | str = Field(
        default=None,
        alias="target",
        description="A Frame that represents a particular segment or location within the object. The target value MUST be expressed either as an object or as a string corresponding to the target entity's IRI.",
    )
    generated: AnnotationModel | str = Field(
        default=None,
        alias="generated",
        description="The generated Annotation or a subtype. The generated value MUST be expressed either as an object or as a string corresponding to the generated entity's IRI.",
    )


class AssessmentEventModel(EventModel):
    type: Literal[TypeTermEnum.ASSESSMENTEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.ASSESSMENTEVENT.value],
    )
    actor: PersonModel | str = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: Literal[
        ActionTermEnum.PAUSED,
        ActionTermEnum.RESET,
        ActionTermEnum.RESTARTED,
        ActionTermEnum.RESUMED,
        ActionTermEnum.STARTED,
        ActionTermEnum.SUBMITTED,
    ] = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the Started, Paused, Resumed, Restarted, Reset, and Submitted actions only.",
    )
    object: AssessmentModel | str = Field(
        alias="object",
        description="The object value MUST be expressed either as an object or as a string corresponding to the object's IRI.",
    )
    generated: AttemptModel | str = Field(
        default=None,
        alias="generated",
        description="The generated value MUST be expressed either as an object or as a string corresponding to the generated entity's IRI.",
    )


class AssessmentItemEventModel(EventModel):
    type: Literal[TypeTermEnum.ASSESSMENTITEMEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.ASSESSMENTITEMEVENT.value],
    )
    actor: PersonModel | str = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: Literal[
        ActionTermEnum.COMPLETED,
        ActionTermEnum.SKIPPED,
        ActionTermEnum.STARTED,
    ] = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the Started, Skipped, and Completed actions only.",
    )
    object: AssessmentItemModel | str = Field(
        alias="object",
        description="The object value MUST be expressed either as an object or as a string corresponding to the object's IRI.",
    )
    generated: AttemptModel | ResponseModel | str = Field(
        default=None,
        alias="generated",
        description="For a completed action a generated Response or a subtype. The generated value MUST be expressed either as an object or as a string corresponding to the generated entity's IRI.",
    )
    referrer: AssessmentItemModel | str = Field(
        default=None,
        alias="referrer",
        description="The previous AssessmentItem attempted MAY be specified as the  referrer. The referrer value MUST be expressed either as an object or as a string corresponding to the referrer's IRI.",
    )


class AssignableEventModel(EventModel):
    type: Literal[TypeTermEnum.ASSIGNABLEEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.ASSIGNABLEEVENT.value],
    )
    actor: PersonModel | str = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: Literal[
        ActionTermEnum.ACTIVATED,
        ActionTermEnum.COMPLETED,
        ActionTermEnum.DEACTIVATED,
        ActionTermEnum.REVIEWED,
        ActionTermEnum.STARTED,
        ActionTermEnum.SUBMITTED,
    ] = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the Activated, Deactivated, Started, Completed, Submitted, and Reviewed actions only.",
    )
    object: AssignableDigitalResourceModel | str = Field(
        alias="object",
        description="The AssignableDigitalResource that constitutes the  object of the interaction. The object value MUST be expressed either as an object or as a string corresponding to the object's IRI.",
    )
    target: FrameModel | str = Field(
        default=None,
        alias="target",
        description="A Frame that represents a particular segment or location within the object. The target value MUST be expressed either as an object or as a string corresponding to the target entity's IRI.",
    )
    generated: AttemptModel | str = Field(
        default=None,
        alias="generated",
        description="For Started, Completed and Reviewed actions, the actor's Attempt SHOULD be specified. The generated value MUST be expressed either as an object or as a string corresponding to the generated entity's IRI.",
    )


class FeedbackEventModel(EventModel):
    type: Literal[TypeTermEnum.FEEDBACKEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.FEEDBACKEVENT.value],
    )
    actor: PersonModel | str = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: Literal[
        ActionTermEnum.COMMENTED,
        ActionTermEnum.RANKED,
    ] = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the Commented and Ranked actions only.",
    )
    object: EntityModel | str = Field(
        alias="object",
        description="The Entity that is the target of the feedback. The object value MUST be expressed either as an object or as a string corresponding to the resource's IRI.",
    )
    target: FrameModel | str = Field(
        default=None,
        alias="target",
        description="If the object of the feedback is a particular segment of a DigitalResource use a Frame to mark its location. The target value MUST be expressed either as an object or as a string corresponding to the target entity's IRI.",
    )
    generated: CommentModel | RatingModel | str = Field(
        default=None,
        alias="generated",
        description="The Rating or Comment entity that describes the feedback provided. If the action is Ranked then the  generated value MUST be expressed as a Rating. If the action is Commented then the generated value MUST be expressed as a Comment. The generated value MUST be expressed either as an object or as a string corresponding to the entity's IRI.",
    )


class ForumEventModel(EventModel):
    type: Literal[TypeTermEnum.FORUMEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.FORUMEVENT.value],
    )
    actor: PersonModel | str = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: Literal[
        ActionTermEnum.SUBSCRIBED,
        ActionTermEnum.UNSUBSCRIBED,
    ] = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the Subscribed and Unsubscribed actions only.",
    )
    object: ForumModel | str = Field(
        alias="object",
        description="The Forum that comprises the object of this interaction. The  object value MUST be expressed either as an object or as a string corresponding to the object's IRI.",
    )


class GradeEventModel(EventModel):
    type: Literal[TypeTermEnum.GRADEEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.GRADEEVENT.value],
    )
    actor: AgentModel | str = Field(
        alias="actor",
        description="An Agent, typically Person or SoftwareApplication, MUST be specified as the actor. The  actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: Literal[ActionTermEnum.GRADED,] = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the Graded action only.",
    )
    object: AttemptModel | str = Field(
        alias="object",
        description="The completed Attempt. The object value MUST be expressed either as an object or as a string corresponding to the object's IRI.",
    )
    generated: ScoreModel | str = Field(
        default=None,
        alias="generated",
        description="The generated Score SHOULD be provided. The generated value MUST be expressed either as an object or as a string corresponding to the generated entity's IRI.",
    )


class MediaEventModel(EventModel):
    type: Literal[TypeTermEnum.MEDIAEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.MEDIAEVENT.value],
    )
    actor: PersonModel | str = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: Literal[
        ActionTermEnum.CHANGEDRESOLUTION,
        ActionTermEnum.CHANGEDSIZE,
        ActionTermEnum.CHANGEDSPEED,
        ActionTermEnum.CHANGEDVOLUME,
        ActionTermEnum.CLOSEDPOPOUT,
        ActionTermEnum.DISABLEDCLOSEDCAPTIONING,
        ActionTermEnum.ENABLEDCLOSEDCAPTIONING,
        ActionTermEnum.ENDED,
        ActionTermEnum.ENTEREDFULLSCREEN,
        ActionTermEnum.EXITEDFULLSCREEN,
        ActionTermEnum.FORWARDEDTO,
        ActionTermEnum.JUMPEDTO,
        ActionTermEnum.MUTED,
        ActionTermEnum.OPENEDPOPOUT,
        ActionTermEnum.PAUSED,
        ActionTermEnum.RESTARTED,
        ActionTermEnum.RESUMED,
        ActionTermEnum.STARTED,
        ActionTermEnum.UNMUTED,
    ] = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the Started, Ended, Paused, Resumed, Restarted, ForwardedTo, JumpedTo, ChangedResolution, ChangedSize, ChangedSpeed, ChangedVolume, EnabledClosedCaptioning, DisabledClosedCaptioning, EnteredFullScreen, ExitedFullScreen, Muted, Unmuted, OpenedPopout, and ClosedPopout actions only.",
    )
    object: MediaObjectModel | str = Field(
        alias="object",
        description="The MediaObject or a subtype that constitutes the object of the interaction. The object value MUST be expressed either as an object or as a string corresponding to the object's IRI.",
    )
    target: MediaLocationModel | str = Field(
        default=None,
        alias="target",
        description="If the MediaEvent object is an AudioObject or VideoObject, a MediaLocation SHOULD be specified in order to provide the currentTime in the audio or video stream that marks the action. If the  currentTime is specified, the value MUST be an ISO 8601 formatted duration, e.g., 'PT30M54S'. The target value MUST be expressed either as an object or as a string corresponding to the target entity's IRI.",
    )


class MessageEventModel(EventModel):
    type: Literal[TypeTermEnum.MESSAGEEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.MESSAGEEVENT.value],
    )
    actor: PersonModel | str = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: Literal[
        ActionTermEnum.MARKEDASREAD,
        ActionTermEnum.MARKEDASUNREAD,
        ActionTermEnum.POSTED,
    ] = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the MarkedAsRead, MarkedAsUnRead, and Posted actions only.",
    )
    object: MessageModel | str = Field(
        alias="object",
        description="The Message that constitutes the object of the interaction. If the object represents a Message posted in reply to a previous post, the prior post prompting the Message SHOULD be referenced using the Message replyTo property. The object value MUST be expressed either as an object or as a string corresponding to the object's IRI.",
    )


class NavigationEventModel(EventModel):
    type: Literal[TypeTermEnum.NAVIGATIONEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.NAVIGATIONEVENT.value],
    )
    actor: PersonModel | str = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: Literal[ActionTermEnum.NAVIGATEDTO,] = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the  object. The value range is limited to the actions: NavigatedTo.",
    )
    object: DigitalResourceModel | SoftwareApplicationModel | str = Field(
        alias="object",
        description="The DigitalResource or SoftwareApplication to which the actor navigated. The object value MUST be expressed either as an object or as a string corresponding to the resource's IRI.",
    )
    target: DigitalResourceModel | str = Field(
        default=None,
        alias="target",
        description="The DigitalResource that represents the particular part or location of the object being navigated to. The target value MUST be expressed either as an object or as a string corresponding to the referrer's IRI.",
    )
    referrer: DigitalResourceModel | SoftwareApplicationModel | str = Field(
        default=None,
        alias="referrer",
        description="The DigitalResource or SoftwareApplication that constitutes the referring context. The referrer value MUST be expressed either as an object or as a string corresponding to the referrer's IRI.",
    )


class QuestionnaireEventModel(EventModel):
    type: Literal[TypeTermEnum.QUESTIONNAIREEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.QUESTIONNAIREEVENT.value],
    )
    actor: PersonModel | str = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: Literal[
        ActionTermEnum.STARTED,
        ActionTermEnum.SUBMITTED,
    ] = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the actions: Started, or Submitted.",
    )
    object: QuestionnaireModel | str = Field(
        alias="object",
        description="The Questionnaire that the actor is taking. The  object value MUST be expressed either as an object or as a string corresponding to the resource's IRI.",
    )


class QuestionnaireItemEventModel(EventModel):
    type: Literal[TypeTermEnum.QUESTIONNAIREITEMEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.QUESTIONNAIREITEMEVENT.value],
    )
    actor: PersonModel | str = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: Literal[
        ActionTermEnum.COMPLETED,
        ActionTermEnum.SKIPPED,
        ActionTermEnum.STARTED,
    ] = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the actions: Started, Skipped, or Completed.",
    )
    object: QuestionnaireItemModel | str = Field(
        alias="object",
        description="The QuestionnaireItem started, attempted, or skipped by the  actor. The object value MUST be expressed either as an object or as a string corresponding to the resource's IRI.",
    )
    generated: ResponseModel | str = Field(
        default=None,
        alias="generated",
        description="For a Completed action a generated Response MAY be referenced. The generated value MUST be expressed either as an object or as a string corresponding to the Response resource's IRI.",
    )


class ResourceManagementEventModel(EventModel):
    type: Literal[TypeTermEnum.RESOURCEMANAGEMENTEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.RESOURCEMANAGEMENTEVENT.value],
    )
    actor: PersonModel | str = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: Literal[
        ActionTermEnum.ARCHIVED,
        ActionTermEnum.COPIED,
        ActionTermEnum.CREATED,
        ActionTermEnum.DELETED,
        ActionTermEnum.DESCRIBED,
        ActionTermEnum.DOWNLOADED,
        ActionTermEnum.MODIFIED,
        ActionTermEnum.PRINTED,
        ActionTermEnum.PUBLISHED,
        ActionTermEnum.RESTORED,
        ActionTermEnum.RETRIEVED,
        ActionTermEnum.SAVED,
        ActionTermEnum.UNPUBLISHED,
        ActionTermEnum.UPLOADED,
    ] = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the  object. The value range is limited to the Archived, Copied, Created, Deleted, Described, Downloaded, Modified, Printed, Published, Restored, Retrieved, Saved, Unpublished, and Uploaded actions only.",
    )
    object: DigitalResourceModel | str = Field(
        alias="object",
        description="The DigitalResource that is being managed. The  object value MUST be expressed either as an object or as a string corresponding to the resource's IRI.",
    )
    generated: DigitalResourceModel | str = Field(
        default=None,
        alias="generated",
        description="The DigitalResource that was generated by the Copied action. The object value MUST be expressed either as an object or as a string corresponding to the resource's IRI. (Copied action only)",
    )

    @field_validator("generated")
    @staticmethod
    def generated_required_condition(generated, values) -> None:
        """Required when the action value is Copied, otherwise optional."""
        if values.data.get("action", "") == ActionTermEnum.COPIED and not generated:
            raise ValueError(
                f"generated cannot be empty if action is {ActionTermEnum.COPIED}",
            )


class SearchEventModel(EventModel):
    type: Literal[TypeTermEnum.SEARCHEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.SEARCHEVENT.value],
    )
    actor: PersonModel | str = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: Literal[ActionTermEnum.SEARCHED,] = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the  object. The value range is limited to the Searched action only.",
    )
    object: EntityModel | str = Field(
        alias="object",
        description="The Entity, typically a DigitalResource or SoftwareApplication, that is the target of the search. The object value MUST be expressed either as an object or as a string corresponding to the resources's IRI.",
    )
    generated: SearchResponseModel | str = Field(
        default=None,
        alias="generated",
        description="The SearchResponse generated by the search provider that describes the search criteria, count of search results returned (if any), and references to the search result items (if any) returned by the search. The SearchResponse value MUST be expressed either as an object or as a string corresponding to the query's IRI.",
    )


class SessionEventModel(EventModel):
    type: Literal[TypeTermEnum.SESSIONEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.SESSIONEVENT.value],
    )
    actor: PersonModel | SoftwareApplicationModel | str = Field(
        alias="actor",
        description="The Agent who initiated the action. For LoggedIn and LoggedOut actions a Person MUST be specified as the actor. For a TimedOut action a SoftwareApplication MUST be specified as the actor. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: Literal[
        ActionTermEnum.LOGGEDIN,
        ActionTermEnum.LOGGEDOUT,
        ActionTermEnum.TIMEDOUT,
    ] = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the LoggedIn, LoggedOut, and TimedOut actions only.",
    )
    object: SessionModel | SoftwareApplicationModel | str = Field(
        alias="object",
        description="For LoggedIn and LoggedOut actions a SoftwareApplication MUST be specified as the object. For a TimedOut action the Session MUST be specified as the object. The object value MUST be expressed either as an object or as a string corresponding to the object's IRI.",
    )
    target: DigitalResourceModel | str = Field(
        default=None,
        alias="target",
        description="When logging in to a SoftwareApplication, if the actor is attempting to access a particular DigitalResource it MAY be designated as the  target of the interaction. The target value MUST be expressed either as an object or as a string corresponding to the target entity's IRI.",
    )
    referrer: DigitalResourceModel | SoftwareApplicationModel | str = Field(
        default=None,
        alias="referrer",
        description="The DigitalResource or SoftwareApplication that constitutes the referring context MAY be specified as the referrer. The  referrer value MUST be expressed either as an object or as a string corresponding to the referrer's IRI.",
    )


class SurveyEventModel(EventModel):
    type: Literal[TypeTermEnum.SURVEYEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.SURVEYEVENT.value],
    )
    actor: PersonModel | str = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: Literal[
        ActionTermEnum.OPTEDIN,
        ActionTermEnum.OPTEDOUT,
    ] = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the  object. The value range is limited to the actions: OptedIn or OptedOut.",
    )
    object: SurveyModel | str = Field(
        alias="object",
        description="The Survey to which the actor is opting into or out of. The object value MUST be expressed either as an object or as a string corresponding to the resource's IRI.",
    )


class SurveyInvitationEventModel(EventModel):
    type: Literal[TypeTermEnum.SURVEYINVITATIONEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.SURVEYINVITATIONEVENT.value],
    )
    actor: PersonModel | str = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: Literal[
        ActionTermEnum.ACCEPTED,
        ActionTermEnum.DECLINED,
        ActionTermEnum.SENT,
    ] = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the actions: Accepted, Declined, or Sent.",
    )
    object: SurveyInvitationModel | str = Field(
        alias="object",
        description="The SurveyInvitation to which the actor is sending out or responding to. The object value MUST be expressed either as an object or as a string corresponding to the resource's IRI.",
    )


class ThreadEventModel(EventModel):
    type: Literal[TypeTermEnum.THREADEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.THREADEVENT.value],
    )
    actor: PersonModel | str = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: Literal[
        ActionTermEnum.MARKEDASREAD,
        ActionTermEnum.MARKEDASUNREAD,
    ] = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the MarkedAsRead and MarkedAsUnRead actions only.",
    )
    object: ThreadModel | str = Field(
        alias="object",
        description="The Thread that constitutes the object of the interaction. The  object value MUST be expressed either as an object or as a string corresponding to the object's IRI.",
    )


class ToolLaunchEventModel(EventModel):
    type: Literal[TypeTermEnum.TOOLLAUNCHEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.TOOLLAUNCHEVENT.value],
    )
    actor: PersonModel | str = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: Literal[
        ActionTermEnum.LAUNCHED,
        ActionTermEnum.RETURNED,
    ] = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to either the Launched or Returned actions.",
    )
    object: SoftwareApplicationModel | str = Field(
        alias="object",
        description="The SoftwareApplication that is the target of the actor's launch activity. The object value MUST be expressed either as an object or as a string corresponding to the software application's IRI.",
    )
    generated: DigitalResourceModel = Field(
        default=None,
        alias="generated",
        description="In the case that the workflow comes with a resource intended for the receiver of the workflow message associated with this event (for example, a file, or image, or LTI resource link for the receiver to embed within its system), this property can carry its representation as a Caliper DigitalResource or, more likely, one of its specific subtypes.",
    )
    target: LinkModel | LtiLinkModel = Field(
        default=None,
        alias="target",
        description="The fully qualified URL to which the workflow was redirected. In the case of the Launched action, this would be the fully qualified entry-point on the external tool to which the platform launches. In the case of the Returned action, this would be the fully qualified entry-point on the platform to which the tool is redirecting the workflow after user activity from the original launch finishes (this could be the launch_presentation_return_url in the case of a simple LTI Resource Link request; it could also be the deep_link_return_url in the case of a Deep Linking Response message).",
    )
    federated_session: LtiSessionModel | str = Field(
        alias="federatedSession",
        description="The Platform's session, constituting part of the tool launch context. The federatedSession value MUST be expressed either as an object or as a string corresponding to the federatedSession's IRI. Required when the action value is Launched, otherwise optional. Workflows that include a specific \"return message\" component (e.g. LTI Deep Linking response messages) SHOULD provide the federatedSession property and SHOULD populate its messageParameters property with the message parameters in the response message.",
    )

    @field_validator("federated_session")
    @staticmethod
    def federated_session_required_condition(federated_session, values):
        """Required when the action value is Launched, otherwise optional."""
        if (
            values.data.get("action", "") == ActionTermEnum.LAUNCHED
            and not federated_session
        ):
            raise ValueError(
                f"federated_session cannot be empty if action is {ActionTermEnum.LAUNCHED}",
            )
        return federated_session


class ToolUseEventModel(EventModel):
    type: Literal[TypeTermEnum.TOOLUSEEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.TOOLUSEEVENT.value],
    )
    actor: PersonModel | str = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: Literal[ActionTermEnum.USED,] = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the Used action only.",
    )
    object: SoftwareApplicationModel | str = Field(
        alias="object",
        description="The SoftwareApplication that constitutes the object of the interaction. The object value MUST be expressed either as an object or as a string corresponding to the object's IRI.",
    )
    target: SoftwareApplicationModel | str = Field(
        default=None,
        alias="target",
        description="A SoftwareApplication that represents a particular capability or feature provided by the object. The target value MUST be expressed either as an object or as a string corresponding to the target entity's IRI.",
    )
    generated: AggregateMeasureCollectionModel | str = Field(
        default=None,
        alias="generated",
        description="An AggregateMeasureCollection created or generated as a result of the interaction. The generated value MUST be expressed either as an object or as a string corresponding to the generated entity's IRI. Note that if the sender of the event wants to send aggregate measure information as part of this ToolUseEvent it should, by best practice, send a single AggregateMeasureCollection as the generated value.",
    )


class ViewEventModel(EventModel):
    type: Literal[TypeTermEnum.VIEWEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.VIEWEVENT.value],
    )
    actor: PersonModel | str = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: Literal[ActionTermEnum.VIEWED,] = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the actions: Viewed.",
    )
    object: DigitalResourceModel | str = Field(
        alias="object",
        description="The DigitalResource that the actor viewed. The object value MUST be expressed either as an object or as a string corresponding to the resource's IRI.",
    )


################################################
##################### MAIN #####################
################################################
class IMSCaliperModel(BaseModel):
    data: list[EntityModel | EventModel] = Field(alias="data")
    data_version: str = Field(
        alias="dataVersion",
        examples=["http://purl.imsglobal.org/ctx/caliper/v1p2"],
    )
    send_time: str = Field(alias="sendTime", examples=["2019-11-16T02:08:59.163Z"])
    sensor: str = Field(alias="sensor", examples=["http://oxana.instructure.com/"])

    @field_validator("data", mode="before")
    @classmethod
    def validation(
        cls,
        value: list[EventModel],
        extra_info: ValidationInfo,
    ) -> list[EventModel]:
        """Pydantic does not allow a model to use a discriminator and a field_validator with mode=`before`.

        This validator will act as a custom discriminator to apply the correct model to all
        the data values by using the `type` field present in all EventModel instances.

        Args:
            value (List[EventModel]): `data` field content
            extra_info (ValidationInfo): Field extra info

        Returns:
            List[EventModel]: List of data in the correct EventModel instance
        """
        # Get FieldInfo
        field = cls.model_fields.get(
            extra_info.field_name if extra_info.field_name else "",
            None,
        )

        if isinstance(field, FieldInfo):
            # Get child classes
            list_event_model = set()
            list_event_model.update(
                ExtendedTypeBaseModel._get_subclasses(field.annotation),
            )
            list_event_model = list(list_event_model)

            # Generate a dict to act as pydantic's discriminator (to know with model to apply)
            dict_discriminator = {}
            for event_model in list_event_model:
                key = event_model.model_fields.get("type")
                key = get_args(key.annotation) if key else None
                key = key[0] if key else None
                dict_discriminator[key] = event_model

            # Apply correct models
            if get_origin(field.annotation) is list and isinstance(value, list):
                new_value = []
                for each_value in value:
                    model_value = each_value
                    if isinstance(each_value, dict) and (
                        event_model := dict_discriminator.get(
                            each_value.get("type", ""),
                            None,
                        )
                    ):
                        model_value = event_model(**each_value)
                    new_value.append(model_value)
                return new_value

        return value
