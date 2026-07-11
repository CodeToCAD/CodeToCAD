#!/bin/bash
# Regenerate the simulation plots in this images/ folder from the example
# scripts one directory up. Requires the spice extra
# (`uv sync --extra spice`) and ngspice (see the examples README).
set -e

IMAGES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXAMPLES_DIR="$(dirname "$IMAGES_DIR")"

SCRIPTS=(
  voltage_divider
  rc_lowpass
  led_driver
)

cd "$EXAMPLES_DIR"
for name in "${SCRIPTS[@]}"; do
  echo "=== $name ==="
  python "${name}.py"
done

# The examples write their PNGs into the examples dir; move them here.
mv -f "$EXAMPLES_DIR"/*.png "$IMAGES_DIR"/
echo "DONE"
