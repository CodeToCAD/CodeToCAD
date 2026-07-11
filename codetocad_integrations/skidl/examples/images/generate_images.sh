#!/bin/bash
# Regenerate the schematic images in this images/ folder from the example
# scripts one directory up. Requires the skidl extra
# (`uv sync --extra skidl`), netlistsvg (`npm install -g netlistsvg`) and,
# for the schematic PNGs, an SVG rasterizer (cairosvg, rsvg-convert,
# inkscape, or macOS qlmanage). The led_board 3D render also needs the
# open3d extra.
set -e

IMAGES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXAMPLES_DIR="$(dirname "$IMAGES_DIR")"

SCRIPTS=(
  voltage_divider
  rc_lowpass
  led_board
)

cd "$EXAMPLES_DIR"
for name in "${SCRIPTS[@]}"; do
  echo "=== $name ==="
  python "${name}.py"
  cp -f "${name}.svg" "$IMAGES_DIR/${name}.svg"
  python "$IMAGES_DIR/render_svg.py" "${name}.svg" "$IMAGES_DIR/${name}.png"
done
mv -f "$EXAMPLES_DIR"/led_board_3d.png "$IMAGES_DIR"/ 2>/dev/null || true

# Clean the intermediate netlists and skidl byproducts.
rm -f "$EXAMPLES_DIR"/*.net "$EXAMPLES_DIR"/*.svg "$EXAMPLES_DIR"/*.xml \
      "$EXAMPLES_DIR"/*_sklib.py "$EXAMPLES_DIR"/*.erc "$EXAMPLES_DIR"/*.log
rm -rf "$EXAMPLES_DIR"/led_board_stl
echo "DONE"
