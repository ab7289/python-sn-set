import pytest
from click.testing import CliRunner


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("SN_USER_NAME", "user")
    monkeypatch.setenv("SN_PASSWORD", "password")


@pytest.fixture
def mock_empty_env_vars(monkeypatch):
    monkeypatch.setenv("SN_USER_NAME", "user")
    monkeypatch.setenv("SN_PASSWORD", "")
