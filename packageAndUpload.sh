#!/usr/bin/env bash

rm -rf ./build/*
rm -rf ./CodeToCAD.egg-info/*
rm -rf ./dist/*
python setup.py sdist bdist_wheel
twine check dist/*
twine upload -r pypi dist/* --config-file ./.pypirc --verbose