from typing import Optional
from codetocad.enums.length_unit import LengthUnit


class BoundaryAxis:
    min: float
    max: float
    unit: Optional[LengthUnit]

    @property
    def center(self) -> float:
        return (self.max + self.min) / 2.0

    def __init__(self, min: float, max: float, unit=None) -> None:
        self.min = min
        self.max = max

        if unit is None:
            return

        unit = (
            LengthUnit.from_string(unit.replace(" ", "").lower())
            if isinstance(unit, str)
            else unit
        )
        assert isinstance(
            unit, LengthUnit
        ), "Dimension unit must be of type LengthUnit or string."

        self.unit = unit

    def __str__(self):
        return f"""    min   max   unit
x   {self.min}  {self.max}  {self.unit.name+'(s)' if self.unit else "No Unit"}
"""

    def __repr__(self) -> str:
        return self.__str__()
