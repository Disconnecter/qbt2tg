# Repository Guidelines

## Project Structure & Module Organization
- `bot.py` is the main entrypoint that wires Telegram handlers and the job queue.
- `handlers/` contains command, button, and upload handlers split by feature.
- `qbittorrent_api.py`, `torrent_notify.py`, and `utils.py` hold API access, completion checks, and shared helpers.
- `config.py` is local configuration (copy from `config_sample.py`); `sanitize_rules.txt` defines name cleanup rules.
- `service/` contains launchd assets for running as a macOS service.
- Runtime artifacts include `notified.txt` and `bot.out.log`/`bot.err.log`; avoid committing these.

## Build, Test, and Development Commands
- `python3 bot.py` runs the bot in the foreground once `config.py` is set.
- `./setup.sh` creates `venv/`, installs dependencies, and registers a launchd service.
- `source venv/bin/activate` then `pip install python-telegram-bot qbittorrent-api apscheduler` mirrors the README install.
- `tail -f bot.out.log` or `tail -f bot.err.log` to watch service logs when using launchd.

## Coding Style & Naming Conventions
- Python, 4-space indentation, and PEP 8–style formatting.
- `snake_case` for functions/variables, `PascalCase` for classes, and `UPPER_CASE` for config constants.
- Keep handler functions action-named (e.g., `handle_torrent_file`, `send_main_menu`).

## Testing Guidelines
- No automated test suite is present. If you add one, use `pytest` and place files under `tests/` with `test_*.py`.
- Manual checks should cover: startup, adding a torrent, listing/removing torrents, and completion notifications.

## Commit & Pull Request Guidelines
- History shows short, direct messages (e.g., “fix active torrents action”, “Update README.md”). Keep commits concise and present-tense.
- PRs should include: a brief summary, test steps, and any config/service changes (especially `config.py`, launchd, or dependency updates).

## Configuration & Secrets
- Copy `config_sample.py` to `config.py` and keep tokens/credentials local.
- Update `SANITIZE_FILE` rules in `sanitize_rules.txt` instead of hardcoding cleanup logic.
