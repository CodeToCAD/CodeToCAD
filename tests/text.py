from pathlib import Path
from CodeToCADBlenderProvider import *

Curve("path").createFromVerticies([[0,0,0],[0,0,0.25]]).rotate("90d,0,0").setVisible(False)

Curve("CodeToCAD").createText("Code To CAD", underlined=True).sweep("path")

Curve("Small text!").createText("Small text!", size="15cm", underlined=True).translate("0,-2,0")

arialFontPath = str(Path(__file__).parent.absolute()) + "/fonts/arial.ttf"
Curve("كود تو كاد").createText("كود تو كاد", fontFilePath=arialFontPath).translate("-5,0,0")


yuGothicFontPath = str(Path(__file__).parent.absolute()) + "/fonts/yu_gothic.ttc"
Curve("curvedTextPath").createCircle("1m").translate("-5,-5,0").setVisible(False)
Curve("コオデツカアド").createText("コオデツカアド",fontFilePath=yuGothicFontPath).profile("curvedTextPath").translate("-5,-5,0")

Curve("multiline").createText(
"""Multiline
    Text
        Is
            Awesome!
"""
).translate("0,-5,0")
