from src.domain.user.entities import User
from src.domain.user.repository import UserRepository
from .commands import Login


class LoginHandler:
    def __init__(
        self, user_repository: UserRepository, password_hasher, token_service
    ) -> None:
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.token_service = token_service

    def handle(self, command: Login) -> str:
        user: User = self.user_repository.get_by_email(command.email)
        self.password_hasher.verify(command.password, user.password_hash)

        return self.token_service.generate(user.uuid)
