# import sys
# from pathlib import Path
# scriptDir = Path(__file__).parent.absolute()
# if scriptDir not in sys.path:
#     sys.path.insert(0, str(scriptDir))

from textToBlender import *

def createLadder():
    shape("base") \
        .primitive("cylinder", "10cm,2cm,10cm")

createLadder()