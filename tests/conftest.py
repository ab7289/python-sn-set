import pytest
from click.testing import CliRunner


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("SN_USER_NAME", "user")
    monkeypatch.setenv("SN_PASSWORD", "password")
    monkeypatch.setenv("SN_SET_USE_OAUTH", "false")


@pytest.fixture
def mock_empty_env_vars(monkeypatch):
    monkeypatch.setenv("SN_USER_NAME", "user")
    monkeypatch.setenv("SN_PASSWORD", "")
    monkeypatch.setenv("SN_SET_USE_OAUTH", "false")


@pytest.fixture
def mock_oauth_env_vars(monkeypatch):
    monkeypatch.setenv("SN_USER_NAME", "abc123")
    monkeypatch.setenv("SN_PASSWORD", "super-secret")
    monkeypatch.setenv("SN_SET_USE_OAUTH", "true")
    monkeypatch.setenv("SN_SET_CLIENT_ID", "client_id")
    monkeypatch.setenv("SN_SET_CLIENT_SECRET", "super-secure")
    monkeypatch.setenv("SN_SET_GRANT_TYPE", "invalid")
