# Groceries

Create a Google Keep note with items from Trello lists.

## Description

This tool exports cards from specified lists in a Trello board and creates a
formatted Google Keep note with those items. It's designed to help manage
grocery lists by extracting items from Trello boards and converting them to a
more portable format that can be easily accessed and checked off on mobile
devices.

The application connects to both the Trello API to fetch list items and the
Google Keep API to create notes. It supports domain-wide delegation for Google
Workspace environments, allowing service accounts to impersonate users when
creating notes.

### Key Features

-   **Trello Integration**: Extract items from multiple lists on any Trello
    board
-   **Google Keep Integration**: Create formatted notes with proper sections
-   **Flexible Configuration**: Customize board IDs, note titles, and user
    impersonation
-   **Multiple List Support**: Process multiple Trello lists in a single run
-   **Case-Insensitive Matching**: List names are matched case-insensitively for
    convenience

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
Usage: groceries [OPTIONS] [LIST_ITEMS]...

  Extract items from Trello lists and create a Google Keep note.

Options:
  --credentials PATH              Path to Google API credentials file.
  --trello-board-id TEXT          Trello board ID to extract items from.
  --title TEXT                    Title of the Google Keep note.
  --impersonated-user-email TEXT  Email address of the user to impersonate.
  --help                          Show this message and exit.
```

### Examples

```bash
# Run the application with default settings
uv run groceries Lidl Carrefour

# Specify a custom credentials file
uv run groceries --credentials /path/to/creds.json Lidl Carrefour

# Use a different Trello board ID
uv run groceries --trello-board-id your_board_id Lidl Carrefour

# Customize the Google Keep note title
uv run groceries --title "Weekly Shopping List" Lidl Carrefour

# Use a different impersonated user email for Google Keep
uv run groceries --impersonated-user-email user@company.com Lidl Carrefour

# Combine multiple options
uv run groceries \
  --credentials ./my-creds.json \
  --trello-board-id abc123 \
  --title "Grocery Shopping" \
  --impersonated-user-email shopper@company.com \
  Lidl Carrefour "Whole Foods"

# Or run directly with Python
uv run python -m groceries.main Lidl Carrefour
```

### Arguments and Options

#### Positional Arguments

-   `LIST_ITEMS`: Names of the lists to export from Trello (space-separated).
    These correspond to the names of lists in your Trello board. List names are
    case-insensitive.

#### Options

-   `--credentials PATH`: Path to the credentials JSON file (default:
    `credentials.json`). This file should contain both Trello API credentials
    and Google service account credentials.
-   `--trello-board-id TEXT`: The unique identifier for your Trello board
    (default: `iVKNyGyE`). You can find this ID in your Trello board's URL.
-   `--title TEXT`: Title for the created Google Keep note (default:
    `Shopping List`).
-   `--impersonated-user-email TEXT`: Email address of the user to impersonate
    when creating the Google Keep note (default: `antoine@openance.com`). This
    requires domain-wide delegation to be properly configured.

#### Examples of List Names

```bash
# Common grocery store names
uv run groceries Lidl Carrefour "Whole Foods" Target

# Category-based lists
uv run groceries Produce Dairy Meat Bakery

# Store and category combinations
uv run groceries "Lidl - Groceries" "Lidl - Household" "Online Orders"
```

## Getting the Trello Token

The `credentials.json` file should contain the appropriate credentials for
accessing both the Trello API and Google Keep API.

### Trello API Setup

The API key is `a947b9efafb4b833d41b6ba4a798f168`.

The token should be obtained by following this link:

https://trello.com/1/authorize?expiration=never&scope=read&response_type=token&key=a947b9efafb4b833d41b6ba4a798f168

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
        "api_key": "a947b9efafb4b833d41b6ba4a798f168",
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

-   Verify your Trello board ID is correct
-   Check that the specified list names exist on your board (case-insensitive)
-   Ensure your Trello token has read access to the board

### Debug Mode

To see the extracted items before they're sent to Google Keep, the application
prints the items as JSON to stdout. This can help verify that the correct items
are being extracted from Trello.

## Development

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

-   **Ruff**: Fast Python linter and formatter
-   **mypy**: Static type checker
-   **Bandit**: Security linter
-   **Safety**: Dependency vulnerability checker (run manually)

Most tools are automatically run via pre-commit hooks on every commit. You can
also run them manually:

```bash
# Lint with Ruff
uv run ruff check src tests

# Type check with mypy
uv run mypy src tests

# Security check with Bandit
uv run bandit -r src

# Check for vulnerabilities with Safety (run periodically)
uv run safety check
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
