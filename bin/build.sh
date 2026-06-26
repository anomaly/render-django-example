#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
uv sync --frozen
uv cache prune --ci

# Convert static asset files
uv run python src/manage.py tailwind install
uv run python src/manage.py tailwind build
uv run python src/manage.py collectstatic --no-input

# Apply any outstanding database migrations
uv run python src/manage.py migrate
