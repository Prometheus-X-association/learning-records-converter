from fastapi import APIRouter, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.exceptions import (BadRequestError, ForbiddenError, InternalServerError,
                                NotFoundElementError)
from app.api.schemas import (TransformInputTraceRequestModel,
                             TransformInputTraceResponseMetaModel,
                             TransformInputTraceResponseModel,
                             ValidateInputTraceRequestModel,
                             ValidateInputTraceResponseModel)
from app.infrastructure.config.contract import ConfigContract
from app.infrastructure.config.envconfig import EnvConfig
from app.infrastructure.logging.contract import LoggerContract
from app.infrastructure.logging.jsonlogger import JsonLogger
from app.mapper.mapper import Mapper
from app.mapper.repositories.yaml.yaml_repository import YamlMappingRepository
from app.profile_enricher.profiler import Profiler
from app.profile_enricher.repositories.jsonld.jsonld_repository import \
    JsonLdProfileRepository


class LRCAPIRouter:
    def __init__(self, config: ConfigContract, logger: LoggerContract):
        self.config = config
        self.logger = logger
        self.router = APIRouter()
        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route(
            "/validate",
            self.validate_input_trace,
            methods=["POST"],
            response_model=ValidateInputTraceResponseModel,
            tags=["Trace validation"],
            description="Validate an input trace. If a trace format is provided, it will check only that format. Otherwise, it will attempt to detect the format.",
            status_code=200,
        )

        self.router.add_api_route(
            "/convert",
            self.transform_input_trace,
            methods=["POST"],
            response_model=TransformInputTraceResponseModel,
            tags=["Trace transformation"],
            description="Transform an input trace into a specific output trace.",
            status_code=200,
        )

    async def validate_input_trace(
        self,
        query: ValidateInputTraceRequestModel,
    ) -> ValidateInputTraceResponseModel:
        """
        Validate or identify a trace.

        :param query: The request query model
        :return: The response model indicating the validated input format
        :raises BadRequestError: If the input format does not match the trace
        """
        try:
            input_trace = query.get_trace()
            return ValidateInputTraceResponseModel(input_format=input_trace.format)
        except ValueError as e:
            raise BadRequestError(str(e))

    async def transform_input_trace(
        self, query: TransformInputTraceRequestModel
    ) -> TransformInputTraceResponseModel:
        """
        Transform and enrich a trace from one format to another.

        :param query: The request query model
        :return: The response model containing the transformed trace
        """
        self.logger.info(
            "Convert endpoint called", {"input_format": query.input_format}
        )

        input_trace = query.get_trace()

        mapper = Mapper(
            repository=YamlMappingRepository(logger=self.logger),
        )

        # Convert
        output_trace = mapper.convert(
            input_trace=input_trace,
            output_format=query.output_format,
        )
        # Enrich and validate
        recommendations = []
        if output_trace.profile:
            profiler = Profiler(
                repository=JsonLdProfileRepository(
                    logger=self.logger, config=self.config
                )
            )
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

        self.logger.info(
            "Convert endpoint completed", {"input_format": input_trace.format}
        )
        return TransformInputTraceResponseModel(
            output_trace=output_trace.data, meta=meta
        )


def create_app() -> FastAPI:
    config = EnvConfig()
    logger = JsonLogger(name=__name__, level=config.get_log_level())
    logger.info("Application starting")

    app = FastAPI(
        title="LRC API",
        version="0.0.1",
        servers=[{"url": "", "description": ""}],
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.get_cors_allowed_origins(),
        allow_methods=["POST"],
        allow_headers=["*"],
        allow_credentials=True,
        max_age=600,
    )

    lrc_router = LRCAPIRouter(config=config, logger=logger)
    app.include_router(router=lrc_router.router)

    @app.exception_handler(RequestValidationError)
    @app.exception_handler(ValueError)
    @app.exception_handler(TypeError)
    @app.exception_handler(BadRequestError)
    @app.exception_handler(ForbiddenError)
    @app.exception_handler(NotFoundElementError)
    @app.exception_handler(InternalServerError)
    async def known_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """
        Handle known exceptions and return appropriate JSON responses.

        :param request: The request that caused the exception
        :param exc: The exception that was raised
        :return: A JSON response containing error details
        """
        error_mapping = {
            BadRequestError: (400, "Bad Request"),
            ValueError: (401, "Unauthorized"),
            ForbiddenError: (403, "Forbidden"),
            NotFoundElementError: (404, "Not Found"),
            RequestValidationError: (422, "Unprocessable Entity"),
            TypeError: (500, "Internal Server Error"),
            InternalServerError: (500, "Internal Server Error"),
        }

        exc_type = type(exc)
        status_code, error_type = error_mapping.get(
            exc_type, (500, "Internal Server Error")
        )

        if status_code == 500 and exc_type not in (TypeError, InternalServerError):
            message = "Something went wrong, please contact our support."
        else:
            message = "; ".join(exc.args) if exc.args else str(exc)

        logger.exception(
            "HTTP Error sent",
            exc,
            {
                "message": message,
                "status_code": status_code,
            },
        )
        return JSONResponse({"msg": message}, status_code=status_code)

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """
        Global exception handler for unhandled exceptions.

        :param request: The request that caused the exception
        :param exc: The unhandled exception
        :return: A JSON response indicating an internal server error
        """
        logger.exception("Unhandled exception", exc)
        return JSONResponse(
            {"msg": "An unexpected error occurred. Please contact support."},
            status_code=500,
        )

    return app


app = create_app()
