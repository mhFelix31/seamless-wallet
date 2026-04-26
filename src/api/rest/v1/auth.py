from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, APIRouter, HTTPException
from src.api.dependencies import get_login_handler
from src.application.auth.commands import Login
from src.application.auth.handler import LoginHandler

router = APIRouter()


@router.post("/login/")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    use_case: LoginHandler = Depends(get_login_handler),
):
    username, password = form.username, form.password
    login_command = Login(email=username, password=password)
    try:
        response = use_case.handle(login_command)
    except Exception as ex:
        raise HTTPException(status_code=401, detail="Invalid Credentials") from ex
    return response
