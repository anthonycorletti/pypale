import pytest

from pypale import Pypale
from tests.factories import test_base_url


@pytest.fixture(scope="function")
def _example_dot_com_1s_token() -> Pypale:
    return Pypale(
        token_ttl_minutes=1,
        token_issue_ttl_seconds=1,
        base_url=test_base_url(),
        secret_key="itsasecret",
    )
