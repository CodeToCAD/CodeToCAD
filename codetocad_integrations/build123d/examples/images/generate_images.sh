#!/bin/bash
# Regenerate the PNG screenshots in this images/ folder from the example
# scripts one directory up. Requires the build123d extra
# (`uv sync --extra build123d`) and Blender on the PATH (or
# CODETOCAD_BLENDER pointing at it).
set -e

IMAGES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXAMPLES_DIR="$(dirname "$IMAGES_DIR")"
BLENDER="${CODETOCAD_BLENDER:-blender}"

SCRIPTS=(
  intro_02_plate_with_hole
  intro_03_prismatic_solid
  intro_09_fillet_chamfer
  intro_26_shelled_box
  intro_34_embossed_text
  gallery_circuit_board
  gallery_handle
  gallery_key_cap
  gallery_multi_sketch_loft
  gallery_vase
)

cd "$EXAMPLES_DIR"
for name in "${SCRIPTS[@]}"; do
  echo "=== $name ==="
  python "${name}.py"
  "$BLENDER" --background --factory-startup --python-exit-code 1 \
    --python "$IMAGES_DIR/render_stl.py" -- \
    "$EXAMPLES_DIR/${name}.stl" "$IMAGES_DIR/${name}.png"
  rm -f "${name}.stl"
done
echo "DONE"
