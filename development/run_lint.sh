SCRIPT_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )" # copypasta from https://stackoverflow.com/a/4774063/

cd "$SCRIPT_DIR/.."

autoflake --in-place --remove-all-unused-imports **/*.py

black .

flake8 **/*.py