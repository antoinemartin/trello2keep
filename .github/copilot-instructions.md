# Copilot Instructions for trello2keep

## Project Architecture

This is a Python CLI tool that extracts items from Trello lists and creates
Google Keep notes. The project uses:

-   **UV package manager** (not pip) for dependency management and project
    execution
-   **Google APIs** with service account authentication and domain-wide
    delegation
-   **Trello API** for board and list data extraction
-   **Click** for command-line interface

### Key Components

-   `src/trello2keep/main.py`: CLI entry point with Google Keep integration
-   `src/trello2keep/trello.py`: Trello API client for board/list operations
-   `credentials.json`: Contains both Trello API keys and Google service account
    credentials in single file

## Development Workflow

### Environment Setup

```bash
# Install dependencies (NOT pip install)
uv sync --group dev

# Setup pre-commit hooks
./scripts/setup-dev.sh
```

### Running the Application

```bash
# Use uv run, not direct python execution
uv run trello2keep "Board Name" "List 1" "List 2"

# Or via module
uv run python -m trello2keep.main
```

### Code Quality Tools

-   **Ruff**: Primary linter and formatter (replaces black, isort, flake8)
-   **mypy**: Type checking with Google API overrides in pyproject.toml
-   **pre-commit**: Enforces all quality checks before commits
-   **Python 3.13+**: Minimum version requirement

## Authentication Pattern

The project uses a **unified credentials file** containing both APIs:

```json
{
    "trello": { "api_key": "...", "token": "..." },
    "type": "service_account",
    "private_key": "..."
    // ... other Google service account fields
}
```

Google Keep uses **domain-wide delegation** with user impersonation
(`DEFAULT_IMPERSONATED_USER_EMAIL`).

## Project-Specific Conventions

1. **Single script entry point**: All functionality accessible via `trello2keep`
   command
2. **Case-insensitive list matching**: Trello list names matched without case
   sensitivity
3. **Dual note formats**: Text notes (reorderable) vs checklist notes (with
   checkboxes)
4. **French grocery optimization**: Special `ordering_instructions.md` for
   store-specific item sorting

## Integration Points

-   **Trello API**: Board/list data via REST API with key+token auth
-   **Google Keep API**: Note creation via service account with user
    impersonation
-   **CLI arguments**: Board name + variable list names as positional arguments

## Common Patterns

-   Use `click.secho()` for colored terminal output
-   Error handling via `click.ClickException` for user-friendly messages
-   Type hints throughout with Google API modules marked as untyped in mypy
    config
-   UV commands for all Python execution (not direct python calls)
