from fastapi import APIRouter, Depends, Request

from app.mapper.mapper import Mapper
from app.profile_enricher.profiler import Profiler

from ..dependencies import get_mapper, get_profiler
from ..schemas import (
    TransformInputTraceRequestModel,
    TransformInputTraceResponseMetaModel,
    TransformInputTraceResponseModel,
    ValidateInputTraceRequestModel,
    ValidateInputTraceResponseModel,
)

router = APIRouter()


@router.post(
    "/validate",
    response_model=ValidateInputTraceResponseModel,
    tags=["Trace validation"],
    description="Validate an input trace. If a trace format is provided, it will check only that format. Otherwise, it will attempt to detect the format.",
    status_code=200,
)
async def validate_input_trace(
    query: ValidateInputTraceRequestModel,
) -> ValidateInputTraceResponseModel:
    """
    Validate or identify a trace.

    ---
    post:
      summary: Validate input trace
      description: Validate an input trace and identify its format.
      requestBody:
        required: true
        content:
          application/json:
            schema: ValidateInputTraceRequestModel
      responses:
        200:
          description: Successfully validated trace
          content:
            application/json:
              schema: ValidateInputTraceResponseModel
        400:
          description: Bad request, input format does not match the trace

    :param query: The request query model
    :return: The response model indicating the validated input format
    :raises ValueError: If the input format does not match the trace
    """
    input_trace = query.get_trace()
    return ValidateInputTraceResponseModel(input_format=input_trace.format)


@router.post(
    "/convert",
    response_model=TransformInputTraceResponseModel,
    tags=["Trace transformation"],
    description="Transform an input trace into a specific output trace.",
    status_code=200,
)
async def transform_input_trace(
    request: Request,
    query: TransformInputTraceRequestModel,
    mapper: Mapper = Depends(get_mapper),
    profiler: Profiler = Depends(get_profiler),
) -> TransformInputTraceResponseModel:
    """
    Transform and enrich a trace from one format to another.

    ---
    post:
      summary: Transform input trace
      description: Transform an input trace into a specific output format and enrich it with profile data if available.
      requestBody:
        required: true
        content:
          application/json:
            schema: TransformInputTraceRequestModel
      responses:
        200:
          description: Successfully transformed trace
          content:
            application/json:
              schema: TransformInputTraceResponseModel
        400:
          description: Bad request, invalid input trace or format
        500:
          description: Internal server error, transformation failed

    :param request: The FastAPI request object
    :param query: The request query model
    :param mapper: The Mapper instance for trace conversion
    :param profiler: The Profiler instance for trace enrichment and validation
    :return: The response model containing the transformed trace
    :raises ValueError: If the trace does not match the profile
    """
    logger = request.state.logger
    logger.info("Convert endpoint called", {"input_format": query.input_format})

    input_trace = query.get_trace()

    # Convert
    output_trace = mapper.convert(
        input_trace=input_trace,
        output_format=query.output_format,
    )
    # Enrich and validate
    recommendations = []
    if output_trace.profile:
        profiler.enrich_trace(trace=output_trace)

        errors = profiler.validate_trace(trace=output_trace)
        if errors:
            raise ValueError(f"The trace does not match the profile: {errors}")

        recommendations = profiler.get_recommendations(
            trace=output_trace,
        )

    meta = TransformInputTraceResponseMetaModel(
        input_format=input_trace.format,
        recommendations=recommendations,
    )

    logger.info("Convert endpoint completed", {"input_format": input_trace.format})
    return TransformInputTraceResponseModel(output_trace=output_trace.data, meta=meta)
