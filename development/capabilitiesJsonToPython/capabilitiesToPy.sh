#!/bin/sh

SCRIPT_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )" # copypasta from https://stackoverflow.com/a/4774063/

VENV_DIR="$SCRIPT_DIR/venv"


if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment"
    python -m venv "$VENV_DIR" || echo "Going to try running tests with python3, instead:" && python3 -m venv "$VENV_DIR"
fi

if [ -f "$VENV_DIR/Scripts/activate" ]; then
    . "$VENV_DIR/Scripts/activate"
else
    . "$VENV_DIR/bin/activate"
fi

if [ ! $(pip list | grep jinja2-cli) ]; then
    pip install jinja2-cli
fi

CORE_DIR="$SCRIPT_DIR/../../core"


jinja2 "$SCRIPT_DIR/templates/capabilitiesToPyInterface.j2" "$CORE_DIR/capabilities.json" --format=json > "$CORE_DIR/CodeToCADInterface.py"


jinja2 "$SCRIPT_DIR/templates/capabilitiesToPyProvider.j2" "$CORE_DIR/capabilities.json" --format=json > "$CORE_DIR/CodeToCADProvider.py"


jinja2 "$SCRIPT_DIR/templates/capabilitiesToPyTest.j2" "$CORE_DIR/capabilities.json" --format=json > "$CORE_DIR/TestCodeToCADProvider.py"