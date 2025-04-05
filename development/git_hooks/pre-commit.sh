#!/bin/sh

# Run with -i to install this git hook

ROOT_DIR=`git rev-parse --show-toplevel`
GIT_HOOKS_DIR=`git rev-parse --git-dir`/hooks

OUT_FILE="$GIT_HOOKS_DIR/pre-commit"

echo "Running pre-commit hooks."

set -e # exit if script errors.

if [ $1 == "-i" ]; then
    echo "Installing pre-commit hook"

    cp "$ROOT_DIR/development/git_hooks/pre-commit.sh" $OUT_FILE

    chmod +x $OUT_FILE
    
    echo "Installed successfully"

    exit 0
fi


# Reference: https://prettier.io/docs/en/precommit.html
# ACMR = Added, Copied, Modified, Renamed (no deleted)
FILES=$(git diff --cached --name-only --diff-filter=ACMR | grep '\.\(py\)$' | sed 's| |\\ |g')

if [ ! -z "$FILES"]; then
    # Prettify all selected files
    echo "$FILES" | xargs sh "$ROOT_DIR/development/run_lint.sh" --autofix

    # Add back the modified/prettified files to staging
    echo "$FILES" | xargs git add
fi

# run tests and lint checks
sh "$ROOT_DIR/development/run_tests.sh"

echo "Done running pre-commit hooks."