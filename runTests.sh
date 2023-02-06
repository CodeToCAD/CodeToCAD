#!/bin/sh

set -e # exit script if there is an error.

SCRIPT_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )" # copypasta from https://stackoverflow.com/a/4774063/

VENV_DIR="$SCRIPT_DIR/development/developmentVirutalEnvironment"

if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment is not set up. Please run 'sh development/createPythonVirtualEnvironment.sh'"
    exit 1
fi


if [ -f "$VENV_DIR/Scripts/activate" ]; then
    . "$VENV_DIR/Scripts/activate"
else
    . "$VENV_DIR/bin/activate"
fi


python -m tests.test_utilities


export PYTHONPATH="$PYTHONPATH:$SCRIPT_DIR/providers"
export PYTHONPATH="$PYTHONPATH:$SCRIPT_DIR/providers/blender"


python -m tests.test_provider_compliance


python -m tests.test_providers