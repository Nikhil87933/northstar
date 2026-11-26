import pytest
from pydantic import SecretStr, ValidationError

from northstar.config.settings import Settings


def test_settings_load_environment_variables(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NORTHSTAR_POSTGRES_HOST", "127.0.0.1")
    monkeypatch.setenv("NORTHSTAR_POSTGRES_PORT", "5432")
    monkeypatch.setenv("NORTHSTAR_POSTGRES_DATABASE", "northstar")
    monkeypatch.setenv("NORTHSTAR_POSTGRES_USERNAME", "test_user")
    monkeypatch.setenv("NORTHSTAR_POSTGRES_PASSWORD", "test_password")
    monkeypatch.setenv("NORTHSTAR_API_BASE_URL", "http://127.0.0.1:8080")
    monkeypatch.setenv("NORTHSTAR_FILES_BASE_URL", "http://127.0.0.1:8081")

    settings = Settings(_env_file=None)

    assert settings.postgres_host == "127.0.0.1"
    assert settings.postgres_port == 5432
    assert settings.postgres_database == "northstar"
    assert str(settings.api_base_url) == "http://127.0.0.1:8080/"
    assert isinstance(settings.postgres_password, SecretStr)


def test_settings_reject_invalid_postgres_port() -> None:
    with pytest.raises(ValidationError):
        Settings(
            _env_file=None,
            NORTHSTAR_POSTGRES_HOST="127.0.0.1",
            NORTHSTAR_POSTGRES_PORT=70000,
            NORTHSTAR_POSTGRES_DATABASE="northstar",
            NORTHSTAR_POSTGRES_USERNAME="test_user",
            NORTHSTAR_POSTGRES_PASSWORD="test_password",
            NORTHSTAR_API_BASE_URL="http://127.0.0.1:8080",
            NORTHSTAR_FILES_BASE_URL="http://127.0.0.1:8081",
        )


def test_settings_reject_empty_database_name() -> None:
    with pytest.raises(ValidationError):
        Settings(
            _env_file=None,
            NORTHSTAR_POSTGRES_HOST="127.0.0.1",
            NORTHSTAR_POSTGRES_DATABASE="",
            NORTHSTAR_POSTGRES_USERNAME="test_user",
            NORTHSTAR_POSTGRES_PASSWORD="test_password",
            NORTHSTAR_API_BASE_URL="http://127.0.0.1:8080",
            NORTHSTAR_FILES_BASE_URL="http://127.0.0.1:8081",
        )


def test_settings_load_from_env_file(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    env_file = tmp_path / ".env"

    env_file.write_text(
        "NORTHSTAR_POSTGRES_HOST=192.168.0.49\n"
        "NORTHSTAR_POSTGRES_PORT=5432\n"
        "NORTHSTAR_POSTGRES_DATABASE=northstar\n"
        "NORTHSTAR_POSTGRES_USERNAME=test_user\n"
        "NORTHSTAR_POSTGRES_PASSWORD=test_password\n"
        "NORTHSTAR_API_BASE_URL=http://127.0.0.1:8080\n"
        "NORTHSTAR_FILES_BASE_URL=http://127.0.0.1:8081\n"
    )

    env_variables = [
        "NORTHSTAR_POSTGRES_HOST",
        "NORTHSTAR_POSTGRES_PORT",
        "NORTHSTAR_POSTGRES_DATABASE",
        "NORTHSTAR_POSTGRES_USERNAME",
        "NORTHSTAR_POSTGRES_PASSWORD",
        "NORTHSTAR_API_BASE_URL",
        "NORTHSTAR_FILES_BASE_URL",
    ]

    for variable in env_variables:
        monkeypatch.delenv(variable, raising=False)

    settings = Settings(_env_file=env_file)

    assert settings.postgres_host == "192.168.0.49"
    assert settings.postgres_port == 5432
    assert settings.postgres_database == "northstar"
    assert str(settings.api_base_url) == "http://127.0.0.1:8080/"
