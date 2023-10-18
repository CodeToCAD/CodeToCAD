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

reservedWords = [min, max, center]


class PresetLandmark(Enum):
    left = 2
    right = 4
    top = 8
    bottom = 16
    front = 32
    back = 64
    center = 128
    leftTop = left | top
    leftBottom = left | bottom
    leftFront = left | front
    leftBack = left | back
    rightTop = right | top
    rightBottom = right | bottom
    rightFront = right | front
    rightBack = right | back
    frontTop = front | top
    backTop = back | top
    frontBottom = front | bottom
    backBottom = back | bottom
    leftFrontTop = left | front | top
    leftBackTop = left | back | top
    leftFrontBottom = left | front | bottom
    leftBackBottom = left | back | bottom
    rightFrontTop = right | front | top
    rightBackTop = right | back | top
    rightFrontBottom = right | front | bottom
    rightBackBottom = right | back | bottom

    def __ror__(self, other):
        return self.value | other.value

    def __and__(self, other):
        return self.value & other.value

    def contains(self, other):
        return (self & other == other.value)

    @staticmethod
    def from_string(landmark_name) -> Optional['PresetLandmark']:
        for preset in PresetLandmark:
            if preset.name == landmark_name:
                return preset
        return None

    def get_xyz(self):
        x = min if self.contains(PresetLandmark.left) else max if self.contains(
            PresetLandmark.right) else center
        y = min if self.contains(PresetLandmark.front) else max if self.contains(
            PresetLandmark.back) else center
        z = min if self.contains(PresetLandmark.bottom) else max if self.contains(
            PresetLandmark.top) else center
        return (x, y, z)


def is_reserved_word_in_string(string_to_check: str) -> bool:
    for word in reservedWords:
        if word in string_to_check:
            return True
    return False


def get_filename(relative_file_path: str):
    path = Path(relative_file_path)
    return path.stem


def get_filenameWithExtension(relative_file_path: str):
    path = Path(relative_file_path)
    return path.name


def get_file_extension(file_path: str):
    path = Path(file_path)
    return path.suffix.replace(".", "")


def get_absolute_filepath(relative_file_path: str):
    path = Path(relative_file_path)
    absoluteFilePath = relative_file_path
    if not path.is_absolute():
        absoluteFilePath = str(
            Path(sys.argv[0]).parent.joinpath(path).resolve())
    return absoluteFilePath


def create_uuid_like_id():
    return str(uuid4()).replace("-", "")[:10]


def format_landmark_entity_name(parent_entity_name: str, landmark_name: str):
    return f"{parent_entity_name}_{landmark_name}"


class EquittableEnum(Enum):
    # define the == operator, otherwise we can't compare enums, thanks python
    def __eq__(self, other):
        return isinstance(self, type(other)) and self.value == other.value


class Units(EquittableEnum):
    pass


class AngleUnit(Units):
    RADIANS = 0
    DEGREES = 1

    @staticmethod
    def from_string(name: str) -> 'AngleUnit':
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

        from_string: str = name.lower().replace("(s)", "")

        parsedUnit: Optional[AngleUnit] = aliases[from_string] if from_string in aliases else None

        assert parsedUnit is not None, f"Could not parse unit {from_string}"

        return parsedUnit


class Angle():

    def to_radians(self) -> 'Angle':
        return Angle(
            math.radians(
                self.value) if self.unit == AngleUnit.DEGREES else self.value,
            AngleUnit.RADIANS
        )

    def to_degrees(self) -> 'Angle':
        return Angle(
            math.degrees(
                self.value) if self.unit == AngleUnit.RADIANS else self.value,
            AngleUnit.DEGREES
        )

    # Default unit is degrees if unit not passed
    def __init__(self, value: float, default_unit: AngleUnit = AngleUnit.DEGREES) -> None:

        unit = AngleUnit.from_string(default_unit.replace(" ", "").lower()) if isinstance(
            default_unit, str) else default_unit
        assert (unit is None and default_unit is None) \
            or isinstance(unit, AngleUnit), \
            "Could not parse default unit."

        self.value = value
        self.unit = unit or AngleUnit.DEGREES

    @staticmethod
    def from_angle_or_its_float_or_string_value(mystery_angle: Union[str, float, 'Angle']) -> 'Angle':
        if isinstance(mystery_angle, Angle):
            return mystery_angle
        if isinstance(mystery_angle, (int, float)):
            return Angle(mystery_angle)
        return Angle.from_string(mystery_angle)

    def __str__(self) -> str:
        return f"{self.value}{' '+self.unit.name.lower() if self.unit else ''}"

    def __repr__(self) -> str:
        return self.__str__()

    def arithmetic_precheck_and_unit_conversion(self, other):
        if not isinstance(other, Angle):
            other = Angle.from_string(other)
        if other.unit != self.unit:
            if self.unit == AngleUnit.DEGREES:
                other.to_degrees()
            else:
                other.to_radians()
        return other

    def __add__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Angle(self.value + other.value, self.unit)

    def __sub__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Angle(self.value - other.value, self.unit)

    def __mul__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Angle(self.value * other.value, self.unit)

    def __truediv__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Angle(self.value / other.value, self.unit)

    def __floordiv__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Angle(self.value // other.value, self.unit)

    def __mod__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Angle(self.value % other.value, self.unit)

    # def __divmod__(self, other):
    #     other = self.arithmetic_precheck_and_unit_conversion(other)
    #     return Angle(divmod(self.value, other.value), self.unit)

    def __pow__(self, other, mod=None):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Angle(pow(self.value, other.value, mod), self.unit)

    def __abs__(self):
        return Angle(abs(self.value), self.unit)

    def __lt__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        assert self.unit == other.unit, "Units are not matching for comparison."
        return self.value < other.value

    def __le__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        assert self.unit == other.unit, "Units are not matching for comparison."
        return self.value <= other.value

    def __gt__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        assert self.unit == other.unit, "Units are not matching for comparison."
        return self.value > other.value

    def __ge__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        assert self.unit == other.unit, "Units are not matching for comparison."
        return self.value >= other.value

    def __eq__(self, other):
        if other is None:
            return False
        other = self.arithmetic_precheck_and_unit_conversion(other)
        assert self.unit == other.unit, "Units are not matching for comparison."
        return self.value == other.value

    def __ne__(self, other):
        return not (self == other)

    def __copy__(self):
        return self.__deepcopy__()

    def __deepcopy__(self):
        return Angle(self.value, self.unit)

    def copy(self):
        return self.__deepcopy__()

    # from_string: takes a string with a math operation and an optional unit of measurement
    # Default unit is degrees if unit not passed
    @staticmethod
    def from_string(from_string: Union[str, float, 'Angle'], default_unit: Union[str, AngleUnit] = AngleUnit.DEGREES):

        if isinstance(from_string, Angle):
            return from_string.copy()

        unit = AngleUnit.from_string(default_unit.replace(" ", "").lower()) if isinstance(
            default_unit, str) else default_unit
        assert (unit is None and default_unit is None) \
            or isinstance(unit, AngleUnit), \
            "Could not parse default unit."

        if isinstance(from_string, (int, float)):
            return Angle(from_string, unit)

        assert isinstance(from_string, str), "from_string must be a string."

        from_string = from_string.replace(" ", "").lower()

        value = from_string

        assert len(value) > 0, "Angle value cannot be empty."

        # check if a unit is passed into from_string, e.g. "1rad" -> radians
        unitInString = re.search('[A-Za-z]+$', from_string)
        if unitInString:
            value = from_string[0:-1*len(unitInString[0])]
            unitInString = AngleUnit.from_string(unitInString[0])
            unit = unitInString or unit or AngleUnit.DEGREES

        # Make sure our value only contains math operations and numbers as a weak safety check before passing it to `eval`
        assert re.match(
            r"[+\-*\/%\d\(\)]+", value), f"Value {value} contains characters that are not allowed."

        value = eval(value)

        return Angle(value, unit)


def get_angles_from_string_list(angles: Union[str, list[str]]) -> list[Angle]:
    anglesList: list[str]
    if isinstance(angles, str):
        anglesList = angles.replace(" ", "").lower().split(",")
    else:
        anglesList = angles

    assert isinstance(anglesList, (list, tuple)
                      ), "Only a list of strings is allowed."

    default_unit: AngleUnit = AngleUnit.DEGREES

    angleString = anglesList[-1]

    if isinstance(angleString, str):
        angleString = angleString.replace(" ", "").lower()
        angleString = re.search('[A-Za-z]+$', angleString)

        unitInString = AngleUnit.from_string(
            angleString[0]) if angleString else None
        if unitInString is not None and angleString is not None:
            default_unit = unitInString
            if len(angleString[0]) == len(anglesList[-1]):
                anglesList.pop()

    parsedAngles = []
    for angle in anglesList:
        parsedAngles.append(Angle.from_string(angle, default_unit))

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
    def from_string(name: str) -> 'LengthUnit':
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

        from_string: str = name.lower().replace("(s)", "")

        parsedUnit: LengthUnit | None = aliases[from_string] if from_string in aliases else None

        assert parsedUnit is not None, f"Could not parse unit {from_string}"

        return parsedUnit


class Axis(EquittableEnum):
    X = 0
    Y = 1
    Z = 2

    @staticmethod
    def from_string(axis: Union[str, float, 'Axis']):
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
    Spiral = 14


class CurveTypes(EquittableEnum):
    POLY = 0
    NURBS = 1
    BEZIER = 2


class FileFormats(EquittableEnum):
    PNG = 0
    JPEG = 1
    OPEN_EXR = 2
    MP4 = 3

    @staticmethod
    def from_string(name: str):
        name = name.lower()
        if name == "png":
            return FileFormats.PNG
        if name == "jpg" or name == "jpeg":
            return FileFormats.JPEG
        if name == "exr" or name == "openexr":
            return FileFormats.OPEN_EXR
        if name == "mp4" or "ffmpeg":
            return FileFormats.MP4

        raise TypeError(f"{name} is not a supported file type.")


class ScalingMethods(Enum):
    toSpecificLength = 0
    scaleFactor = 1
    lockAspectRatio = 2  # scale one dimension, the others scale with it


class ConstraintTypes(EquittableEnum):
    # Translation locked between specified start and end points in all axes.
    LimitLocation = 0
    # Rotation locked between specified start and end angles in all axes.
    LimitRotation = 1
    # Rotation locked between specified start and end angles in all axes, but rotation origin is offset.
    Pivot = 2
    # Rotation of one object is a percentage of another's in a specified axis.
    Gear = 3
    # Fixed position:
    FixedPosition = 4
    # Fixed rotation:
    FixedRotation = 5


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

        if (unit is None):
            return

        unit = LengthUnit.from_string(unit.replace(
            " ", "").lower()) if isinstance(unit, str) else unit
        assert isinstance(
            unit, LengthUnit), "Dimension unit must be of type LengthUnit or string."

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

        unit = LengthUnit.from_string(unit.replace(
            " ", "").lower()) if isinstance(unit, str) else unit
        assert unit is None or isinstance(
            unit, LengthUnit), "Dimension unit must be of type LengthUnit or None."

        self.value = value
        self.unit = unit

    @staticmethod
    def from_dimension_or_its_float_or_string_value(mystery_dimension: Union[str, float, 'Dimension'], boundary_axis: Optional[BoundaryAxis]) -> 'Dimension':
        if isinstance(mystery_dimension, Dimension):
            return mystery_dimension
        if isinstance(mystery_dimension, (int, float)):
            return Dimension(mystery_dimension)
        return Dimension.from_string(
            mystery_dimension, None, boundary_axis)

    def __str__(self) -> str:
        return f"{self.value}{' '+self.unit.name if self.unit else ''}"

    def __repr__(self) -> str:
        return self.__str__()

    def convert_to_unit(self, target_unit: Union[str, LengthUnit]) -> 'Dimension':
        assert self.unit is not None, "Current dimension does not have a unit."
        target_unit = LengthUnit.from_string(target_unit) if not isinstance(
            target_unit, LengthUnit) else target_unit
        assert isinstance(
            target_unit, LengthUnit), f"Could not convert to unit {target_unit}"

        newDimension = Dimension(
            self.value * (self.unit.value/target_unit.value),
            target_unit
        )
        return newDimension

    def arithmetic_precheck_and_unit_conversion(self, other) -> 'Dimension':
        assert other is not None, "Right-hand value cannot be None."
        if not isinstance(other, Dimension):
            other = Dimension.from_string(other)
        if other.unit is not None and self.unit is not None and other.unit != self.unit:
            other = other.convert_to_unit(self.unit)
        return other

    def __add__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Dimension(self.value + other.value, self.unit or other.unit)

    def __sub__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Dimension(self.value - other.value, self.unit or other.unit)

    def __mul__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Dimension(self.value * other.value, self.unit or other.unit)

    def __truediv__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Dimension(self.value / other.value, self.unit or other.unit)

    def __floordiv__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Dimension(self.value // other.value, self.unit or other.unit)

    def __mod__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Dimension(self.value % other.value, self.unit or other.unit)

    # def __divmod__(self, other):
    #     other = self.arithmetic_precheck_and_unit_conversion(other)
    #     return Dimension(divmod(self.value, other.value), self.unit)

    def __pow__(self, other, mod=None):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Dimension(pow(self.value, other.value, mod), self.unit or other.unit)

    def __abs__(self):
        return Dimension(abs(self.value), self.unit)

    def __lt__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        assert self.unit == other.unit, "Units are not matching for comparison."
        return self.value < other.value

    def __le__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        assert self.unit == other.unit, "Units are not matching for comparison."
        return self.value <= other.value

    def __gt__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        assert self.unit == other.unit, "Units are not matching for comparison."
        return self.value > other.value

    def __ge__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        assert self.unit == other.unit, "Units are not matching for comparison."
        return self.value >= other.value

    def __eq__(self, other):
        if other is None:
            return False
        other = self.arithmetic_precheck_and_unit_conversion(other)
        assert self.unit == other.unit, "Units are not matching for comparison."
        return self.value == other.value

    def __ne__(self, other):
        return not (self == other)

    def __copy__(self):
        return self.__deepcopy__()

    def __deepcopy__(self):
        return Dimension(self.value, self.unit)

    def copy(self):
        return self.__deepcopy__()

    # from_string: takes a string with a math operation and an optional unit of measurement
    # Default unit is None (scale factor) if it's not passed in
    # examples: "1m", "1.5ft", "3/8in", "1", "1-(3/4)cm"
    # boundary_axis is required if min,center,max are used

    @staticmethod
    def from_string(from_string: Union[str, float, 'Dimension'], default_unit: Optional[LengthUnit] = None, boundary_axis: Optional[BoundaryAxis] = None):

        if isinstance(from_string, Dimension):
            return from_string.copy()

        unit = LengthUnit.from_string(default_unit.replace(" ", "").lower()) if isinstance(
            default_unit, str) else default_unit
        assert (unit is None and default_unit is None) \
            or isinstance(unit, LengthUnit), \
            "Could not parse default unit."

        if isinstance(from_string, (int, float)):
            return Dimension(from_string, unit)

        assert isinstance(from_string, str), "from_string must be a string."

        from_string = from_string.replace(" ", "").lower()

        value = from_string

        # check if a unit is passed into from_string, e.g. "1-(3/4)cm" -> cm
        unitInString = get_unit_in_string(from_string)
        if unitInString:
            value = from_string[0:-1*len(unitInString)]
            unitInString = LengthUnit.from_string(unitInString)
            unit = unitInString or unit

        # if min,max,center is used, try to parse those words into their respective values.
        if is_reserved_word_in_string(value):
            assert boundary_axis is not None, "min,max,center keywords used, but boundary_axis is not known."
            if unit is None:
                unit = boundary_axis.unit

            assert unit, "Could not determine the unit to convert the boundary axis."

            value = replace_min_max_center_with_respective_value(
                value, boundary_axis, unit)

        assert len(value) > 0, "Dimension value cannot be empty."

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

    def to_list(self):
        return [self.x, self.y, self.z]

    @classmethod
    def from_list(cls, point_list: list[Dimension]):
        assert len(point_list) == 3, "Point list must contain three Dimensions."
        return cls(point_list[0], point_list[1], point_list[2])

    def arithmetic_precheck_and_unit_conversion(self, other) -> 'Point':
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
            [x, y, z] = get_dimension_list_from_string_list(other)

        if isinstance(other, str):
            if "," in other:
                [x, y, z] = get_dimension_list_from_string_list(other)
            else:
                other = Dimension.from_string(other)

        if isinstance(other, Dimension):
            x = other
            y = other
            z = other

        if isinstance(other, Point):
            x = other.x
            y = other.y
            z = other.z

        if x.unit is not None and self.x.unit is not None and x.unit != self.x.unit:
            x: Dimension = x.convert_to_unit(self.x.unit)
        if y.unit is not None and self.y.unit is not None and y.unit != self.y.unit:
            y: Dimension = y.convert_to_unit(self.y.unit)
        if z.unit is not None and self.z.unit is not None and z.unit != self.z.unit:
            z: Dimension = z.convert_to_unit(self.z.unit)
        return Point(x, y, z)

    def __eq__(self, other) -> bool:
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __add__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Point(x, y, z)

    def __sub__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Point(x, y, z)

    def __mul__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        x = self.x * other.x
        y = self.y * other.y
        z = self.z * other.z
        return Point(x, y, z)

    def __truediv__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        x = self.x / other.x
        y = self.y / other.y
        z = self.z / other.z
        return Point(x, y, z)

    def __floordiv__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        x = self.x // other.x
        y = self.y // other.y
        z = self.z // other.z
        return Point(x, y, z)

    def __mod__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        x = self.x % other.x
        y = self.y % other.y
        z = self.z % other.z
        return Point(x, y, z)

    # def __divmod__(self, other):
    #     other = self.arithmetic_precheck_and_unit_conversion(other)
    #     x = divmod(self.x, other.x)
    #     y = divmod(self.y, other.y)
    #     z = divmod(self.z, other.z)
    #     return Point(x, y, z)

    def __pow__(self, other, mod=None):
        other = self.arithmetic_precheck_and_unit_conversion(other)
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

    def to_list(self):
        return self.point.to_list()

    @staticmethod
    def from_point(point: Point) -> 'Dimensions':
        return Dimensions(point.x, point.y, point.z)

    @classmethod
    def from_list(cls, dimensions_list: list[Dimension]):
        assert len(
            dimensions_list) == 3, "Dimensions list must contain three Dimensions."
        return cls(dimensions_list[0], dimensions_list[1], dimensions_list[2])

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
def replace_min_max_center_with_respective_value(dimension: str, boundary_axis: BoundaryAxis, default_unit: LengthUnit):
    dimension = dimension.lower()

    while "min" in dimension:
        dimension = dimension.replace("min", "({})".format(Dimension(
            boundary_axis.min, boundary_axis.unit).convert_to_unit(default_unit).value))
    while "max" in dimension:
        dimension = dimension.replace("max", "({})".format(Dimension(
            boundary_axis.max, boundary_axis.unit).convert_to_unit(default_unit).value))
    while "center" in dimension:
        dimension = dimension.replace("center", "({})".format(Dimension(
            boundary_axis.center, boundary_axis.unit).convert_to_unit(default_unit).value))

    return dimension


def get_unit_in_string(dimension_string):
    if not isinstance(dimension_string, str):
        return None

    dimension_string = dimension_string.replace(" ", "").lower()

    unitSearchResults = re.search('[A-Za-z]+$', dimension_string)

    unitInString = unitSearchResults[0] if unitSearchResults else None

    return unitInString if unitInString and not is_reserved_word_in_string(unitInString) else None


def get_dimension_list_from_string_list(dimensions: Union[str, list[str]], bounding_box: Optional[BoundaryBox] = None) -> list[Dimension]:

    if isinstance(dimensions, str):
        dimensions = dimensions.replace(" ", "").lower().split(",")

    assert isinstance(dimensions, (list, tuple)
                      ), "Only a list of strings is allowed."

    parsedDimensions = []

    default_unit = None

    unitInString = get_unit_in_string(dimensions[-1])
    if unitInString is not None:
        default_unit = LengthUnit.from_string(unitInString)
        if len(unitInString) == len(dimensions[-1].replace(" ", "").lower()):
            dimensions.pop()

    for index, dimension in enumerate(dimensions):
        if bounding_box is not None and index < 3:
            boundary_axis = getattr(bounding_box, "xyz"[index])
            parsedDimensions.append(Dimension.from_string(
                dimension, default_unit, boundary_axis))
            continue

        parsedDimensions.append(
            Dimension.from_string(dimension, default_unit, None))

    return parsedDimensions
