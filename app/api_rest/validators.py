from django.core.exceptions import ValidationError
from django.conf import settings


def validate_file_size(value):
    filesize = value.size

    if filesize > settings.FILE_UPLOAD_SIZE_LIMIT:
        raise ValidationError(
            "Por el tamaño de este archivo, es posible esté"
            + " corrupto. Por favor reparar con Microsoft Excel."  # noqa: W503
        )
    else:
        return value
