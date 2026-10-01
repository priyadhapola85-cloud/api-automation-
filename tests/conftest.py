"""Shared pytest fixtures. Every test can request `settings` or `api_client` by name."""
import pytest

from config.settings import load_settings
from core.api_client import APIClient


def pytest_addoption(parser):
    parser.addoption("--env", default="dev", help="Environment to test against (file name in config/environments)")


@pytest.fixture(scope="session")
def settings(request):
    return load_settings(request.config.getoption("--env"))


@pytest.fixture(scope="session")
def api_client(settings):
    client = APIClient(settings.base_url, settings.api_key, settings.api_key_header, settings.timeout)
    yield client
    client.close()
