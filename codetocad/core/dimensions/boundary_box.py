from dataclasses import dataclass
from codetocad.core import BoundaryAxis


@dataclass
class BoundaryBox:
    x: BoundaryAxis
    y: BoundaryAxis
    z: BoundaryAxis

    def __str__(self):
        return f"""    min   max   unit
x   {self.x and self.x.min}  {self.x and self.x.max} m
y   {self.y and self.y.min}  {self.y and self.y.max} m
z   {self.z and self.z.min}  {self.z and self.z.max} m
"""

    def __repr__(self) -> str:
        return self.__str__()
