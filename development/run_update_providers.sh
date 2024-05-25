SCRIPT_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )" # copypasta from https://stackoverflow.com/a/4774063/

cd "$SCRIPT_DIR/.."

python -m development.update_provider -p Blender -w
python -m development.update_provider -p Onshape -w
python -m development.update_provider -p Fusion360 -w

if code -v &> /dev/null; then
    code providers/blender/update_providers_changelog.md
    code providers/onshape/update_providers_changelog.md
    code providers/fusion360/update_providers_changelog.md
fi

sh "$SCRIPT_DIR/run_lint.sh" --autofix