import logging
from http import HTTPStatus

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


logger = logging.getLogger(__name__)


class ApiResponse(Response):
    def __init__(
            self,
            data=None,
            status=None,
            template_name=None,
            headers=None,
            exception=False,
            content_type=None,
            error=None
    ):
        if error:
            error = str(error)
        data = {'error': error, 'data': data}
        super().__init__(
            data=data,
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type
        )


def validation_exception_handler(exc):
    error = ''
    for arg in exc.args:
        for field in arg:
            for message in arg[field]:
                error += f'{field.capitalize()}: {message.capitalize() }'

    return ApiResponse(error=error.strip(), status=exc.status_code)


def custom_exception_handler(exc, _):
    logger.exception(exc)

    if isinstance(exc,  ValidationError):
        return validation_exception_handler(exc)

    try:
        status = exc.status_code
    except AttributeError:
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    error = str(exc)
    return ApiResponse(error=error, status=status)
