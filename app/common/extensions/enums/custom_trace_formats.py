"""
Use this file to add additional mapping formats
"""

from app.common.utils.utils_enum import CaseInsensitiveStrEnum, extend_enum, str_enum
from enums import TraceFormatEnum, TraceFormatModelEnum, TraceFormatOutputMappingEnum


@extend_enum(TraceFormatModelEnum, enum_class=TraceFormatEnum)
class CustomTraceFormatModelEnum(TraceFormatEnum):
    """All Trace format models"""

    # FAKE_SCORM = FakeScormModel
    # FAKE_XAPI = FakeXapiModel


class TraceFormatToFakeXapiMappingEnum(TraceFormatEnum):
    """All mappings to transform a trace format into `fake_xapi`"""

    # FAKE_SCORM = "data/mappers/mapping_example_fake_scorm_to_fake_xapi.yml"


@extend_enum(TraceFormatOutputMappingEnum, enum_class=TraceFormatEnum)
class CustomTraceFormatOutputMappingEnum(TraceFormatEnum):
    """All Output Format Enums that regroups the mapping for each input"""

    # FAKE_XAPI = TraceFormatToFakeXapiMappingEnum


class CaseInsensitiveStrTraceFormatEnum(TraceFormatEnum, CaseInsensitiveStrEnum):
    """Inherit TraceFormatEnum and CaseInsensitiveStrEnum for typing"""


@str_enum(CustomTraceFormatModelEnum, enum_class=CaseInsensitiveStrTraceFormatEnum)
class CustomTraceFormatStrEnum(TraceFormatEnum):
    """
    All trace format stringed name
    CAUTION : DO NOT MODIFY IF NOT NEEDED. This Enum is automatically filled
    """
