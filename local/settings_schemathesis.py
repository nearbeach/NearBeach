"""Settings used ONLY for Schemathesis fuzz runs (local + CI).

Never point this at a real database - Schemathesis will create, change and delete data.
Set SCHEMATHESIS_DB to the sqlite file the run should use (a throw-away file).
"""
import os

from local.settings import *  # noqa: F401,F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ["SCHEMATHESIS_DB"],
    }
}

# Fuzzing makes thousands of requests - the throttles would just return 429s
REST_FRAMEWORK = {
    **REST_FRAMEWORK,  # noqa: F405
    "DEFAULT_THROTTLE_CLASSES": [],
    "DEFAULT_THROTTLE_RATES": {
        **REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"],  # noqa: F405
        "anon": "100000/min",
        "user": "100000/min",
        "auth_minute": "100000/min",
        "auth_hour": "100000/hour",
    },
}

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# local.settings reads api_settings while it is still importing, which caches DRF's
# defaults before REST_FRAMEWORK exists here - throw the cache away.
from rest_framework.settings import api_settings  # noqa: E402

api_settings.reload()
