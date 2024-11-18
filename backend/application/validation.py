from werkzeug.exceptions import HTTPException
from flask import make_response
from werkzeug.sansio.response import Response


class NotFoundError(HTTPException):
    def __init__(
        self, description: str | None = None, status_code: Response | None = None
    ) -> None:
        self.response = make_response(description, status_code)


class DuplicationError(HTTPException):
    def __init__(
        self, description: str | None = None, status_code: Response | None = None
    ) -> None:
        self.response = make_response(description, status_code)


class NotAuthorizedError(HTTPException):
    def __init__(
        self, description: str | None = None, status_code: Response | None = None
    ) -> None:
        self.response = make_response(description, status_code)


class BusinessValidationError(HTTPException):
    def __init__(
        self, description: str | None = None, status_code: Response | None = None
    ) -> None:
        self.response = make_response(description, status_code)
