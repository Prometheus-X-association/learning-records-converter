from enum import StrEnum
from typing import Any, List, Optional

from pydantic import BaseModel, Field


# Enums for SCORM 2004
class Credit(StrEnum):
    CREDIT = "credit"
    NO_CREDIT = "no-credit"


class CompletionStatus(StrEnum):
    COMPLETED = "completed"
    INCOMPLETE = "incomplete"
    NOT_ATTEMPTED = "not attempted"
    UNKNOWN = "unknown"


class Entry(StrEnum):
    AB_INITIO = "ab-initio"
    RESUME = "resume"
    EMPTY = ""


class ExitMode(StrEnum):
    TIME_OUT = "timeout"
    SUSPEND = "suspend"
    LOGOUT = "logout"
    NORMAL = "normal"
    EMPTY = ""


class InteractionResult(StrEnum):
    CORRECT = "correct"
    INCORRECT = "incorrect"
    UNANTICIPATED = "unanticipated"
    NEUTRAL = "neutral"


class Mode(StrEnum):
    BROWSE = "browse"
    NORMAL = "normal"
    REVIEW = "review"


class InteractionType(StrEnum):
    TRUE_FALSE = "true-false"
    CHOICE = "choice"
    FILL_IN = "fill-in"
    LONG_FILL_IN = "long-fill-in"
    MATCHING = "matching"
    PERFORMANCE = "performance"
    SEQUENCING = "sequencing"
    LIKERT = "likert"
    NUMERIC = "numeric"
    OTHER = "other"


class LearnerAudioCaptioning(StrEnum):
    MINUS_ONE = "-1"
    ZERO = "0"
    ONE = "1"


class TimeLimitAction(StrEnum):
    EXIT_MESSAGE = "exit,message"
    CONTINUE_MESSAGE = "continue,message"
    EXIT_NOMESSAGE = "exit,no message"
    CONTINUE_NOMESSAGE = "continue,no message"


class SuccessStatus(StrEnum):
    FAILED = "failed"
    PASSED = "passed"
    UNKNOWN = "unknown"


# SCORM 2004 Data Model Elements
class CMIScore(BaseModel):
    scaled: float = Field(
        ...,
        title="Raw Score",
        description="Reflects the performance of the learner.",
        ge=0,
        le=1,
    )
    raw: float = Field(
        ..., title="Raw Score", description="Reflects the performance of the learner."
    )
    max: float = Field(
        ...,
        title="Maximum Score",
        description="Maximum value in the range for the raw score.",
    )
    min: float = Field(
        ...,
        title="Minimum Score",
        description="Minimum value in the range for the raw score.",
    )


class CMIObjectiveIDOnly(BaseModel):
    id: str = Field(
        ..., title="Objective ID", description="Unique label for the objective."
    )


class CMIObjective(CMIObjectiveIDOnly):
    score: CMIScore = Field(
        ..., title="Objective Score", description="Score related to the objective."
    )
    success_status: SuccessStatus = Field(
        ...,
        title="Objective success Status",
        description="Success status of the objective.",
    )
    completion_status: CompletionStatus = Field(
        ...,
        title="Objective completion Status",
        description="Completion status of the objective.",
    )
    progress_measure: float = Field(
        ...,
        title="Objective Progress Measure",
        description="Measure of the learner's progress.",
        ge=0,
        le=1,
    )
    description: str = Field(
        ...,
        max_length=250,
        title="Description",
        description="Description of the objective.",
    )


class CMICorrectResponses(BaseModel):
    pattern: Any = Field(..., title="Pattern", description="Correct responses pattern.")


class CMIInteraction(BaseModel):
    id: str = Field(
        ...,
        max_length=4000,
        title="Interaction ID",
        description="Unique label for the interaction.",
    )
    type: InteractionType = Field(
        ..., title="Interaction Type", description="Type of interaction."
    )
    objectives: List[CMIObjectiveIDOnly] = Field(
        ..., title="Objectives", description="List of objectives."
    )
    timestamp: int = Field(
        ..., title="Interaction Time", description="Time of interaction."
    )
    correct_responses: List[CMICorrectResponses] = Field(
        ..., title="Correct Responses", description="List of correct responses."
    )
    weighting: float = Field(
        ..., title="Weighting", description="Weight of the interaction."
    )
    learner_response: Any = Field(
        ..., title="Learner Response", description="Response given by the learner."
    )
    result: InteractionResult = Field(
        ...,
        title="Result",
        description="Judgment of the correctness of the learner response.",
    )
    latency: float = Field(
        ...,
        title="Latency",
        description="Time taken for the response (timeinterval(second,10,2)).",
    )
    description: str = Field(
        ...,
        max_length=250,
        title="Description",
        description="Description of the interaction.",
    )


class CMIComments(BaseModel):
    comment: str = Field(..., max_length=4000, title="Comment", description="Comment.")
    location: str = Field(
        ..., max_length=250, title="Location", description="Location of the comment."
    )
    timestamp: int = Field(
        ..., title="Timestamp", description="Time of the comment (time(second,10,0))."
    )


class CMICommentsFromLearner(CMIComments): ...


class CMICommentsFromLMS(CMIComments): ...


class LearnerPreference(BaseModel):
    audio_level: float = Field(
        ..., title="Audio Level", description="Audio level preference.", ge=0
    )
    language: str = Field(
        ..., max_length=250, title="Language", description="Language preference."
    )
    delivery_speed: float = Field(
        ..., title="Delivery Speed", description="Delivery speed preference.", ge=0
    )
    audio_captioning: LearnerAudioCaptioning = Field(
        ..., title="Audio Captioning", description="Audio captioning preference."
    )


# SCORM 2004 Main Data Model
class SCORM2004DataModel(BaseModel):
    comments_from_learner: Optional[CMICommentsFromLearner] = Field(
        None, title="Comments from Learner", description="Comments from the learner."
    )
    comments_from_lms: Optional[CMICommentsFromLMS] = Field(
        None, title="Comments from LMS", description="Comments from the LMS."
    )
    completion_status: Optional[CompletionStatus] = Field(
        None, title="Completion Status", description="Completion status of the SCO."
    )
    completion_threshold: Optional[float] = Field(
        None,
        title="Completion Threshold",
        description="Minimum scaled score required for completion.",
        ge=0,
        le=1,
    )
    credit: Optional[Credit] = Field(
        None, title="Credit", description="Indicates if credit is given for SCO."
    )
    entry: Optional[Entry] = Field(
        None, title="Entry", description="Entry status of the learner."
    )
    exit: Optional[ExitMode] = Field(
        None, title="Exit Mode", description="How or why the learner exited the SCO."
    )
    interactions: Optional[List[CMIInteraction]] = Field(
        None, title="Interactions", description="List of interactions."
    )
    launch_data: Optional[str] = Field(
        None,
        max_length=4000,
        title="Launch Data",
        description="Data provided upon launch.",
    )
    learner_id: Optional[str] = Field(
        None, max_length=4000, title="Learner ID", description="Identifies the learner."
    )
    learner_name: Optional[str] = Field(
        None, max_length=250, title="Learner Name", description="Name of the learner."
    )
    learner_preference: Optional[LearnerPreference] = Field(
        None, title="Learner Preference", description="Preferences of the learner."
    )
    location: Optional[str] = Field(
        None,
        max_length=1000,
        title="Location",
        description="Learner's current location in the SCO.",
    )
    max_time_allowed: Optional[float] = Field(
        None,
        title="Max Time Allowed",
        description="Maximum time allowed for the SCO (timeinterval(second, 10, 2)).",
    )
    mode: Mode = Field(None, title="Mode", description="Mode.")
    objectives: Optional[List[CMIObjective]] = Field(
        None, title="Objectives", description="List of objectives."
    )
    progress_measure: Optional[float] = Field(
        None,
        title="Progress Measure",
        description="Measure of the learner's progress.",
        ge=0,
        le=1,
    )
    scaled_passing_score: Optional[float] = Field(
        None,
        title="Scaled Passing Score",
        description="Scaled score required for passing.",
        ge=-1,
        le=1,
    )
    score: Optional[CMIScore] = Field(
        None, title="Score", description="Score of the learner."
    )
    session_time: Optional[float] = Field(
        None,
        title="Session Time",
        description="Time spent in the current session (timeinterval(second,10,2)).",
    )
    success_status: Optional[SuccessStatus] = Field(
        None, title="Success Status", description="Completion status of the SCO."
    )
    suspend_data: Optional[str] = Field(
        None,
        max_length=64000,
        title="Suspend Data",
        description="Data stored between sessions.",
    )
    time_limit_action: Optional[TimeLimitAction] = Field(
        None,
        max_length=250,
        title="Time Limit Action",
        description="Action to take when time limit is reached.",
    )
    total_time: Optional[float] = Field(
        None,
        title="Total Time",
        description="Total time spent by the learner (timeinterval(second,10,2)).",
    )

    class Config:
        extra = "forbid"
        use_enum_values = True
        populate_by_name = True
