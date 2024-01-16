#!/bin/sh

set -e

# this scripts copies files from ./git_hooks into ../.git/
SCRIPT_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )" # copypasta from https://stackoverflow.com/a/4774063/

GIT_HOOKS_DIR=`git rev-parse --git-dir`/hooks

cp "$SCRIPT_DIR/git_hooks/pre-commit.sh" "$GIT_HOOKS_DIR/pre-commit"
chmod +x "$GIT_HOOKS_DIR/pre-commit"

echo "git hooks installed successfully"