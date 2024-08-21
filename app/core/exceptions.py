from typing import Any, Dict, Optional

from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: Any = None, headers: Optional[Dict[str, Any]] = None) -> None:
        detail = [
            {
                'msg': detail,
            }
        ]
        super().__init__(status_code, detail, headers)


class DuplicatedError(BaseHTTPException):
    def __init__(self, detail: Any = None, headers: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, detail, headers)


class AuthError(BaseHTTPException):
    def __init__(self, detail: Any = None, headers: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, headers)


class NotFoundError(BaseHTTPException):
    def __init__(self, detail: Any = None, headers: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, detail, headers)


class ValidationError(BaseHTTPException):
    def __init__(self, detail: Any = None, headers: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, detail, headers)


class ForbiddenError(BaseHTTPException):
    def __init__(self, detail: Any = None, headers: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, detail, headers)


class ConflictError(BaseHTTPException):
    def __init__(self, detail: Any = None, headers: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(status.HTTP_409_CONFLICT, detail, headers)


class NotAcceptableError(BaseHTTPException):
    def __init__(self, detail: Any = None, headers: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(status.HTTP_406_NOT_ACCEPTABLE, detail, headers)

class BadRequestError(BaseHTTPException):
    def __init__(self, detail: Any = None, headers: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, detail, headers)
