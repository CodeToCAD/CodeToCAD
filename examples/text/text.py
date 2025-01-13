from pathlib import Path
from codetocad import *

red_material = Material("red").set_color(0.709804, 0.109394, 0.245126, 1.0)
green_material = Material("green").set_color(0.118213, 0.709804, 0.109477, 0.8)
blue_material = Material("blue").set_color(0.0865257, 0.102776, 0.709804, 0.8)

Part.create_text(
    "Code To CAD", extrude_amount="1cm", underlined=True, name="CodeToCAD"
).set_material(green_material)

Sketch.create_text(
    "Small text!", font_size="15cm", underlined=True, name="Small text!"
).translate_xyz(0, -2, 0)

arial_font_path = str(Path(__file__).parent.absolute()) + "/fonts/arial.ttf"
Sketch.create_text(
    "كود تو كاد", font_file_path=arial_font_path, name="كود تو كاد"
).translate_xyz(-5, 0, 0)


yi_gothic_font_path = str(Path(__file__).parent.absolute()) + "/fonts/yu_gothic.ttc"
Sketch.create_circle("1m", name="curvedTextPath").translate_xyz(-5, -5, 0).set_visible(
    False
)

# This broke with API changes, need to put it back!
# Sketch.create_text(
#     "コオデツカアド", font_file_path=yi_gothic_font_path, name="コオデツカアド"
# ).profile("curvedTextPath").translate_xyz(-5, -5, 0).extrude(0.1).set_material(
#     red_material
# )

Part.create_text(
    """Multiline
    Text
        Is
            Awesome!
""",
    extrude_amount=0.1,
    name="multiline",
).translate_xyz(0, -5, 0).set_material(blue_material)
