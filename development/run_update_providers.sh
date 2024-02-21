SCRIPT_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )" # copypasta from https://stackoverflow.com/a/4774063/

cd "$SCRIPT_DIR/.."

python -m development.update_provider -p Blender -w
python -m development.update_provider -p Onshape -w
python -m development.update_provider -p Fusion360 -w