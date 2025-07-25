#!/usr/bin/env bash
# Setup script for pre-commit hooks

set -e

echo "🔧 Setting up development environment..."

# Install dependencies
echo "📦 Installing dependencies..."
uv sync --group dev

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
uv run pre-commit install

# Run pre-commit on all files to ensure everything is working
echo "✅ Running pre-commit hooks on all files..."
uv run pre-commit run --all-files

echo "🎉 Development environment setup complete!"
echo "Pre-commit hooks are now installed and will run automatically on commit."
echo ""
echo "You can manually run pre-commit with:"
echo "  uv run pre-commit run --all-files"
echo ""
echo "To run individual tools:"
echo "  uv run black src tests"
echo "  uv run isort src tests"
echo "  uv run ruff check src tests"
echo "  uv run mypy src tests"
echo "  uv run pytest"
