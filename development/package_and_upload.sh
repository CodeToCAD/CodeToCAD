#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )" # copypasta from https://stackoverflow.com/a/4774063/

cd "$SCRIPT_DIR/.."

rm -rf ./build/*
rm -rf ./codetocad.egg-info/*
rm -rf ./dist/*
python setup.py sdist bdist_wheel
twine check dist/*
twine upload -r pypi dist/* --config-file ./.pypirc --verbose