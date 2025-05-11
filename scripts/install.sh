#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Usage: ./scripts/install.sh PACKAGE_NAME"
  echo "Example: ./scripts/install.sh fastapi"
  echo "Description: Install a package with uv at latest version, then update requirements.txt with locked version"
  exit 1
fi

uv pip install "$@" && uv pip freeze > requirements.txt