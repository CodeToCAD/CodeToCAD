from typing import Optional

from codetocad.core.boundary_axis import BoundaryAxis


class BoundaryBox:
    x: Optional[BoundaryAxis]
    y: Optional[BoundaryAxis]
    z: Optional[BoundaryAxis]

    def __init__(
        self,
        x: Optional[BoundaryAxis],
        y: Optional[BoundaryAxis],
        z: Optional[BoundaryAxis],
    ):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"""    min   max   unit
x   {self.x and self.x.min}  {self.x and self.x.max}  {self.x and self.x.unit and self.x.unit.name+'(s)'}
y   {self.y and self.y.min}  {self.y and self.y.max}  {self.y and self.y.unit and self.y.unit.name+'(s)'}
z   {self.z and self.z.min}  {self.z and self.z.max}  {self.z and self.z.unit and self.z.unit.name+'(s)'}
"""

    def __repr__(self) -> str:
        return self.__str__()
