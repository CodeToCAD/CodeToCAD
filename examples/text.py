from pathlib import Path
from CodeToCAD import *

redMaterial = Material("red").setColor(0.709804, 0.109394, 0.245126, 1.0)
greenMaterial = Material("green").setColor(0.118213, 0.709804, 0.109477, 0.8)
blueMaterial = Material("blue").setColor(0.0865257, 0.102776, 0.709804, 0.8)

Curve("CodeToCAD").createText("Code To CAD",
                              underlined=True).extrude("1cm").setMaterial(greenMaterial)

Curve("Small text!").createText("Small text!",
                                fontSize="15cm", underlined=True).translateXYZ(0, -2, 0)

arialFontPath = str(Path(__file__).parent.absolute()) + "/fonts/arial.ttf"
Curve("كود تو كاد").createText("كود تو كاد",
                               fontFilePath=arialFontPath).translateXYZ(-5, 0, 0)


yuGothicFontPath = str(Path(__file__).parent.absolute()
                       ) + "/fonts/yu_gothic.ttc"
Curve("curvedTextPath").createCircle(
    "1m").translateXYZ(-5, -5, 0).setVisible(False)
Curve("コオデツカアド").createText("コオデツカアド", fontFilePath=yuGothicFontPath).profile(
    "curvedTextPath").translateXYZ(-5, -5, 0).extrude(.1).setMaterial(redMaterial)

Curve("multiline").createText(
    """Multiline
    Text
        Is
            Awesome!
"""
).translateXYZ(0, -5, 0).extrude(0.1).setMaterial(blueMaterial)
