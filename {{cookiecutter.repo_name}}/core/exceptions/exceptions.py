from rest_framework.exceptions import APIException


class BaseCustomException(APIException):
    status_code = 400
    success = False
    default_detail = "An error occurred"

    def __init__(self, detail=None, key=None, errors=None):
        self.detail = detail or self.default_detail
        self.key = key or self.__class__.__name__
        self.errors = errors or {}


class EntityNotFoundException(BaseCustomException):
    status_code = 404
    default_detail = "Entity not found"


class ValidationException(BaseCustomException):
    status_code = 400
    default_detail = "Validation error"


class EntityDeleteRestrictedException(BaseCustomException):
    status_code = 400
    default_detail = "Entity cannot be deleted"


class InvalidTokenException(BaseCustomException):
    status_code = 401
    default_detail = "Invalid token"


class InvalidIdException(BaseCustomException):
    status_code = 400
    default_detail = "Invalid ID"


class PasswordMismatchException(BaseCustomException):
    status_code = 400
    default_detail = "Password mismatch"


class CastDtoException(BaseCustomException):
    status_code = 400
    default_detail = "Invalid data type"


class SMSException(BaseCustomException):
    status_code = 500
    default_detail = "SMS service error"


class InvalidOTPException(BaseCustomException):
    status_code = 400
    default_detail = "Invalid OTP"


class PermissionDeniedException(BaseCustomException):
    status_code = 403
    default_detail = "Permission denied"


class NotAuthenticatedException(BaseCustomException):
    status_code = 401
    default_detail = "Not authenticated"


class RecaptchaInvalidException(BaseCustomException):
    status_code = 400
    default_detail = "Invalid reCAPTCHA"


class RecaptchaBadGatewayException(BaseCustomException):
    status_code = 502
    default_detail = "reCAPTCHA service unavailable"
