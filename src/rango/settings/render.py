"""Settings customised for deployment on Render.com

- See Base Django app https://render.com/docs/deploy-django
- Render Workflows, https://render.com/docs/workflows

Note that at this point Render does not support objects stores.
"""

import os

from .base import *

DEBUG = False

# From Render environment variables
SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = [
    os.environ.get("RENDER_EXTERNAL_HOSTNAME"),
]

# CSRF settings for development with ngrok
CSRF_TRUSTED_ORIGINS = [
    os.environ.get("RENDER_EXTERNAL_URL"),
]

# This simple Django utility allows you to utilize the
# 12factor inspired DATABASE_URL environment variable
# https://www.12factor.net/backing-services
# to configure your Django application.
# https://github.com/jazzband/dj-database-url
import dj_database_url

DATABASES = {
    "default": dj_database_url.config(
        # Replace this value with your local database's connection string.
        env="DATABASE_URL",  # Use DATABASE_URL for Render's database
        default="postgresql://postgres:postgres@localhost:5432/mysite",
        conn_max_age=60,
        conn_health_checks=True,
        disable_server_side_cursors=True,
    )
}

# https://render.com/docs/deploy-django#set-up-static-file-serving
MIDDLEWARE += [
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Django uses this to validate that redis is available, our configuration
DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL", "Banjara Support <support@banjara.app>"
)
# If you’re using django-allauth, have it pick up the same value:
ACCOUNT_DEFAULT_FROM_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_BACKEND = "anymail.backends.resend.EmailBackend"
ANYMAIL = {
    "RESEND_API_KEY": os.environ.get("RESEND_API_KEY"),
}
