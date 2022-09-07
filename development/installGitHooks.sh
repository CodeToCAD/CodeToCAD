#!/bin/sh

# this scripts copies files from ./gitHooks into ../.git/
SCRIPT_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )" # copypasta from https://stackoverflow.com/a/4774063/

GIT_HOOKS_DIR=`git rev-parse --git-dir`/hooks

cp "$SCRIPT_DIR/gitHooks/pre-commit.sh" "$GIT_HOOKS_DIR/pre-commit"