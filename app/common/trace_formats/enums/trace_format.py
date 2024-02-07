from enum import Enum, StrEnum

from trace_formats.models import BaseXapiStatement, SCORMDataModel


class TraceFormatEnum(Enum):
    pass


class TraceFormatModelEnum(TraceFormatEnum):
    SCORM_1_1 = SCORMDataModel
    XAPI = BaseXapiStatement


class TraceFormatToXapiMappingEnum(TraceFormatEnum):
    SCORM_1_1 = "app/common/trace_formats/mappers/mapping_scorm_1_1_to_xapi.yml"
    XAPI = ""


class TraceFormatToScorm11MappingEnum(TraceFormatEnum):
    SCORM_1_1 = ""
    XAPI = "app/common/trace_formats/mappers/mapping_xapi_to_scorm_1_1.yml"


class TraceFormatOutputMappingEnum(TraceFormatEnum):
    SCORM_1_1 = TraceFormatToScorm11MappingEnum
    XAPI = TraceFormatToXapiMappingEnum
