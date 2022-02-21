import time

import pytest

from pypale import Pypale
from tests.factories import test_email


def test_pypale_valid_token(_example_dot_com_1s_token: Pypale) -> None:
    email = test_email()
    token = _example_dot_com_1s_token.generate_token(email=email)
    assert _example_dot_com_1s_token.valid_token(return_token=token, return_email=email)


def test_pypale_invalid_token_wrong_user(_example_dot_com_1s_token: Pypale) -> None:
    email = test_email(name="userA")
    token = _example_dot_com_1s_token.generate_token(email=email)
    assert not _example_dot_com_1s_token.valid_token(
        return_token=token, return_email=test_email(name="userB")
    )


def test_pypale_token_issue_expiry(_example_dot_com_1s_token: Pypale) -> None:
    email = test_email()
    token = _example_dot_com_1s_token.generate_token(email=email)
    time.sleep(2)
    assert not _example_dot_com_1s_token.valid_token(
        return_token=token, return_email=email
    )


def test_pypale_invalid_token_no_user(_example_dot_com_1s_token: Pypale) -> None:
    email = test_email(name="user")
    token = _example_dot_com_1s_token.generate_token(email=email)
    assert not _example_dot_com_1s_token.valid_token(
        return_token=token, return_email=None
    )


def test_pypale_invalid_token_no_return_token(
    _example_dot_com_1s_token: Pypale,
) -> None:
    email = test_email(name="user")
    with pytest.raises(ValueError):
        _example_dot_com_1s_token.valid_token(return_token=None, return_email=email)
