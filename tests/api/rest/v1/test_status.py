import pytest


@pytest.mark.e2e
@pytest.mark.parametrize("check_param", ["db", "cache"])
def test_all_checks_happy_path(check_param, default_client):
    response = default_client.get("/rest/v1/status")
    response_json = response.json()

    assert response_json["services"][check_param] == "ok", (
        f"Checked {check_param}, is not ok"
    )


@pytest.mark.e2e
def test_all_checks_with_failed_parameter(mock_setting, client_factory):
    mock_setting.database_type = "sqlalchemy"
    mock_setting.database_url = (
        "postgresql+psycopg://sqlalchemy:password@invalid:5432/app"
    )
    mock_setting.cache_type = "redis"
    mock_setting.cache_url = "redis://invalid:6379/0"

    with client_factory(mock_setting) as test_client:
        response = test_client.get("/rest/v1/status")
    response_json = response.json()

    assert response.status_code == 503, (
        f"Status expected is 503, received {response.status_code}"
    )
    assert response_json["services"] == {"db": "failed", "cache": "failed"}


@pytest.mark.e2e
def test_app_check_happy_path(default_client):
    response = default_client.get("/rest/v1/status/app")

    assert response.status_code == 200


@pytest.mark.e2e
def test_db_check_happy_path(default_client):
    response = default_client.get("/rest/v1/status/db")

    assert response.status_code == 200


@pytest.mark.e2e
def test_db_check_no_db(): ...


@pytest.mark.e2e
def test_cache_check_happy_path(default_client):
    response = default_client.get("/rest/v1/status/cache")

    assert response.status_code == 200


@pytest.mark.e2e
def test_cache_check_no_cache(): ...
