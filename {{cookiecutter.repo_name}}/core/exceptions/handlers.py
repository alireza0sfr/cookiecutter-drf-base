import logging
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response
from .exceptions import BaseCustomException

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    if isinstance(exc, BaseCustomException):
        if exc.status_code >= 500:
            logger.error(f"Server error: {exc.key} - {exc.detail}", exc_info=exc)
        else:
            logger.warning(f"Client error: {exc.key} - {exc.detail}")

        return Response(
            {
                "success": False,
                "code": exc.status_code,
                "message": str(exc.detail),
                "key": exc.key,
                "errors": exc.errors,
            },
            status=exc.status_code,
        )

    if isinstance(exc, DRFValidationError):
        if isinstance(exc.detail, dict):
            errors = exc.detail
        elif isinstance(exc.detail, list):
            errors = {"non_field_errors": exc.detail}
        else:
            errors = {"detail": exc.detail}

        logger.warning(f"Validation error: {errors}")

        return Response(
            {
                "success": False,
                "code": 400,
                "message": "Validation error",
                "key": "validation_error",
                "errors": errors,
            },
            status=400,
        )

    logger.error(f"Unhandled exception: {type(exc).__name__}", exc_info=exc)

    return Response(
        {
            "success": False,
            "code": 500,
            "message": "Internal server error",
            "key": "server_error",
            "errors": {},
        },
        status=500,
    )
