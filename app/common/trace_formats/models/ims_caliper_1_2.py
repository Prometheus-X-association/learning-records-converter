from __future__ import annotations

from enum import StrEnum
from typing import List, Literal, Union, get_args

from base import ExtendedTypeBaseModel
from pydantic import BaseModel, Field, field_validator
from pydantic.fields import FieldInfo
from pydantic_core.core_schema import ValidationInfo
from typing_extensions import get_args, get_origin


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


class StatusTermEnum(StrEnum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"


class RoleTermEnum(StrEnum):
    ADMINISTRATOR = "Administrator"
    ADMINISTRATOR_ADMINISTRATOR = "Administrator#Administrator"
    ADMINISTRATOR_DEVELOPER = "Administrator#Developer"
    ADMINISTRATOR_EXTERNALDEVELOPER = "Administrator#ExternalDeveloper"
    ADMINISTRATOR_EXTERNALSUPPORT = "Administrator#ExternalSupport"
    ADMINISTRATOR_EXTERNALSYSTEMADMINISTRATOR = "Administrator#ExternalSystemAdministrator"
    ADMINISTRATOR_SUPPORT = "Administrator#Support"
    ADMINISTRATOR_SYSTEMADMINISTRATOR = "Administrator#SystemAdministrator"
    CONTENTDEVELOPER = "ContentDeveloper"
    CONTENTDEVELOPER_CONTENTDEVELOPER = "ContentDeveloper#ContentDeveloper"
    CONTENTDEVELOPER_CONTENTEXPERT = "ContentDeveloper#ContentExpert"
    CONTENTDEVELOPER_EXTERNALCONTENTEXPERT = "ContentDeveloper#ExternalContentExpert"
    CONTENTDEVELOPER_LIBRARIAN = "ContentDeveloper#Librarian"
    INSTRUCTOR = "Instructor"
    INSTRUCTOR_EXTERNALINSTRUCTOR = "Instructor#ExternalInstructor"
    INSTRUCTOR_GRADER = "Instructor#Grader"
    INSTRUCTOR_GUESTINSTRUCTOR = "Instructor#GuestInstructor"
    INSTRUCTOR_INSTRUCTOR = "Instructor#Instructor"
    INSTRUCTOR_LECTURER = "Instructor#Lecturer"
    INSTRUCTOR_PRIMARYINSTRUCTOR = "Instructor#PrimaryInstructor"
    INSTRUCTOR_SECONDARYINSTRUCTOR = "Instructor#SecondaryInstructor"
    INSTRUCTOR_TEACHINGASSISTANT = "Instructor#TeachingAssistant"
    INSTRUCTOR_TEACHINGASSISTANTGROUP = "Instructor#TeachingAssistantGroup"
    INSTRUCTOR_TEACHINGASSISTANTOFFERING = "Instructor#TeachingAssistantOffering"
    INSTRUCTOR_TEACHINGASSISTANTSECTION = "Instructor#TeachingAssistantSection"
    INSTRUCTOR_TEACHINGASSISTANTTEMPLATE = "Instructor#TeachingAssistantTemplate"
    LEARNER = "Learner"
    LEARNER_EXTERNALLEARNER = "Learner#ExternalLearner"
    LEARNER_GUESTLEARNER = "Learner#GuestLearner"
    LEARNER_LEARNER = "Learner#Learner"
    LEARNER_NONCREDITLEARNER = "Learner#NonCreditLearner"
    MANAGER = "Manager"
    MANAGER_AREAMANAGER = "Manager#AreaManager"
    MANAGER_COURSECOORDINATOR = "Manager#CourseCoordinator"
    MANAGER_EXTERNALOBSERVER = "Manager#ExternalObserver"
    MANAGER_MANAGER = "Manager#Manager"
    MANAGER_OBSERVER = "Manager#Observer"
    MEMBER = "Member"
    MEMBER_MEMBER = "Member#Member"
    MENTOR = "Mentor"
    MENTOR_ADVISOR = "Mentor#Advisor"
    MENTOR_EXTERNALADVISOR = "Mentor#ExternalAdvisor"
    MENTOR_EXTERNALAUDITOR = "Mentor#ExternalAuditor"
    MENTOR_EXTERNALLEARNINGFACILITATOR = "Mentor#ExternalLearningFacilitator"
    MENTOR_EXTERNALMENTOR = "Mentor#ExternalMentor"
    MENTOR_EXTERNALREVIEWER = "Mentor#ExternalReviewer"
    MENTOR_EXTERNALTUTOR = "Mentor#ExternalTutor"
    MENTOR_LEARNINGFACILITATOR = "Mentor#LearningFacilitator"
    MENTOR_MENTOR = "Mentor#Mentor"
    MENTOR_REVIEWER = "Mentor#Reviewer"
    MENTOR_TUTOR = "Mentor#Tutor"
    OFFICER = "Officer"
    OFFICER_CHAIR = "Officer#Chair"
    OFFICER_SECRETARY = "Officer#Secretary"
    OFFICER_TREASURER = "Officer#Treasurer"
    OFFICER_VICECHAIR = "Officer#Vice-Chair"


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
    GENERALPROFILE = "GeneralProfile"
    ANNOTATIONPROFILE = "AnnotationProfile"
    ASSESSMENTPROFILE = "AssessmentProfile"
    ASSIGNABLEPROFILE = "AssignableProfile"
    FEEDBACKPROFILE = "FeedbackProfile"
    FORUMPROFILE = "ForumProfile"
    GRADINGPROFILE = "GradingProfile"
    MEDIAPROFILE = "MediaProfile"
    READINGPROFILE = "ReadingProfile"
    RESOURCEMANAGEMENTPROFILE = "ResourceManagementProfile"
    SEARCHPROFILE = "SearchProfile"
    SESSIONPROFILE = "SessionProfile"
    TOOLLAUNCHPROFILE = "ToolLaunchProfile"
    TOOLUSEPROFILE = "ToolUseProfile"


class TypeTermEnum(StrEnum):
    EVENT = "Event"
    ANNOTATIONEVENT = "AnnotationEvent"
    ASSESSMENTEVENT = "AssessmentEvent"
    ASSESSMENTITEMEVENT = "AssessmentItemEvent"
    ASSIGNABLEEVENT = "AssignableEvent"
    FEEDBACKEVENT = "FeedbackEvent"
    FORUMEVENT = "ForumEvent"
    GRADEEVENT = "GradeEvent"
    MEDIAEVENT = "MediaEvent"
    MESSAGEEVENT = "MessageEvent"
    NAVIGATIONEVENT = "NavigationEvent"
    QUESTIONNAIREEVENT = "QuestionnaireEvent"
    QUESTIONNAIREITEMEVENT = "QuestionnaireItemEvent"
    RESOURCEMANAGEMENTEVENT = "ResourceManagementEvent"
    SEARCHEVENT = "SearchEvent"
    SESSIONEVENT = "SessionEvent"
    SURVEYEVENT = "SurveyEvent"
    SURVEYINVITATIONEVENT = "SurveyInvitationEvent"
    THREADEVENT = "ThreadEvent"
    TOOLLAUNCHEVENT = "ToolLaunchEvent"
    TOOLUSEEVENT = "ToolUseEvent"
    VIEWEVENT = "ViewEvent"
    ENTITY = "Entity"
    AGENT = "Agent"
    AGGREGATEMEASURE = "AggregateMeasure"
    AGGREGATEMEASURECOLLECTION = "AggregateMeasureCollection"
    ANNOTATION = "Annotation"
    ASSESSMENT = "Assessment"
    ASSESSMENTITEM = "AssessmentItem"
    ASSIGNABLEDIGITALRESOURCE = "AssignableDigitalResource"
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
    FILLINBLANKRESPONSE = "FillinBlankResponse"
    FORUM = "Forum"
    FRAME = "Frame"
    GROUP = "Group"
    HIGHLIGHTANNOTATION = "HighlightAnnotation"
    IMAGEOBJECT = "ImageObject"
    LEARNINGOBJECTIVE = "LearningObjective"
    LIKERTSCALE = "LikertScale"
    LINK = "Link"
    LTILINK = "LtiLink"
    LTISESSION = "LtiSession"
    MEDIALOCATION = "MediaLocation"
    MEDIAOBJECT = "MediaObject"
    MEMBERSHIP = "Membership"
    MESSAGE = "Message"
    MULTIPLECHOICERESPONSE = "MultipleChoiceResponse"
    MULTIPLERESPONSERESPONSE = "MultipleResponseResponse"
    MULTISELECTQUESTION = "MultiselectQuestion"
    MULTISELECTRESPONSE = "MultiselectResponse"
    MULTISELECTSCALE = "MultiselectScale"
    NUMERICSCALE = "NumericScale"
    OPENENDEDQUESTION = "OpenEndedQuestion"
    OPENENDEDRESPONSE = "OpenEndedResponse"
    ORGANIZATION = "Organization"
    PAGE = "Page"
    PERSON = "Person"
    QUERY = "Query"
    QUESTION = "Question"
    QUESTIONNAIRE = "Questionnaire"
    QUESTIONNAIREITEM = "QuestionnaireItem"
    RATING = "Rating"
    RATINGSCALEQUESTION = "RatingScaleQuestion"
    RATINGSCALERESPONSE = "RatingScaleResponse"
    RESPONSE = "Response"
    RESULT = "Result"
    SCALE = "Scale"
    SCORE = "Score"
    SEARCHRESPONSE = "SearchResponse"
    SELECTTEXTRESPONSE = "SelectTextResponse"
    SESSION = "Session"
    SHAREDANNOTATION = "SharedAnnotation"
    SOFTWAREAPPLICATION = "SoftwareApplication"
    SURVEY = "Survey"
    SURVEYINVITATION = "SurveyInvitation"
    TAGANNOTATION = "TagAnnotation"
    THREAD = "Thread"
    TRUEFALSERESPONSE = "TrueFalseResponse"
    VIDEOOBJECT = "VideoObject"
    WEBPAGE = "WebPage"
    TEXTPOSITIONSELECTOR = "TextPositionSelector"
    SYSTEMIDENTIFIER = "SystemIdentifier"


##############################################################
##################### INFORMATION MODELS #####################
##############################################################
class TextPositionSelectorModel(ExtendedTypeBaseModel):
    type: Literal[TypeTermEnum.TEXTPOSITIONSELECTOR] = Field(
        alias="type", examples=["TextPositionSelector"]
    )
    start: int = Field(
        alias="start",
        description="The starting position of the selected text MUST be specified. The first character in the full text is character position 0.",
    )
    end: int = Field(
        alias="end", description="The end position of the selected text MUST be specified."
    )


class SystemIdentifierModel(ExtendedTypeBaseModel):
    type: Literal[TypeTermEnum.SYSTEMIDENTIFIER] = Field(
        alias="type", examples=["SystemIdentifier"]
    )
    identifier_type: SystemIdentifierTypeEnum = Field(alias="identifierType")
    identifier: str = Field(alias="identifier")
    source: Union[SoftwareApplicationModel, str] = Field(default=None, alias="source")
    extensions: dict = Field(default=None, alias="extensions")


####################################################
##################### ENTITIES #####################
####################################################
class EntityModel(ExtendedTypeBaseModel):
    context: str = Field(
        default="http://purl.imsglobal.org/ctx/caliper/v1p2",
        alias="@context",
        examples=["http://purl.imsglobal.org/ctx/caliper/v1p2"],
    )
    id: str = Field(alias="id", examples=["urn:instructure:canvas:user:21070000000000001"])
    type: Literal[TypeTermEnum.ENTITY] = Field(alias="type", examples=["Person"])
    name: str = Field(default=None, alias="name")
    description: str = Field(default=None, alias="description")
    date_created: str = Field(default=None, alias="dateCreated")  # Datetime
    date_modified: str = Field(default=None, alias="dateModified")  # Datetime
    other_identifiers: List[Union[SystemIdentifierModel, str]] = Field(
        default=None, alias="otherIdentifiers"
    )
    extensions: dict = Field(default=None, alias="extensions")


class AgentModel(EntityModel):
    type: Literal[TypeTermEnum.AGENT] = Field(alias="type", examples=["Agent"])


class PersonModel(AgentModel):
    type: Literal[TypeTermEnum.PERSON] = Field(alias="type", examples=["Person"])


class SoftwareApplicationModel(AgentModel):
    type: Literal[TypeTermEnum.SOFTWAREAPPLICATION] = Field(
        alias="type", examples=["SoftwareApplication"]
    )
    host: str = Field(default=None, alias="host")
    ip_address: str = Field(default=None, alias="ipAddress")
    user_agent: str = Field(default=None, alias="userAgent")
    version: str = Field(default=None, alias="version")


class LearningObjectiveModel(EntityModel):
    type: Literal[TypeTermEnum.LEARNINGOBJECTIVE] = Field(
        alias="type", examples=["LearningObjective"]
    )


class AggregateMeasureModel(EntityModel):
    type: Literal[TypeTermEnum.AGGREGATEMEASURE] = Field(
        alias="type", examples=["AggregateMeasure"]
    )
    metric_value: float = Field(alias="metricValue")
    max_metric_value: float = Field(default=None, alias="maxMetricValue")
    metric: MetricEnum = Field(alias="metric")
    started_at_time: str = Field(default=None, alias="startedAtTime")  # Datetime
    ended_at_time: str = Field(default=None, alias="endedAtTime")  # Datetime


class OrganizationModel(AgentModel):
    type: Literal[TypeTermEnum.ORGANIZATION] = Field(alias="type", examples=["Organization"])
    sub_organization_of: Union[OrganizationModel, str] = Field(
        default=None, alias="subOrganizationOf"
    )
    members: List[Union[AgentModel, str]] = Field(default=None, alias="members")


class DigitalResourceModel(EntityModel):
    type: Literal[TypeTermEnum.DIGITALRESOURCE] = Field(alias="type", examples=["DigitalResource"])
    storage_name: str = Field(
        default=None,
        alias="storageName",
        description="The name of resource when stored in a file system.",
    )
    creators: List[Union[AgentModel, str]] = Field(
        default=None,
        alias="creators",
        description="An ordered collection of Agent entities, typically of type Person, that are responsible for bringing resource into being. Each array item MUST be expressed either as an object or as a string corresponding to the item's IRI.",
    )
    media_type: str = Field(
        default=None,
        alias="mediaType",
        description="A string value drawn from the list of IANA approved media types and subtypes that identifies the file format of the resource.",
    )
    keywords: List[str] = Field(
        default=None,
        alias="keywords",
        description="An ordered collection of one or more string values that represent tags or labels used to identify the resource.",
    )
    learning_objectives: List[Union[LearningObjectiveModel, str]] = Field(
        default=None,
        alias="learningObjectives",
        description="An ordered collection of one or more LearningObjective entities that describe what a learner is expected to comprehend or accomplish after engaging with the resource. Each array item MUST be expressed either as an object or as a string corresponding to the item's IRI.",
    )
    is_part_of: Union[EntityModel, str] = Field(
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
    type: Literal[TypeTermEnum.QUESTION] = Field(alias="type", examples=["Question"])
    question_posed: str = Field(
        default=None,
        alias="questionPosed",
        description="A string value comprising the question posed.",
    )


class AnnotationModel(EntityModel):
    type: Literal[TypeTermEnum.ANNOTATION] = Field(alias="type", examples=["Annotation"])
    annotator: Union[PersonModel, str] = Field(
        default=None,
        alias="annotator",
        description="The Person who created the Annotation. The annotator value MUST be expressed either as an object or as a string corresponding to the annotator's IRI.",
    )
    annotated: Union[DigitalResourceModel, str] = Field(
        default=None,
        alias="annotated",
        description="The DigitalResource that was annotated by the annotator. The annotated value MUST be expressed either as an object or as a string corresponding to the annotated resource's IRI.",
    )


class AttemptModel(EntityModel):
    type: Literal[TypeTermEnum.ATTEMPT] = Field(alias="type", examples=["Attempt"])
    assignee: Union[PersonModel, str] = Field(
        default=None,
        alias="assignee",
        description="The Person who initiated the Attempt. The assignee value MUST be expressed either as an object or as a string corresponding to the assignee's IRI.",
    )
    assignable: Union[DigitalResourceModel, str] = Field(
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
    type: Literal[TypeTermEnum.COLLECTION] = Field(alias="type", examples=["Collection"])
    items: List[Union[EntityModel, str]] = Field(
        default=None,
        alias="items",
        description="An ordered collection of entities. Each array item MUST be expressed either as an object or as a string corresponding to the resource's IRI.",
    )


class CommentModel(EntityModel):
    type: Literal[TypeTermEnum.COMMENT] = Field(alias="type", examples=["Comment"])
    commenter: Union[PersonModel, str] = Field(
        default=None,
        alias="commenter",
        description="The Person who provided the comment. The commenter value MUST be expressed either as an object or as a string corresponding to the commenter’s IRI.",
    )
    commented_on: Union[EntityModel, str] = Field(
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
    type: Literal[TypeTermEnum.LINK] = Field(alias="type", examples=["Link"])


class MembershipModel(EntityModel):
    type: Literal[TypeTermEnum.MEMBERSHIP] = Field(alias="type", examples=["Membership"])
    organization: Union[OrganizationModel, str] = Field(default=None, alias="organization")
    member: Union[PersonModel, str] = Field(default=None, alias="member")
    roles: List[RoleTermEnum] = Field(default=None, alias="roles", examples=[["Learner"]])
    status: StatusTermEnum = Field(default=None, alias="status")


class QueryModel(EntityModel):
    type: Literal[TypeTermEnum.QUERY] = Field(alias="type", examples=["Query"])
    creator: Union[PersonModel, str] = Field(
        default=None,
        alias="creator",
        description="The Person who devised the search terms comprising this Query. The creator value MUST be expressed either as an object or as a string corresponding to the creator's IRI.",
    )
    search_target: Union[EntityModel, str] = Field(
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
    type: Literal[TypeTermEnum.RATING] = Field(alias="type", examples=["Rating"])
    rater: Union[PersonModel, str] = Field(
        default=None,
        alias="rater",
        description="The Person who provided the Rating. The rater value MUST be expressed either as an object or as a string corresponding to the rater’s IRI.",
    )
    rated: Union[EntityModel, str] = Field(
        default=None,
        alias="rated",
        description="The Entity which received the rating. The rated value MUST be expressed either as an object or as a string corresponding to the rated object's IRI.",
    )
    question: Union[QuestionModel, str] = Field(
        default=None,
        alias="question",
        description="The Question used for the Rating. The question value MUST be expressed either as an object or as a string corresponding to the question's IRI.",
    )
    selections: List[str] = Field(
        default=None,
        alias="selections",
        description="An array of the values representing the rater's selected response.",
    )
    rating_comment: Union[CommentModel, str] = Field(
        default=None,
        alias="ratingComment",
        description="The Comment left with the Rating. The ratingComment value MUST be expressed either as an object or as a string corresponding to the comment’s IRI.",
    )


class ResponseModel(EntityModel):
    type: Literal[TypeTermEnum.RESPONSE] = Field(alias="type", examples=["Response"])
    attempt: Union[AttemptModel, str] = Field(
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
    type: Literal[TypeTermEnum.SESSION] = Field(alias="type", examples=["Session"])
    user: PersonModel = Field(default=None, alias="user")
    client: SoftwareApplicationModel = Field(default=None, alias="client")
    started_at_time: str = Field(default=None, alias="startedAtTime")  # Datetime
    ended_at_time: str = Field(default=None, alias="endedAtTime")  # Datetime
    duration: str = Field(default=None, alias="duration")  # Duration ISO 8601


class ResultModel(EntityModel):
    type: Literal[TypeTermEnum.RESULT] = Field(alias="type", examples=["Result"])
    attempt: Union[AttemptModel, str] = Field(
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
    scored_by: Union[AgentModel, str] = Field(
        default=None,
        alias="scoredBy",
        description="The Agent who scored or graded the Attempt. The  scoredBy value MUST be expressed either as an object or as a string corresponding to the scorer's IRI.",
    )
    comment: str = Field(
        default=None, alias="comment", description="Plain text feedback provided by the scorer."
    )


class ScaleModel(EntityModel):
    type: Literal[TypeTermEnum.SCALE] = Field(alias="type", examples=["Scale"])


class ScoreModel(EntityModel):
    type: Literal[TypeTermEnum.SCORE] = Field(alias="type", examples=["Score"])
    attempt: Union[AttemptModel, str] = Field(
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
    scored_by: Union[AgentModel, str] = Field(
        default=None,
        alias="scoredBy",
        description="The Agent who scored or graded the Attempt. The  scoredBy value MUST be expressed either as an object or as a string corresponding to the scorer's IRI.",
    )
    comment: str = Field(
        default=None, alias="comment", description="Plain text feedback provided by the scorer."
    )


class SearchResponseModel(EntityModel):
    type: Literal[TypeTermEnum.SEARCHRESPONSE] = Field(alias="type", examples=["SearchResponse"])
    search_provider: Union[SoftwareApplicationModel, str] = Field(
        default=None,
        alias="searchProvider",
        description="The SoftwareApplication that is the provider of this  SearchResponse. The searchProvider value MUST be expressed either as an object or as a string corresponding to the resources's IRI.",
    )
    search_target: Union[EntityModel, str] = Field(
        default=None,
        alias="searchTarget",
        description="The Entity, typically a DigitalResource or  SoftwareApplication, that is the target of the search. The resourceSearched value MUST be expressed either as an object or as a string corresponding to the resources's IRI.",
    )
    query: Union[QueryModel, str] = Field(
        default=None, alias="query", description="The Query submitted by the actor."
    )
    search_results_item_count: int = Field(
        default=None,
        alias="searchResultsItemCount",
        description="A total count of searchResults returned. If the Query submitted returned no results the count equal to zero (0).",
    )


class PageModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.PAGE] = Field(alias="type", examples=["Page"])


class LtiSessionModel(SessionModel):
    type: Literal[TypeTermEnum.LTISESSION] = Field(alias="type", examples=["LtiSession"])
    message_parameters: dict = Field(
        default=None,
        alias="messageParameters",
        description="A map of LTI-specified message parameters that provide platform-related contextual information",
    )


class AssignableDigitalResourceModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.ASSIGNABLEDIGITALRESOURCE] = Field(
        alias="type", examples=["AssignableDigitalResource"]
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
    type: Literal[TypeTermEnum.ASSESSMENTITEM] = Field(alias="type", examples=["AssessmentItem"])
    is_time_dependent: bool = Field(
        default=None,
        alias="isTimeDependent",
        description="A boolean value indicating whether or not interacting with the item is time dependent.",
    )


class DigitalResourceCollectionModel(CollectionModel, DigitalResourceModel):
    type: Literal[TypeTermEnum.DIGITALRESOURCECOLLECTION] = Field(
        alias="type", examples=["DigitalResourceCollection"]
    )
    items: List[Union[DigitalResourceModel, str]] = Field(
        default=None,
        alias="items",
        description="An ordered collection of DigitalResource entities. Each array item MUST be expressed either as an object or as a string corresponding to the item's IRI.",
    )


class AggregateMeasureCollectionModel(CollectionModel):
    type: Literal[TypeTermEnum.AGGREGATEMEASURECOLLECTION] = Field(
        alias="type", examples=["AggregateMeasureCollection"]
    )
    items: List[Union[AggregateMeasureModel, str]] = Field(
        default=None,
        alias="items",
        description="An ordered collection of AggregateMeasure entities. Each array item MUST be expressed either as an object or as a string corresponding to the item’s IRI.",
    )


class AssessmentModel(AssignableDigitalResourceModel, DigitalResourceCollectionModel):
    type: Literal[TypeTermEnum.ASSESSMENT] = Field(alias="type", examples=["Assessment"])
    items: List[Union[AssessmentItemModel, str]] = Field(
        default=None,
        alias="items",
        description="An ordered collection of AssessmentItem entities. Each array item MUST be expressed either as an object or as a string corresponding to the item's IRI.",
    )


class MediaObjectModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.MEDIAOBJECT] = Field(alias="type", examples=["MediaObject"])
    duration: str = Field(
        default=None,
        alias="duration",
        description="An optional time interval that represents the total time required to view and/or listen to the  MediaObject at normal speed. If a duration is specified the value MUST conform to the ISO 8601 duration format.",
    )  # Duration


class AudioObjectModel(MediaObjectModel):
    type: Literal[TypeTermEnum.AUDIOOBJECT] = Field(alias="type", examples=["AudioObject"])
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
        alias="type", examples=["BookmarkAnnotation"]
    )
    bookmark_notes: str = Field(
        default=None,
        alias="bookmarkNotes",
        description="A string value comprising a plain text rendering of the note that accompanies the bookmark.",
    )


class ChapterModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.CHAPTER] = Field(alias="type", examples=["Chapter"])


class CourseOfferingModel(OrganizationModel):
    type: Literal[TypeTermEnum.COURSEOFFERING] = Field(alias="type", examples=["CourseOffering"])
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
    type: Literal[TypeTermEnum.COURSESECTION] = Field(alias="type", examples=["CourseSection"])
    category: str = Field(
        default=None,
        alias="category",
        description="A string value that characterizes the purpose of the section such as lecture, lab or seminar.",
    )


class DateTimeQuestionModel(QuestionModel):
    type: Literal[TypeTermEnum.DATETIMEQUESTION] = Field(
        alias="type", examples=["DateTimeQuestion"]
    )
    min_date_time: str = Field(
        default=None,
        alias="minDateTime",
        description="A DateTime value used to determine the minimum value allowed.",
    )  # DateTime
    min_label: str = Field(
        default=None, alias="minLabel", description="The label for the minimum DateTime."
    )
    max_date_time: str = Field(
        default=None,
        alias="maxDateTime",
        description="A DateTime value used to determine the maximum value allowed.",
    )  # DateTime
    max_label: str = Field(
        default=None, alias="maxLabel", description="The label for the maximum value."
    )


class DateTimeResponseModel(ResponseModel):
    type: Literal[TypeTermEnum.DATETIMERESPONSE] = Field(
        alias="type", examples=["DateTimeResponse"]
    )
    date_time_selected: str = Field(
        default=None,
        alias="dateTimeSelected",
        description="The DateTime selected in response to the question.",
    )  # DateTime


class DocumentModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.DOCUMENT] = Field(alias="type", examples=["Document"])


class FillinBlankResponseModel(ResponseModel):
    type: Literal[TypeTermEnum.FILLINBLANKRESPONSE] = Field(
        alias="type", examples=["FillinBlankResponse"]
    )
    values: List[str] = Field(
        default=None,
        alias="values",
        description="An ordered collection of one or more string values representing words, expressions or short phrases that constitute the 'fill in the blank' response.",
    )


class MessageModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.MESSAGE] = Field(alias="type", examples=["Message"])
    reply_to: Union[MessageModel, str] = Field(
        default=None,
        alias="replyTo",
        description="A Message that represents the post to which this Message is directed in reply. The replyTo value MUST be expressed either as an object or as a string corresponding to the associated message's IRI.",
    )
    body: str = Field(
        default=None,
        alias="body",
        description="A string value comprising a plain-text rendering of the body content of the  Message.",
    )
    attachments: List[Union[DigitalResourceModel, str]] = Field(
        default=None,
        alias="attachments",
        description="An ordered collection of one or more DigitalResource entities attached to this Message. Each array item MUST be expressed either as an object or as a string corresponding to the item's IRI.",
    )


class ThreadModel(DigitalResourceCollectionModel):
    type: Literal[TypeTermEnum.THREAD] = Field(alias="type", examples=["Thread"])
    items: List[Union[MessageModel, str]] = Field(
        default=None,
        alias="items",
        description="An ordered collection of Message entities. Each array item MUST be expressed either as an object or as a string corresponding to the item's IRI.",
    )


class ForumModel(DigitalResourceCollectionModel):
    type: Literal[TypeTermEnum.FORUM] = Field(alias="type", examples=["Forum"])
    items: List[Union[ThreadModel, str]] = Field(
        default=None,
        alias="items",
        description="An ordered collection of Thread entities. Each array item MUST be expressed either as an object or as a string corresponding to the item's IRI.",
    )


class FrameModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.FRAME] = Field(alias="type", examples=["Frame"])
    index: int = Field(
        default=None,
        alias="index",
        description="A non-negative integer that represents the position of the Frame.",
    )


class GroupModel(OrganizationModel):
    type: Literal[TypeTermEnum.GROUP] = Field(alias="type", examples=["Group"])


class HighlightAnnotationModel(AnnotationModel):
    type: Literal[TypeTermEnum.HIGHLIGHTANNOTATION] = Field(
        alias="type", examples=["HighlightAnnotation"]
    )
    selection_text: str = Field(
        default=None,
        alias="selectionText",
        description="A string value representing a plain-text rendering of the highlighted segment of the annotated DigitalResource.",
    )


class ImageObjectModel(MediaObjectModel):
    type: Literal[TypeTermEnum.IMAGEOBJECT] = Field(alias="type", examples=["ImageObject"])


class LikertScaleModel(ScaleModel):
    type: Literal[TypeTermEnum.LIKERTSCALE] = Field(alias="type", examples=["LikertScale"])
    scale_points: int = Field(
        default=None,
        alias="scalePoints",
        description="A integer value used to determine the amount of points on the LikertScale.",
    )
    item_labels: List[str] = Field(
        default=None,
        alias="itemLabels",
        description="The ordered list of labels for each point on the scale. The values MUST be cast as strings.",
    )
    item_values: List[str] = Field(
        default=None,
        alias="itemValues",
        description="The ordered list of values for each point on the scale. The values MUST be cast as strings.",
    )


class LtiLinkModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.LTILINK] = Field(alias="type", examples=["LtiLink"])
    message_type: LtiMessageTypesEnum = Field(
        default=None,
        alias="messageType",
        description="If present, the string value MUST be set to the term name of the LTI message type used to gain access to this LTI resource link (including but not limited to, LtiResourceLinkRequest or LtiDeepLinkingRequest, LtiDeepLinkingResponse).",
    )


class MediaLocationModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.MEDIALOCATION] = Field(
        alias="type", examples=["AgMediaLocationent"]
    )
    current_time: str = Field(
        default=None,
        alias="currentTime",
        description="A time interval or duration that represents the current playback position measured from the beginning of an AudioObject or VideoObject. If a  currentTime is specified the value MUST conform to the ISO 8601 duration format.",
    )  # Duration


class MultipleChoiceResponseModel(ResponseModel):
    type: Literal[TypeTermEnum.MULTIPLECHOICERESPONSE] = Field(
        alias="type", examples=["MultipleChoiceResponse"]
    )
    value: str = Field(
        default=None,
        alias="value",
        description="A string value that represents the selected option.",
    )


class MultipleResponseResponseModel(ResponseModel):
    type: Literal[TypeTermEnum.MULTIPLERESPONSERESPONSE] = Field(
        alias="type", examples=["MultipleResponseResponse"]
    )
    values: List[str] = Field(
        default=None,
        alias="values",
        description="An ordered collection of one or more selected options MAY be specified",
    )


class MultiselectQuestionModel(QuestionModel):
    type: Literal[TypeTermEnum.MULTISELECTQUESTION] = Field(
        alias="type", examples=["MultiselectQuestion"]
    )
    points: int = Field(
        default=None,
        alias="points",
        description="A integer value used to determine the amount of points on the MultiselectQuestion.",
    )
    item_labels: List[str] = Field(
        default=None,
        alias="itemLabels",
        description="The list of labels that describe the set of selectable question options. Each label MUST be cast as a string.",
    )
    item_values: List[str] = Field(
        default=None,
        alias="itemValues",
        description="The list of values associated with the set of selectable question options. Each value MUST be cast as a string.",
    )


class MultiselectResponseModel(ResponseModel):
    type: Literal[TypeTermEnum.MULTISELECTRESPONSE] = Field(
        alias="type", examples=["MultiselectResponse"]
    )
    selections: List[str] = Field(
        default=None,
        alias="selections",
        description="An array of the values representing the rater's selected responses.",
    )


class MultiselectScaleModel(ScaleModel):
    type: Literal[TypeTermEnum.MULTISELECTSCALE] = Field(
        alias="type", examples=["MultiselectScale"]
    )
    scale_points: int = Field(
        default=None,
        alias="scalePoints",
        description="A integer value used to determine the amount of points on the MultiselectScale.",
    )
    item_labels: List[str] = Field(
        default=None,
        alias="itemLabels",
        description="The ordered list of labels for each point on the scale. The values MUST be cast as strings.",
    )
    item_values: List[str] = Field(
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
    type: Literal[TypeTermEnum.NUMERICSCALE] = Field(alias="type", examples=["NumericScale"])
    min_value: float = Field(
        default=None,
        alias="minValue",
        description="A decimal value used to determine the minimum value of the NumericScale.",
    )
    min_label: str = Field(
        default=None, alias="minLabel", description="The label for the minimum value."
    )
    max_value: float = Field(
        default=None,
        alias="maxValue",
        description="A decimal value used to determine the maximum value of the NumericScale.",
    )
    max_label: str = Field(
        default=None, alias="maxLabel", description="The label for the maximum value."
    )
    step: float = Field(
        default=None,
        alias="step",
        description="Indicates the decimal step used for determining the options between the minimum and maximum values.",
    )


class OpenEndedQuestionModel(QuestionModel):
    type: Literal[TypeTermEnum.OPENENDEDQUESTION] = Field(
        alias="type", examples=["OpenEndedQuestion"]
    )


class OpenEndedResponseModel(ResponseModel):
    type: Literal[TypeTermEnum.OPENENDEDRESPONSE] = Field(
        alias="type", examples=["OpenEndedResponse"]
    )
    value: str = Field(
        default=None, alias="value", description="the textual value of the response."
    )


class QuestionnaireItemModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.QUESTIONNAIREITEM] = Field(
        alias="type", examples=["QuestionnaireItem"]
    )
    question: Union[QuestionModel, str] = Field(
        default=None,
        alias="question",
        description="The Question entity posed by the QuestionnaireItem. The Question value MUST be expressed either as an object or as a string corresponding to the question's IRI.",
    )
    categories: List[str] = Field(
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
    type: Literal[TypeTermEnum.QUESTIONNAIRE] = Field(alias="type", examples=["Questionnaire"])
    items: List[Union[QuestionnaireItemModel, str]] = Field(
        alias="items",
        description="An array of one or more QuestionnaireItem entities that together comprise the Questionnaire. The object value MUST be expressed either as an object or as a string corresponding to the resource's IRI.",
    )


class RatingScaleQuestionModel(QuestionModel):
    type: Literal[TypeTermEnum.RATINGSCALEQUESTION] = Field(
        alias="type", examples=["RatingScaleQuestion"]
    )
    scale: Union[ScaleModel, str] = Field(
        default=None,
        alias="scale",
        description="The Scale used in the question. The scale value MUST be expressed either as an object or as a string corresponding to the scale's IRI.",
    )


class RatingScaleResponseModel(ResponseModel):
    type: Literal[TypeTermEnum.RATINGSCALERESPONSE] = Field(
        alias="type", examples=["RatingScaleResponse"]
    )
    selections: List[str] = Field(
        default=None,
        alias="selections",
        description="An array of the values representing the rater's selected responses.",
    )


class SelectTextResponseModel(ResponseModel):
    type: Literal[TypeTermEnum.SELECTTEXTRESPONSE] = Field(
        alias="type", examples=["SelectTextResponse"]
    )
    values: List[str] = Field(
        default=None,
        alias="values",
        description="An ordered collection of one or more selected options.",
    )


class SharedAnnotationModel(AnnotationModel):
    type: Literal[TypeTermEnum.SHAREDANNOTATION] = Field(
        alias="type", examples=["SharedAnnotation"]
    )
    with_agents: List[Union[AgentModel, PersonModel, str]] = Field(
        default=None,
        alias="withAgents",
        description="An ordered collection of one or more Agent entities, typically of type Person, with whom the annotated DigitalResource has been shared. Each array item MUST be expressed either as an object or as a string corresponding to the item's IRI.",
    )


class SurveyModel(CollectionModel):
    type: Literal[TypeTermEnum.SURVEY] = Field(alias="type", examples=["Survey"])
    items: List[Union[QuestionnaireModel, str]] = Field(
        default=None,
        alias="items",
        description="An array of one or more Questionnaire entities that together comprise the Survey. Each array item MUST be expressed either as an object or as a string corresponding to the Questionnaire resource's IRI.",
    )


class SurveyInvitationModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.SURVEYINVITATION] = Field(
        alias="type", examples=["SurveyInvitation"]
    )
    rater: Union[PersonModel, str] = Field(
        default=None,
        alias="rater",
        description="The Person which will rate the Survey. The rater value MUST be expressed either as an object or as a string corresponding to the rater resource’s IRI.",
    )
    survey: Union[SurveyModel, str] = Field(
        default=None,
        alias="survey",
        description="The Survey that the invitation is for. The survey value MUST be expressed either as an object or as a string corresponding to the rater resource’s IRI.",
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
    type: Literal[TypeTermEnum.TAGANNOTATION] = Field(alias="type", examples=["TagAnnotation"])
    tags: List[str] = Field(
        default=None,
        alias="tags",
        description="An ordered collection of one or more string values that represent the tags associated with the annotated DigitalResource.",
    )


class TrueFalseResponseModel(ResponseModel):
    type: Literal[TypeTermEnum.TRUEFALSERESPONSE] = Field(
        alias="type", examples=["TrueFalseResponse"]
    )
    value: str = Field(
        default=None,
        alias="value",
        description="A string value that provides the true/false, yes/no binary selection SHOULD be provided.",
    )


class VideoObjectModel(MediaObjectModel):
    type: Literal[TypeTermEnum.VIDEOOBJECT] = Field(alias="type", examples=["VideoObject"])


class WebPageModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.WEBPAGE] = Field(alias="type", examples=["WebPage"])


##################################################
##################### EVENTS #####################
##################################################
class EventModel(ExtendedTypeBaseModel):
    context: str = Field(
        default="http://purl.imsglobal.org/ctx/caliper/v1p2",
        alias="@context",
        examples=["http://purl.imsglobal.org/ctx/caliper/v1p2"],
    )
    id: str = Field(alias="id", examples=["urn:uuid:cf6e0f3b-3511-4254-86c5-6936ff33f267"])
    type: Literal[TypeTermEnum.EVENT] = Field(alias="type", examples=["NavigationEvent"])
    profile: ProfileTermEnum = Field(default=None, alias="profile", examples=["GeneralProfile"])
    actor: Union[AgentModel, str] = Field(alias="actor")
    action: ActionTermEnum = Field(alias="action", examples=["NavigatedTo"])
    object: Union[EntityModel, str] = Field(alias="object")
    event_time: str = Field(alias="eventTime", examples=["2019-11-01T00:09:06.878Z"])  # Datetime

    ed_app: Union[SoftwareApplicationModel, str] = Field(default=None, alias="edApp")
    generated: Union[EntityModel, str] = Field(default=None, alias="generated")
    target: Union[EntityModel, str] = Field(default=None, alias="target")
    referrer: Union[EntityModel, str] = Field(
        default=None,
        alias="referrer",
        examples=[
            "https://oxana.instructure.com/courses/565/discussion_topics/1072925?module_item_id=4635201"
        ],
    )
    group: Union[OrganizationModel, CourseSectionModel, str] = Field(default=None, alias="group")
    membership: Union[MembershipModel, str] = Field(default=None, alias="membership")

    session: Union[SessionModel, str] = Field(default=None, alias="session")
    federated_session: Union[LtiSessionModel, str] = Field(default=None, alias="federatedSession")
    extensions: dict = Field(default=None, alias="extensions")


class AnnotationEventModel(EventModel):
    type: Literal[TypeTermEnum.ANNOTATIONEVENT] = Field(alias="type", examples=["AnnotationEvent"])
    actor: Union[PersonModel, str] = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: ActionTermEnum = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the Bookmarked, Highlighted, Shared, and Tagged actions only.",
    )
    object: Union[DigitalResourceModel, str] = Field(
        alias="object",
        description="The annotated DigitalResource that constitutes the object of the interaction. The object value MUST be expressed either as an object or as a string corresponding to the object's IRI.",
    )
    target: Union[FrameModel, str] = Field(
        default=None,
        alias="target",
        description="A Frame that represents a particular segment or location within the object. The target value MUST be expressed either as an object or as a string corresponding to the target entity's IRI.",
    )
    generated: Union[AnnotationModel, str] = Field(
        default=None,
        alias="generated",
        description="The generated Annotation or a subtype. The generated value MUST be expressed either as an object or as a string corresponding to the generated entity's IRI.",
    )

    @field_validator("action")
    def action_limited_values(cls, action):
        """ """
        list_accepted_values = [
            ActionTermEnum.BOOKMARKED,
            ActionTermEnum.HIGHLIGHTED,
            ActionTermEnum.SHARED,
            ActionTermEnum.TAGGED,
        ]
        if action not in list_accepted_values:
            raise ValueError(f"action has to be in this list: {list_accepted_values}")


class AssessmentEventModel(EventModel):
    type: Literal[TypeTermEnum.ASSESSMENTEVENT] = Field(alias="type", examples=["AssessmentEvent"])
    actor: Union[PersonModel, str] = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: ActionTermEnum = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the Started, Paused, Resumed, Restarted, Reset, and Submitted actions only.",
    )
    object: Union[AssessmentModel, str] = Field(
        alias="object",
        description="The object value MUST be expressed either as an object or as a string corresponding to the object's IRI.",
    )
    generated: Union[AttemptModel, str] = Field(
        default=None,
        alias="generated",
        description="The generated value MUST be expressed either as an object or as a string corresponding to the generated entity's IRI.",
    )

    @field_validator("action")
    def action_limited_values(cls, action):
        """ """
        list_accepted_values = [
            ActionTermEnum.STARTED,
            ActionTermEnum.PAUSED,
            ActionTermEnum.RESUMED,
            ActionTermEnum.RESTARTED,
            ActionTermEnum.RESET,
            ActionTermEnum.SUBMITTED,
        ]
        if action not in list_accepted_values:
            raise ValueError(f"action has to be in this list: {list_accepted_values}")


class AssessmentItemEventModel(EventModel):
    type: Literal[TypeTermEnum.ASSESSMENTITEMEVENT] = Field(
        alias="type", examples=["AssessmentItemEvent"]
    )
    actor: Union[PersonModel, str] = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: ActionTermEnum = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the Started, Skipped, and Completed actions only.",
    )
    object: Union[AssessmentItemModel, str] = Field(
        alias="object",
        description="The object value MUST be expressed either as an object or as a string corresponding to the object's IRI.",
    )
    generated: Union[ResponseModel, str] = Field(
        default=None,
        alias="generated",
        description="For a completed action a generated Response or a subtype. The generated value MUST be expressed either as an object or as a string corresponding to the generated entity's IRI.",
    )
    referrer: Union[AssessmentItemModel, str] = Field(
        default=None,
        alias="referrer",
        description="The previous AssessmentItem attempted MAY be specified as the  referrer. The referrer value MUST be expressed either as an object or as a string corresponding to the referrer's IRI.",
    )

    @field_validator("action")
    def action_limited_values(cls, action):
        """ """
        list_accepted_values = [
            ActionTermEnum.STARTED,
            ActionTermEnum.SKIPPED,
            ActionTermEnum.COMPLETED,
        ]
        if action not in list_accepted_values:
            raise ValueError(f"action has to be in this list: {list_accepted_values}")


class AssignableEventModel(EventModel):
    type: Literal[TypeTermEnum.ASSIGNABLEEVENT] = Field(alias="type", examples=["AssignableEvent"])
    actor: Union[PersonModel, str] = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: ActionTermEnum = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the Activated, Deactivated, Started, Completed, Submitted, and Reviewed actions only.",
    )
    object: Union[AssignableDigitalResourceModel, str] = Field(
        alias="object",
        description="The AssignableDigitalResource that constitutes the  object of the interaction. The object value MUST be expressed either as an object or as a string corresponding to the object's IRI.",
    )
    target: Union[FrameModel, str] = Field(
        default=None,
        alias="target",
        description="A Frame that represents a particular segment or location within the object. The target value MUST be expressed either as an object or as a string corresponding to the target entity's IRI.",
    )
    generated: Union[AttemptModel, str] = Field(
        default=None,
        alias="generated",
        description="For Started, Completed and Reviewed actions, the actor's Attempt SHOULD be specified. The generated value MUST be expressed either as an object or as a string corresponding to the generated entity's IRI.",
    )

    @field_validator("action")
    def action_limited_values(cls, action):
        """ """
        list_accepted_values = [
            ActionTermEnum.ACTIVATED,
            ActionTermEnum.DEACTIVATED,
            ActionTermEnum.STARTED,
            ActionTermEnum.COMPLETED,
            ActionTermEnum.SUBMITTED,
            ActionTermEnum.REVIEWED,
        ]
        if action not in list_accepted_values:
            raise ValueError(f"action has to be in this list: {list_accepted_values}")


class FeedbackEventModel(EventModel):
    type: Literal[TypeTermEnum.FEEDBACKEVENT] = Field(alias="type", examples=["FeedbackEvent"])
    actor: Union[PersonModel, str] = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: ActionTermEnum = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the Commented and Ranked actions only.",
    )
    object: Union[EntityModel, str] = Field(
        alias="object",
        description="The Entity that is the target of the feedback. The object value MUST be expressed either as an object or as a string corresponding to the resource's IRI.",
    )
    target: Union[FrameModel, str] = Field(
        default=None,
        alias="target",
        description="If the object of the feedback is a particular segment of a DigitalResource use a Frame to mark its location. The target value MUST be expressed either as an object or as a string corresponding to the target entity’s IRI.",
    )
    generated: Union[RatingModel, CommentModel, str] = Field(
        default=None,
        alias="generated",
        description="The Rating or Comment entity that describes the feedback provided. If the action is Ranked then the  generated value MUST be expressed as a Rating. If the action is Commented then the generated value MUST be expressed as a Comment. The generated value MUST be expressed either as an object or as a string corresponding to the entity's IRI.",
    )

    @field_validator("action")
    def action_limited_values(cls, action):
        """ """
        list_accepted_values = [ActionTermEnum.COMMENTED, ActionTermEnum.RANKED]
        if action not in list_accepted_values:
            raise ValueError(f"action has to be in this list: {list_accepted_values}")


class ForumEventModel(EventModel):
    type: Literal[TypeTermEnum.FORUMEVENT] = Field(alias="type", examples=["ForumEvent"])
    actor: Union[PersonModel, str] = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: ActionTermEnum = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the Subscribed and Unsubscribed actions only.",
    )
    object: Union[ForumModel, str] = Field(
        alias="object",
        description="The Forum that comprises the object of this interaction. The  object value MUST be expressed either as an object or as a string corresponding to the object's IRI.",
    )

    @field_validator("action")
    def action_limited_values(cls, action):
        """ """
        list_accepted_values = [ActionTermEnum.SUBSCRIBED, ActionTermEnum.UNSUBSCRIBED]
        if action not in list_accepted_values:
            raise ValueError(f"action has to be in this list: {list_accepted_values}")


class GradeEventModel(EventModel):
    type: Literal[TypeTermEnum.GRADEEVENT] = Field(alias="type", examples=["GradeEvent"])
    actor: Union[AgentModel, str] = Field(
        alias="actor",
        description="An Agent, typically Person or SoftwareApplication, MUST be specified as the actor. The  actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: ActionTermEnum = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the Graded action only.",
    )
    object: Union[AttemptModel, str] = Field(
        alias="object",
        description="The completed Attempt. The object value MUST be expressed either as an object or as a string corresponding to the object's IRI.",
    )
    generated: Union[ScoreModel, str] = Field(
        default=None,
        alias="generated",
        description="The generated Score SHOULD be provided. The generated value MUST be expressed either as an object or as a string corresponding to the generated entity's IRI.",
    )

    @field_validator("action")
    def action_limited_values(cls, action):
        """ """
        list_accepted_values = [ActionTermEnum.GRADED]
        if action not in list_accepted_values:
            raise ValueError(f"action has to be in this list: {list_accepted_values}")


class MediaEventModel(EventModel):
    type: Literal[TypeTermEnum.MEDIAEVENT] = Field(alias="type", examples=["MediaEvent"])
    actor: Union[PersonModel, str] = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: ActionTermEnum = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the Started, Ended, Paused, Resumed, Restarted, ForwardedTo, JumpedTo, ChangedResolution, ChangedSize, ChangedSpeed, ChangedVolume, EnabledClosedCaptioning, DisabledClosedCaptioning, EnteredFullScreen, ExitedFullScreen, Muted, Unmuted, OpenedPopout, and ClosedPopout actions only.",
    )
    object: Union[MediaObjectModel, str] = Field(
        alias="object",
        description="The MediaObject or a subtype that constitutes the object of the interaction. The object value MUST be expressed either as an object or as a string corresponding to the object's IRI.",
    )
    target: Union[MediaLocationModel, str] = Field(
        default=None,
        alias="target",
        description="If the MediaEvent object is an AudioObject or VideoObject, a MediaLocation SHOULD be specified in order to provide the currentTime in the audio or video stream that marks the action. If the  currentTime is specified, the value MUST be an ISO 8601 formatted duration, e.g., 'PT30M54S'. The target value MUST be expressed either as an object or as a string corresponding to the target entity's IRI.",
    )

    @field_validator("action")
    def action_limited_values(cls, action):
        """ """
        list_accepted_values = [
            ActionTermEnum.STARTED,
            ActionTermEnum.ENDED,
            ActionTermEnum.PAUSED,
            ActionTermEnum.RESUMED,
            ActionTermEnum.RESTARTED,
            ActionTermEnum.FORWARDEDTO,
            ActionTermEnum.JUMPEDTO,
            ActionTermEnum.CHANGEDRESOLUTION,
            ActionTermEnum.CHANGEDSIZE,
            ActionTermEnum.CHANGEDSPEED,
            ActionTermEnum.CHANGEDVOLUME,
            ActionTermEnum.ENABLEDCLOSEDCAPTIONING,
            ActionTermEnum.DISABLEDCLOSEDCAPTIONING,
            ActionTermEnum.ENTEREDFULLSCREEN,
            ActionTermEnum.EXITEDFULLSCREEN,
            ActionTermEnum.MUTED,
            ActionTermEnum.UNMUTED,
            ActionTermEnum.OPENEDPOPOUT,
            ActionTermEnum.CLOSEDPOPOUT,
        ]
        if action not in list_accepted_values:
            raise ValueError(f"action has to be in this list: {list_accepted_values}")


class MessageEventModel(EventModel):
    type: Literal[TypeTermEnum.MESSAGEEVENT] = Field(alias="type", examples=["MessageEvent"])
    actor: Union[PersonModel, str] = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: ActionTermEnum = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the MarkedAsRead, MarkedAsUnRead, and Posted actions only.",
    )
    object: Union[MessageModel, str] = Field(
        alias="object",
        description="The Message that constitutes the object of the interaction. If the object represents a Message posted in reply to a previous post, the prior post prompting the Message SHOULD be referenced using the Message replyTo property. The object value MUST be expressed either as an object or as a string corresponding to the object's IRI.",
    )

    @field_validator("action")
    def action_limited_values(cls, action):
        """ """
        list_accepted_values = [
            ActionTermEnum.MARKEDASREAD,
            ActionTermEnum.MARKEDASUNREAD,
            ActionTermEnum.POSTED,
        ]
        if action not in list_accepted_values:
            raise ValueError(f"action has to be in this list: {list_accepted_values}")


class NavigationEventModel(EventModel):
    type: Literal[TypeTermEnum.NAVIGATIONEVENT] = Field(alias="type", examples=["NavigationEvent"])
    actor: Union[PersonModel, str] = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: ActionTermEnum = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the  object. The value range is limited to the actions: NavigatedTo.",
    )
    object: Union[DigitalResourceModel, SoftwareApplicationModel, str] = Field(
        alias="object",
        description="The DigitalResource or SoftwareApplication to which the actor navigated. The object value MUST be expressed either as an object or as a string corresponding to the resource's IRI.",
    )
    target: Union[DigitalResourceModel, str] = Field(
        default=None,
        alias="target",
        description="The DigitalResource that represents the particular part or location of the object being navigated to. The target value MUST be expressed either as an object or as a string corresponding to the referrer's IRI.",
    )
    referrer: Union[DigitalResourceModel, SoftwareApplicationModel, str] = Field(
        default=None,
        alias="referrer",
        description="The DigitalResource or SoftwareApplication that constitutes the referring context. The referrer value MUST be expressed either as an object or as a string corresponding to the referrer's IRI.",
    )

    @field_validator("action")
    def action_limited_values(cls, action):
        """ """
        list_accepted_values = [ActionTermEnum.NAVIGATEDTO]
        if action not in list_accepted_values:
            raise ValueError(f"action has to be in this list: {list_accepted_values}")


class QuestionnaireEventModel(EventModel):
    type: Literal[TypeTermEnum.QUESTIONNAIREEVENT] = Field(
        alias="type", examples=["QuestionnaireEvent"]
    )
    actor: Union[PersonModel, str] = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: ActionTermEnum = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the actions: Started, or Submitted.",
    )
    object: Union[QuestionnaireModel, str] = Field(
        alias="object",
        description="The Questionnaire that the actor is taking. The  object value MUST be expressed either as an object or as a string corresponding to the resource's IRI.",
    )

    @field_validator("action")
    def action_limited_values(cls, action):
        """ """
        list_accepted_values = [ActionTermEnum.STARTED, ActionTermEnum.SUBMITTED]
        if action not in list_accepted_values:
            raise ValueError(f"action has to be in this list: {list_accepted_values}")


class QuestionnaireItemEventModel(EventModel):
    type: Literal[TypeTermEnum.QUESTIONNAIREITEMEVENT] = Field(
        alias="type", examples=["QuestionnaireItemEvent"]
    )
    actor: Union[PersonModel, str] = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: ActionTermEnum = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the actions: Started, Skipped, or Completed.",
    )
    object: Union[QuestionnaireItemModel, str] = Field(
        alias="object",
        description="The QuestionnaireItem started, attempted, or skipped by the  actor. The object value MUST be expressed either as an object or as a string corresponding to the resource's IRI.",
    )
    generated: Union[ResponseModel, str] = Field(
        default=None,
        alias="generated",
        description="For a Completed action a generated Response MAY be referenced. The generated value MUST be expressed either as an object or as a string corresponding to the Response resource's IRI.",
    )

    @field_validator("action")
    def action_limited_values(cls, action):
        """ """
        list_accepted_values = [
            ActionTermEnum.STARTED,
            ActionTermEnum.SKIPPED,
            ActionTermEnum.COMPLETED,
        ]
        if action not in list_accepted_values:
            raise ValueError(f"action has to be in this list: {list_accepted_values}")


class ResourceManagementEventModel(EventModel):
    type: Literal[TypeTermEnum.RESOURCEMANAGEMENTEVENT] = Field(
        alias="type", examples=["ResourceManagementEvent"]
    )
    actor: Union[PersonModel, str] = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: ActionTermEnum = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the  object. The value range is limited to the Archived, Copied, Created, Deleted, Described, Downloaded, Modified, Printed, Published, Restored, Retrieved, Saved, Unpublished, and Uploaded actions only.",
    )
    object: Union[DigitalResourceModel, str] = Field(
        alias="object",
        description="The DigitalResource that is being managed. The  object value MUST be expressed either as an object or as a string corresponding to the resource's IRI.",
    )
    generated: Union[DigitalResourceModel, str] = Field(
        default=None,
        alias="generated",
        description="The DigitalResource that was generated by the Copied action. The object value MUST be expressed either as an object or as a string corresponding to the resource's IRI. (Copied action only)",
    )

    @field_validator("generated")
    def generated_required_condition(cls, generated, values):
        """Required when the action value is Copied, otherwise optional"""
        if values.get("action", "") == ActionTermEnum.COPIED and not generated:
            raise ValueError(f"generated cannot be empty if action is {ActionTermEnum.COPIED}")

    @field_validator("action")
    def action_limited_values(cls, action):
        """ """
        list_accepted_values = [
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
        ]
        if action not in list_accepted_values:
            raise ValueError(f"action has to be in this list: {list_accepted_values}")


class SearchEventModel(EventModel):
    type: Literal[TypeTermEnum.SEARCHEVENT] = Field(alias="type", examples=["SearchEvent"])
    actor: Union[PersonModel, str] = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: ActionTermEnum = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the  object. The value range is limited to the Searched action only.",
    )
    object: Union[EntityModel, str] = Field(
        alias="object",
        description="The Entity, typically a DigitalResource or SoftwareApplication, that is the target of the search. The object value MUST be expressed either as an object or as a string corresponding to the resources's IRI.",
    )
    generated: Union[SearchResponseModel, str] = Field(
        default=None,
        alias="generated",
        description="The SearchResponse generated by the search provider that describes the search criteria, count of search results returned (if any), and references to the search result items (if any) returned by the search. The SearchResponse value MUST be expressed either as an object or as a string corresponding to the query’s IRI.",
    )

    @field_validator("action")
    def action_limited_values(cls, action):
        """ """
        list_accepted_values = [ActionTermEnum.SEARCHED]
        if action not in list_accepted_values:
            raise ValueError(f"action has to be in this list: {list_accepted_values}")


class SessionEventModel(EventModel):
    type: Literal[TypeTermEnum.SESSIONEVENT] = Field(alias="type", examples=["SessionEvent"])
    actor: Union[PersonModel, SoftwareApplicationModel, str] = Field(
        alias="actor",
        description="The Agent who initiated the action. For LoggedIn and LoggedOut actions a Person MUST be specified as the actor. For a TimedOut action a SoftwareApplication MUST be specified as the actor. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: ActionTermEnum = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the LoggedIn, LoggedOut, and TimedOut actions only.",
    )
    object: Union[SessionModel, SoftwareApplicationModel, str] = Field(
        alias="object",
        description="For LoggedIn and LoggedOut actions a SoftwareApplication MUST be specified as the object. For a TimedOut action the Session MUST be specified as the object. The object value MUST be expressed either as an object or as a string corresponding to the object's IRI.",
    )
    target: Union[DigitalResourceModel, str] = Field(
        default=None,
        alias="target",
        description="When logging in to a SoftwareApplication, if the actor is attempting to access a particular DigitalResource it MAY be designated as the  target of the interaction. The target value MUST be expressed either as an object or as a string corresponding to the target entity's IRI.",
    )
    referrer: Union[DigitalResourceModel, SoftwareApplicationModel, str] = Field(
        default=None,
        alias="referrer",
        description="The DigitalResource or SoftwareApplication that constitutes the referring context MAY be specified as the referrer. The  referrer value MUST be expressed either as an object or as a string corresponding to the referrer's IRI.",
    )

    @field_validator("action")
    def action_limited_values(cls, action):
        """ """
        list_accepted_values = [
            ActionTermEnum.LOGGEDIN,
            ActionTermEnum.LOGGEDOUT,
            ActionTermEnum.TIMEDOUT,
        ]
        if action not in list_accepted_values:
            raise ValueError(f"action has to be in this list: {list_accepted_values}")


class SurveyEventModel(EventModel):
    type: Literal[TypeTermEnum.SURVEYEVENT] = Field(alias="type", examples=["SurveyEvent"])
    actor: Union[PersonModel, str] = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: ActionTermEnum = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the  object. The value range is limited to the actions: OptedIn or OptedOut.",
    )
    object: Union[SurveyModel, str] = Field(
        alias="object",
        description="The Survey to which the actor is opting into or out of. The object value MUST be expressed either as an object or as a string corresponding to the resource's IRI.",
    )

    @field_validator("action")
    def action_limited_values(cls, action):
        """ """
        list_accepted_values = [ActionTermEnum.OPTEDIN, ActionTermEnum.OPTEDOUT]
        if action not in list_accepted_values:
            raise ValueError(f"action has to be in this list: {list_accepted_values}")


class SurveyInvitationEventModel(EventModel):
    type: Literal[TypeTermEnum.SURVEYINVITATIONEVENT] = Field(
        alias="type", examples=["SurveyInvitationEvent"]
    )
    actor: Union[PersonModel, str] = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: ActionTermEnum = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the actions: Accepted, Declined, or Sent.",
    )
    object: Union[SurveyInvitationModel, str] = Field(
        alias="object",
        description="The SurveyInvitation to which the actor is sending out or responding to. The object value MUST be expressed either as an object or as a string corresponding to the resource's IRI.",
    )

    @field_validator("action")
    def action_limited_values(cls, action):
        """ """
        list_accepted_values = [
            ActionTermEnum.ACCEPTED,
            ActionTermEnum.DECLINED,
            ActionTermEnum.SENT,
        ]
        if action not in list_accepted_values:
            raise ValueError(f"action has to be in this list: {list_accepted_values}")


class ThreadEventModel(EventModel):
    type: Literal[TypeTermEnum.THREADEVENT] = Field(alias="type", examples=["ThreadEvent"])
    actor: Union[PersonModel, str] = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: ActionTermEnum = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the MarkedAsRead and MarkedAsUnRead actions only.",
    )
    object: Union[ThreadModel, str] = Field(
        alias="object",
        description="The Thread that constitutes the object of the interaction. The  object value MUST be expressed either as an object or as a string corresponding to the object's IRI.",
    )

    @field_validator("action")
    def action_limited_values(cls, action):
        """ """
        list_accepted_values = [ActionTermEnum.MARKEDASREAD, ActionTermEnum.MARKEDASUNREAD]
        if action not in list_accepted_values:
            raise ValueError(f"action has to be in this list: {list_accepted_values}")


class ToolLaunchEventModel(EventModel):
    type: Literal[TypeTermEnum.TOOLLAUNCHEVENT] = Field(alias="type", examples=["ToolLaunchEvent"])
    actor: Union[PersonModel, str] = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: ActionTermEnum = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to either the Launched or Returned actions.",
    )
    object: Union[SoftwareApplicationModel, str] = Field(
        alias="object",
        description="The SoftwareApplication that is the target of the actor's launch activity. The object value MUST be expressed either as an object or as a string corresponding to the software application's IRI.",
    )
    generated: DigitalResourceModel = Field(
        default=None,
        alias="generated",
        description="In the case that the workflow comes with a resource intended for the receiver of the workflow message associated with this event (for example, a file, or image, or LTI resource link for the receiver to embed within its system), this property can carry its representation as a Caliper DigitalResource or, more likely, one of its specific subtypes.",
    )
    target: Union[LinkModel, LtiLinkModel] = Field(
        default=None,
        alias="target",
        description="The fully qualified URL to which the workflow was redirected. In the case of the Launched action, this would be the fully qualified entry-point on the external tool to which the platform launches. In the case of the Returned action, this would be the fully qualified entry-point on the platform to which the tool is redirecting the workflow after user activity from the original launch finishes (this could be the launch_presentation_return_url in the case of a simple LTI Resource Link request; it could also be the deep_link_return_url in the case of a Deep Linking Response message).",
    )
    federated_session: Union[LtiSessionModel, str] = Field(
        alias="federatedSession",
        description='The Platform\'s session, constituting part of the tool launch context. The federatedSession value MUST be expressed either as an object or as a string corresponding to the federatedSession’s IRI. Required when the action value is Launched, otherwise optional. Workflows that include a specific "return message" component (e.g. LTI Deep Linking response messages) SHOULD provide the federatedSession property and SHOULD populate its messageParameters property with the message parameters in the response message.',
    )

    @field_validator("federated_session")
    def federated_session_required_condition(cls, federated_session, values):
        """Required when the action value is Launched, otherwise optional"""
        if values.get("action", "") == ActionTermEnum.LAUNCHED and not federated_session:
            raise ValueError(
                f"federated_session cannot be empty if action is {ActionTermEnum.LAUNCHED}"
            )

    @field_validator("action")
    def action_limited_values(cls, action):
        """ """
        list_accepted_values = [ActionTermEnum.LAUNCHED, ActionTermEnum.RETURNED]
        if action not in list_accepted_values:
            raise ValueError(f"action has to be in this list: {list_accepted_values}")


class ToolUseEventModel(EventModel):
    type: Literal[TypeTermEnum.TOOLUSEEVENT] = Field(alias="type", examples=["ToolUseEvent"])
    actor: Union[PersonModel, str] = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor’s IRI.",
    )
    action: ActionTermEnum = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the Used action only.",
    )
    object: Union[SoftwareApplicationModel, str] = Field(
        alias="object",
        description="The SoftwareApplication that constitutes the object of the interaction. The object value MUST be expressed either as an object or as a string corresponding to the object’s IRI.",
    )
    target: Union[SoftwareApplicationModel, str] = Field(
        default=None,
        alias="target",
        description="A SoftwareApplication that represents a particular capability or feature provided by the object. The target value MUST be expressed either as an object or as a string corresponding to the target entity’s IRI.",
    )
    generated: Union[AggregateMeasureCollectionModel, str] = Field(
        default=None,
        alias="generated",
        description="An AggregateMeasureCollection created or generated as a result of the interaction. The generated value MUST be expressed either as an object or as a string corresponding to the generated entity’s IRI. Note that if the sender of the event wants to send aggregate measure information as part of this ToolUseEvent it should, by best practice, send a single AggregateMeasureCollection as the generated value.",
    )

    @field_validator("action")
    def action_limited_values(cls, action):
        """ """
        list_accepted_values = [ActionTermEnum.USED]
        if action not in list_accepted_values:
            raise ValueError(f"action has to be in this list: {list_accepted_values}")


class ViewEventModel(EventModel):
    type: Literal[TypeTermEnum.VIEWEVENT] = Field(alias="type", examples=["ViewEvent"])
    actor: Union[PersonModel, str] = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: ActionTermEnum = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object. The value range is limited to the actions: Viewed.",
    )
    object: Union[DigitalResourceModel, str] = Field(
        alias="object",
        description="The DigitalResource that the actor viewed. The object value MUST be expressed either as an object or as a string corresponding to the resource's IRI.",
    )

    @field_validator("action")
    def action_limited_values(cls, action):
        """ """
        list_accepted_values = [ActionTermEnum.VIEWED]
        if action not in list_accepted_values:
            raise ValueError(f"action has to be in this list: {list_accepted_values}")


################################################
##################### MAIN #####################
################################################
class IMSCapilerModel(BaseModel):
    data: List[EventModel] = Field(alias="data")
    data_version: str = Field(
        alias="dataVersion", examples=["http://purl.imsglobal.org/ctx/caliper/v1p2"]
    )
    send_time: str = Field(alias="sendTime", examples=["2019-11-16T02:08:59.163Z"])
    sensor: str = Field(alias="sensor", examples=["http://oxana.instructure.com/"])

    @field_validator("data", mode="before")
    def validation(cls, value: List[EventModel], extra_info: ValidationInfo):
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
        field = cls.model_fields.get(extra_info.field_name if extra_info.field_name else "", None)

        if isinstance(field, FieldInfo):
            # Get child classes
            list_event_model = set()
            list_event_model.update(ExtendedTypeBaseModel._get_subclasses(field.annotation))
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
                    if isinstance(each_value, dict) and (
                        event_model := dict_discriminator.get(each_value.get("type", ""), None)
                    ):
                        each_value = event_model(**each_value)
                    new_value.append(each_value)
                return new_value

        return value
