from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.config.envconfig import EnvConfig
from app.infrastructure.logging.jsonlogger import JsonLogger
from app.infrastructure.logging.types import LogLevel

from .exception_handlers import ExceptionHandler
from .routers.traces import router as traces_router

config = EnvConfig()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> dict[str, Any]:
    """Lifespan context manager for the FastAPI application.

    :param _app: The FastAPI application instance
    :yield: A dictionary containing logger and config objects
    """
    logger = JsonLogger(name=__name__, level=config.get_log_level())
    logger.info(
        "Application starting",
        {
            "app_log_level": config.get_log_level().name,
            "app_env": config.get_environment().name,
        },
    )

    yield {"logger": logger, "config": config}

    logger.info("Application shutting down")


app = FastAPI(
    title="LRC API",
    version="0.0.1",
    debug=config.get_log_level() == LogLevel.DEBUG and not config.is_env_production(),
    lifespan=lifespan,
)

exception_handler = ExceptionHandler()
exception_handler.configure(app)

app.include_router(router=traces_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.get_cors_allowed_origins(),
    allow_methods=["POST"],
    allow_headers=["*"],
    allow_credentials=True,
    max_age=600,
)
