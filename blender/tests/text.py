import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.absolute()))

from textToBlender import *

curve("path").createFromVerticies([[0,0,0],[0,0,2]])

curve("CodeToCAD").createText("Code To CAD", underlined=True).sweep("path")

curve("Small text!").createText("Small text!", size="5cm", underlined=True).sweep("path").translate("0,5,0")

fontPath = str(Path(__file__).parent.absolute()) + "/arial.ttf"
curve("كود تو كاد").createText("كود تو كاد", fontFilePath=fontPath).translate("-5,0,0")


curve("multiline").createText(
"""Multiline
    Text
        Is
            Awesome!
"""
).translate("0,-5,0")