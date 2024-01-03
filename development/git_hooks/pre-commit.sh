#!/bin/sh

ROOT_DIR=`git rev-parse --show-toplevel`

set -e # exit if script errors.

# Reference: https://prettier.io/docs/en/precommit.html
# ACMR = Added, Copied, Modified, Renamed (no deleted)
FILES=$(git diff --cached --name-only --diff-filter=ACMR | grep '\.\(py\)$' | sed 's| |\\ |g')
[ -z "$FILES" ] && exit 0

# Prettify all selected files
echo "$FILES" | xargs black

# Add back the modified/prettified files to staging
echo "$FILES" | xargs git add

# NO_EMPTY=git diff --cached --exit-code
# if [ $NO_EMPTY -eq 0 ]
# then
#     echo "Black formatting resulted in an empty commit, cancelling!"
#     exit 1
# fi

# Mark: run tests  and lint checks
sh "$ROOT_DIR/development/run_tests.sh"

sh "$ROOT_DIR/development/run_lint.sh"

echo "Done running pre-commit hooks."