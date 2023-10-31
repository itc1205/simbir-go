from typing import Any, Dict, Optional
from typing_extensions import Annotated, Doc
from fastapi import HTTPException, status


class NotEnoughPrivileges(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_403_FORBIDDEN,
        detail: Any = "You dont have enough privileges to use this command",
        headers: Dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class InvalidCredentials(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: Any = "Invalid authentication credentials",
        headers: Dict[str, str] | None = {"WWW-Authenticate": "Bearer"},
    ) -> None:
        super().__init__(status_code, detail, headers)


class InvalidLoginOrPassword(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: Any = "Invalid password or login",
        headers: Dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class TokenExpired(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: Any = "Token expired",
        headers: Dict[str, str] | None = {"WWW-Authenticate": "Bearer"},
    ) -> None:
        super().__init__(status_code, detail, headers)


class InvalidToken(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: Any = "Invalid token! Try to login again",
        headers: Dict[str, str] | None = {"WWW-Authenticate": "Bearer"},
    ) -> None:
        super().__init__(status_code, detail, headers)


class EntityNotFound(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: Any = None,
        headers: Dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class LoginAlreadyExists(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_409_CONFLICT,
        detail: Any = "Login already exists",
        headers: Dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
