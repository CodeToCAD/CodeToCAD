from codetocad.enums.units import Units
from typing import Optional


class AngleUnit(Units):
    RADIANS = 0
    DEGREES = 1

    @staticmethod
    def from_string(name: str) -> "AngleUnit":
        aliases: dict[str, AngleUnit] = {
            "radians": AngleUnit.RADIANS,
            "rad": AngleUnit.RADIANS,
            "rads": AngleUnit.RADIANS,
            "r": AngleUnit.RADIANS,
            "degrees": AngleUnit.DEGREES,
            "degree": AngleUnit.DEGREES,
            "degs": AngleUnit.DEGREES,
            "deg": AngleUnit.DEGREES,
            "d": AngleUnit.DEGREES,
        }

        from_string: str = name.lower().replace("(s)", "")

        parsedUnit: Optional[AngleUnit] = (
            aliases[from_string] if from_string in aliases else None
        )

        assert parsedUnit is not None, f"Could not parse unit {from_string}"

        return parsedUnit
