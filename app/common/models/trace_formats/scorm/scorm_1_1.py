from enum import StrEnum
from typing import List, Optional

from pydantic import BaseModel, Field


# Enums for SCORM 1.1
class Credit(StrEnum):
    CREDIT = "credit"
    NO_CREDIT = "no-credit"


class LessonStatus(StrEnum):
    PASSED = "passed"
    COMPLETED = "completed"
    FAILED = "failed"
    INCOMPLETE = "incomplete"
    BROWSED = "browsed"
    NOT_ATTEMPTED = "not attempted"


class Entry(StrEnum):
    AB_INITIO = "ab-initio"
    RESUME = ""


class LessonMode(StrEnum):
    BROWSE = "browse"
    NORMAL = "normal"
    REVIEW = "review"


class ExitMode(StrEnum):
    TIME_OUT = "time-out"
    SUSPEND = "suspend"
    LOGOUT = "logout"
    EMPTY = ""


class InteractionType(StrEnum):
    TRUE_FALSE = "true-false"
    CHOICE = "choice"
    FILL_IN = "fill-in"
    MATCHING = "matching"
    PERFORMANCE = "performance"
    SEQUENCING = "sequencing"
    LIKERT = "likert"
    NUMERIC = "numeric"


# SCORM 1.1 Data Model Elements
class CMIScore(BaseModel):
    raw: Optional[float] = Field(
        None, title="Raw Score", description="Reflects the performance of the learner."
    )
    max: Optional[float] = Field(
        None,
        title="Maximum Score",
        description="Maximum value in the range for the raw score.",
    )
    min: Optional[float] = Field(
        None,
        title="Minimum Score",
        description="Minimum value in the range for the raw score.",
    )


class CMIObjective(BaseModel):
    id: str = Field(
        ..., title="Objective ID", description="Unique label for the objective."
    )
    score: CMIScore = Field(
        ..., title="Objective Score", description="Score related to the objective."
    )
    status: LessonStatus = Field(
        ..., title="Objective Status", description="Completion status of the objective."
    )


class CMIInteraction(BaseModel):
    id: str = Field(
        ..., title="Interaction ID", description="Unique label for the interaction."
    )
    time: str = Field(..., title="Interaction Time", description="Time of interaction.")
    type: InteractionType = Field(
        ..., title="Interaction Type", description="Type of interaction."
    )
    correct_responses: List[str] = Field(
        ..., title="Correct Responses", description="List of correct responses."
    )
    weighting: float = Field(
        ..., title="Weighting", description="Weight of the interaction."
    )
    student_response: str = Field(
        ..., title="Student Response", description="Response given by the student."
    )
    result: str = Field(
        ...,
        title="Result",
        description="Judgment of the correctness of the learner response.",
    )
    latency: str = Field(
        ..., title="Latency", description="Time taken for the response."
    )


# SCORM 1.1 Main Data Model
class SCORMDataModel(BaseModel):
    student_id: str = Field(
        ..., max_length=255, title="Student ID", description="Identifies the student."
    )
    student_name: str = Field(
        ..., max_length=255, title="Student Name", description="Name of the student."
    )
    lesson_location: str = Field(
        ...,
        max_length=255,
        title="Lesson Location",
        description="Current location in the SCO.",
    )
    credit: Credit = Field(
        ..., title="Credit", description="Indicates if credit is given for SCO."
    )
    lesson_status: LessonStatus = Field(
        ..., title="Lesson Status", description="Completion status of the SCO."
    )
    entry: Entry = Field(..., title="Entry", description="Entry status of the learner.")
    score: CMIScore = Field(..., title="Score", description="Score of the learner.")
    total_time: str = Field(
        ..., title="Total Time", description="Total time spent by the learner."
    )
    lesson_mode: LessonMode = Field(
        ..., title="Lesson Mode", description="Mode of the lesson."
    )
    exit: ExitMode = Field(
        ..., title="Exit Mode", description="How or why the learner exited the SCO."
    )
    session_time: str = Field(
        ..., title="Session Time", description="Time spent in the current session."
    )
    suspend_data: str = Field(
        ...,
        max_length=4096,
        title="Suspend Data",
        description="Data stored between sessions.",
    )
    launch_data: str = Field(
        ...,
        max_length=4096,
        title="Launch Data",
        description="Data provided upon launch.",
    )
    comments: str = Field(
        ..., max_length=4096, title="Comments", description="Comments from the learner."
    )
    comments_from_lms: str = Field(
        ...,
        max_length=4096,
        title="Comments from LMS",
        description="Comments from the LMS.",
    )
    objectives: List[CMIObjective] = Field(
        ..., title="Objectives", description="List of objectives."
    )
    objectives_count: int = Field(
        ..., title="Objectives Count", description="Number of objectives."
    )
    student_data: dict = Field(
        ..., title="Student Data", description="Data related to the student."
    )
    student_preference: dict = Field(
        ..., title="Student Preference", description="Preferences of the student."
    )
    interactions: List[CMIInteraction] = Field(
        ..., title="Interactions", description="List of interactions."
    )
    interactions_count: int = Field(
        ..., title="Interactions Count", description="Number of interactions."
    )
