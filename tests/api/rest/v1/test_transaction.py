from typing import Callable

import pytest

from infrastructure.db.models.currency_model import CurrencyModel
from infrastructure.db.models.wallet_model import WalletModel


@pytest.fixture()
def test_currency(currency_factory):
    cur = currency_factory(code="BRL")
    return cur


@pytest.mark.parametrize("parameter, expected_value",[
    ("sender", "bank"),
    ("receiver", "receiver"),
    ("amount", {"value": 10.50,"currency_code": "BRL"}),
    ("balance", {"value": 10.50,"currency_code": "BRL"})
])
@pytest.mark.e2e
def test_deposit_happy_path_return(
        parameter:str,
        expected_value: str | dict,
        default_client,
        test_currency:CurrencyModel,
        wallet_factory: Callable[..., WalletModel]
):
    source_wallet:WalletModel = wallet_factory(label="bank")
    receiver_wallet:WalletModel = wallet_factory(label="receiver")

    payload = {
        "wallet_id": receiver_wallet.uuid,
        "currency_code": test_currency.code,
        "value": 10.50
    }
    response = default_client.post("/rest/v1/transactions/deposit", payload)

    # ASSERT
    assert response.json()[parameter] == expected_value

@pytest.mark.e2e
def test_deposit_negative_value(): ...


@pytest.mark.e2e
def test_deposit_zero_value(): ...


@pytest.mark.e2e
def test_deposit_with_bank_with_is_external_managed_false_and_amount_over(): ...


@pytest.mark.e2e
def test_deposit_with_bank_with_is_external_managed_and_amount_over(): ...



@pytest.mark.e2e
def test_withdraw_happy_path():...


@pytest.mark.e2e
def test_withdraw_negative_value(): ...


@pytest.mark.e2e
def test_withdraw_zero_value(): ...


@pytest.mark.e2e
def test_withdraw_with_bank_with_is_external_managed_false_and_amount_over(): ...


@pytest.mark.e2e
def test_withdraw_with_is_external_managed_true_and_amount_over(): ...



@pytest.mark.e2e
def test_transfer_happy_path():...


@pytest.mark.e2e
def test_transfer_negative_value(): ...


@pytest.mark.e2e
def test_transfer_zero_value(): ...


@pytest.mark.e2e
def test_transfer_with_bank_with_is_external_managed_false_and_amount_over(): ...


@pytest.mark.e2e
def test_transfer_with_is_external_managed_true_and_amount_over(): ...