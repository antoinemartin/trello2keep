# trello2keep

Create a Google Keep note with items from Trello lists.

## Description

This tool exports cards from specified lists in a Trello board and creates a
formatted Google Keep note with those items. It's designed to help manage todo
lists by extracting items from Trello boards and converting them to a more
portable format that can be easily accessed and checked off on mobile devices.

I personally use this tool to manage my errands and tasks on my digital watch,
where I can quickly check off items as I complete them.

The application connects to both the Trello API to fetch list items and the
Google Keep API to create notes. It supports domain-wide delegation for Google
Workspace environments, allowing service accounts to impersonate users when
creating notes.

### Key Features

-   **Trello Integration**: Extract items from multiple lists on any Trello
    board
-   **Google Keep Integration**: Create formatted notes with proper sections
-   **AI-Powered Filtering**: Use LLMs to intelligently filter, organize, and
    categorize items with custom prompts (powered by
    [Pythonic AI](https://ai.pydantic.dev/))
-   **Multiple AI Models**: Support for various AI providers (Azure OpenAI,
    OpenAI) with customizable model selection
-   **Flexible Configuration**: Customize board IDs, note titles, and user
    impersonation
-   **Multiple List Support**: Process multiple Trello lists in a single run
-   **Case-Insensitive Matching**: List names are matched case-insensitively for
    convenience
-   **Dual Note Formats**: Create either text notes (reorderable) or checklist
    notes (with checkboxes)
-   **Custom Organization**: Support for custom item ordering (see
    `ordering_instructions_sample.md` for template)

## Requirements

-   Python >= 3.13
-   UV package manager

## Getting Started

1. Clone this repository
2. Navigate to the project directory
3. Follow the installation instructions below

## Installation

```bash
# Install dependencies using UV
uv sync

# Or install in development mode with dev dependencies
uv sync --group dev
```

## Usage

```bash
Usage: trello2keep [OPTIONS] TRELLO_BOARD [LIST_ITEMS]...

  Extract items from Trello lists and create a Google Keep note.

  This command extracts items from specified Trello lists and creates a
  formatted Google Keep note. Specify list names as arguments.

  Example: trello2keep Kanban Ongoing Validating

Options:
  --credentials PATH              Path to credentials file.  [default:
                                  credentials.json]
  --title TEXT                    Title of the Google Keep note. Name of the
                                  Trello board will be used if not specified.
  --impersonated-user-email TEXT  Email address of the user to impersonate.
                                  [default: antoine@openance.com]
  --text / --no-text              Create a text note instead of a checklist
                                  note. Default is False (checklist note).
  --ai-filter PATH                Path to a markdown file with system prompt
                                  to filter items via LLM.
  --ai-model TEXT                 Model identifier. Prefix with provider (e.g.,
                                  azure:gpt-4o).  [default: azure:gpt-4o]
  --help                          Show this message and exit.
```

### Examples

```bash
# Run the application with default settings
uv run trello2keep Kanban Developing Validating

# Specify a custom credentials file
uv run trello2keep --credentials /path/to/creds.json Kanban Developing Validating

# Customize the Google Keep note title
uv run trello2keep --title "Weekly Task List" Kanban Developing Validating

# Use a different impersonated user email for Google Keep
uv run trello2keep --impersonated-user-email user@company.com Kanban Developing Validating

# Create a text note instead of checklist
uv run trello2keep --text Kanban Developing Validating

# Use AI filtering with a custom system prompt
uv run trello2keep --ai-filter ./filter_prompt.md Kanban Developing Validating

# Use a different AI model for filtering
uv run trello2keep --ai-model openai:gpt-4 --ai-filter ./grocery_filter.md Kanban Shopping Lists

# Combine multiple options including AI filtering
uv run trello2keep \
  --credentials ./my-creds.json \
  --title "Organized Shopping List" \
  --ai-filter ./store_layout_filter.md \
  --ai-model azure:gpt-4o \
  --text \
  Kanban \
  Developing Validating "Ready for QA"

# Or run directly with Python
uv run python -m trello2keep.main Kanban Developing Validating
```

### Arguments and Options

#### Positional Arguments

-   `TRELLO_BOARD`: The name of the Trello board to extract items from. This is
    a required positional argument.
-   `LIST_ITEMS`: Names of the lists to export from Trello (space-separated).
    These correspond to the names of lists in your Trello board. List names are
    case-insensitive.

#### Options

-   `--credentials PATH`: Path to the credentials JSON file (default:
    `credentials.json`). This file should contain both Trello API credentials
    and Google service account credentials.
-   `--title TEXT`: Title for the created Google Keep note. If not specified,
    the Trello board name will be used as the title.
-   `--impersonated-user-email TEXT`: Email address of the user to impersonate
    when creating the Google Keep note (default: `antoine@openance.com`). This
    requires domain-wide delegation to be properly configured.
-   `--text / --no-text`: Create a text note instead of a checklist note.
    Default is False (checklist note).
-   `--ai-filter PATH`: Path to a markdown file containing a system prompt that
    will be used to filter and organize items via a Large Language Model (LLM).
    This enables intelligent filtering and categorization of items.
-   `--ai-model TEXT`: Model identifier for the AI filtering feature (default:
    `azure:gpt-4o`). Follows the same syntax as the pydantic-ai CLI with
    provider prefixes (e.g., `azure:gpt-4o`, `openai:gpt-4`,
    `gemini:gemini-1.5-pro`). See
    [pydantic-ai model selection](https://ai.pydantic.dev/cli/#choose-a-model)
    for complete syntax reference. Requires appropriate API credentials.

#### Examples of Usage

```bash
# Common project stages
uv run trello2keep "My Board" "To Do" "In Progress" "Done"

# Category-based lists
uv run trello2keep "Project Board" "Frontend Tasks" "Backend Tasks" "DevOps"

# Team and status combinations
uv run trello2keep "Team Board" "Team A - In Progress" "Team B - Blocked" "Ready for Review"

# AI-filtered grocery shopping with store layout optimization
uv run trello2keep --ai-filter ./grocery_filter.md "Shopping Board" "Groceries" "Household Items"

# AI-filtered task management with priority organization
uv run trello2keep --ai-filter ./task_priority_filter.md --ai-model openai:gpt-4 "Project Board" "Backlog" "Sprint"
```

## Getting the Trello Token

The `credentials.json` file should contain the appropriate credentials for
accessing both the Trello API and Google Keep API.

### Trello API Setup

To obtain your Trello API credentials, follow these steps:

1. **Get your API Key**: Visit the
   [Trello Power-Ups Admin page](https://trello.com/power-ups/admin) and create
   a new Power-Up to generate your API key.

2. **Generate a Token**: Once you have your API key, authorize the application
   by visiting the following URL (replace `<your_api_key>` with your actual API
   key):

    ```
    https://trello.com/1/authorize?expiration=never&scope=read&response_type=token&key=<your_api_key>
    ```

3. **Authorize Access**: Click "Allow" to grant read access to your Trello
   boards. The token will be displayed on the resulting page.

4. **Save Credentials**: Copy both the API key and token to use in your
   `credentials.json` file.

> **Note**: The token is set to never expire and only requires read access to
> your boards, ensuring minimal permissions while maintaining functionality.

After authorizing the application, you will receive a token that should be
placed in the `credentials.json` file under the `trello` key.

### Google Keep API Setup

For Google Keep access, you'll need to set up a service account with domain-wide
delegation:

1. Create a service account in the Google Cloud Console
2. Enable the Google Keep API for your project
3. Configure domain-wide delegation for the service account on the following
   scopes:

```text
https://www.googleapis.com/auth/keep,
https://www.googleapis.com/auth/keep.readonly,
https://www.googleapis.com/auth/userinfo.email
```

4. Download the service account key JSON file
5. The service account credentials should be placed directly in the
   `credentials.json` file

### Credentials File Format

Your `credentials.json` file should look like this:

```json
{
    "trello": {
        "api_key": "your_api_key",
        "token": "ATT..."
    },
    "type": "service_account",
    "project_id": "your-project-id",
    "private_key_id": "key-id",
    "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
    "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
    "client_id": "client-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
}
```

## Advanced Features

### Custom Item Ordering

The application supports custom ordering of items for optimized shopping
experiences. This is particularly useful for grocery lists where items can be
organized by store layout.

#### Creating Ordering Instructions

1. Copy the sample template:
   `cp ordering_instructions_sample.md ordering_instructions.md`
2. Customize the categories and order based on your preferred store layout
3. The application will automatically use `ordering_instructions.md` if present

For detailed examples and formatting guidelines, see
`ordering_instructions_sample.md`.

## Troubleshooting

### Common Issues

#### "ModuleNotFoundError: No module named 'google'"

This means the dependencies haven't been installed. Run:

```bash
uv sync
```

#### "Error: Trello credentials not found in the credentials file."

Ensure your `credentials.json` file has a `trello` section with `api_key` and
`token` fields.

#### Google Keep API errors

-   Ensure your service account has domain-wide delegation enabled
-   Verify the impersonated user email is in the same domain as your service
    account
-   Check that the Google Keep API is enabled for your project

#### "Invalid JSON file" or "Failed to extract items from Trello"

-   Verify your Trello board name is correct
-   Check that the specified list names exist on your board (case-insensitive)
-   Ensure your Trello token has read access to the board

## Development

### Quick Setup

Use the provided setup script for a complete development environment:

```bash
# Run the setup script (recommended)
./scripts/setup-dev.sh
```

This script will:

-   Install all dependencies including dev dependencies
-   Set up pre-commit hooks
-   Run initial code quality checks

### Manual Setup

If you prefer to set up manually:

```bash
# Install development dependencies
uv sync --group dev

# Set up pre-commit hooks for code quality
uv run pre-commit install

# Run pre-commit hooks manually on all files (optional)
uv run pre-commit run --all-files

# Run tests
uv run pytest
```

### Code Quality Tools

This project uses several tools to maintain code quality:

-   **Ruff**: Fast Python linter and formatter (replaces Black, isort, flake8)
-   **mypy**: Static type checker
-   **Bandit**: Security linter
-   **pre-commit**: Automatically runs quality checks on commit

Most tools are automatically run via pre-commit hooks on every commit. You can
also run them manually:

```bash
# Lint and format with Ruff
uv run ruff check src tests
uv run ruff format src tests

# Type check with mypy
uv run mypy src tests

# Security check with Bandit
uv run bandit -r src

# Run all pre-commit hooks manually
uv run pre-commit run --all-files
```

### Project Structure and Guidelines

This project follows specific development conventions:

-   **Package Manager**: Uses UV exclusively (not pip) for all Python operations
-   **Code Style**: Ruff formatting with 120-character line length, single
    quotes
-   **Type Checking**: Type hints required throughout with mypy validation
-   **CLI Framework**: Click for command-line interfaces with colored output
-   **Error Handling**: User-friendly errors via `click.ClickException`
-   **Python Version**: Requires Python 3.13 or higher

For detailed development guidelines, see:

-   `CRUSH.md` - Quick reference for common development tasks
-   `.github/copilot-instructions.md` - AI coding assistant guidelines

### Testing

```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src

# Run specific test file
uv run pytest tests/test_file.py

# Run single test function
uv run pytest tests/test_file.py::test_function_name
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Set up the development environment:
    ```bash
    uv sync --group dev
    uv run pre-commit install
    ```
4. Make your changes
5. Run tests and ensure code quality checks pass:
    ```bash
    uv run pytest
    uv run pre-commit run --all-files
    ```
6. Submit a pull request

## License

This project is licensed under the MIT License - see the project metadata for
details.

## Author

Antoine Martin (antoine@mrtn.fr)
