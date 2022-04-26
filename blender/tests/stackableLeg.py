import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.absolute()))

from textToBlender import *

# scene().setDefaultUnit(BlenderLength.MILLIMETERS)


curve("legExtrudePath").createLine("5in").rotate("0,0,90d")

curve("ellipseLeg").createEllipse("24mm", "29*2mm").sweep("extrudePath", False).thicken("3mm")


