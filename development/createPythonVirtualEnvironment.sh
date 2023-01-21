#!/bin/sh

SCRIPT_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )" # copypasta from https://stackoverflow.com/a/4774063/

VENV_DIR="$SCRIPT_DIR/developmentVirutalEnvironment"


if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment"
    python -m venv "$VENV_DIR" || echo "Going to try running tests with python3, instead:" && python3 -m venv "$VENV_DIR"
fi

if [ -f "$VENV_DIR/Scripts/activate" ]; then
    . "$VENV_DIR/Scripts/activate"
else
    . "$VENV_DIR/bin/activate"
fi

pip install -r "$SCRIPT_DIR/requirements.txt"