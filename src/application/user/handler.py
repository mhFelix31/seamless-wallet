from src.application.user.commands import (
    DeleteUserCommand,
    NewUserCommand,
    UpdateUserCommand,
)
from src.application.user.dto import UserDeletionDTO, UserResponseDTO
from src.application.user.exceptions import (
    UserAlreadyCreatedException,
    UserNotFoundException,
)


class UserHandler:
    def __init__(self, repository) -> None:
        self.repo = repository
        pass

    def create(self, new_user_command: NewUserCommand) -> UserResponseDTO:
        user = self.repo.get_by_email(new_user_command.new_user.email)
        if user:
            raise UserAlreadyCreatedException()
        user = self.repo.save(new_user_command.new_user)
        return user

    def update(self, update_user_command: UpdateUserCommand) -> UserResponseDTO:
        user = self.repo.get(update_user_command.user_id)
        if not user:
            raise UserNotFoundException()
        user_id = update_user_command.user_id
        updated_user = update_user_command.updated_user

        user = self.repo.update(user_id, updated_user)
        return user

    def delete(self, delete_user_command: DeleteUserCommand) -> UserDeletionDTO:
        user = self.repo.get(delete_user_command.user_id)
        if not user:
            raise UserNotFoundException()
        user = self.repo.delete(delete_user_command.user_id)
        detail = "Data will be deactivated and deleted in the beggining of next month"

        return UserDeletionDTO(
            uuid=user.user_id,
            data_full_deletion_date=user.data_full_deletion_date,
            detail=detail,
        )
