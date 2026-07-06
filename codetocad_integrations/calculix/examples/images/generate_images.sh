#!/bin/bash
# Regenerate the PNG renders in this images/ folder. beam_fea.py already
# calls results.visualize() itself; this just runs it and collects the
# output next to this script. Requires `uv sync --extra calculix --extra
# build123d` and the ccx solver (see the integration README).
set -e

IMAGES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXAMPLES_DIR="$(dirname "$IMAGES_DIR")"

cd "$EXAMPLES_DIR"
python beam_fea.py
mv -f beam_fea.png beam_deflection.png "$IMAGES_DIR/"
rm -rf beam_fea_output
echo "DONE"
