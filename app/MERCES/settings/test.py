from datetime import timedelta
from .local import *  # noqa: F401, F403

try:
    JWT_AUTH["JWT_EXPIRATION_DELTA"] = timedelta(seconds=10)  # noqa: F405
except KeyError:
    pass
