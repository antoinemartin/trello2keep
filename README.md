# Groceries

Create a CSV file with grocery lists from Trello JSON exports.

## Description

This tool exports cards from specified lists in a Trello JSON export file to format suitable for the creation of a Google Keep note. It's designed to help manage grocery lists by extracting items from Trello boards and converting them to a more portable CSV format.

## Requirements

- Python >= 3.13
- UV package manager

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
# Run the application
uv run groceries <json_file> <list_names...>

# Example: Export items from 'Lidl' and 'Carrefour' lists
uv run groceries courses.json Lidl Carrefour

# Or run directly with Python
uv run python -m groceries.main courses.json Lidl Carrefour
```

### Arguments

- `json_file`: Path to the Trello JSON export file
- `list_names`: Names of the lists to export (space-separated)

## TODO

- [ ] Implement automatic download of JSON file from Trello URL with proper credentials
  - Target URL format: `https://trello.com/b/iVKNyGyE/courses.json`
  - Need to handle authentication for private boards

## Development

```bash
# Install development dependencies
uv sync --group dev

# Run tests
uv run pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure everything works
5. Submit a pull request

## License

This project is licensed under the MIT License - see the project metadata for details.

## Author

Antoine Martin (antoine.martin@octave.biz)
