"""
A re-creation of the famous OpenCascade Bottle (https://dev.opencascade.org/doc/overview/html/occt__tutorial.html)

Code inspired by
- https://replicad.xyz/docs/examples/occt-bottle
- https://cadquery.readthedocs.io/en/latest/examples.html#the-classic-occ-bottle
"""

from codetocad import *

(L, w, t) = (20.0, 6.0, 3.0)
# s = cq.Workplane("XY")
# Sketch is missing the sketch plane
bottle_profile = Sketch("bottle_profile").create_line(w / 2.0)
arc = Sketch("bottle_arc").create_arc(L / 2)
# # Draw half the profile of the bottle and extrude it
# p = (
#     s.center(-L / 2.0, 0)
#     .vLine(w / 2.0)
#     .threePointArc((L / 2.0, w / 2.0 + t), (L, w / 2.0))
#     .vLine(-w / 2.0)
#     .mirrorX()
#     .extrude(30.0, True)
# )

# # Make the neck
# p = p.faces(">Z").workplane(centerOption="CenterOfMass").circle(3.0).extrude(2.0, True)

# # Make a shell
# result = p.faces(">Z").shell(0.3)
