import sys
from typing import Generator
from unittest.mock import MagicMock

import pytest


@pytest.fixture(autouse=True)
def mock_requests() -> Generator[MagicMock, None, None]:
    """Автоматически подменяет requests во всех тестах"""
    mock_requests = MagicMock()

    sys.modules['requests'] = mock_requests
    sys.modules['requests.exceptions'] = MagicMock()
    sys.modules['requests.models'] = MagicMock()

    yield mock_requests

    if 'requests' in sys.modules:
        del sys.modules['requests']
