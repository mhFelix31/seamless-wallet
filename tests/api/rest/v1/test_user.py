from datetime import datetime, timedelta, timezone

import pytest


def test_create_user_returns_200(
    default_client,
    create_header,
):
    # Arrange
    payload = {
        "name": "John",
        "email": "john@example.com",
        "password": "123456",
    }

    # Act
    response = default_client.post(
        "/",
        json=payload,
        headers=create_header(),
    )

    # Assert
    assert response.status_code == 200


def test_create_user_with_expired_token(
    default_client, create_header, custom_token_payload
):
    # Arrange
    payload = {
        "name": "John",
        "email": "john@example.com",
        "password": "123456",
    }
    custom_expired_token = custom_token_payload(
        {"u": 1, "exp": datetime.now(timezone.utc) - timedelta(hours=1)}
    )
    # Act
    response = default_client.post(
        "/",
        json=payload,
        headers=create_header(custom_expired_token),
    )

    # Assert
    assert response.status_code == 401


def test_create_user_with_invalid_jwt(
    default_client, create_header, custom_token_payload
):
    # Arrange
    payload = {
        "name": "John",
        "email": "john@example.com",
        "password": "123456",
    }
    custom_expired_token = custom_token_payload(
        {"u": 1, "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
        secret_token="invalid",
    )
    # Act
    response = default_client.post(
        "/",
        json=payload,
        headers=create_header(custom_expired_token),
    )

    # Assert
    assert response.status_code == 403


@pytest.mark.parametrize("field", ["name", "email", "created_at", "updated_at"])
def test_create_user_returns_required_parameters(
    field,
    default_client,
    create_header,
):
    # Arrange
    payload = {
        "name": "John",
        "email": "john@example.com",
        "password": "123456",
    }

    # Act
    response = default_client.post(
        "/",
        json=payload,
        headers=create_header(),
    )

    # Assert
    assert field in response.json().keys()


def test_retrieve_user_returns_200(
    default_client,
    create_header,
    user_factory,
):
    # Arrange
    user = user_factory()

    # Act
    response = default_client.get(
        f"/{user.uuid}",
        headers=create_header(),
    )

    # Assert
    assert response.status_code == 200


def test_retrieve_user_returns_404_for_missing_user(
    default_client,
    create_header,
):
    # Arrange
    user_id = 999999

    # Act
    response = default_client.get(
        f"/{user_id}",
        headers=create_header(),
    )

    # Assert
    assert response.status_code == 404


def test_update_user_returns_200(
    default_client,
    create_header,
    user_factory,
):
    # Arrange
    user = user_factory()

    payload = {"name": "Updated Name"}

    # Act
    response = default_client.patch(
        f"/{user.uuid}",
        json=payload,
        headers=create_header(),
    )

    # Assert
    assert response.status_code == 200


def test_update_user_changes_name(
    default_client,
    create_header,
    user_factory,
):
    # Arrange
    user = user_factory()

    payload = {"name": "Updated Name"}

    # Act
    response = default_client.patch(
        f"/{user.uuid}",
        json=payload,
        headers=create_header(),
    )

    # Assert
    assert response.json()["name"] == "Updated Name"


def test_delete_user_returns_200(
    default_client,
    create_header,
    user_factory,
):
    # Arrange
    user = user_factory()

    # Act
    response = default_client.delete(
        f"/{user.uuid}",
        headers=create_header(),
    )

    # Assert
    assert response.status_code == 200


def test_delete_user_returns_404_for_missing_user(
    default_client,
    create_header,
):
    # Arrange
    user_id = 999999

    # Act
    response = default_client.delete(
        f"/{user_id}",
        headers=create_header(),
    )

    # Assert
    assert response.status_code == 404