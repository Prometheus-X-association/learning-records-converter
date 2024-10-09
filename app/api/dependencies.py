from fastapi import Request

from app.mapper.mapper import Mapper
from app.mapper.repositories.yaml.yaml_repository import YamlMappingRepository
from app.profile_enricher.profiler import Profiler
from app.profile_enricher.repositories.jsonld.jsonld_repository import (
    JsonLdProfileRepository,
)


async def get_mapper(request: Request) -> Mapper:
    """
    Dependency injection function to get a Mapper instance.

    :param request: The FastAPI request object
    :return: An instance of Mapper
    """
    return Mapper(
        repository=YamlMappingRepository(
            logger=request.state.logger,
        ),
        logger=request.state.logger,
    )


async def get_profiler(request: Request) -> Profiler:
    """
    Dependency injection function to get a Profiler instance.

    :param request: The FastAPI request object
    :return: An instance of Profiler
    """
    return Profiler(
        repository=JsonLdProfileRepository(
            logger=request.state.logger,
            config=request.state.config,
        ),
    )
