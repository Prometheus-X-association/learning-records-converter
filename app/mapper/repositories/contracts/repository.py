from abc import ABC, abstractmethod

from app.common.enums import CustomTraceFormatStrEnum
from app.common.models.trace import Trace


class MappingRepository(ABC):
    """
    An abstract base class defining the interface for mapper repositories.
    """

    @abstractmethod
    def convert(
        self, input_trace: Trace, output_format: CustomTraceFormatStrEnum
    ) -> Trace:
        """
        Convert an input trace to the specified output format.

        :param input_trace: The input trace to be converted
        :param output_format: The desired output format for the trace
        :return: The converted trace
        """
        ...
