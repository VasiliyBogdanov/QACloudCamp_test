import pytest

from tests.helpers.API import API, API_BASE


@pytest.fixture(scope="session")
def api():
    return API(API_BASE)
