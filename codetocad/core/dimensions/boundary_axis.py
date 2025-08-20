from dataclasses import dataclass


@dataclass
class BoundaryAxis:
    min: float
    max: float

    @property
    def center(self) -> float:
        return (self.max + self.min) / 2.0

    def __str__(self):
        return f"""    min   max   unit
x   {self.min}  {self.max}
"""

    def __repr__(self) -> str:
        return self.__str__()
