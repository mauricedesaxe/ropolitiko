#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Usage: ./scripts/db-migrate.sh MIGRATION_MESSAGE"
  echo "Example: ./scripts/db-migrate.sh \"Add news article\""
  echo "Description: Generate a new alembic migration with autogenerate"
  exit 1
fi

alembic revision --autogenerate -m "$1" 