#!/bin/sh
# This script creates a python venv and soft-links a few files for VSCode to work properly.
# Note: We're not going to maintain separate tooling for Windows, so please use Git Bash.
# Note 2: But because this script needs to run on Windows, we're including Windows-specific logic.

SCRIPT_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )" # copypasta from https://stackoverflow.com/a/4774063/

VENV_DIR="$SCRIPT_DIR/dev_virtual_environment"

set -e

# First parameter can be a path to a python executable. This script will use it to create the python environment.
# e.g. run it with sh create_python_virtual_environment /path/to/python
if [ ! -z $1 ]; then
    alias python=$1
    
    if [[ -z $(python -V) ]]; then echo "Your python path input might be invalid." & exit 1; fi;
fi

PYTHON_VERSION=$(python --version 2>&1 | sed -n 's/Python \([0-9]\{1,\}\.[0-9]\{1,\}\).*/\1/p')

numCompare() {
   awk -v n1="$1" -v n2="$2" 'BEGIN {printf "%s " (n1<n2?"<":">=") " %s\n", n1, n2}'
}

if awk "BEGIN {exit !($PYTHON_VERSION <= 3.10)}"; then
    echo "Please run this with at least Python 3.10. Currently" $(python -V) ". If you have multiple versions of Python installed, you may run this script using 'sh create_python_virtual_environment /path/to/python'"
    exit 1
fi


if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment"
    python -m venv "$VENV_DIR"
fi


if [ -d "$VENV_DIR/Scripts" ]; then
    echo "Linking defaultInterpreterPath for Windows"
    # venv module on Windows puts its files in a different folder structure.
    # if they can run this script, it's assumed they can run a few shell commands.
    ln -sf "$VENV_DIR/Scripts" "$VENV_DIR/bin"
fi

. "$VENV_DIR/bin/activate"

pip install -r "$SCRIPT_DIR/requirements.txt"