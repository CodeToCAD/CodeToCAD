from codetocad.enums.units import Units


class LengthUnit(Units):
    # metric
    μm = 1 / 1000
    mm = 1
    cm = 10
    m = 1000
    km = 1000000

    # imperial
    thou = 25.4 / 1000
    inch = 25.4
    ft = 25.4 * 12
    mi = 25.4 * 63360

    @staticmethod
    def from_string(name: str) -> "LengthUnit":
        aliases: dict[str, LengthUnit] = {
            # metric
            "micrometer": LengthUnit.μm,
            "millimeter": LengthUnit.mm,
            "millimeters": LengthUnit.mm,
            "centimeter": LengthUnit.cm,
            "centimeters": LengthUnit.cm,
            "kilometer": LengthUnit.km,
            "meter": LengthUnit.m,
            "meters": LengthUnit.m,
            "mm": LengthUnit.mm,
            "cm": LengthUnit.cm,
            "m": LengthUnit.m,
            "km": LengthUnit.km,
            # imperial
            "thousandthInch": LengthUnit.thou,
            "thousandth": LengthUnit.thou,
            "inch": LengthUnit.inch,
            "inches": LengthUnit.inch,
            "foot": LengthUnit.ft,
            "feet": LengthUnit.ft,
            "mile": LengthUnit.mi,
            "miles": LengthUnit.mi,
            "thou": LengthUnit.thou,
            "in": LengthUnit.inch,
            "ft": LengthUnit.ft,
            "mi": LengthUnit.mi,
        }

        from_string: str = name.lower().replace("(s)", "")

        parsedUnit: LengthUnit | None = (
            aliases[from_string] if from_string in aliases else None
        )

        assert parsedUnit is not None, f"Could not parse unit {from_string}"

        return parsedUnit
