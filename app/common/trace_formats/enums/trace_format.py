from enum import Enum, StrEnum

from trace_formats.models import BaseXapiStatement, SCORM2004DataModel, SCORMDataModel


class TraceFormatEnum(Enum):
    pass


class TraceFormatModelEnum(TraceFormatEnum):
    SCORM_1_1 = SCORMDataModel
    SCORM_2004 = SCORM2004DataModel
    XAPI = BaseXapiStatement


class TraceFormatToXapiMappingEnum(TraceFormatEnum):
    SCORM_1_1 = "app/common/trace_formats/mappers/mapping_scorm_1_1_to_xapi.yml"
    SCORM_2004 = "app/common/trace_formats/mappers/mapping_scorm2004_to_xapi.yml"
    XAPI = ""


class TraceFormatToScorm11MappingEnum(TraceFormatEnum):
    SCORM_1_1 = ""
    XAPI = "app/common/trace_formats/mappers/mapping_xapi_to_scorm_1_1.yml"


class TraceFormatOutputMappingEnum(TraceFormatEnum):
    SCORM_1_1 = TraceFormatToScorm11MappingEnum
    XAPI = TraceFormatToXapiMappingEnum
