"""
CAUTION : DO NOT MODIFY.

Use app/extension/enums/custom_trace_formats.py if you need to add additional mapping formats.
"""

from enum import Enum

from models.trace_formats import (
    BaseXapiStatement,
    IMSCaliperSensorModel1_1,
    IMSCaliperSensorModel1_2,
    SCORM2004DataModel,
    CustomDataModel,
)


class TraceFormatEnum(Enum):
    """Base enumeration for trace formats."""


class TraceFormatModelEnum(TraceFormatEnum):
    """Enumeration mapping trace formats to their model classes."""

    SCORM_2004 = SCORM2004DataModel
    XAPI = BaseXapiStatement
    IMSCALIPER1_2 = IMSCaliperSensorModel1_2
    IMSCALIPER1_1 = IMSCaliperSensorModel1_1
    CUSTOM = CustomDataModel


class TraceFormatToXapiMappingEnum(TraceFormatEnum):
    """Enumeration for mapping files from various formats to xAPI."""

    SCORM_2004 = "data/mappers/mapping_scorm2004_to_xapi.yml"
    XAPI = "data/mappers/mapping_xapi_to_xapi.yml"
    IMSCALIPER1_2 = "data/mappers/mapping_imscaliper_1_1_to_xapi.yml"
    IMSCALIPER1_1 = "data/mappers/mapping_imscaliper_1_1_to_xapi.yml"


class TraceFormatOutputMappingEnum(TraceFormatEnum):
    """Enumeration for output mapping options."""

    XAPI = TraceFormatToXapiMappingEnum
