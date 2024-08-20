import os

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError

from app.api.exceptions import (
    BadRequestError,
    ForbiddenError,
    InternalServerError,
    NotFoundElementError,
)
from app.api.handlers import get_format_from_trace
from app.api.schemas import (
    TransformInputTraceResponseMetaModel,
    TransformInputTraceRequestModel,
    TransformInputTraceResponseModel,
    ValidateInputTraceRequestModel,
    ValidateInputTraceResponseModel,
)
from app.profile_enricher.profiler import Profiler
from app.profile_enricher.repositories.jsonld.jsonld_repository import JsonLdProfileRepository
from app.xapi_converter.transformer.mapping_input import (
    MappingInput,
    get_mapping_by_input_and_output_format,
)
from enums.custom_trace_format import CustomTraceFormatModelEnum, CustomTraceFormatStrEnum

ROOT_PATH = ""

app = FastAPI(
    title="LRC API",
    version="0.0.1",
    servers=[
        {"url": "", "description": ""},
    ],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


def handle_trace_and_format(
    trace: dict, format: CustomTraceFormatStrEnum | None = None
) -> CustomTraceFormatModelEnum:
    """Get the pydantic model of a speific trace

    Args:
        trace (dict): Trace
        format (CustomTraceFormatStrEnum | None, optional): Trace format. Defaults to None.

    Raises:
        NotFoundElementError: No matched trace format for passed input

    Returns:
        CustomTraceFormatModelEnum: Enum element with the trace model
    """
    # Get input format if not provided
    if format is None:
        input_model = get_format_from_trace(trace)
    else:
        # Get input format model
        input_model = CustomTraceFormatModelEnum[format.name]
    # Handle empty input_model
    if input_model is None:
        raise NotFoundElementError("Input format not found from trace. Please specify one.")
    return input_model


@app.post(
    path="/convert",
    response_model=TransformInputTraceResponseModel,
    tags=["Trace transformation"],
    description="Transform a input trace into a specific output trace.",
    status_code=200,
)
def transform_input_trace(query: TransformInputTraceRequestModel):
    """Transform a trace from an format into another format

    Args:
        query (TransformInputTraceRequestModel): Request query model

    Returns:
        TransformInputTraceResponseModel: Response model
    """
    input_model = handle_trace_and_format(trace=query.input_trace, format=query.input_format)
    # Get output format model
    output_model = CustomTraceFormatModelEnum[query.output_format.name]
    # Get Mapping
    mapping_config = get_mapping_by_input_and_output_format(input_model, output_model)

    # Profile handling
    jsonld_repository = JsonLdProfileRepository(base_path=os.path.join('data', 'dases_profiles'))
    profiler = Profiler(repository=jsonld_repository)

    # Apply Mapping
    mapper = MappingInput(
        input_format=input_model, mapping_to_apply=mapping_config, output_format=output_model, profile_enricher=profiler
    )
    response = mapper.run(query.input_trace)

    # Metadata
    recommendations = mapper.get_recommendations(response)
    meta = TransformInputTraceResponseMetaModel(
        input_format=query.input_format,
        recommendations=recommendations,
    )

    # Done
    return TransformInputTraceResponseModel(output_trace=response, meta= meta)


@app.post(
    path="/validate",
    response_model=ValidateInputTraceResponseModel,
    tags=["Trace validation"],
    description="Validate an input trace. If a trace format is passed, it will only check the specific format. If no trace format is passed, it will try to detect one.",
    status_code=200,
)
def validate_input_trace(query: ValidateInputTraceRequestModel):
    """Validate or identify a trace

    Args:
        query (ValidateInputTraceRequestModel): Request Query Model

    Returns:
        ValidateInputTraceResponseModel: Response Model
    """
    input_model = handle_trace_and_format(trace=query.input_trace, format=query.input_format)
    try:
        input_model.value(**query.input_trace)
    except ValidationError as ve:
        raise BadRequestError("Input format does not match trace.")
    return ValidateInputTraceResponseModel(input_format=input_model.name)


## Exception
@app.exception_handler(ValueError)
@app.exception_handler(TypeError)
@app.exception_handler(InternalServerError)
@app.exception_handler(NotFoundElementError)
@app.exception_handler(Exception)
@app.exception_handler(BadRequestError)
@app.exception_handler(ForbiddenError)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: Exception):
    """Handles validation and request validation errors
    Errors are raised by the validations of the pieces of information given by the user

    Args:
        request (_type_): request that led to the error(s)
        exc (Exception): raised exception

    Returns:
        JSONResponse: a response containing the validation error details
    """
    print(exc)
    try:
        message = "".join(exc.args).replace("\n", "; ")
        if not message:
            message = str(exc)
    except Exception as e:
        message = str(exc).replace("\n", "; ")
    if isinstance(exc, BadRequestError):
        status_code = 400
    elif isinstance(exc, ValueError):
        status_code = 401
    elif isinstance(exc, ForbiddenError):
        status_code = 403
    elif isinstance(exc, NotFoundElementError):
        status_code = 404
    elif isinstance(exc, RequestValidationError):
        status_code = 422
    elif isinstance(exc, TypeError):
        status_code = 500
    else:
        status_code = 500
        message = "Something went wrong, please contact our support."
    return JSONResponse(
        {
            "msg": message,
        },
        status_code=status_code,
    )
