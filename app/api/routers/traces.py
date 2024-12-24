from json import dumps
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import Json

from app.api.dependencies import get_mapper, get_profiler
from app.api.schemas import (
    DEFAULT_OUTPUT_FORMAT,
    CustomConfigModel,
    TransformInputTraceRequestModel,
    TransformInputTraceResponseMetaModel,
    TransformInputTraceResponseModel,
    ValidateInputTraceRequestModel,
    ValidateInputTraceResponseModel,
)
from app.common.extensions.enums import CustomTraceFormatStrEnum
from app.mapper.mapper import Mapper
from app.parsers.factory import ParserFactory
from app.parsers.jsonencoder import CustomJSONEncoder
from app.profile_enricher.profiler import Profiler

router = APIRouter()


@router.post(
    "/validate",
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
    tags=["Trace transformation"],
    description="Transform an input trace into a specific output trace.",
    status_code=200,
)
async def transform_input_trace(
    request: Request,
    query: TransformInputTraceRequestModel,
    mapper: Annotated[Mapper, Depends(get_mapper)],
    profiler: Annotated[Profiler, Depends(get_profiler)],
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

    mapper.load_schema_by_formats(
        input_format=input_trace.format,
        output_format=query.output_format,
    )

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
        output_format=output_trace.format,
        profile=output_trace.profile,
    )

    logger.info("Convert endpoint completed", {"input_format": input_trace.format})
    return TransformInputTraceResponseModel(
        output_trace=output_trace.data,
        meta=meta,
        recommendations=recommendations,
    )


@router.post(
    "/convert_custom",
    response_class=StreamingResponse,
    tags=["Custom transformation"],
    description="Transform a custom file using a provided mapping file and parsing configuration.",
    status_code=200,
)
async def transform_custom_file(
    request: Request,
    data_file: UploadFile,
    mapping_file: UploadFile,
    config: Json[CustomConfigModel] | None = Form(default=None),
    output_format: CustomTraceFormatStrEnum = Form(default=DEFAULT_OUTPUT_FORMAT),
    mapper: Mapper = Depends(get_mapper),
) -> StreamingResponse:
    """
    Transform a custom file using a provided mapping file and parsing configuration.
    This method processes an uploaded file, applies a custom mapping, and streams the
    transformed data as xAPI statements.
    :param request: The request object
    :param data_file: The uploaded file containing the data to be transformed
    :param mapping_file: The uploaded file containing the mapping configuration
    :param config: Optional custom configuration for parsing
    :param output_format: The desired output format for the transformation
    :param mapper: The Mapper instance for trace conversion
    :return: A streaming response containing the transformed xAPI statements
    """
    parser = ParserFactory.get_parser(
        mime_type=data_file.content_type,
        logger=request.state.logger,
        parsing_config=config,
    )

    mapper.load_schema_by_file(file=mapping_file.file)

    async def generate_xapi_statements():
        for trace in parser.parse(file=data_file.file):
            output_trace = mapper.convert(
                input_trace=trace,
                output_format=output_format,
            )
            yield dumps(obj=output_trace.data, cls=CustomJSONEncoder) + "\n"

    return StreamingResponse(
        content=generate_xapi_statements(),
        media_type="application/x-ndjson",
    )
