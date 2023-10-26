#!/bin/sh

ROOT_DIR=`git rev-parse --show-toplevel`

set -e # exit if script errors.

echo "Running pre-commit hooks."

sh "$ROOT_DIR/development/run_tests.sh"

sh "$ROOT_DIR/development/run_lint.sh"

echo "Done running pre-commit hooks."