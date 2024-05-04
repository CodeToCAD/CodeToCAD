SCRIPT_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )" # copypasta from https://stackoverflow.com/a/4774063/

cd "$SCRIPT_DIR/.."

autoflake --recursive -v --in-place --remove-all-unused-imports --exclude=__init__.py,codetocad_types.py,development/ codetocad providers examples tests tests_integration

black .

flake8 **/*.py