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

# Rasterize an SVG to PNG with whichever tool is available (rsvg-convert,
# Inkscape or cairosvg).
rasterize() {  # $1 = svg, $2 = png
  if command -v rsvg-convert >/dev/null 2>&1; then
    rsvg-convert -w 1400 "$1" -o "$2"
  elif command -v inkscape >/dev/null 2>&1; then
    inkscape "$1" --export-type=png --export-filename="$2" -w 1400
  elif [ -x /Applications/Inkscape.app/Contents/MacOS/inkscape ]; then
    /Applications/Inkscape.app/Contents/MacOS/inkscape "$1" \
      --export-type=png --export-filename="$2" -w 1400
  else
    python -c "import cairosvg,sys; cairosvg.svg2png(url=sys.argv[1], write_to=sys.argv[2], output_width=1400)" "$1" "$2"
  fi
}

cd "$EXAMPLES_DIR"
for name in "${SCRIPTS[@]}"; do
  echo "=== $name ==="
  python "${name}.py"
  "$BLENDER" --background --factory-startup --python-exit-code 1 \
    --python "$IMAGES_DIR/render_stl.py" -- \
    "$EXAMPLES_DIR/${name}.stl" "$IMAGES_DIR/${name}.png"
  rm -f "${name}.stl" "${name}.blend" "${name}.glb"
done

# The drawing example outputs an SVG sheet, rasterized here instead of rendered.
echo "=== technical_drawing ==="
python technical_drawing.py
rasterize "$EXAMPLES_DIR/technical_drawing.svg" "$IMAGES_DIR/technical_drawing.png"
rm -f "$EXAMPLES_DIR/technical_drawing.svg"
echo "DONE"
