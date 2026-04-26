import pytest


@pytest.fixture
def get_jwt_token():
    def _get_jwt_token(user): ...

    return _get_jwt_token


@pytest.fixture
def admin_jwt_token(get_jwt_token):
    return get_jwt_token("admin")


@pytest.fixture
def create_user():
    def _create_user(name: str, balance: int):
        return {"name": name, "balance": balance}

    return _create_user


@pytest.fixture
def create_currency():
    def _create_currency(): ...

    return _create_currency


@pytest.fixture
def currency_usd(create_currency):
    create_currency("USD")


@pytest.mark.e2e
def test_deposit_happy_path(default_client, create_user, currency_usd, admin_jwt_token):
    user = create_user(name="test", balance=0)
    header = {"Authorization Token": admin_jwt_token}
    payload = {
        "user_id": user.id,
        "value": 0,
        "currency_code": "USD",
    }

    response = default_client.post(
        "/rest/v1/transaction/deposit/", header=header, json=payload
    )

    assert response.status_code == 200
    assert response.json() == {"user_id": user.id, "balance": 0}


@pytest.mark.parametrize(
    "test_user, token, status_code, response_body",
    [
        (create_user("test_user"), get_jwt_token("test_user"), 401, {}),
    ],
)
@pytest.mark.e2e
def test_deposit(
    test_user,
    token,
    status_code,
    response_body,
    default_client,
    create_user,
    currency_usd,
):
    user = create_user(name="test", balance=0)
    header = {"Authorization Token": admin_jwt_token}
    payload = {
        "user_id": user.id,
        "value": 0,
        "currency_code": "USD",
    }

    response = default_client.post(
        "/rest/v1/transaction/deposit/", header=header, json=payload
    )

    assert response.status_code == 200
    assert response.json() == {"user_id": user.id, "balance": 0}


@pytest.mark.e2e
def test_withdraw_happy_path(
    default_client, create_user, currency_usd, admin_jwt_token
):
    user = create_user(name="test", balance=0)
    header = {"Authorization Token": admin_jwt_token}
    payload = {
        "user_id": user.id,
        "value": 0,
        "currency_code": "USD",
    }

    response = default_client.post(
        "/rest/v1/transaction/withdraw/", header=header, json=payload
    )

    assert response.status_code == 200
    assert response.json() == {"user_id": user.id, "balance": 0}


@pytest.mark.e2e
def test_transaction_user_a_to_b_happy_path(default_client, create_user, get_jwt_token):
    user_a = create_user(name="a", balance=0)
    user_b = create_user(name="b", balance=0)

    header = {"Authorization Token": get_jwt_token(user_a)}
    payload = {"receiver_id": user_b.id, "value": 0, "currency_code": "USD"}

    response = default_client.post(
        "/rest/v1/transaction/transfer/", header=header, json=payload
    )

    assert response.status_code == 200
    assert response.json() == {
        "user_id": user_a.id,
        "balance": 0,
        "receiver_id": user_b.id,
        "transfer_status": "COMPLETED",
    }
