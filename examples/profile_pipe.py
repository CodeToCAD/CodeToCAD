from codetocad import *

# We are trying to draw a bull-horn shapes pipe:
"""
Pipe is 1/4" thick.
          |------------------21.5"----------------|
              __________________________________
                 B____________C______________D
            /   /                            \\   \
           /   /                              \\   \
          |_A_|                               |_E_|
               |------------18.5"------------|
"""

profile_vertices = [
    [0, 0, 0],  # start A
    "2,1,0,in",  # B
    # "21.5/2,1,0,in", #midpoint C
    "21.5-2,1,0,in",  # D
    "21.5,0,0,in",  # end E
]

circle = Sketch("circle")
circle.create_circle("1in")
circle.set_visible(False)

profile = Sketch("profile")
profile.create_from_vertices(profile_vertices)
profile.sweep("circle", fill_cap=False)
