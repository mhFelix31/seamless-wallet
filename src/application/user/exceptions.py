from fastapi import HTTPException, status


class UserAlreadyCreatedException(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "User already exists in our database."


class FailedToCreateUserException(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = "System Failed to properly create the user."


class UserNotFoundException(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = "We were not able to find the user associated with the requested information."
