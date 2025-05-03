import sentry_sdk

from EnergyYar.settings.base import *

BASE_URL = env_setting('BASE_URL', 'http://localhost:8000/')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env_setting('DEBUG', 'False')

ALLOWED_HOSTS = env_setting("ALLOWED_HOSTS", "").split(",")
SECRET_KEY = env_setting("SECRET_KEY", "")

# django-cors-headers configs
CORS_ORIGIN_ALLOW_ALL = env_setting('CORS_ORIGIN_ALLOW_ALL', 'False')
CSRF_TRUSTED_ORIGINS = env_setting("CSRF_TRUSTED_ORIGINS", "").split(",")
CORS_ALLOWED_ORIGINS = env_setting('CORS_ALLOWED_ORIGINS', '').split(",")

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env_setting('DB_NAME'),
        'USER': env_setting('DB_USER'),
        'PASSWORD': env_setting('DB_PASSWORD'),
        'HOST': env_setting('DB_HOST', 'localhost'),
        'PORT': env_setting('DB_PORT', '5432'),
    }
}

# SENTRY

if env_setting("SENTRY_ENABLE"):
    sentry_sdk.init(
        dsn=env_setting("SENTRY_URL", ""),
        # Add data like request headers and IP for users,
        # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
        send_default_pii=True,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=1.0,
        _experiments={
            # Set continuous_profiling_auto_start to True
            # to automatically start the profiler on when
            # possible.
            "continuous_profiling_auto_start": True,
        },
    )
