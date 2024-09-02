from enum import Enum

from trace_formats.models import (BaseXapiStatement, IMSCaliperSensorModel1_1,
                                  IMSCaliperSensorModel1_2, SCORM2004DataModel,
                                  SCORMDataModel)


class TraceFormatEnum(Enum):
    pass


class TraceFormatModelEnum(TraceFormatEnum):
    SCORM_1_1 = SCORMDataModel
    SCORM_2004 = SCORM2004DataModel
    XAPI = BaseXapiStatement
    IMSCALIPER1_2 = IMSCaliperSensorModel1_2
    IMSCALIPER1_1 = IMSCaliperSensorModel1_1


class TraceFormatToXapiMappingEnum(TraceFormatEnum):
    SCORM_1_1 = "data/mappers/mapping_scorm_1_1_to_xapi.yml"
    SCORM_2004 = "data/mappers/mapping_scorm2004_to_xapi.yml"
    XAPI = ""
    IMSCALIPER1_2 = "data/mappers/mapping_imscaliper_1_1_to_xapi.yml"
    IMSCALIPER1_1 = "data/mappers/mapping_imscaliper_1_1_to_xapi.yml"


class TraceFormatToScorm11MappingEnum(TraceFormatEnum):
    SCORM_1_1 = ""
    XAPI = "data/mappers/mapping_xapi_to_scorm_1_1.yml"


class TraceFormatOutputMappingEnum(TraceFormatEnum):
    SCORM_1_1 = TraceFormatToScorm11MappingEnum
    XAPI = TraceFormatToXapiMappingEnum
