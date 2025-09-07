# Repository Guidelines

## Project Structure & Module Organization
- `src/api/`: FastAPI app and routes (entrypoint `src.api.app:app`; `/health`, `/tools/*`).
- `src/client/`: ElevenLabs client helpers (agents, tools, phone numbers, pronunciation).
- `src/utils/`: Utilities (e.g., `logging_config.py`, `prompt_utils.py`).
- `src/prompts/`: Prompt templates used by agents/tools.
- `src/config.py`: Environment-driven settings. `src/demo.py`: local demo script.
- `deploy/`: Container build and compose files.

## Build, Test, and Development Commands
- Local (uv recommended):
  - `uv sync` — install deps from `pyproject.toml`/`uv.lock` into a venv.
  - `uv run uvicorn src.api.app:app --reload` — start API for local dev.
- Uvicorn without uv (if deps already installed): `uvicorn src.api.app:app --reload`.
- Docker (compose): `docker compose -f deploy/docker-compose.yml up --build`.
- Docker (manual): `docker build -f deploy/Dockerfile -t elevenlabs-ai . && docker run --rm -p 8000:8000 --env-file .env elevenlabs-ai`.
- Health check: `curl http://localhost:8000/health`.

## Coding Style & Naming Conventions
- Python 3.10+, PEP 8, 4-space indentation, type hints encouraged.
- Names: `snake_case` for modules/functions/variables; `CamelCase` for classes.
- Keep functions small; add docstrings describing purpose and inputs/outputs.
- Use `logging.getLogger(__name__)` and central config in `src/utils/logging_config.py`.

## Testing Guidelines
- Current repo has no tests; add `pytest`-based tests under `tests/` mirroring `src/` (e.g., `tests/api/test_tools.py`).
- File naming: `test_*.py`; function naming: `test_*`.
- Run: `pytest -q` (add to dev deps as needed). Aim to cover API happy paths, validation errors, and edge cases.

## Commit & Pull Request Guidelines
- Prefer Conventional Commits (seen: `build:`, `chore:`): `feat:`, `fix:`, `docs:`, `build:`, `chore:`.
- Commit messages: imperative, concise subject; details/rationale in body when helpful.
- PRs: clear description, linked issues, test steps (e.g., `curl` examples), screenshots/logs when relevant, and README/docs updates.

## Security & Configuration Tips
- Use `.env` for secrets: `ELEVENLABS_API_KEY`, `AGENT_ID`, `VOICE_ID`, `MAX_RETRIES`, `SESSION_TTL_SECONDS`, etc. Never commit secrets.
- Pass env via Compose `env_file` or `--env-file` in `docker run`. Consider adding `.env` to `.dockerignore` to avoid sending it in build context.
- Avoid logging PII; validate and sanitize inputs in server tool endpoints.

