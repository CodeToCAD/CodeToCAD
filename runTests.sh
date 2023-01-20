#!/bin/sh

SCRIPT_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )" # copypasta from https://stackoverflow.com/a/4774063/

set -e # exit script if there is an error.

python -m tests.test_utilities || echo "Going to try running tests with python3, instead:" && python3 -m tests.test_utilities


export PYTHONPATH=$PYTHONPATH:"$SCRIPT_DIR/providers"
export PYTHONPATH=$PYTHONPATH:"$SCRIPT_DIR/providers/blender"

python -m tests.test_provider_compliance || echo "Going to try running tests with python3, instead:" && python3 -m tests.test_provider_compliance


python -m tests.test_provider || echo "Going to try running tests with python3, instead:" && python3 -m tests.test_provider