from codetocad import *

# Following these SolidWorks tutorial: https://youtu.be/ZluN3w9omgM and https://youtu.be/p_u4f2EfenM

"""
The following steps overlook important steps such as dimensioning. All sketches start at the top plane.

Steps to sketch a Mounting Bracket (aka an L-bracket) using a single profile:
1. Draw a line going through origin.
2. At the end of that line, draw another line perpendicular to it.
3. Either offset the two wires created so far, or draw two more lines parallel to them.
4. Close the shape by connecting the two L-shaped wires.
5. Extrude the closed L shape.

Steps to sketch a Mounting Bracket (aka an L-bracket) using two rectangular profiles:
1. Draw a rectangle centered at the origin.
2. Extrude this profile.
3. Select the face on the front plane, create a sketch on this face.
4. Create a rectangle coinciding with the bottom vertices of the rectangle.
5. Extrude this rectangle.

In CodeToCAD, do the following:
"""


def createMountingBracket():
    Part("")
