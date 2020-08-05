from .settings import *

DEBUG = True

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
SECURE_CONTENT_TYPE_NOSNIFF = False
X_FRAME_OPTIONS = ""
SECURE_BROWSER_XSS_FILTER = False
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_PRELOAD = False
SECURE_HSTS_INCLUDE_SUBDOMAINS = False

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:",}
}

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# REST API settings
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "project.pagination.DetailedPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
    ],
}

JWT_AUTH = {
    "JWT_AUTH_COOKIE": "jwt_auth_token",
    "CSRF_COOKIE": True,
    "JWT_RESPONSE_PAYLOAD_HANDLER": "project.utils.jwt_response_handler",
    "JWT_VERIFY_EXPIRATION": False,
    "JWT_ALLOW_REFRESH": True,
}

# Celery

CELERY_ALWAYS_EAGER = True
