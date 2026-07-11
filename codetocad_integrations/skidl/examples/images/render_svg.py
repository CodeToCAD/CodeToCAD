"""Convert a schematic SVG to a trimmed PNG for the docs.

Tries, in order, whatever SVG rasterizer is available: cairosvg (Python),
then the rsvg-convert / inkscape / qlmanage (macOS) command-line tools.
Whitespace is trimmed with Pillow.

    python render_svg.py schematic.svg schematic.png [scale]
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def _rasterize(svg: Path, png: Path, scale: float) -> None:
    try:
        import cairosvg

        cairosvg.svg2png(url=str(svg), write_to=str(png), scale=scale)
        return
    except ImportError:
        pass

    if shutil.which("rsvg-convert"):
        subprocess.run(
            ["rsvg-convert", "-z", str(scale), "-o", str(png), str(svg)], check=True
        )
        return
    if shutil.which("inkscape"):
        subprocess.run(
            ["inkscape", str(svg), "--export-type=png", f"--export-filename={png}",
             f"--export-dpi={int(96 * scale)}"],
            check=True,
        )
        return
    if shutil.which("qlmanage"):  # macOS fallback
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                ["qlmanage", "-t", "-s", str(int(900 * scale)), "-o", tmp, str(svg)],
                check=True,
                capture_output=True,
            )
            produced = next(Path(tmp).glob("*.png"))
            shutil.copyfile(produced, png)
        return
    raise RuntimeError(
        "No SVG rasterizer found. Install one of: cairosvg (pip), rsvg-convert, "
        "inkscape (or use macOS qlmanage)."
    )


def _trim(png: Path, border: int = 24) -> None:
    from PIL import Image, ImageChops

    # Flatten onto white first so transparent regions count as background,
    # then trim to the non-white bounding box.
    source = Image.open(png).convert("RGBA")
    image = Image.new("RGBA", source.size, (255, 255, 255, 255))
    image.alpha_composite(source)
    image = image.convert("RGB")

    background = Image.new("RGB", image.size, (255, 255, 255))
    bbox = ImageChops.difference(image, background).getbbox()
    if bbox:
        left, top, right, bottom = bbox
        image = image.crop(
            (
                max(left - border, 0),
                max(top - border, 0),
                min(right + border, image.width),
                min(bottom + border, image.height),
            )
        )
    image.save(png)


def main() -> None:
    svg = Path(sys.argv[1])
    png = Path(sys.argv[2])
    scale = float(sys.argv[3]) if len(sys.argv) > 3 else 3.0
    _rasterize(svg, png, scale)
    _trim(png)
    print(f"wrote {png}")


if __name__ == "__main__":
    main()
