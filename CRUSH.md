# CRUSH.md - Development Guidelines for trello2keep

## Build & Dependency Management

-   Use **UV package manager** (not pip) for all Python operations
-   Install dependencies: `uv sync --group dev`
-   Add new dependencies: `uv add <package>` or `uv add --group dev <package>`

## Running the Application

-   Main entry: `uv run trello2keep "Board Name" "List 1" "List 2"`
-   Direct module: `uv run python -m trello2keep.main`

## Code Quality Commands

-   Lint & format: `uv run ruff check .` and `uv run ruff format .`
-   Type checking: `uv run mypy .`
-   Security scan: `uv run bandit -r src/`
-   Run all checks: `pre-commit run --all-files`

## Testing

-   Run all tests: `uv run pytest`
-   Run specific test file: `uv run pytest tests/test_file.py`
-   Run single test: `uv run pytest tests/test_file.py::test_function_name`
-   Run with coverage: `uv run pytest --cov=src`

## Code Style Guidelines

-   Python 3.13+ required
-   Use Ruff for formatting (replaces Black/isort)
    -   Single quotes for strings
    -   Line length: 120 characters
    -   Combine import statements
-   Type hints required throughout
-   Google docstring convention
-   Use Click for CLI interfaces with click.secho() for colored output
-   Error handling via click.ClickException for user-friendly messages

## Project Conventions

-   Single script entry point via `trello2keep` command
-   Case-insensitive Trello list matching
-   Unified credentials.json for Trello and Google APIs
-   Google Keep uses domain-wide delegation with user impersonation
-   Follow existing import organization (stdlib, third-party, first-party)

## Authentication Pattern

```json
{
    "trello": { "api_key": "...", "token": "..." },
    "type": "service_account",
    "private_key": "..."
}
```

## Copilot Instructions Summary

-   Follow all guidelines in `.github/copilot-instructions.md`
-   Use UV commands for all Python execution
-   Google API modules marked as untyped in mypy config
-   Special French grocery optimization in `ordering_instructions.md`
