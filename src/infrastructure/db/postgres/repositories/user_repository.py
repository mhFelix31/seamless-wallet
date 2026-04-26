from uuid import UUID
from src.domain.user.repository import UserRepository
from src.domain.user.entities import User
from src.infrastructure.db.models.user_model import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session):
        self.session = session

    def get(self, id: UUID) -> User:
        model = self.session.query(UserModel).get(id)
        domain = self._to_domain(model)
        return domain

    def get_by_email(self, email: str) -> User:
        model = self.session.query(UserModel).get(email=email)
        domain = self._to_domain(model)
        return domain

    def save(self, user: User) -> bool:
        # FIXME mock save
        try:
            self._to_model(user)
        except Exception:
            return False

        return True
        # END FIXME

    def _to_model(self, user: User) -> UserModel:
        model = UserModel(
            uuid=str(user.uuid),
            full_name=user.full_name,
            email=user.email,
            date_of_birth=user.date_of_birth,
            password_hash=user.password_hash,
            is_active=user.is_active,
        )
        return model

    def _to_domain(self, model: UserModel) -> User:
        domain = User(
            uuid=UUID(model.uuid),
            full_name=model.full_name,
            email=model.email,
            date_of_birth=model.date_of_birth,
            password_hash=model.password_hash,
            is_active=model.is_active,
        )
        return domain
