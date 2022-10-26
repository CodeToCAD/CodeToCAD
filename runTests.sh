#!/bin/sh

set -e # exit script if there is an error.

python -m tests.test_utilities || echo "Going to try running tests with python3, instead:" && python3 -m tests.test_utilities