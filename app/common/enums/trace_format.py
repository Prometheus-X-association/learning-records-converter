from enum import Enum

from models.trace_format import SCORMDataModel


class TraceFormatEnum(Enum):
    # Case insensitive
    @classmethod
    def _missing_(cls, name):
        for member in cls:
            if member.name.lower().strip() == name.lower().strip():
                return member


class TraceFormatModelEnum(TraceFormatEnum):
    SCORM_1_1 = SCORMDataModel
    # XAPI = None


class TraceFormatMappingEnum(TraceFormatEnum):
    SCORM_1_1 = "chemin/vers/mapping"
    # XAPI = None
