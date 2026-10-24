#!/usr/bin/env bash
# Fuzz the NearBeach API with Schemathesis against a throw-away database.
#
# Usage: scripts/run_schemathesis.sh [username] [-- extra schemathesis args]
#   username  fixture user to authenticate as (default: admin). Run it once per role.
#
# Env: SCHEMATHESIS_CHECKS (default not_a_server_error; use 'all' for schema/status conformance too),
#      SCHEMATHESIS_MAX_EXAMPLES (50), SCHEMATHESIS_SEED (1), SCHEMATHESIS_PASSWORD, PYTHON
# Needs: pip install -r requirements-dev.txt
set -euo pipefail
cd "$(dirname "$0")/.."

USER_NAME="${1:-admin}"; [ $# -gt 0 ] && shift
[ "${1:-}" = "--" ] && shift
PASSWORD="${SCHEMATHESIS_PASSWORD:-Test1234\$}"
PORT="${SCHEMATHESIS_PORT:-8765}"
PY="${PYTHON:-python}"

WORK="$(mktemp -d)"
export SCHEMATHESIS_DB="$WORK/fuzz.sqlite3"
export DJANGO_SETTINGS_MODULE=local.settings_schemathesis
# NOTE: manage.py hard-codes local.settings, so run django through `-m django`
# to make sure the throw-away database is used and never db.sqlite3.
DJ=("$PY" -m django)
SERVER_PID=""
trap '[ -n "$SERVER_PID" ] && kill "$SERVER_PID" 2>/dev/null; rm -rf "$WORK"' EXIT

# Safety check: refuse to run against anything but the throw-away database
"$PY" - <<'PYEOF'
import django, os
django.setup()
from django.conf import settings
name = str(settings.DATABASES["default"]["NAME"])
assert name == os.environ["SCHEMATHESIS_DB"] and not name.endswith("db.sqlite3"), f"Refusing to fuzz {name}"
PYEOF

"${DJ[@]}" migrate --noinput >/dev/null
"${DJ[@]}" loaddata NearBeach_basic_setup.json >/dev/null
"${DJ[@]}" spectacular --file "$WORK/schema.yml" >/dev/null

"${DJ[@]}" runserver "$PORT" --noreload >"$WORK/server.log" 2>&1 &
SERVER_PID=$!
for _ in $(seq 1 30); do
  curl -s -o /dev/null "http://127.0.0.1:$PORT/api/v1/coffee/" && break
  sleep 1
done

schemathesis run "$WORK/schema.yml" \
  --url "http://127.0.0.1:$PORT" \
  --auth "$USER_NAME:$PASSWORD" \
  --checks "${SCHEMATHESIS_CHECKS:-not_a_server_error}" \
  --exclude-path-regex '^/api/v1/authentication/' \
  --max-examples "${SCHEMATHESIS_MAX_EXAMPLES:-50}" \
  --seed "${SCHEMATHESIS_SEED:-1}" \
  "$@"
