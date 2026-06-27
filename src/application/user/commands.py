from dataclasses import dataclass
from uuid import UUID

from src.application.user.dto import UserDTO


@dataclass
class NewUserCommand:
    new_user: UserDTO


@dataclass
class UpdateUserCommand:
    user_id: UUID
    updated_user: UserDTO


@dataclass
class DeleteUserCommand:
    user_id: UUID
