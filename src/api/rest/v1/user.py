from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.api.dependencies import get_user_repository, require_permissions
from src.application.user.commands import (
    DeleteUserCommand,
    NewUserCommand,
    UpdateUserCommand,
)
from src.application.user.dto import UserDeletionDTO, UserDTO, UserResponseDTO
from src.application.user.handler import UserHandler
from src.domain.user.repository import UserRepository
from src.enums import Role

router = APIRouter(
    dependencies=[Depends(require_permissions(roles_with_permission=[Role.CLERK]))]
)


@router.post(
    "/create", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED
)
def create_user(
    new_user: UserDTO, user_repository: UserRepository = Depends(get_user_repository)
):
    new_user_command = NewUserCommand(new_user=new_user)
    user_handler = UserHandler(user_repository)
    user = user_handler.create(new_user_command=new_user_command)
    return user


@router.post(
    "{user_id}/update",
    response_model=UserResponseDTO,
    status_code=status.HTTP_200_OK,
)
def update_user_information(
    user_id: UUID,
    updated_user: UserDTO,
    user_repository: UserRepository = Depends(get_user_repository),
):
    update_user_command = UpdateUserCommand(user_id=user_id, updated_user=updated_user)
    user_handler = UserHandler(user_repository)
    user = user_handler.update(update_user_command)
    return user


@router.delete(
    "{user_id}",
    response_model=UserDeletionDTO,
    status_code=status.HTTP_200_OK,
)
def delete_user(
    user_id: UUID, user_repository: UserRepository = Depends(get_user_repository)
):
    delete_user_command = DeleteUserCommand(user_id=user_id)
    user_handler = UserHandler(user_repository)
    user_deletion: UserDeletionDTO = user_handler.delete(delete_user_command)
    return user_deletion
