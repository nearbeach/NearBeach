---
name: manual-qa
description: Run NearBeach locally for manual browser testing without touching the real dev DB, SMTP or S3, and report findings in the Method / Expected / Actual format. Use for QA, regression checks or visual verification.
---

# Manual QA

## Safety first
`.env` holds real SMTP and S3 credentials and `local/settings.py` uses them. Never run plain dev settings for QA. Use `local/settings_qa.py`, which wraps them: console email backend, blob-storage keys nulled, and a separate database (`qa.sqlite3`, git-ignored, override with `NEARBEACH_QA_DB`). It also calls `api_settings.reload()`, which is required or login returns 500 ("No default throttle rate set for 'auth_minute'").

## Setup
1. `cp db.sqlite3 qa.sqlite3`
2. Set a known password on the copied users (seed users: `admin`, `team_leader`, `team_member`, `team_intern`, `read_only`, `read_only_extra`, `team_no_permissions`, `no_group`, `dark_admin`), e.g. in `venv/bin/python manage.py shell --settings=local.settings_qa`.
3. Start both servers (or `preview_start` with `nearbeach-vite` and `nearbeach-django-qa` from `.claude/launch.json`):
   - Vite: `npm run dev -- --host localhost --port 5173 --strictPort`
   - Django: `venv/bin/python manage.py runserver 8000 --settings=local.settings_qa` (`manage.py` hard-sets `DJANGO_SETTINGS_MODULE`, so the flag is required).
4. Keep the Browser pane visible: when hidden, Vue transitions stall and screenshots are blank.

## Reporting
For each finding give **Method** (steps), **Expected Results**, **Actual Results**. Report only; do not fix unless asked. Example: `QA_REPORT_2026-11-12.md`.
