from datetime import timedelta
from .base import *  # noqa: F401, F403
from corsheaders.defaults import default_headers

SECRET_KEY = "h9s33#kz!cjf#h=bepvwdd10f$7w9)=slne4nndd!isr&i=2d-"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "covid19grm",
        "USER": "covid19grm",
        "PASSWORD": "covid19grm",
        "HOST": "db",
        "PORT": 5432,
    }
}

# Rest configuration
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # 'rest_framework.authentication.TokenAuthentication',
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
        # 'rest_framework.permissions.AllowAny',
    ),
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_PAGINATION_CLASS": "api_rest.pagination.ReactAdminPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_FILTER_BACKENDS": ["api_rest.filtering.ReactAdminFilterBackend"],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        "drf_renderer_xlsx.renderers.XLSXRenderer",
    ],
}

SWAGGER_SETTINGS = {
    "api_version": "1.0",
    "SHOW_REQUEST_HEADERS": True,
    "SUPPORTED_SUBMIT_METHODS": [
        "get",
        "post",
        "put",
        "delete",
        "patch",
        "options",
    ],
    "SECURITY_DEFINITIONS": {
        "api_key": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        }
    },
    "USE_SESSION_AUTH": True,
    "JSON_EDITOR": True,
}


JWT_AUTH = {
    "JWT_AUTH_HEADER_PREFIX": "Bearer",
    "JWT_ALLOW_REFRESH": True,
    "JWT_EXPIRATION_DELTA": timedelta(days=367),
    "JWT_REFRESH_EXPIRATION_DELTA": timedelta(days=7),
    "JWT_SECRET_KEY": SECRET_KEY,
    "JWT_RESPONSE_PAYLOAD_HANDLER": "api_rest.jwt.jwt_response_payload_handler",  # noqa: E501
}

LOGIN_URL = "/admin/login"
LOGOUT_URL = "/admin/logout"
LOGIN_REDIRECT_URL = "/admin"
LOGOUT_REDIRECT_URL = "/admin/login"

REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "api_rest.serializer.AccountSerializer",
}

# Cors header configurations
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = list(default_headers) + [
    "X-Total-Count",
]

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
    ("admin", "admin@mysite.com"),
)
ADMIN_USERNAME = "admin"
ADMIN_EMAIL = "admin@mysite.com"
ADMIN_INITIAL_PASSWORD = "admin"  # To be changed after first login by admin


# ssl
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Security Headers
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 3600
