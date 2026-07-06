#!/bin/bash
# Regenerate the PNG screenshots in this images/ folder from the example
# scripts one directory up. Each example calls ensure_blender() itself, so
# `python <name>.py` relaunches under `blender --background` automatically.
# Requires Blender on the PATH (or CODETOCAD_BLENDER pointing at it).
set -e

IMAGES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXAMPLES_DIR="$(dirname "$IMAGES_DIR")"
BLENDER="${CODETOCAD_BLENDER:-blender}"

SCRIPTS=(
  plate_with_hole
  embossed_text
  shelled_cup
  suzanne
)

cd "$EXAMPLES_DIR"
for name in "${SCRIPTS[@]}"; do
  echo "=== $name ==="
  python "${name}.py"
  "$BLENDER" --background --factory-startup --python-exit-code 1 \
    --python "$IMAGES_DIR/render_stl.py" -- \
    "$EXAMPLES_DIR/${name}.stl" "$IMAGES_DIR/${name}.png"
  rm -f "${name}.stl" "${name}.blend" "${name}.glb"
done
echo "DONE"
