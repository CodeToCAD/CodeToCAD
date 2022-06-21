from CodeToCADBlenderProvider import *

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

curve("circle").createCircle(circleRadius)

curve("profile").createFromVerticies(profile).sweep("circle")