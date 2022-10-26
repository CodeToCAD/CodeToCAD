#!/bin/sh

ROOT_DIR=`git rev-parse --show-toplevel`

echo "Running pre-commit hooks."

sh "$ROOT_DIR/runTests.sh"

echo "Done running pre-commit hooks."