from uuid import UUID

from src.domain.user.entities import User
from src.domain.user.repository import UserRepository
from src.enums import Role
from src.infrastructure.db.models.user_model import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session):
        self.session = session

    def get(self, uuid: str) -> User:
        model = self.session.query(UserModel).get(uuid)
        domain = self._to_domain(model)
        return domain

    def get_by_email(self, email: str) -> User:
        model = self.session.query(UserModel).filter(email=email)
        domain = self._to_domain(model)
        return domain

    def save(self, user: User) -> bool:
        try:
            model = self._to_model(user)
            self.session.add(model)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            return False

    def update(self, uuid: str, user: User) -> User | None:
        try:
            user_already_saved = self.session.query(UserModel).get(uuid)
            if not user_already_saved:
                return None
            model = self._update_model_from_domain(
                model=user_already_saved, domain=user
            )
            self.session.commit()
            domain = self._to_domain(model)
            return domain
        except Exception:
            self.session.rollback()
            return None

    def delete(self, uuid: str) -> bool:
        try:
            model = self.session.query(UserModel).get(uuid)
            if not model.is_active:
                return True
            model.is_active = False
            self.session.commit()
            return True
        except Exception:
            return False

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

    def _update_model_from_domain(self, model: UserModel, domain: User) -> UserModel:
        model.full_name = domain.full_name
        model.email = domain.email
        model.date_of_birth = domain.date_of_birth
        model.password_hash = domain.password_hash
        model.is_active = domain.is_active
        return model

    def _to_domain(self, model: UserModel) -> User:
        domain = User(
            uuid=UUID(model.uuid),
            full_name=model.full_name,
            email=model.email,
            date_of_birth=model.date_of_birth,
            password_hash=model.password_hash,
            is_active=model.is_active,
            role=Role(model.role),
        )
        return domain
