from enum import Enum
import re
import math

class Units(Enum):
    # define the == operator, otherwise we can't compare enums, thanks python
    def __eq__(self, other):
        lhs = self.name if self else None
        rhs = other.name if other else None
        return lhs == rhs

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
            "degrees": AngleUnit.DEGREES,
            "degree": AngleUnit.DEGREES,
            "degs": AngleUnit.DEGREES,
            "deg": AngleUnit.DEGREES
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

  # Default unit is radians if unit not passed
  def __init__(self, value:float, unit:AngleUnit = AngleUnit.RADIANS):
      self.value = value
      self.unit = unit

  # fromString: takes a string with a math operation and an optional unit of measurement
  # Default unit is radians if unit not passed
  def __init__(self, fromString:str, unit:AngleUnit = AngleUnit.RADIANS):

      fromString = str(fromString) # safe-guard if a non-string is passed in

      fromString = fromString.replace(" ", "")

      unitInString = re.search('[A-Za-z]+$', fromString)

      if unitInString:
          value = fromString[0:-1*len(unitInString[0])]

          self.unit = AngleUnit.fromString(unitInString[0])
      else:
          value = fromString

          self.unit = unit or AngleUnit.RADIANS
      
      # Make sure our value only contains math operations and numbers as a weak safety check before passing it to `eval`
      if re.match("[+\-*\/%\d]+", value):
          self.value = eval(value)
      else:
          self.value = None

def getAnglesFromString(anglesString):
    
    if type(anglesString) == list:
        anglesString = ",".join(
            map(
                lambda angle:str(angle),
                anglesString
            )
        )

    parsedAngles = None
    if anglesString and "," in anglesString:
        anglesArray = anglesString.split(',')

        # besides accepting a unit in the angle, e.g. 1deg,1rad,1,rad. we also
        # accept the last input as a default unit
        # e.g. 1,1,1,rad => default value radians
        defaultUnit = re.search('[A-Za-z]+$', anglesArray[-1].strip())
        # check if the last value contains only a unit:
        if defaultUnit and len(defaultUnit[0]) == len(anglesArray[-1].strip()):
            defaultUnit = anglesArray.pop().strip()
        else:
            defaultUnit = None

        defaultUnit = AngleUnit.fromString(defaultUnit) if defaultUnit else None
        
        parsedAngles = [Angle(angle, defaultUnit) for angle in anglesArray ]
    elif anglesString and type(anglesString) == str:
        parsedAngles = [Angle(anglesString)]
    else:
        print("getAnglesFromString: ", anglesString, " is not a valid input. Cannot parse angles.")

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
            "millimeter": LengthUnit.millimeter,
            "millimeters": LengthUnit.millimeter,
            "centimeter": LengthUnit.centimeter,
            "centimeters": LengthUnit.centimeter,
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
        return aliases[fromString.lower()]

    
    


class Dimension():

  # Default unit is None (scale factor) if it's not passed in
  def __init__(self, value:float, unit:LengthUnit = None):
      self.value = value
      self.unit = unit

  # fromString: takes a string with a math operation and an optional unit of measurement
  # Default unit is None (scale factor) if it's not passed in
  # examples: "1m", "1.5ft", "3/8in", "1", "1-(3/4)cm" 
  def __init__(self, fromString:str, unit:LengthUnit = None):

      fromString = str(fromString) # safe-guard if a non-string is passed in

      fromString = fromString.replace(" ", "")

      unitInString = re.search('[A-Za-z]+$', fromString)

      if unitInString:
          value = fromString[0:-1*len(unitInString[0])]

          self.unit = LengthUnit.fromString(unitInString[0])
      else:
          value = fromString

          self.unit = unit or None
      
      # Make sure our value only contains math operations and numbers as a weak safety check before passing it to `eval`
      if re.match("[+\-*\/%\d]+", value):
          self.value = eval(value)
      else:
          self.value = None

def convertToLengthUnit(targetUnit:LengthUnit, value, unit:LengthUnit) -> float:
    # LengthUnit enum has conversions based on the millimeter, so multiplying by the enum value will always yield millimeters
    return value * (unit.value/targetUnit.value)

def getDimensionsFromString(dimensions):

    if type(dimensions) == list:
        dimensions = ",".join(
            map(
                lambda dimension:str(dimension),
                dimensions
            )
        )

    parsedDimensions = None
    if dimensions and "," in dimensions:
        dimensionsArray = dimensions.split(',')

        # besides accepting a unit in the dimension, e.g. 1m,1cm,1,m. we also
        # accept the last input as a default unit
        # e.g. 1,1,1,m => default value meter
        defaultUnit = re.search('[A-Za-z]+$', dimensionsArray[-1].strip())
        # check if the last value contains only a unit:
        if defaultUnit and len(defaultUnit[0]) == len(dimensionsArray[-1].strip()):
            defaultUnit = dimensionsArray.pop().strip()
        else:
            defaultUnit = None

        defaultUnit = LengthUnit.fromString(defaultUnit) if defaultUnit else None
        
        parsedDimensions = [Dimension(dimension, defaultUnit) for dimension in dimensionsArray ]
    elif dimensions and type(dimensions) == str:
        parsedDimensions = [Dimension(dimensions)]
    else:
        print("getDimensionsFromString: ", dimensions, " is not a valid input. Cannot parse dimensions.")

    return parsedDimensions

class BlenderLength(Units):
    #metric
    KILOMETERS = LengthUnit.kilometer
    METERS = LengthUnit.meter
    CENTIMETERS = LengthUnit.centimeter
    MILLIMETERS = LengthUnit.millimeter
    MICROMETERS = LengthUnit.micrometer
    #imperial
    MILES = LengthUnit.mile
    FEET = LengthUnit.foot
    INCHES = LengthUnit.inch
    THOU = LengthUnit.thousandthInch

    def getSystem(self):
        if self == self.KILOMETERS or self == self.METERS or self == self.CENTIMETERS or self == self.MILLIMETERS or self == self.MICROMETERS:
            return'METRIC'
        else:
            return'IMPERIAL'

# Use this value to scale any number operations done throughout this implementation
defaultBlenderUnit = BlenderLength.METERS

# Takes in a list of Dimension and converts them to the `defaultBlenderUnit`, which is the unit blender deals with, no matter what we set the document unit to. 
def convertDimensionsToBlenderUnit(dimensions:list):
    return [
        Dimension(
            float(
                convertToLengthUnit(
                    defaultBlenderUnit.value, dimension.value,
                    dimension.unit or defaultBlenderUnit.value
                )
            ),
            defaultBlenderUnit.value
        )
        
            if (dimension.unit != None and dimension.unit != defaultBlenderUnit.value)

            else dimension

                for dimension in dimensions 
    ]

