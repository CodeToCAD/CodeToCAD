from pathlib import Path
from CodeToCADBlenderProvider import *

curve("path").createFromVerticies([[0,0,0],[0,0,0.25]]).rotate("90d,0,0").isVisible(False)

curve("CodeToCAD").createText("Code To CAD", underlined=True).sweep("path")

curve("Small text!").createText("Small text!", size="15cm", underlined=True).translate("0,-2,0")

arialFontPath = str(Path(__file__).parent.absolute()) + "/fonts/arial.ttf"
curve("كود تو كاد").createText("كود تو كاد", fontFilePath=arialFontPath).translate("-5,0,0")


yuGothicFontPath = str(Path(__file__).parent.absolute()) + "/fonts/yu_gothic.ttc"
curve("curvedTextPath").createCircle("1m").translate("-5,-5,0").isVisible(False)
curve("コオデツカアド").createText("コオデツカアド",fontFilePath=yuGothicFontPath).curve("curvedTextPath").translate("-5,-5,0")

curve("multiline").createText(
"""Multiline
    Text
        Is
            Awesome!
"""
).translate("0,-5,0")
