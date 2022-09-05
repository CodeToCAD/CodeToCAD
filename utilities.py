# utilities.py contains enums and helper functions for CodeToCAD python functionality.

from enum import Enum
import re
import math

reservedWords = ["min", "max", "center"]

def isReservedWordInString(stringToCheck:str) -> bool:
    for word in reservedWords: 
        if word in stringToCheck: return True
    return False

# An enum that uses the enum type and value for comparison
class EquittableEnum(Enum):
    # define the == operator, otherwise we can't compare enums, thanks python
    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value

class Units(EquittableEnum):
    pass


class AngleUnit(Units):
    RADIANS = 0
    DEGREES = 1

    def toDegrees(va):
        return math.degrees()

    def fromString(fromString:str):
        aliases = {
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
        return aliases[fromString.lower()]


class Angle():

  def toRadians(self):
      if self.unit == AngleUnit.DEGREES:
          self.value = math.radians(self.value)

      return self

  def toDegrees(self):
      if self.unit == AngleUnit.RADIANS:
          self.value = math.degrees(self.value)
          
      return self

  # Default unit is degrees if unit not passed
  def __init__(self, value:float, defaultUnit:AngleUnit = AngleUnit.DEGREES):
    
    unit = AngleUnit.fromString(defaultUnit.replace(" ", "").lower()) if type(defaultUnit) is str else defaultUnit
    assert (unit is None and defaultUnit is None) \
        or type(unit) is AngleUnit, \
            "Could not parse default unit."
            
    self.value = value
    self.unit = unit or AngleUnit.DEGREES
    
  def __str__(self) -> str:
      return f"{self.value}{' '+self.unit.name.lower() if self.unit else ''}"

  def __repr__(self) -> str:
      return self.__str__()
      
  def arithmeticPrecheckAndUnitConversion(self, other, operationName):
    if not isinstance(other, Angle):
        other = Angle.fromString(other)
    if other.unit != self.unit:
        if self.unit == AngleUnit.DEGREES:
            other.toDegrees()
        else:
            other.toRadians()
    return other


  def __add__(self, other):
    other = self.arithmeticPrecheckAndUnitConversion(other, "add")
    return Angle(self.value + other.value, self.unit)
  def __sub__(self, other):
    other = self.arithmeticPrecheckAndUnitConversion(other, "subtract")
    return Angle(self.value - other.value, self.unit)
  def __mul__(self, other):
    other = self.arithmeticPrecheckAndUnitConversion(other, "multiply")
    return Angle(self.value * other.value, self.unit)
  def __truediv__(self, other):
    other = self.arithmeticPrecheckAndUnitConversion(other, "divide")
    return Angle(self.value / other.value, self.unit)
  def __floordiv__(self, other):
    other = self.arithmeticPrecheckAndUnitConversion(other, "floor divide")
    return Angle(self.value // other.value, self.unit)
  def __mod__(self, other):
    other = self.arithmeticPrecheckAndUnitConversion(other, "modulo")
    return Angle(self.value % other.value, self.unit)
  def __divmod__(self, other):
    other = self.arithmeticPrecheckAndUnitConversion(other, "divmod")
    return Angle( divmod(self.value, other.value), self.unit)
  def __pow__(self, other, mod=None):
    other = self.arithmeticPrecheckAndUnitConversion(other, "pow")
    return Angle( pow(self.value, other.value,mod), self.unit)
  def __abs__(self):
    return Angle(abs(self.value), self.unit)

  # fromString: takes a string with a math operation and an optional unit of measurement
  # Default unit is degrees if unit not passed
  @staticmethod
  def fromString(fromString:str, defaultUnit:AngleUnit = AngleUnit.DEGREES):
    
    if isinstance(fromString, Angle):
        return fromString

    unit = AngleUnit.fromString(defaultUnit.replace(" ", "").lower()) if type(defaultUnit) is str else defaultUnit
    assert (unit is None and defaultUnit is None) \
        or type(unit) is AngleUnit, \
            "Could not parse default unit."

    if isinstance(fromString, (int, float)):
        return Angle(fromString, unit)

    assert type(fromString) is str, "fromString must be a string."

    fromString = fromString.replace(" ", "").lower()

    value = fromString
    
    # check if a unit is passed into fromString, e.g. "1-(3/4)cm" -> cm
    unitInString = re.search('[A-Za-z]+$', fromString)
    if unitInString:
        value = fromString[0:-1*len(unitInString[0])]
        unitInString = LengthUnit.fromString(unitInString[0])
        unit = unitInString or unit or AngleUnit.DEGREES
    
    # Make sure our value only contains math operations and numbers as a weak safety check before passing it to `eval`
    assert re.match("[+\-*\/%\d\(\)]+", value), f"Value {value} contains characters that are not allowed."

    value = eval(value)

    return Angle(value, unit)


def getAnglesFromStringList(angles):
    
    if type(angles) == str:
        angles = angles.replace(" ","").lower().split(",")


    assert isinstance(angles, (list,tuple)), "Only a list of strings is allowed."

    defaultUnit = None

    angleString = angles[-1]
    
    if type(angleString) == str:
        angleString = angleString.replace(" ", "").lower()
        angleString = re.search('[A-Za-z]+$', angleString)
        
        unitInString = AngleUnit.fromString(angleString[0]) if angleString else None
        if unitInString != None:
            defaultUnit = unitInString
            if len(angleString[0]) == len(angles[-1]):
                angles.pop()

    parsedAngles = []
    for angle in angles:
        parsedAngles.append(Angle.fromString(angle, defaultUnit))

    return parsedAngles

class LengthUnit(Units):
    #metric
    micrometer = 1 / 1000
    millimeter = 1
    centimeter = 10
    meter = 1000
    kilometer = 1000000

    #imperial
    thousandthInch = 25.4 / 1000
    inch = 25.4
    foot = 25.4 * 12
    mile = 25.4 * 63360

    def fromString(fromString:str):
        aliases = {
            #metric
            "micrometer": LengthUnit.micrometer,
            "millimeter": LengthUnit.millimeter,
            "millimeters": LengthUnit.millimeter,
            "centimeter": LengthUnit.centimeter,
            "centimeters": LengthUnit.centimeter,
            "kilometer": LengthUnit.kilometer,
            "meter": LengthUnit.meter,
            "meters": LengthUnit.meter,
            "mm": LengthUnit.millimeter,
            "cm": LengthUnit.centimeter,
            "m": LengthUnit.meter,
            "km": LengthUnit.kilometer,
            #imperial
            "thousandthInch": LengthUnit.thousandthInch,
            "thousandth": LengthUnit.thousandthInch,
            "inch": LengthUnit.inch,
            "inches": LengthUnit.inch,
            "foot": LengthUnit.foot,
            "feet": LengthUnit.foot,
            "mile": LengthUnit.mile,
            "miles": LengthUnit.mile,
            "thou": LengthUnit.thousandthInch,
            "in": LengthUnit.inch,
            "ft": LengthUnit.foot,
            "mi": LengthUnit.mile
        }

        fromString = fromString.lower().replace("(s)","")

        return aliases[fromString] if fromString in aliases else None

    
class Axis(EquittableEnum):
    X = 0
    Y = 1
    Z = 2

    @staticmethod
    def fromString(axis):
        axis = str(axis).lower()
        if axis == "x" or axis == "0":
            return Axis.X
        if axis == "y" or axis == "1":
            return Axis.Y
        if axis == "z" or axis == "2":
            return Axis.Z
        return None

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
    toSpecificLength=0
    scaleFactor=1
    lockAspectRatio=2 # scale one dimension, the others scale with it

class ConstraintTypes(EquittableEnum):
    Translation = 0 # Translation locked between specified start and end points in all axes.
    Rotation = 1 # Rotation locked between specified start and end angles in all axes.
    Pivot = 2 # Rotation locked between specified start and end angles in all axes, but rotation origin is offset.
    Gear = 3 # Rotation of one object is a percentage of another's in a specified axis.

class Point:
    x:float
    y:float
    z:float

class BoundaryAxis:
    min = None
    max = None
    center = None
    unit = LengthUnit.meter
    def __init__(self, min=None, max=None, center=None, unit=LengthUnit.meter):
        self.min = min
        self.max = max
        self.center = center
        self.unit = unit if unit else LengthUnit.meter
    def __str__(self):
        return \
f"""    min   max   unit
x   {self.min}  {self.max}  {self.unit.name+'(s)'}
"""
    def __repr__(self) -> str:
        return self.__str__()


class BoundaryBox:
    x = BoundaryAxis()
    y = BoundaryAxis()
    z = BoundaryAxis()
    def __init__(self, x:BoundaryAxis=BoundaryAxis(), y:BoundaryAxis=BoundaryAxis(), z:BoundaryAxis=BoundaryAxis()):
        self.x = x
        self.y = y
        self.z = z
    def __str__(self):
        return \
f"""    min   max   unit
x   {self.x.min}  {self.x.max}  {self.x.unit.name+'(s)'}
y   {self.y.min}  {self.y.max}  {self.y.unit.name+'(s)'}
z   {self.z.min}  {self.z.max}  {self.z.unit.name+'(s)'}
"""

    def __repr__(self) -> str:
        return self.__str__()

class Dimension():
  def __init__(self, value:float, unit:LengthUnit = None):
    assert isinstance(value, (int, float)) , "Dimension value must be a number."

    unit = LengthUnit.fromString(unit.replace(" ", "").lower()) if type(unit) is str else unit
    assert unit is None or type(unit) is LengthUnit , "Dimension unit must be of type LengthUnit or None."

    self.value = value
    self.unit = unit
  def __str__(self) -> str:
      return f"{self.value}{' '+self.unit.name+'s' if self.unit else ''}"

  def __repr__(self) -> str:
      return self.__str__()

  def convertToUnit(self, targetUnit:LengthUnit) -> float:
    assert self.unit != None, f"Current dimension does not have a unit."
    targetUnit = LengthUnit.fromString(targetUnit) if not isinstance(targetUnit, LengthUnit) else targetUnit
    assert isinstance(targetUnit, LengthUnit), f"Could not convert to unit {targetUnit}"
    self.value = self.value * (self.unit.value/targetUnit.value)
    self.unit = targetUnit
    return self

  def arithmeticPrecheckAndUnitConversion(self, other, operationName):
    if not isinstance(other, Dimension):
        other = Dimension.fromString(other)
    if other.unit != None and other.unit != self.unit:
        other = other.convertToUnit(self.unit)
    return other


  def __add__(self, other):
    other = self.arithmeticPrecheckAndUnitConversion(other, "add")
    return Dimension(self.value + other.value, self.unit)
  def __sub__(self, other):
    other = self.arithmeticPrecheckAndUnitConversion(other, "subtract")
    return Dimension(self.value - other.value, self.unit)
  def __mul__(self, other):
    other = self.arithmeticPrecheckAndUnitConversion(other, "multiply")
    return Dimension(self.value * other.value, self.unit)
  def __truediv__(self, other):
    other = self.arithmeticPrecheckAndUnitConversion(other, "divide")
    return Dimension(self.value / other.value, self.unit)
  def __floordiv__(self, other):
    other = self.arithmeticPrecheckAndUnitConversion(other, "floor divide")
    return Dimension(self.value // other.value, self.unit)
  def __mod__(self, other):
    other = self.arithmeticPrecheckAndUnitConversion(other, "modulo")
    return Dimension(self.value % other.value, self.unit)
  def __divmod__(self, other):
    other = self.arithmeticPrecheckAndUnitConversion(other, "divmod")
    return Dimension( divmod(self.value, other.value), self.unit)
  def __pow__(self, other, mod=None):
    other = self.arithmeticPrecheckAndUnitConversion(other, "pow")
    return Dimension( pow(self.value, other.value,mod), self.unit)
  def __abs__(self):
    return Dimension(abs(self.value), self.unit)

  # fromString: takes a string with a math operation and an optional unit of measurement
  # Default unit is None (scale factor) if it's not passed in
  # examples: "1m", "1.5ft", "3/8in", "1", "1-(3/4)cm" 
  # boundaryAxis is required if min,center,max are used
  @staticmethod
  def fromString(fromString:str, defaultUnit:LengthUnit = None, boundaryAxis:BoundaryAxis = None):

    if isinstance(fromString, Dimension):
        return fromString

    unit = LengthUnit.fromString(defaultUnit.replace(" ", "").lower()) if type(defaultUnit) is str else defaultUnit
    assert (unit is None and defaultUnit is None) \
        or type(unit) is LengthUnit, \
            "Could not parse default unit."

    if isinstance(fromString, (int, float)):
        return Dimension(fromString, unit)

    assert type(fromString) is str, "fromString must be a string."

    fromString = fromString.replace(" ", "").lower()
    value = fromString
    
    # check if a unit is passed into fromString, e.g. "1-(3/4)cm" -> cm
    unitInString = re.search('[A-Za-z]+$', fromString)
    if unitInString and not isReservedWordInString(unitInString[0]):
        value = fromString[0:-1*len(unitInString[0])]
        unitInString = LengthUnit.fromString(unitInString[0])
        unit = unitInString or unit

    # if min,max,center is used, try to parse those words into their respective values.
    if isReservedWordInString(value):
        assert boundaryAxis != None, "min,max,center keywords used, but boundaryAxis is not known."
        assert unit != None, "min,max,center keywords used, but unit is not known."
        value = replaceMinMaxCenterWithRespectiveValue(value, boundaryAxis, unit)
    
    # Make sure our value only contains math operations and numbers as a weak safety check before passing it to `eval`
    assert re.match("[+\-*\/%\d\(\)]+", value), f"Value {value} contains characters that are not allowed."

    value = eval(value)

    return Dimension(value, unit)


# Replace "min|max|center" in "min+0.2" to the value in the bounding box's BoundaryAxis
def replaceMinMaxCenterWithRespectiveValue(dimension:str, boundaryAxis:BoundaryAxis, defaultUnit:LengthUnit):
    dimension = dimension.lower()

    while "min" in dimension:
        dimension = dimension.replace("min","({})".format(Dimension(boundaryAxis.min, boundaryAxis.unit).convertToUnit(defaultUnit).value))
    while "max" in dimension:
        dimension = dimension.replace("max","({})".format(Dimension(boundaryAxis.max, boundaryAxis.unit).convertToUnit(defaultUnit).value))
    while "center" in dimension:
        dimension = dimension.replace("center","({})".format( Dimension(boundaryAxis.center, boundaryAxis.unit).convertToUnit(defaultUnit).value))

    return dimension


def getDimensionsFromStringList(dimensions:list[str], boundingBox:BoundaryBox=None) -> list[Dimension]:

    if type(dimensions) is str:
        dimensions = dimensions.replace(" ","").lower().split(",")

    assert isinstance(dimensions, (list,tuple)), "Only a list of strings is allowed."

    parsedDimensions = []
    
    defaultUnit = LengthUnit.meter

    dimensionString = dimensions[-1]
    
    if type(dimensionString) == str:
        dimensionString = dimensionString.replace(" ", "").lower()
        dimensionString = re.search('[A-Za-z]+$', dimensionString)

        unitInString = LengthUnit.fromString(dimensionString[0]) if dimensionString else None
        if unitInString != None:
            defaultUnit = unitInString
            if len(dimensionString[0]) == len(dimensions[-1]):
                dimensions.pop()

    for index, dimension in enumerate(dimensions):
        if boundingBox != None and index < 3:
            boundaryAxis = getattr(boundingBox, "xyz"[index])
            parsedDimensions.append(Dimension.fromString(dimension, defaultUnit, boundaryAxis))
            continue

        parsedDimensions.append(Dimension.fromString(dimension, defaultUnit, None))

    return parsedDimensions