# utilities.py contains enums and helper functions for CodeToCAD python functionality.

import re
import math
import sys
from enum import Enum
from uuid import uuid4
from pathlib import Path

from typing import Optional, Union


min = "min"
max = "max"
center = "center"

reservedWords = ["min", "max", "center"]


def isReservedWordInString(stringToCheck: str) -> bool:
    for word in reservedWords:
        if word in stringToCheck:
            return True
    return False


def getFilename(relativeFilePath: str):
    path = Path(relativeFilePath)
    return path.stem


def createUUIDLikeId():
    return str(uuid4()).replace("-", "")[:10]


def formatLandmarkEntityName(parentEntityName: str, landmarkName: str):
    return f"{parentEntityName}_{landmarkName}"


def getAbsoluteFilepath(relativeFilePath: str):
    path = Path(relativeFilePath)
    absoluteFilePath = relativeFilePath
    if not path.is_absolute():
        absoluteFilePath = str(
            Path(sys.argv[0]).parent.joinpath(path).resolve())
    return absoluteFilePath


class EquittableEnum(Enum):
    # define the == operator, otherwise we can't compare enums, thanks python
    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value


class Units(EquittableEnum):
    pass


class AngleUnit(Units):
    RADIANS = 0
    DEGREES = 1

    @staticmethod
    def fromString(name: str) -> 'AngleUnit':
        aliases: dict[str, AngleUnit] = {
            "radians": AngleUnit.RADIANS,
            "rad": AngleUnit.RADIANS,
            "rads": AngleUnit.RADIANS,
            "r": AngleUnit.RADIANS,
            "degrees": AngleUnit.DEGREES,
            "degree": AngleUnit.DEGREES,
            "degs": AngleUnit.DEGREES,
            "deg": AngleUnit.DEGREES,
            "d": AngleUnit.DEGREES
        }

        fromString: str = name.lower().replace("(s)", "")

        parsedUnit: Optional[AngleUnit] = aliases[fromString] if fromString in aliases else None

        assert parsedUnit is not None, f"Could not parse unit {fromString}"

        return parsedUnit


class Angle():

    def toRadians(self) -> 'Angle':
        return Angle(
            math.radians(
                self.value) if self.unit == AngleUnit.DEGREES else self.value,
            AngleUnit.RADIANS
        )

    def toDegrees(self) -> 'Angle':
        return Angle(
            math.degrees(
                self.value) if self.unit == AngleUnit.RADIANS else self.value,
            AngleUnit.DEGREES
        )

    # Default unit is degrees if unit not passed
    def __init__(self, value: float, defaultUnit: AngleUnit = AngleUnit.DEGREES) -> None:

        unit = AngleUnit.fromString(defaultUnit.replace(" ", "").lower()) if type(
            defaultUnit) is str else defaultUnit
        assert (unit is None and defaultUnit is None) \
            or type(unit) is AngleUnit, \
            "Could not parse default unit."

        self.value = value
        self.unit = unit or AngleUnit.DEGREES

    @staticmethod
    def fromAngleOrItsFloatOrStringValue(mysteryAngle: Union[str, float, 'Angle']) -> 'Angle':
        if isinstance(mysteryAngle, Angle):
            return mysteryAngle
        if isinstance(mysteryAngle, (int, float)):
            return Angle(mysteryAngle)
        return Angle.fromString(mysteryAngle)

    def __str__(self) -> str:
        return f"{self.value}{' '+self.unit.name.lower() if self.unit else ''}"

    def __repr__(self) -> str:
        return self.__str__()

    def arithmeticPrecheckAndUnitConversion(self, other):
        if not isinstance(other, Angle):
            other = Angle.fromString(other)
        if other.unit != self.unit:
            if self.unit == AngleUnit.DEGREES:
                other.toDegrees()
            else:
                other.toRadians()
        return other

    def __add__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        return Angle(self.value + other.value, self.unit)

    def __sub__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        return Angle(self.value - other.value, self.unit)

    def __mul__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        return Angle(self.value * other.value, self.unit)

    def __truediv__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        return Angle(self.value / other.value, self.unit)

    def __floordiv__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        return Angle(self.value // other.value, self.unit)

    def __mod__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        return Angle(self.value % other.value, self.unit)

    # def __divmod__(self, other):
    #     other = self.arithmeticPrecheckAndUnitConversion(other)
    #     return Angle(divmod(self.value, other.value), self.unit)

    def __pow__(self, other, mod=None):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        return Angle(pow(self.value, other.value, mod), self.unit)

    def __abs__(self):
        return Angle(abs(self.value), self.unit)

    def __lt__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        return self.value < other.value

    def __le__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        return self.value <= other.value

    def __gt__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        return self.value > other.value

    def __ge__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        return self.value >= other.value

    def __eq__(self, other):
        if other == None:
            return False
        other = self.arithmeticPrecheckAndUnitConversion(other)
        return self.value == other.value

    def __ne__(self, other):
        return not (self == other)

    def __copy__(self):
        return self.__deepcopy__()

    def __deepcopy__(self):
        return Angle(self.value, self.unit)

    def copy(self):
        return self.__deepcopy__()

    # fromString: takes a string with a math operation and an optional unit of measurement
    # Default unit is degrees if unit not passed
    @staticmethod
    def fromString(fromString: Union[str, float, 'Angle'], defaultUnit: Union[str, AngleUnit] = AngleUnit.DEGREES):

        if isinstance(fromString, Angle):
            return fromString.copy()

        unit = AngleUnit.fromString(defaultUnit.replace(" ", "").lower()) if type(
            defaultUnit) is str else defaultUnit
        assert (unit is None and defaultUnit is None) \
            or type(unit) is AngleUnit, \
            "Could not parse default unit."

        if isinstance(fromString, (int, float)):
            return Angle(fromString, unit)

        assert type(fromString) is str, "fromString must be a string."

        fromString = fromString.replace(" ", "").lower()

        value = fromString

        assert len(value) > 0, f"Angle value cannot be empty."

        # check if a unit is passed into fromString, e.g. "1rad" -> radians
        unitInString = re.search('[A-Za-z]+$', fromString)
        if unitInString:
            value = fromString[0:-1*len(unitInString[0])]
            unitInString = AngleUnit.fromString(unitInString[0])
            unit = unitInString or unit or AngleUnit.DEGREES

        # Make sure our value only contains math operations and numbers as a weak safety check before passing it to `eval`
        assert re.match(
            r"[+\-*\/%\d\(\)]+", value), f"Value {value} contains characters that are not allowed."

        value = eval(value)

        return Angle(value, unit)


def getAnglesFromStringList(angles: Union[str, list[str]]) -> list[Angle]:
    anglesList: list[str]
    if isinstance(angles, str):
        anglesList = angles.replace(" ", "").lower().split(",")
    else:
        anglesList = angles

    assert isinstance(anglesList, (list, tuple)
                      ), "Only a list of strings is allowed."

    defaultUnit: AngleUnit = AngleUnit.DEGREES

    angleString = anglesList[-1]

    if type(angleString) == str:
        angleString = angleString.replace(" ", "").lower()
        angleString = re.search('[A-Za-z]+$', angleString)

        unitInString = AngleUnit.fromString(
            angleString[0]) if angleString else None
        if unitInString is not None and angleString is not None:
            defaultUnit = unitInString
            if len(angleString[0]) == len(anglesList[-1]):
                anglesList.pop()

    parsedAngles = []
    for angle in anglesList:
        parsedAngles.append(Angle.fromString(angle, defaultUnit))

    return parsedAngles


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
    def fromString(name: str) -> 'LengthUnit':
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
            "mi": LengthUnit.mi
        }

        fromString: str = name.lower().replace("(s)", "")

        parsedUnit: LengthUnit | None = aliases[fromString] if fromString in aliases else None

        assert parsedUnit is not None, f"Could not parse unit {fromString}"

        return parsedUnit


class Axis(EquittableEnum):
    X = 0
    Y = 1
    Z = 2

    @staticmethod
    def fromString(axis: Union[str, float, 'Axis']):
        if isinstance(axis, Axis):
            return axis
        axis = str(axis).lower()
        if axis == "x" or axis == "0":
            return Axis.X
        if axis == "y" or axis == "1":
            return Axis.Y
        if axis == "z" or axis == "2":
            return Axis.Z

        assert False, f"Cannot parse axis {axis}"


class CurvePrimitiveTypes(EquittableEnum):
    Point = 0
    LineTo = 1
    Line = 2
    Angle = 3
    Circle = 4
    Ellipse = 5
    Sector = 6
    Segment = 7
    Rectangle = 8
    Rhomb = 9
    Trapezoid = 10
    Polygon = 11
    Polygon_ab = 12
    Arc = 13


class CurveTypes(EquittableEnum):
    POLY = 0
    NURBS = 1
    BEZIER = 2


class ScalingMethods(Enum):
    toSpecificLength = 0
    scaleFactor = 1
    lockAspectRatio = 2  # scale one dimension, the others scale with it


class ConstraintTypes(EquittableEnum):
    # Translation locked between specified start and end points in all axes.
    Translation = 0
    # Rotation locked between specified start and end angles in all axes.
    Rotation = 1
    # Rotation locked between specified start and end angles in all axes, but rotation origin is offset.
    Pivot = 2
    # Rotation of one object is a percentage of another's in a specified axis.
    Gear = 3


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

        if (unit == None):
            return

        unit = LengthUnit.fromString(unit.replace(
            " ", "").lower()) if type(unit) is str else unit
        assert type(
            unit) is LengthUnit, "Dimension unit must be of type LengthUnit or string."

        self.unit = unit

    def __str__(self):
        return \
            f"""    min   max   unit
x   {self.min}  {self.max}  {self.unit.name+'(s)' if self.unit else "No Unit"}
"""

    def __repr__(self) -> str:
        return self.__str__()


class BoundaryBox:
    x: Optional[BoundaryAxis]
    y: Optional[BoundaryAxis]
    z: Optional[BoundaryAxis]

    def __init__(self, x: Optional[BoundaryAxis], y: Optional[BoundaryAxis], z: Optional[BoundaryAxis]):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return \
            f"""    min   max   unit
x   {self.x and self.x.min}  {self.x and self.x.max}  {self.x and self.x.unit and self.x.unit.name+'(s)'}
y   {self.y and self.y.min}  {self.y and self.y.max}  {self.y and self.y.unit and self.y.unit.name+'(s)'}
z   {self.z and self.z.min}  {self.z and self.z.max}  {self.z and self.z.unit and self.z.unit.name+'(s)'}
"""

    def __repr__(self) -> str:
        return self.__str__()


class Dimension():
    def __init__(self, value: float, unit: Optional[Union[str, LengthUnit]] = None):
        assert isinstance(value, (int, float)
                          ), "Dimension value must be a number."

        unit = LengthUnit.fromString(unit.replace(
            " ", "").lower()) if type(unit) is str else unit
        assert unit is None or type(
            unit) is LengthUnit, "Dimension unit must be of type LengthUnit or None."

        self.value = value
        self.unit = unit

    @staticmethod
    def fromDimensionOrItsFloatOrStringValue(mysteryDimension: Union[str, float, 'Dimension'], boundaryAxis: Optional[BoundaryAxis]) -> 'Dimension':
        if isinstance(mysteryDimension, Dimension):
            return mysteryDimension
        if isinstance(mysteryDimension, (int, float)):
            return Dimension(mysteryDimension)
        return Dimension.fromString(
            mysteryDimension, None, boundaryAxis)

    def __str__(self) -> str:
        return f"{self.value}{' '+self.unit.name if self.unit else ''}"

    def __repr__(self) -> str:
        return self.__str__()

    def convertToUnit(self, targetUnit: LengthUnit) -> 'Dimension':
        assert self.unit is not None, f"Current dimension does not have a unit."
        targetUnit = LengthUnit.fromString(targetUnit) if not isinstance(
            targetUnit, LengthUnit) else targetUnit
        assert isinstance(
            targetUnit, LengthUnit), f"Could not convert to unit {targetUnit}"

        newDimension = Dimension(
            self.value * (self.unit.value/targetUnit.value),
            targetUnit
        )
        return newDimension

    def arithmeticPrecheckAndUnitConversion(self, other) -> 'Dimension':
        assert other is not None, "Right-hand value cannot be None."
        if not isinstance(other, Dimension):
            other = Dimension.fromString(other)
        if other.unit is not None and self.unit is not None and other.unit != self.unit:
            other = other.convertToUnit(self.unit)
        return other

    def __add__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        return Dimension(self.value + other.value, self.unit)

    def __sub__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        return Dimension(self.value - other.value, self.unit)

    def __mul__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        return Dimension(self.value * other.value, self.unit)

    def __truediv__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        return Dimension(self.value / other.value, self.unit)

    def __floordiv__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        return Dimension(self.value // other.value, self.unit)

    def __mod__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        return Dimension(self.value % other.value, self.unit)

    # def __divmod__(self, other):
    #     other = self.arithmeticPrecheckAndUnitConversion(other)
    #     return Dimension(divmod(self.value, other.value), self.unit)

    def __pow__(self, other, mod=None):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        return Dimension(pow(self.value, other.value, mod), self.unit)

    def __abs__(self):
        return Dimension(abs(self.value), self.unit)

    def __lt__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        return self.value < other.value

    def __le__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        return self.value <= other.value

    def __gt__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        return self.value > other.value

    def __ge__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        return self.value >= other.value

    def __eq__(self, other):
        if other == None:
            return False
        other = self.arithmeticPrecheckAndUnitConversion(other)
        return self.value == other.value

    def __ne__(self, other):
        return not (self == other)

    def __copy__(self):
        return self.__deepcopy__()

    def __deepcopy__(self):
        return Dimension(self.value, self.unit)

    def copy(self):
        return self.__deepcopy__()

    # fromString: takes a string with a math operation and an optional unit of measurement
    # Default unit is None (scale factor) if it's not passed in
    # examples: "1m", "1.5ft", "3/8in", "1", "1-(3/4)cm"
    # boundaryAxis is required if min,center,max are used

    @staticmethod
    def fromString(fromString: Union[str, float, 'Dimension'], defaultUnit: Optional[LengthUnit] = None, boundaryAxis: Optional[BoundaryAxis] = None):

        if isinstance(fromString, Dimension):
            return fromString.copy()

        unit = LengthUnit.fromString(defaultUnit.replace(" ", "").lower()) if type(
            defaultUnit) is str else defaultUnit
        assert (unit is None and defaultUnit is None) \
            or type(unit) is LengthUnit, \
            "Could not parse default unit."

        if isinstance(fromString, (int, float)):
            return Dimension(fromString, unit)

        assert type(fromString) is str, "fromString must be a string."

        fromString = fromString.replace(" ", "").lower()

        value = fromString

        # check if a unit is passed into fromString, e.g. "1-(3/4)cm" -> cm
        unitInString = getUnitInString(fromString)
        if unitInString:
            value = fromString[0:-1*len(unitInString)]
            unitInString = LengthUnit.fromString(unitInString)
            unit = unitInString or unit

        # if min,max,center is used, try to parse those words into their respective values.
        if isReservedWordInString(value):
            assert boundaryAxis is not None, "min,max,center keywords used, but boundaryAxis is not known."
            if unit == None:
                unit = boundaryAxis.unit

            assert unit, "Could not determine the unit to convert the boundary axis."

            value = replaceMinMaxCenterWithRespectiveValue(
                value, boundaryAxis, unit)

        assert len(value) > 0, f"Dimension value cannot be empty."

        # Make sure our value only contains math operations and numbers as a weak safety check before passing it to `eval`
        assert re.match(
            "[+\-*\/%\d\(\)]+", value), f"Value {value} contains characters that are not allowed."

        value = eval(value)

        return Dimension(value, unit)


class Point:
    x: Dimension
    y: Dimension
    z: Dimension

    def __init__(self, x: Dimension, y: Dimension, z: Dimension) -> None:
        self.x = x
        self.y = y
        self.z = z

    def toList(self):
        return [self.x, self.y, self.z]

    @classmethod
    def fromList(cls, pointList: list[Dimension]):
        assert len(pointList) == 3, "Point list must contain three Dimensions."
        return cls(pointList[0], pointList[1], pointList[2])

    def arithmeticPrecheckAndUnitConversion(self, other) -> 'Point':
        assert other is not None, "Right-hand value cannot be None."

        if not isinstance(other, (int, float, str, Dimension, list, Point)):
            raise TypeError(
                "Only int/float, Dimension, or Dimension String, or a list of those types is allowed.")

        if isinstance(other, (int, float)):
            return Point(Dimension(other), Dimension(other), Dimension(other))

        x = Dimension(0)
        y = Dimension(0)
        z = Dimension(0)

        if isinstance(other, list):
            [x, y, z] = getDimensionListFromStringList(other)

        if isinstance(other, str):
            if "," in other:
                [x, y, z] = getDimensionListFromStringList(other)
            else:
                other = Dimension.fromString(other)

        if isinstance(other, Dimension):
            x = other
            y = other
            z = other

        if isinstance(other, Point):
            x = other.x
            y = other.y
            z = other.z

        if x.unit is not None and self.x.unit is not None and x.unit != self.x.unit:
            x: Dimension = x.convertToUnit(self.x.unit)
        if y.unit is not None and self.y.unit is not None and y.unit != self.y.unit:
            y: Dimension = y.convertToUnit(self.y.unit)
        if z.unit is not None and self.z.unit is not None and z.unit != self.z.unit:
            z: Dimension = z.convertToUnit(self.z.unit)
        return Point(x, y, z)

    def __eq__(self, other) -> bool:
        other = self.arithmeticPrecheckAndUnitConversion(other)
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __add__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Point(x, y, z)

    def __sub__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Point(x, y, z)

    def __mul__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        x = self.x * other.x
        y = self.y * other.y
        z = self.z * other.z
        return Point(x, y, z)

    def __truediv__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        x = self.x / other.x
        y = self.y / other.y
        z = self.z / other.z
        return Point(x, y, z)

    def __floordiv__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        x = self.x // other.x
        y = self.y // other.y
        z = self.z // other.z
        return Point(x, y, z)

    def __mod__(self, other):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        x = self.x % other.x
        y = self.y % other.y
        z = self.z % other.z
        return Point(x, y, z)

    # def __divmod__(self, other):
    #     other = self.arithmeticPrecheckAndUnitConversion(other)
    #     x = divmod(self.x, other.x)
    #     y = divmod(self.y, other.y)
    #     z = divmod(self.z, other.z)
    #     return Point(x, y, z)

    def __pow__(self, other, mod=None):
        other = self.arithmeticPrecheckAndUnitConversion(other)
        x = pow(self.x, other.x)
        y = pow(self.y, other.y)
        z = pow(self.z, other.z)
        return Point(x, y, z)

    def __abs__(self):
        x = abs(self.x)
        y = abs(self.y)
        z = abs(self.z)
        return Point(x, y, z)

    def __copy__(self):
        return self.__deepcopy__()

    def __deepcopy__(self):
        return Point(self.x, self.y, self.z)

    def copy(self):
        return self.__deepcopy__()

    def __getitem__(self, key):
        if (key == 0):
            return self.x
        if (key == 1):
            return self.y
        if (key == 2):
            return self.z

    def __str__(self):
        return \
            f"""x   y   z
{self.x}  {self.y}  {self.z}
"""

    def __repr__(self) -> str:
        return self.__str__()


class Dimensions():

    def __init__(self,
                 x: Dimension,
                 y: Dimension,
                 z: Dimension
                 ) -> None:
        self.point = Point(x, y, z)

    def toList(self):
        return self.point.toList()

    @staticmethod
    def fromPoint(point: Point) -> 'Dimensions':
        return Dimensions(point.x, point.y, point.z)

    @classmethod
    def fromList(cls, dimensionsList: list[Dimension]):
        assert len(
            dimensionsList) == 3, "Dimensions list must contain three Dimensions."
        return cls(dimensionsList[0], dimensionsList[1], dimensionsList[2])

    def __eq__(self, other) -> bool:
        return self.point == other.point

    def __add__(self, other):
        point = self.point + other.point
        return Dimensions(point.x, point.y, point.z)

    def __sub__(self, other):
        point = self.point - other.point
        return Dimensions(point.x, point.y, point.z)

    def __mul__(self, other):
        point = self.point * other.point
        return Dimensions(point.x, point.y, point.z)

    def __truediv__(self, other):
        point = self.point / other.point
        return Dimensions(point.x, point.y, point.z)

    def __floordiv__(self, other):
        point = self.point // other.point
        return Dimensions(point.x, point.y, point.z)

    def __mod__(self, other):
        point = self.point % other.point
        return Dimensions(point.x, point.y, point.z)

    def __divmod__(self, other):
        point = divmod(self.point, other.point)
        return Dimensions(point.x, point.y, point.z)

    def __pow__(self, other, mod=None):
        point = pow(self.point, other.point)
        return Dimensions(point.x, point.y, point.z)

    def __abs__(self):
        point = abs(self.point)
        return Dimensions(point.x, point.y, point.z)

    def __copy__(self):
        return self.__deepcopy__()

    def __deepcopy__(self):
        return Dimensions(self.point.x, self.point.y, self.point.z)

    def copy(self):
        return self.__deepcopy__()

    @property
    def x(self):
        return self.point.x

    @property
    def y(self):
        return self.point.y

    @property
    def z(self):
        return self.point.z

    @property
    def radius(self):
        return self.x

    @property
    def width(self):
        return self.x

    @property
    def length(self):
        return self.y

    @property
    def height(self):
        return self.z

    def __getitem__(self, key):
        if (key == 0):
            return self.x
        if (key == 1):
            return self.y
        if (key == 2):
            return self.z
        if (key == "radius"):
            return self.radius
        if (key == "width"):
            return self.width
        if (key == "length"):
            return self.length
        if (key == "height"):
            return self.height


# Replace "min|max|center" in "min+0.2" to the value in the bounding box's BoundaryAxis
def replaceMinMaxCenterWithRespectiveValue(dimension: str, boundaryAxis: BoundaryAxis, defaultUnit: LengthUnit):
    dimension = dimension.lower()

    while "min" in dimension:
        dimension = dimension.replace("min", "({})".format(Dimension(
            boundaryAxis.min, boundaryAxis.unit).convertToUnit(defaultUnit).value))
    while "max" in dimension:
        dimension = dimension.replace("max", "({})".format(Dimension(
            boundaryAxis.max, boundaryAxis.unit).convertToUnit(defaultUnit).value))
    while "center" in dimension:
        dimension = dimension.replace("center", "({})".format(Dimension(
            boundaryAxis.center, boundaryAxis.unit).convertToUnit(defaultUnit).value))

    return dimension


def getUnitInString(dimensionString):
    if type(dimensionString) != str:
        return None

    dimensionString = dimensionString.replace(" ", "").lower()

    unitSearchResults = re.search('[A-Za-z]+$', dimensionString)

    unitInString = unitSearchResults[0] if unitSearchResults else None

    return unitInString if unitInString and not isReservedWordInString(unitInString) else None


def getDimensionListFromStringList(dimensions: Union[str, list[str]], boundingBox: Optional[BoundaryBox] = None) -> list[Dimension]:

    if type(dimensions) is str:
        dimensions = dimensions.replace(" ", "").lower().split(",")

    assert isinstance(dimensions, (list, tuple)
                      ), "Only a list of strings is allowed."

    parsedDimensions = []

    defaultUnit = None

    unitInString = getUnitInString(dimensions[-1])
    if unitInString is not None:
        defaultUnit = LengthUnit.fromString(unitInString)
        if len(unitInString) == len(dimensions[-1].replace(" ", "").lower()):
            dimensions.pop()

    for index, dimension in enumerate(dimensions):
        if boundingBox is not None and index < 3:
            boundaryAxis = getattr(boundingBox, "xyz"[index])
            parsedDimensions.append(Dimension.fromString(
                dimension, defaultUnit, boundaryAxis))
            continue

        parsedDimensions.append(
            Dimension.fromString(dimension, defaultUnit, None))

    return parsedDimensions
