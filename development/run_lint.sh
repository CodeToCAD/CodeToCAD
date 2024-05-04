SCRIPT_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )" # copypasta from https://stackoverflow.com/a/4774063/

cd "$SCRIPT_DIR/.."

if [ $1 == "--autofix" ]; then

    FILES="${@:2}"

    echo "Autofixing $FILES" 

    if [ -z $FILES ]; then
        FILES="codetocad providers examples tests tests_integration"
    fi

    autoflake --recursive -v --in-place --remove-all-unused-imports --exclude=__init__.py,codetocad_types.py,development/ $FILES

    black $FILES
fi

flake8 **/*.py