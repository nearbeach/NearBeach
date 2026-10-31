"""Settings used only by scripts/benchmark_indexes.py - points Django at a throwaway benchmark database."""

import os

from local.settings import *  # noqa: F401,F403

if os.environ.get("BENCH_ENGINE") == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("BENCH_PG_NAME", "nearbeach_bench"),
            "USER": os.environ.get("BENCH_PG_USER", "postgres"),
            "PASSWORD": os.environ.get("BENCH_PG_PASSWORD", ""),
            "HOST": os.environ.get("BENCH_PG_HOST", "localhost"),
            "PORT": os.environ.get("BENCH_PG_PORT", "5432"),
        }
    }
elif os.environ.get("BENCH_ENGINE") == "mysql":
    try:
        import pymysql

        pymysql.install_as_MySQLdb()  # Only needed when mysqlclient isn't installed
    except ImportError:
        pass
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.environ.get("BENCH_MYSQL_NAME", "nearbeach_bench"),
            "USER": os.environ.get("BENCH_MYSQL_USER", "root"),
            "PASSWORD": os.environ.get("BENCH_MYSQL_PASSWORD", ""),
            "HOST": os.environ.get("BENCH_MYSQL_HOST", "127.0.0.1"),
            "PORT": os.environ.get("BENCH_MYSQL_PORT", "3306"),
            "OPTIONS": {"charset": "utf8mb4"},
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.environ.get("BENCH_DB", os.path.join(BASE_DIR, "benchmark.sqlite3")),  # noqa: F405
        }
    }
