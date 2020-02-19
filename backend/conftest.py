import pytest

from PyMatcha import application


@pytest.fixture
def app():
    return application
