from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING, Literal, get_args, get_origin

from models.trace_formats.base import ExtendedTypeBaseModel
from pydantic import BaseModel, Field, field_validator
from pydantic.fields import FieldInfo

if TYPE_CHECKING:
    from pydantic_core.core_schema import ValidationInfo

#############################################################
##################### ENUMS/TERMS/TYPES #####################
#############################################################
class StatusTermEnum(StrEnum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"


class RoleTermEnum(StrEnum):
    ADMINISTRATOR = "Administrator"
    ADMINISTRATOR_ADMINISTRATOR = "Administrator#Administrator"
    ADMINISTRATOR_DEVELOPER = "Administrator#Developer"
    ADMINISTRATOR_EXTERNALDEVELOPER = "Administrator#ExternalDeveloper"
    ADMINISTRATOR_EXTERNALSUPPORT = "Administrator#ExternalSupport"
    ADMINISTRATOR_EXTERNALSYSTEMADMINISTRATOR = (
        "Administrator#ExternalSystemAdministrator"
    )
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
    ACTIVATED = "Activated"
    ADDED = "Added"
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
    CREATED = "Created"
    DEACTIVATED = "Deactivated"
    DELETED = "Deleted"
    DESCRIBED = "Described"
    DISABLEDCLOSEDCAPTIONING = "DisabledClosedCaptioning"
    DISLIKED = "Disliked"
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
    PAUSED = "Paused"
    POSTED = "Posted"
    QUESTIONED = "Questioned"
    RANKED = "Ranked"
    RECOMMENDED = "Recommended"
    REMOVED = "Removed"
    RESET = "Reset"
    RESTARTED = "Restarted"
    RESUMED = "Resumed"
    RETRIEVED = "Retrieved"
    REVIEWED = "Reviewed"
    REWOUND = "Rewound"
    SEARCHED = "Searched"
    SHARED = "Shared"
    SHOWED = "Showed"
    SKIPPED = "Skipped"
    STARTED = "Started"
    SUBMITTED = "Submitted"
    SUBSCRIBED = "Subscribed"
    TAGGED = "Tagged"
    TIMEDOUT = "TimedOut"
    UNMUTED = "Unmuted"
    UNSUBSCRIBED = "Unsubscribed"
    USED = "Used"
    VIEWED = "Viewed"


class ProfileTermEnum(StrEnum):
    ANNOTATIONPROFILE = "AnnotationProfile"
    ASSESSMENTPROFILE = "AssessmentProfile"
    ASSIGNABLEPROFILE = "AssignableProfile"
    BASICPROFILE = "BasicProfile"
    FORUMPROFILE = "ForumProfile"
    GRADINGPROFILE = "GradingProfile"
    MEDIAPROFILE = "MediaProfile"
    READINGPROFILE = "ReadingProfile"
    SESSIONPROFILE = "SessionProfile"
    TOOLUSEPROFILE = "ToolUseProfile"


class TypeTermEnum(StrEnum):
    AGENT = "Agent"
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
    COURSEOFFERING = "CourseOffering"
    COURSESECTION = "CourseSection"
    DIGITALRESOURCE = "DigitalResource"
    DIGITALRESOURCECOLLECTION = "DigitalResourceCollection"
    DOCUMENT = "Document"
    ENTITY = "Entity"
    EPUBCHAPTER = "EpubChapter"
    EPUBPART = "EpubPart"
    EPUBSUBCHAPTER = "EpubSubChapter"
    EPUBVOLUME = "EpubVolume"
    EVENT = "Event"
    FILLINBLANKRESPONSE = "FillinBlankResponse"
    FORUM = "Forum"
    FORUMEVENT = "ForumEvent"
    FRAME = "Frame"
    GRADEEVENT = "GradeEvent"
    GROUP = "Group"
    HIGHLIGHTANNOTATION = "HighlightAnnotation"
    IMAGEOBJECT = "ImageObject"
    LEARNINGOBJECTIVE = "LearningObjective"
    LTISESSION = "LtiSession"
    MEDIAEVENT = "MediaEvent"
    MEDIALOCATION = "MediaLocation"
    MEDIAOBJECT = "MediaObject"
    MEMBERSHIP = "Membership"
    MESSAGE = "Message"
    MESSAGEEVENT = "MessageEvent"
    MULTIPLECHOICERESPONSE = "MultipleChoiceResponse"
    MULTIPLERESPONSERESPONSE = "MultipleResponseResponse"
    NAVIGATIONEVENT = "NavigationEvent"
    ORGANIZATION = "Organization"
    OUTCOMEEVENT = "OutcomeEvent"
    PAGE = "Page"
    PERSON = "Person"
    READING = "Reading"
    READINGEVENT = "ReadingEvent"
    RESPONSE = "Response"
    RESULT = "Result"
    SCORE = "Score"
    SELECTTEXTRESPONSE = "SelectTextResponse"
    SESSION = "Session"
    SESSIONEVENT = "SessionEvent"
    SHAREDANNOTATION = "SharedAnnotation"
    SOFTWAREAPPLICATION = "SoftwareApplication"
    TAGANNOTATION = "TagAnnotation"
    TEXTPOSITIONSELECTOR = "TextPositionSelector"
    THREAD = "Thread"
    THREADEVENT = "ThreadEvent"
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
        description="The staring position of the selected text MUST be specified. The first character in the full text is character position 0.",
    )
    end: int = Field(
        alias="end",
        description="The end position of the selected text MUST be specified.",
    )


####################################################
##################### ENTITIES #####################
####################################################
class EntityModel(ExtendedTypeBaseModel):
    context: Literal["http://purl.imsglobal.org/ctx/caliper/v1p1"] = Field(
        default=None,
        alias="@context",
        examples=["http://purl.imsglobal.org/ctx/caliper/v1p1"],
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


class OrganizationModel(AgentModel):
    type: Literal[TypeTermEnum.ORGANIZATION] = Field(
        alias="type",
        examples=[TypeTermEnum.ORGANIZATION.value],
    )
    sub_organization_of: OrganizationModel | str = Field(
        default=None,
        alias="subOrganizationOf",
    )
    members: list[AgentModel | str] = Field(
        default=None,
        alias="members",
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


class GroupModel(OrganizationModel):
    type: Literal[TypeTermEnum.GROUP] = Field(
        alias="type",
        examples=[TypeTermEnum.GROUP.value],
    )


class LearningObjectiveModel(EntityModel):
    type: Literal[TypeTermEnum.LEARNINGOBJECTIVE] = Field(
        alias="type",
        examples=[TypeTermEnum.LEARNINGOBJECTIVE.value],
    )


class DigitalResourceModel(EntityModel):
    type: Literal[TypeTermEnum.DIGITALRESOURCE] = Field(
        alias="type", examples=[TypeTermEnum.DIGITALRESOURCE.DIGITALRESOURCE],
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
    # DEPRECATED
    object_type: str = Field(
        default=None,
        alias="objectType",
        description="A string value that designates the DigitalResource type.",
        json_schema_extra={"deprecated": True},
    )
    aligned_learning_objective: list[LearningObjectiveModel] = Field(
        default=None,
        alias="alignedLearningObjective",
        description="An ordered collection of one or more LearningObjective entities that describe what a learner is expected to comprehend or accomplish after engaging with a DigitalResource. alignedLearningObjective has been DEPRECATED and replaced by learningObjectives.",
        json_schema_extra={"deprecated": True},
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


# DeprecationWarning
class ReadingModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.READING] = Field(
        alias="type",
        examples=[TypeTermEnum.READING.value],
    )


class PageModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.PAGE] = Field(
        alias="type",
        examples=[TypeTermEnum.PAGE.value],
    )


class MediaObjectModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.MEDIAOBJECT] = Field(
        alias="type",
        examples=[TypeTermEnum.MEDIAOBJECT.value],
    )
    duration: str = Field(
        default=None,
        alias="duration",
        description="An optional time interval that represents the total time required to view and/or listen to the MediaObject at normal speed. If a duration is specified the value MUST conform to the ISO 8601 duration format.",
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


class ImageObjectModel(MediaObjectModel):
    type: Literal[TypeTermEnum.IMAGEOBJECT] = Field(
        alias="type",
        examples=[TypeTermEnum.IMAGEOBJECT.value],
    )


class VideoObjectModel(MediaObjectModel):
    type: Literal[TypeTermEnum.VIDEOOBJECT] = Field(
        alias="type",
        examples=[TypeTermEnum.VIDEOOBJECT.value],
    )


class ChapterModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.CHAPTER] = Field(
        alias="type",
        examples=[TypeTermEnum.CHAPTER.value],
    )


class DocumentModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.DOCUMENT] = Field(
        alias="type",
        examples=[TypeTermEnum.DOCUMENT.value],
    )


# DeprecationWarning
class EpubChapterModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.EPUBCHAPTER] = Field(
        alias="type",
        examples=[TypeTermEnum.EPUBCHAPTER.value],
    )


# DeprecationWarning
class EpubPartModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.EPUBPART] = Field(
        alias="type",
        examples=[TypeTermEnum.EPUBPART.value],
    )


# DeprecationWarning
class EpubSubChapterModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.EPUBSUBCHAPTER] = Field(
        alias="type",
        examples=[TypeTermEnum.EPUBSUBCHAPTER.value],
    )


# DeprecationWarning
class EpubVolumeModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.EPUBVOLUME] = Field(
        alias="type",
        examples=[TypeTermEnum.EPUBVOLUME.value],
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
        description="A string value comprising a plain-text rendering of the body content of the Message.",
    )
    attachments: list[DigitalResourceModel | str] = Field(
        default=None,
        alias="attachments",
        description="An ordered collection of one or more DigitalResource entities attached to this Message. Each array item MUST be expressed either as an object or as a string corresponding to the item's IRI.",
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


class DigitalResourceCollectionModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.DIGITALRESOURCECOLLECTION] = Field(
        alias="type",
        examples=[TypeTermEnum.DIGITALRESOURCECOLLECTION.value],
    )
    items: list[DigitalResourceModel | str] = Field(
        default=None,
        alias="items",
        description="An ordered collection of DigitalResource entities. Each array item MUST be expressed either as an object or as a string corresponding to the item's IRI.",
    )


class WebPageModel(DigitalResourceModel):
    type: Literal[TypeTermEnum.WEBPAGE] = Field(
        alias="type",
        examples=[TypeTermEnum.WEBPAGE.value],
    )


class ThreadModel(DigitalResourceCollectionModel):
    type: Literal[TypeTermEnum.THREAD] = Field(
        alias="type",
        examples=[TypeTermEnum.THREAD.value],
    )
    is_part_of: ForumModel | str = Field(
        default=None,
        alias="isPartOf",
        description="A related Entity that includes or incorporates the resource as a part of its whole. The isPartOf value MUST be expressed either as an object or as a string corresponding to the associated entity's IRI.",
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


class BookmarkAnnotationModel(AnnotationModel):
    type: Literal[TypeTermEnum.BOOKMARKANNOTATION] = Field(
        alias="type", examples=[TypeTermEnum.BOOKMARKANNOTATION.value],
    )
    bookmark_notes: str = Field(
        default=None,
        alias="bookmarkNotes",
        description="A string value comprising a plain text rendering of the note that accompanies the bookmark.",
    )


class HighlightAnnotationModel(AnnotationModel):
    type: Literal[TypeTermEnum.HIGHLIGHTANNOTATION] = Field(
        alias="type",
        examples=[TypeTermEnum.HIGHLIGHTANNOTATION.value],
    )
    selection: TextPositionSelectorModel = Field(
        default=None,
        alias="selection",
        description="The start and end positions of the highlighted text segment. The first character in the full text is character position 0. If a TextPositionSelector is defined both its start and end positions MUST be specified.",
    )
    selection_text: str = Field(
        default=None,
        alias="selectionText",
        description="A string value representing a plain-text rendering of the highlighted segment of the annotated DigitalResource.",
    )


class SharedAnnotationModel(AnnotationModel):
    type: Literal[TypeTermEnum.SHAREDANNOTATION] = Field(
        alias="type",
        examples=[TypeTermEnum.SHAREDANNOTATION.value],
    )
    with_agents: list[AgentModel | str] = Field(
        default=None,
        alias="withAgents",
        description="An ordered collection of one or more Agent entities, typically of type Person, with whom the annotated DigitalResource has been shared. Each array item MUST be expressed either as an object or as a string corresponding to the item's IRI.",
    )


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
    assignable: AssessmentModel | DigitalResourceModel | str = Field(
        default=None,
        alias="assignable",
        description="The DigitalResource that constitutes the object of the assignment. The assignable value MUST be expressed either as an object or as a string corresponding to the assigned resource's IRI.",
    )
    is_part_of: AttemptModel | str = Field(
        default=None,
        alias="isPartOf",
        description="The parent Attempt, if one exists. The isPartOf value MUST be expressed either as an object or as a string corresponding to the associated attempt's IRI.",
    )
    count: int = Field(
        default=None,
        alias="count",
        description="The total number of attempts inclusive of the current attempt that have been registered against the assigned DigitalResource.",
    )
    started_at_time: str = Field(
        default=None,
        alias="startedAtTime",
        description="An ISO 8601 date and time value expressed with millisecond precision that describes when the Attempt was commenced. The value MUST be expressed using the format YYYY-MM-DDTHH:mm:ss.SSSZ set to UTC with no offset specified.",
    )  # DateTime
    ended_at_time: str = Field(
        default=None,
        alias="endedAtTime",
        description="An ISO 8601 date and time value expressed with millisecond precision that describes when the Attempt was completed or terminated. The value MUST be expressed using the format YYYY-MM-DDTHH:mm:ss.SSSZ set to UTC with no offset specified.",
    )  # DateTime
    duration: str = Field(
        default=None,
        alias="duration",
        description="A time interval that represents the time taken to complete the Attempt. If a duration is specified the value MUST conform to the ISO 8601 duration format.",
    )  # Duration
    # DEPRECATED
    actor: PersonModel = Field(
        default=None,
        alias="actor",
        description="The Person who initiated the Attempt. actor has been DEPRECATED and replaced by assignee.",
        json_schema_extra={"deprecated": True},
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
        examples=[[RoleTermEnum.LEARNER.value]],
    )
    status: StatusTermEnum = Field(default=None, alias="status")


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
        description="An ISO 8601 date and time value expressed with millisecond precision that describes when the Response was commenced. The value MUST be expressed using the format YYYY-MM-DDTHH:mm:ss.SSSZ set to UTC with no offset specified.",
    )  # DateTime
    ended_at_time: str = Field(
        default=None,
        alias="endedAtTime",
        description="An ISO 8601 date and time value expressed with millisecond precision that describes when the Response was completed or terminated. The value MUST be expressed using the format YYYY-MM-DDTHH:mm:ss.SSSZ set to UTC with no offset specified.",
    )  # DateTime
    duration: str = Field(
        default=None,
        alias="duration",
        description="A time interval that represents the time taken to complete the Response. If a duration is specified the value MUST conform to the ISO 8601 duration format.",
    )  # Duration
    # DEPRECATED
    actor: PersonModel = Field(
        default=None,
        alias="actor",
        description="The Person who generated the Response. actor has been DEPRECATED and replaced by attempt.",
        json_schema_extra={"deprecated": True},
    )
    assignable: AssessmentItemModel = Field(
        default=None,
        alias="assignable",
        description="The AssessmentItem associated with the Response. assignable has been DEPRECATED and replaced by attempt.",
        json_schema_extra={"deprecated": True},
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


class SessionModel(EntityModel):
    type: Literal[TypeTermEnum.SESSION] = Field(
        alias="type",
        examples=[TypeTermEnum.SESSION.value],
    )
    user: PersonModel | str = Field(default=None, alias="user")
    started_at_time: str = Field(default=None, alias="startedAtTime")  # Datetime
    ended_at_time: str = Field(default=None, alias="endedAtTime")  # Datetime
    duration: str = Field(default=None, alias="duration")  # Duration ISO 8601
    # DEPRECATED
    actor: PersonModel = Field(
        default=None,
        alias="actor",
        description="The Person who initiated the Session. actor property has been DEPRECATED and replaced by user.",
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
        description="The Agent who scored or graded the Attempt. The scoredBy value MUST be expressed either as an object or as a string corresponding to the scorer's IRI.",
    )
    comment: str = Field(
        default=None,
        alias="comment",
        description="Plain text feedback provided by the scorer.",
    )
    # DEPRECATED
    actor: PersonModel = Field(
        default=None,
        alias="actor",
        description="The Person who generated the Attempt. actor has been DEPRECATED and replaced by attempt.",
        json_schema_extra={"deprecated": True},
    )
    assignable: DigitalResourceModel = Field(
        default=None,
        alias="assignable",
        description="The assigned DigitalResource associated with the Result. assignable has been DEPRECATED and replaced by attempt.",
        json_schema_extra={"deprecated": True},
    )
    normal_score: float = Field(
        default=None,
        alias="normalScore",
        description="The score earned by the learner before adding the extraCreditScore, subtracting the penaltyScore or applying the curveFactor, if any.",
        json_schema_extra={"deprecated": True},
    )
    penalty_score: float = Field(
        default=None,
        alias="penaltyScore",
        description="The number of points deducted from the normalScore due to an infraction such as submitting an Attempt after the due date.",
        json_schema_extra={"deprecated": True},
    )
    extra_credit_score: float = Field(
        default=None,
        alias="extraCreditScore",
        description="The number of extra credit points earned by the learner.",
        json_schema_extra={"deprecated": True},
    )
    total_score: float = Field(
        default=None,
        alias="totalScore",
        description="A score earned by the learner equal to the sum of normalScore + extraCreditScore - penaltyScore. This value does not take into account the effects of curving.",
        json_schema_extra={"deprecated": True},
    )
    curved_total_score: float = Field(
        default=None,
        alias="curvedTotalScore",
        description="The total score earned by the learner after applying a curveFactor to a method for computing a scaled score; e.g., adjusting the score equal to the sum of 100 - curvedFactor(100 - totalScore).",
        json_schema_extra={"deprecated": True},
    )
    curve_factor: float = Field(
        default=None,
        alias="curveFactor",
        description="A scale factor to be used in adjusting the totalScore.",
        json_schema_extra={"deprecated": True},
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
        description="The Agent who scored or graded the Attempt. The scoredBy value MUST be expressed either as an object or as a string corresponding to the scorer's IRI.",
    )
    comment: str = Field(
        default=None,
        alias="comment",
        description="Plain text feedback provided by the scorer.",
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


##################################################
##################### EVENTS #####################
##################################################
class EventModel(ExtendedTypeBaseModel):
    context: Literal["http://purl.imsglobal.org/ctx/caliper/v1p1"] = Field(
        default=None,
        alias="@context",
        examples=["http://purl.imsglobal.org/ctx/caliper/v1p1"],
    )
    id: str = Field(
        alias="id",
        examples=["urn:uuid:cf6e0f3b-3511-4254-86c5-6936ff33f267"],
    )
    type: Literal[TypeTermEnum.EVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.NAVIGATIONEVENT.value],
    )
    actor: AgentModel | str = Field(
        alias="actor",
        description="An Agent, typically Person or SoftwareApplication, MUST be specified as the actor. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )
    action: ActionTermEnum = Field(
        alias="action",
        description="The action or predicate that binds the actor or subject to the object",
        examples=[ActionTermEnum.NAVIGATEDTO.value],
    )
    object: EntityModel | str = Field(
        alias="object",
        description="The object value MUST be expressed either as an object or as a string corresponding to the object's IRI.",
    )
    event_time: str = Field(
        alias="eventTime",
        examples=["2019-11-01T00:09:06.878Z"],
    )  # Datetime
    target: EntityModel | str = Field(
        default=None,
        alias="target",
        description="The target value MUST be expressed either as an object or as a string corresponding to the target entity's IRI.",
    )
    generated: EntityModel | str = Field(
        default=None,
        alias="generated",
        description="The generated value MUST be expressed either as an object or as a string corresponding to the generated entity's IRI.",
    )
    ed_app: SoftwareApplicationModel | str = Field(default=None, alias="edApp")
    referrer: EntityModel | str = Field(
        default=None,
        alias="referrer",
        examples=[
            "https://oxana.instructure.com/courses/565/discussion_topics/1072925?module_item_id=4635201",
        ],
        description="The referrer value MUST be expressed either as an object or as a string corresponding to the referrer's IRI.",
    )
    group: OrganizationModel | str = Field(default=None, alias="group")
    membership: MembershipModel | str = Field(default=None, alias="membership")

    session: SessionModel | str = Field(default=None, alias="session")
    federated_session: LtiSessionModel | str = Field(
        default=None,
        alias="federatedSession",
    )
    extensions: dict = Field(
        default=None,
        alias="extensions",
    )


class EventPersonModel(EventModel):
    actor: PersonModel | str = Field(
        alias="actor",
        description="The Person who initiated the action. The actor value MUST be expressed either as an object or as a string corresponding to the actor's IRI.",
    )


class AnnotationEventModel(EventPersonModel):
    type: Literal[TypeTermEnum.ANNOTATIONEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.ANNOTATIONEVENT.value],
    )
    action: Literal[
        ActionTermEnum.BOOKMARKED,
        ActionTermEnum.HIGHLIGHTED,
        ActionTermEnum.SHARED,
        ActionTermEnum.TAGGED,
    ] = Field(alias="action")
    object: DigitalResourceModel | str = Field(
        alias="object",
        description="The annotated DigitalResource that constitutes the object of the interaction.",
    )
    target: FrameModel | str = Field(
        default=None,
        alias="target",
        description="A Frame that represents a particular segment or location within the object.",
    )
    generated: AnnotationModel | str = Field(
        default=None,
        alias="generated",
        description="The generated Annotation or a subtype.",
    )


class AssessmentEventModel(EventPersonModel):
    type: Literal[TypeTermEnum.ASSESSMENTEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.ASSESSMENTEVENT.value],
    )
    action: Literal[
        ActionTermEnum.PAUSED,
        ActionTermEnum.RESET,
        ActionTermEnum.RESTARTED,
        ActionTermEnum.RESUMED,
        ActionTermEnum.STARTED,
        ActionTermEnum.SUBMITTED,
    ] = Field(alias="action")
    object: AssessmentModel | AttemptModel | str = Field(alias="object")
    generated: AttemptModel | str = Field(default=None, alias="generated")


class AssessmentItemEventModel(EventPersonModel):
    type: Literal[TypeTermEnum.ASSESSMENTITEMEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.ASSESSMENTITEMEVENT.value],
    )
    action: Literal[
        ActionTermEnum.COMPLETED,
        ActionTermEnum.SKIPPED,
        ActionTermEnum.STARTED,
    ] = Field(alias="action")
    object: AssessmentItemModel | str = Field(alias="object")
    generated: ResponseModel | str = Field(
        default=None,
        alias="generated",
        description="For a completed action a generated Response or a subtype.",
    )
    referrer: AssessmentItemModel | str = Field(
        default=None,
        alias="referrer",
        description="The previous AssessmentItem attempted MAY be specified as the referrer.",
    )


class AssignableEventModel(EventPersonModel):
    type: Literal[TypeTermEnum.ASSIGNABLEEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.ASSIGNABLEEVENT.value],
    )
    action: Literal[
        ActionTermEnum.ACTIVATED,
        ActionTermEnum.COMPLETED,
        ActionTermEnum.DEACTIVATED,
        ActionTermEnum.REVIEWED,
        ActionTermEnum.STARTED,
        ActionTermEnum.SUBMITTED,
    ] = Field(alias="action")
    object: AssignableDigitalResourceModel | AttemptModel | str = Field(
        alias="object",
        description="The AssignableDigitalResource that constitutes the object of the interaction.",
    )
    target: FrameModel | str = Field(
        default=None,
        alias="target",
        description="A Frame that represents a particular segment or location within the object.",
    )
    generated: AttemptModel | str = Field(
        default=None,
        alias="generated",
        description="For Started, Completed and Reviewed actions, the actor's Attempt SHOULD be specified.",
    )


class ForumEventModel(EventPersonModel):
    type: Literal[TypeTermEnum.FORUMEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.FORUMEVENT.value],
    )
    action: Literal[
        ActionTermEnum.SUBSCRIBED,
        ActionTermEnum.UNSUBSCRIBED,
    ] = Field(alias="action")
    object: ForumModel | str = Field(
        alias="object",
        description="The Forum that comprises the object of this interaction.",
    )


class GradeEventModel(EventModel):
    type: Literal[TypeTermEnum.GRADEEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.GRADEEVENT.value],
    )
    action: Literal[ActionTermEnum.GRADED,] = Field(alias="action")
    object: AttemptModel | str = Field(
        alias="object",
        description="The completed Attempt.",
    )
    generated: ScoreModel | str = Field(
        default=None,
        alias="generated",
        description="The generated Score SHOULD be provided.",
    )


class MediaEventModel(EventPersonModel):
    type: Literal[TypeTermEnum.MEDIAEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.MEDIAEVENT.value],
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
    ] = Field(alias="action")
    object: MediaObjectModel | str = Field(alias="object")
    target: MediaLocationModel | str = Field(
        default=None,
        alias="target",
        description="If the MediaEvent object is an AudioObject or VideoObject, a MediaLocation SHOULD be specified in order to provide the currentTime in the audio or video stream that marks the action. If the currentTime is specified, the value MUST be an ISO 8601 formatted duration, e.g., 'PT30M54S'.",
    )


class MessageEventModel(EventPersonModel):
    type: Literal[TypeTermEnum.MESSAGEEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.MESSAGEEVENT.value],
    )
    action: Literal[
        ActionTermEnum.MARKEDASREAD,
        ActionTermEnum.MARKEDASUNREAD,
        ActionTermEnum.POSTED,
    ] = Field(alias="action")
    object: MessageModel | str = Field(alias="object")


class NavigationEventModel(EventModel):
    type: Literal[TypeTermEnum.NAVIGATIONEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.NAVIGATIONEVENT.value],
    )
    actor: PersonModel | SoftwareApplicationModel | str = Field(alias="actor")
    action: Literal[ActionTermEnum.NAVIGATEDTO,] = Field(alias="action")
    object: DigitalResourceModel | EntityModel | SoftwareApplicationModel | str = (
        Field(
            alias="object",
            description="The DigitalResource or SoftwareApplication to which the actor navigated.",
        )
    )
    target: FrameModel | str = Field(
        default=None,
        alias="target",
        description="The DigitalResource that represents the particular part or location of the object being navigated to.",
    )
    referrer: DigitalResourceModel | SoftwareApplicationModel | str = Field(
        default=None,
        alias="referrer",
        description="The DigitalResource or SoftwareApplication that constitutes the referring context.",
    )
    # DEPRECATED
    navigated_from: DigitalResourceModel | SoftwareApplicationModel = Field(
        default=None,
        alias="navigatedFrom",
        description="navigatedFrom has been DEPRECATED and replaced by referrer.",
        json_schema_extra={"deprecated": True},
    )


# DeprecationWarning
class OutcomeEventModel(EventModel):
    type: Literal[TypeTermEnum.OUTCOMEEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.OUTCOMEEVENT.value],
    )
    action: Literal[ActionTermEnum.GRADED,] = Field(alias="action")
    object: AttemptModel | str = Field(
        alias="object",
        description="The completed Attempt.",
    )
    generated: ResultModel | str = Field(
        default=None,
        alias="generated",
        description="The generated Result SHOULD be provided.",
    )


# DeprecationWarning
class ReadingEventModel(EventPersonModel):
    type: Literal[TypeTermEnum.READINGEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.READINGEVENT.value],
    )
    action: Literal[
        ActionTermEnum.NAVIGATEDTO,
        ActionTermEnum.SEARCHED,
        ActionTermEnum.VIEWED,
    ] = Field(alias="action")
    object: DigitalResourceModel | str = Field(alias="object")
    target: FrameModel | str = Field(default=None, alias="target")


class SessionEventModel(EventModel):
    type: Literal[TypeTermEnum.SESSIONEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.SESSIONEVENT.value],
    )
    actor: PersonModel | SoftwareApplicationModel | str = Field(
        alias="actor",
        description="The Agent who initiated the action. For LoggedIn and LoggedOut actions a Person MUST be specified as the actor. For a TimedOut action a SoftwareApplication MUST be specified as the actor.",
    )
    action: Literal[
        ActionTermEnum.LOGGEDIN,
        ActionTermEnum.LOGGEDOUT,
        ActionTermEnum.TIMEDOUT,
    ] = Field(alias="action")
    object: SessionModel | SoftwareApplicationModel | str = Field(
        alias="object",
        description="For LoggedIn and LoggedOut actions a SoftwareApplication MUST be specified as the object. For a TimedOut action the Session MUST be specified as the object.",
    )
    target: DigitalResourceModel | str = Field(
        default=None,
        alias="target",
        description="When logging in to a SoftwareApplication, if the actor is attempting to access a particular DigitalResource it MAY be designated as the target of the interaction.",
    )
    referrer: DigitalResourceModel | SoftwareApplicationModel | str = Field(
        default=None,
        alias="referrer",
        description="The DigitalResource or SoftwareApplication that constitutes the referring context MAY be specified as the referrer.",
    )


class ThreadEventModel(EventPersonModel):
    type: Literal[TypeTermEnum.THREADEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.THREADEVENT.value],
    )
    action: Literal[
        ActionTermEnum.CREATED,
        ActionTermEnum.MARKEDASREAD,
        ActionTermEnum.MARKEDASUNREAD,
    ] = Field(alias="action")
    object: ThreadModel | str = Field(
        alias="object",
        description="The Thread that constitutes the object of the interaction.",
    )


class ToolUseEventModel(EventPersonModel):
    type: Literal[TypeTermEnum.TOOLUSEEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.TOOLUSEEVENT.value],
    )
    action: Literal[ActionTermEnum.USED,] = Field(alias="action")
    object: SoftwareApplicationModel | str = Field(alias="object")
    target: SoftwareApplicationModel | str = Field(default=None, alias="target")


class ViewEventModel(EventPersonModel):
    type: Literal[TypeTermEnum.VIEWEVENT] = Field(
        alias="type",
        examples=[TypeTermEnum.VIEWEVENT.value],
    )
    action: Literal[ActionTermEnum.VIEWED,] = Field(alias="action")
    object: DigitalResourceModel | str = Field(
        alias="object",
        description="The DigitalResource that the actor viewed.",
    )
    target: FrameModel | str = Field(default=None, alias="target")


################################################
##################### MAIN #####################
################################################
class IMSCaliperModel(BaseModel):
    data: list[EntityModel | EventModel] = Field(alias="data")
    data_version: str = Field(
        alias="dataVersion", examples=["http://purl.imsglobal.org/ctx/caliper/v1p1"],
    )
    send_time: str = Field(alias="sendTime", examples=["2019-11-16T02:08:59.163Z"])
    sensor: str = Field(alias="sensor", examples=["http://oxana.instructure.com/"])

    @field_validator("data", mode="before")
    @classmethod
    def validation(
        cls, value: list[EventModel], extra_info: ValidationInfo,
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
            extra_info.field_name if extra_info.field_name else "", None,
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
                            each_value.get("type", ""), None,
                        )
                    ):
                        model_value = event_model(**each_value)
                    new_value.append(model_value)
                return new_value

        return value
