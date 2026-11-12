@AGENTS.md

## Claude-specific notes
- Deep system map: @Architecture.md
- Manual browser QA: use the `manual-qa` skill. Run Django with `--settings=local.settings_qa` (console email, no S3/Azure, separate `qa.sqlite3`), never plain `local.settings`. `.env` is deny-listed in `.claude/settings.json`.
- `manage.py` hard-sets `DJANGO_SETTINGS_MODULE`, so the `--settings` flag is required.
- Keep the Browser pane visible while testing or Vue transitions stall and screenshots go blank.
- QA findings are reported as Method / Expected Results / Actual Results per finding, with no fixes unless asked.
- After changing structure, patterns or commands, update `Architecture.md` / `AGENTS.md` and run `python3 scripts/check_agent_docs.py`.
