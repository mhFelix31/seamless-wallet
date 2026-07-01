import pytest

from infrastructure.db.models.currency_model import CurrencyModel
from infrastructure.db.models.wallet_model import WalletModel
from tests.conftest import db_session


# @pytest.fixture
# def user_factory(db_session, mock_setting):
#     password_hasher = Argon2PasswordHasher(secret_pepper=mock_setting.secret_pepper)
#
#     def _create_user(
#         email="user@example.com",
#         password="valid-password",
#         name="Test User",
#     ):
#         user = UserModel(
#             name=name,
#             email=email,
#             password_hash=password_hasher.hash(password),
#         )
#
#         db_session.add(user)
#         db_session.commit()
#         db_session.refresh(user)
#
#         return user
#
#     return _create_user
#
#
# @pytest.fixture
# def token_factory(user_factory, mock_setting):
#     token_service = JWTTokenService(secret_token=mock_setting.secret_token)
#
#     def _generate_token(user=user_factory()):
#         token = token_service.generate(user_id=user.id)
#         return token
#
#     return _generate_token
#
#
# @pytest.fixture
# def custom_token_payload(mock_setting):
#     def _custom_payload(payload, secret_token=mock_setting.secret_token):
#         jwt_token = jwt.encode(payload, secret_token, algorithm="HS256")
#         return jwt_token
#
#     return _custom_payload
#
#
# @pytest.fixture
# def create_header(token_factory):
#     def _header(jwt_token=token_factory()):
#         header = {"Authorization": f"Bearer {jwt_token}"}
#         return header
#
#     return _header


@pytest.fixture(scope="session")
def currency_factory(db_session, mock_setting):
    def _currency_factory(code:str) -> CurrencyModel:
        currency_model = CurrencyModel(code=code)

        db_session.add(currency_model)
        db_session.commit()
        db_session.refresh(currency_model)
        return currency_model

    return _currency_factory

@pytest.fixture(scope="session")
def wallet_factory(db_session, mock_setting):
    def _wallet_factory(label:str) -> WalletModel:
        wallet_model = WalletModel(label=label)

        db_session.add(wallet_model)
        db_session.commit()
        db_session.refresh(wallet_model)
        return wallet_model

    return _wallet_factory