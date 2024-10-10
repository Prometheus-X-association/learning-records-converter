from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def configure_exception_handlers(app: FastAPI):
    """
    Configure exception handlers for the FastAPI application.

    :param app: The FastAPI application instance
    """
    # Configure the known_exception_handler for all custom exceptions
    for exception in [
        RequestValidationError,
        ValueError,
        TypeError,
    ]:
        app.add_exception_handler(
            exc_class_or_status_code=exception,
            handler=known_exception_handler,
        )

    # Add a catch-all handler for any unhandled exceptions
    app.add_exception_handler(
        exc_class_or_status_code=Exception,
        handler=global_exception_handler,
    )


async def known_exception_handler(request: Request, exc: Exception):
    """
    Handle known exceptions and return appropriate JSON responses.

    :param request: The request that caused the exception
    :param exc: The exception that was raised
    """
    print("known_exception_handler")
    error_mapping = {
        ValueError: 401,
        RequestValidationError: 422,
        TypeError: 500,
    }

    status_code = error_mapping.get(type(exc), 500)

    request.state.logger.exception(
        "HTTP Error sent",
        exc,
        {
            "status_code": status_code,
        },
    )

    raise HTTPException(status_code=status_code, detail=str(exc))


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler for unhandled exceptions.

    :param request: The request that caused the exception
    :param exc: The unhandled exception
    :return: A JSON response indicating an internal server error
    """

    request.state.logger.exception("Unhandled exception", exc)

    return JSONResponse(
        status_code=500,
        content=str(exc),
    )
