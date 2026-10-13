from local.settings import *


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]
LANGUAGE_CODE = "en-us"
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

DJANGO_VITE = {
    **DJANGO_VITE,
    "default": {
        **DJANGO_VITE.get("default", {}),
        "dev_mode": True,
        "dev_server_host": "localhost",
        "dev_server_port": 5173,
    },
}
