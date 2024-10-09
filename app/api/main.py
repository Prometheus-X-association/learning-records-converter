from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.config.envconfig import EnvConfig
from app.infrastructure.logging.jsonlogger import JsonLogger

from .exception_handlers import configure_exception_handlers
from .routers.traces import router as traces_router

config = EnvConfig()


@asynccontextmanager
async def lifespan(app: FastAPI) -> dict[str, Any]:
    """
    Lifespan context manager for the FastAPI application.

    :param app: The FastAPI application instance
    :yield: A dictionary containing logger and config objects
    """
    logger = JsonLogger(name=__name__, level=config.get_log_level())
    logger.info("Application starting")

    yield {"logger": logger, "config": config}

    logger.info("Application shutting down")


app = FastAPI(
    title="LRC API",
    version="0.0.1",
    servers=[{"url": "", "description": ""}],
    debug=config.get_log_level() == "DEBUG",
    lifespan=lifespan,
)

configure_exception_handlers(app)

app.include_router(router=traces_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.get_cors_allowed_origins(),
    allow_methods=["POST"],
    allow_headers=["*"],
    allow_credentials=True,
    max_age=600,
)
