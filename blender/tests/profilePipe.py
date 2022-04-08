import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.absolute()))

from textToBlender import *

# We are trying to draw a bull-horn shapes pipe:
"""
Pipe is 1/4" thick.
          |------------------21.5"----------------|
              __________________________________
                 ____________________________
            /   /                            \   \
           /   /                              \   \
          |___|                               |___|
               |------------18.5"------------|
"""

profile = [
    "0,0,0,in", #start
    "2,1,0,in",
    "21.5/2,1,0,in", #midpoint
    "21.5-2,1,0,in",
    "21.5,0,0,in" #end
    ]

circleRadius = "(1/4)/2 in"


# sample data
coords = [(0,0,0), (1,0,0), (1,1,0), (2,1,0)]

curve("verticies").fromVerticies(coords)

curve("arc").createArc(2,45)