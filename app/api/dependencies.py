from fastapi import Request

from app.mapper.evaluator.contract import ExpressionEvaluatorContract
from app.mapper.evaluator.eval import EvalExpressionEvaluator
from app.mapper.mapper import Mapper
from app.mapper.repositories.contracts.repository import MappingRepository
from app.mapper.repositories.yaml.yaml_repository import YamlMappingRepository
from app.profile_enricher.profiler import Profiler
from app.profile_enricher.repositories.contracts.repository import ProfileRepository
from app.profile_enricher.repositories.jsonld.jsonld_repository import (
    JsonLdProfileRepository,
)


async def get_mapping_repository(request: Request) -> MappingRepository:
    """
    Dependency injection function to get MappingRepository instance.

    :param request: The FastAPI request object
    :return: An instance of MappingRepository
    """
    return YamlMappingRepository(
        logger=request.state.logger,
    )


async def get_profile_repository(request: Request) -> ProfileRepository:
    """
    Dependency injection function to get ProfileRepository instance.

    :param request: The FastAPI request object
    :return: An instance of ProfileRepository
    """
    return JsonLdProfileRepository(
        logger=request.state.logger,
        config=request.state.config,
    )


async def get_expression_evaluator(request: Request) -> ExpressionEvaluatorContract:
    """
    Dependency injection function to get an ExpressionEvaluator instance.

    :param request: The FastAPI request object
    :return: An instance of ExpressionEvaluatorContract
    """
    return EvalExpressionEvaluator(logger=request.state.logger)


async def get_mapper(request: Request) -> Mapper:
    """
    Dependency injection function to get a Mapper instance.

    :param request: The FastAPI request object
    :return: An instance of Mapper
    """
    return Mapper(
        repository=await get_mapping_repository(request=request),
        expression_evaluator=await get_expression_evaluator(request=request),
        logger=request.state.logger,
    )


async def get_profiler(request: Request) -> Profiler:
    """
    Dependency injection function to get a Profiler instance.

    :param request: The FastAPI request object
    :return: An instance of Profiler
    """
    return Profiler(
        repository=await get_profile_repository(request=request),
    )
