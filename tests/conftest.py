from unittest.mock import Mock

import pytest

from app.infrastructure.logging.contract import LoggerContract


@pytest.fixture
def mock_logger() -> Mock:
    """
    Create a mock logger.

    :return: A mock logger conforming to LoggerContract
    """
    return Mock(spec=LoggerContract)
