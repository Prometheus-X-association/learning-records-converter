from typing import Optional

from app.common.enums import CustomTraceFormatStrEnum
from app.common.models.trace import Trace
from app.mapper.repositories.contracts.repository import MappingRepository
from app.profile_enricher.profiler import Profiler


class Mapper:
    """
    A class for converting traces between different formats and enriching them with profile information.

    This class uses a repository for conversion and an optional profile enricher to enhance and validate traces.

    :param repository: An instance of MappingRepository for trace conversion
    :param profile_enricher: An optional instance of Profiler for trace enrichment and validation
    """

    def __init__(
        self,
        repository: MappingRepository,
        profile_enricher: Optional[Profiler] = None,
    ):
        self.repository = repository
        self.profile_enricher = profile_enricher

    def convert(
        self, input_trace: Trace, output_format: CustomTraceFormatStrEnum
    ) -> Trace:
        """
        Convert an input trace to the specified output format and optionally enrich it.

        :param input_trace: The input trace to be converted
        :param output_format: The desired output format for the trace
        :return: The converted (and possibly enriched) trace
        :raises ValueError: If the converted trace does not match the profile
        """
        # Convert
        converted_trace = self.repository.convert(
            input_trace=input_trace, output_format=output_format
        )

        # Enrich and validate
        if self.profile_enricher and converted_trace.profile:
            self.profile_enricher.enrich_trace(trace=converted_trace)

            errors = self.profile_enricher.validate_trace(
                trace=converted_trace,
            )
            if errors:
                raise ValueError(f"The trace does not match the profile: {errors}")

        return converted_trace
