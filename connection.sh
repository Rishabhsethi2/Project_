#!/bin/bash

ROOT_PATH="/home/rishabh_sethi/Projects/Project_"
VENV_PATH="$ROOT_PATH/.venv/bin/python"

cd "$ROOT_PATH" || exit 1

"$VENV_PATH" api/auth.py
