from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.mapper.exceptions import (
    CodeEvaluationError,
    InputTraceToModelError,
    MapperError,
    MappingConfigToModelError,
    OutputTraceToModelError,
)
from app.parsers.exceptions import (
    CSVParsingError,
    InvalidCSVStructureError,
    ParserError,
    ParserFactoryError,
)
from app.profile_enricher.exceptions import (
    BasePathError,
    InvalidJsonError,
    ProfileNotFoundError,
    ProfilerError,
    ProfileValidationError,
    TemplateNotFoundError,
)


class ExceptionHandler:
    def __init__(self):
        self.error_mapping: dict[type[Exception], int] = {
            ValueError: status.HTTP_400_BAD_REQUEST,
            TypeError: status.HTTP_500_INTERNAL_SERVER_ERROR,
            # MapperError and its subclasses
            MapperError: status.HTTP_500_INTERNAL_SERVER_ERROR,
            MappingConfigToModelError: status.HTTP_500_INTERNAL_SERVER_ERROR,
            InputTraceToModelError: status.HTTP_422_UNPROCESSABLE_ENTITY,
            OutputTraceToModelError: status.HTTP_500_INTERNAL_SERVER_ERROR,
            CodeEvaluationError: status.HTTP_500_INTERNAL_SERVER_ERROR,
            # ProfilerError and its subclasses
            ProfilerError: status.HTTP_500_INTERNAL_SERVER_ERROR,
            ProfileNotFoundError: status.HTTP_404_NOT_FOUND,
            TemplateNotFoundError: status.HTTP_404_NOT_FOUND,
            InvalidJsonError: status.HTTP_500_INTERNAL_SERVER_ERROR,
            ProfileValidationError: status.HTTP_500_INTERNAL_SERVER_ERROR,
            BasePathError: status.HTTP_500_INTERNAL_SERVER_ERROR,
            # ParserError and its subclasses
            ParserError: status.HTTP_400_BAD_REQUEST,
            ParserFactoryError: status.HTTP_400_BAD_REQUEST,
            CSVParsingError: status.HTTP_422_UNPROCESSABLE_ENTITY,
            InvalidCSVStructureError: status.HTTP_422_UNPROCESSABLE_ENTITY,
        }

    def configure(self, app: FastAPI):
        """
        Configure exception handlers for the FastAPI application.

        :param app: The FastAPI application instance
        """
        # Configure the known_exception_handler for all custom exceptions
        for exception in self.error_mapping:
            app.add_exception_handler(
                exc_class_or_status_code=exception,
                handler=self.known_exception_handler,
            )

        # Add a catch-all handler for any unhandled exceptions
        app.add_exception_handler(
            exc_class_or_status_code=Exception,
            handler=self.global_exception_handler,
        )

    async def known_exception_handler(
        self,
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """
        Handle known exceptions and return appropriate JSON responses.

        :param request: The request that caused the exception
        :param exc: The exception that was raised

        :return: A JSON response containing error details
        """
        status_code = self.error_mapping.get(
            type(exc),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

        return JSONResponse(
            status_code=status_code,
            content=self.get_error_detail(
                exc=exc,
                status_code=status_code,
                request=request,
            ),
        )

    async def global_exception_handler(
        self,
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """
        Global exception handler for unhandled exceptions.

        :param request: The request that caused the exception
        :param exc: The unhandled exception
        :return: A JSON response indicating an internal server error
        """
        request.state.logger.warning("Unhandled exception", type(exc).__name__)

        return JSONResponse(
            status_code=500,
            content=self.get_error_detail(
                exc=exc,
                status_code=500,
                request=request,
            ),
        )

    def get_error_detail(
        self,
        exc: Exception,
        status_code: int,
        request: Request,
    ) -> dict[str, str]:
        """
        Generate an error detail dictionary based on the exception, status code, and environment.

        In production, internal server errors are given a generic message.

        :param exc: The exception that was raised
        :param status_code: The HTTP status code associated with the error
        :param request: The request that caused the exception
        :return: A dictionary containing the error detail
        """
        request.state.logger.exception(
            "HTTP Error",
            exc,
            {
                "status_code": status_code,
            },
        )

        if (
            request.state.config.is_env_production()
            and status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        ):
            return {"detail": "An internal server error occurred."}
        return {"detail": str(exc)}
