"""Safe settings for manual QA (humans and agents).

Wraps ``local.settings`` so a QA run never sends real email, never talks to S3/Azure,
and never touches the real development database.

Setup:
    cp db.sqlite3 qa.sqlite3          # qa.sqlite3 is git-ignored; override with NEARBEACH_QA_DB
    # set a known password on the copied users (e.g. via manage.py shell)
    venv/bin/python manage.py runserver 8000 --settings=local.settings_qa

``manage.py`` hard-sets DJANGO_SETTINGS_MODULE, so the --settings flag is required.
"""

import os

from rest_framework.settings import api_settings

from local.settings import *  # noqa: F401,F403
from local.settings import BASE_DIR

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.getenv("NEARBEACH_QA_DB", os.path.join(BASE_DIR, "qa.sqlite3")),
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Disable blob storage credentials loaded from .env
AWS_ACCESS_KEY_ID = None
AZURE_STORAGE_CONNECTION_STRING = None

# Required after `from local.settings import *`, otherwise the login API returns 500
# ("No default throttle rate set for 'auth_minute'").
api_settings.reload()
