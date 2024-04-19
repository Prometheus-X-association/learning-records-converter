from enums.custom_trace_format import CustomTraceFormatModelEnum
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.exceptions import (
    BadRequestError,
    ForbiddenError,
    InternalServerError,
    NotFoundElementError,
)
from app.api.handlers import get_format_from_trace
from app.api.schemas import TransformInputTraceRequestModel, TransformInputTraceResponseModel
from app.xapi_converter.transformer.mapping_input import (
    MappingInput,
    get_mapping_by_input_and_output_format,
)

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


@app.post(
    path="/convert",
    response_model=TransformInputTraceResponseModel,
    tags=["Trace transformation"],
    description="Transform a input trace into a specific output trace.",
    status_code=200,
)
def transform_input_trace(query: TransformInputTraceRequestModel):
    # Get input format if not provided
    if query.input_format is None:
        input_model = get_format_from_trace(query.input_trace)
        if input_model is None:
            raise NotFoundElementError("Input format not found from trace. Please specify one.")
    else:
        # Get input format model
        input_model = CustomTraceFormatModelEnum[query.input_format.name]

    # Get output format model
    output_model = CustomTraceFormatModelEnum[query.output_format.name]
    # Get Mapping
    mapping_config = get_mapping_by_input_and_output_format(input_model, output_model)
    # Apply Mapping
    mapper = MappingInput(
        input_format=input_model,
        mapping_to_apply=mapping_config,
        output_format=output_model,
    )
    response = mapper.run(query.input_trace)
    # Done
    return TransformInputTraceResponseModel(output_trace=response)


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
