#!/bin/sh

set -e # exit script if there is an error.

SCRIPT_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )" # copypasta from https://stackoverflow.com/a/4774063/

VENV_DIR="$SCRIPT_DIR/dev_virtual_environment"

if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment is not set up. Please run 'sh development/create_python_virtual_environment.sh'"
    exit 1
fi


if [ -f "$VENV_DIR/Scripts/activate" ]; then
    . "$VENV_DIR/Scripts/activate"
else
    . "$VENV_DIR/bin/activate"
fi


python -m unittest tests/test_utilities.py


export PYTHONPATH="$PYTHONPATH:$SCRIPT_DIR/../providers"
export PYTHONPATH="$PYTHONPATH:$SCRIPT_DIR/../providers/blender"


python -m unittest tests/test_provider_compliance.py


python -m unittest tests/test_provider.py