from enum import Enum
import re

class Units(Enum):
    # define the == operator, otherwise we can't compare enums, thanks python
    def __eq__(self, other):
        lhs = self.name if self else None
        rhs = other.name if other else None
        return lhs == rhs

class Length(Units):
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
            "millimeter": Length.millimeter,
            "millimeters": Length.millimeter,
            "centimeter": Length.centimeter,
            "centimeters": Length.centimeter,
            "meter": Length.meter,
            "meters": Length.meter,
            "mm": Length.millimeter,
            "cm": Length.centimeter,
            "m": Length.meter,
            "km": Length.kilometer,
            #imperial
            "thousandthInch": Length.thousandthInch,
            "thousandth": Length.thousandthInch,
            "inch": Length.inch,
            "inches": Length.inch,
            "foot": Length.foot,
            "feet": Length.foot,
            "mile": Length.mile,
            "miles": Length.mile,
            "thou": Length.thousandthInch,
            "in": Length.inch,
            "ft": Length.foot,
            "mi": Length.mile
        }
        return aliases[fromString]

    
    


class Dimension():

  # fromString: takes a string with a math operation and an optional unit of measurement
  # Default unit is mm if unit not passed
  # examples: "1m", "1.5ft", "3/8in", "1", "1-(3/4)cm" 
  def __init__(self, value:float, unit:Length = None):
      self.value = value
      self.unit = unit

  def __init__(self, fromString:str, unit:Length = None):
      
      # python is frustrating and auto-converts a "100" to 100(int) when passed as a parameter.
      fromString = str(fromString)

      fromString = fromString.replace(" ", "")

      unitInString = re.search('[A-Za-z]+$', fromString)

      if unitInString:
          value = fromString[0:-1*len(unitInString[0])]

          self.unit = Length.fromString(unitInString[0])
      else:
          value = fromString

          self.unit = unit or None
      
      # Make sure our value only contains math operations and numbers as a weak safety check before passing it to `eval`
      if re.match("[+\-*\/%\d]+", value):
          self.value = eval(value)
      else:
          self.value = None
    
def convertToMillimeters(value, unit:Length) -> float:
    # Length enum has conversions based on the millimeter, so multiplying by the enum value will always yield millimeters
    return value * unit.value

def convertToUnit(targetUnit:Length, value, unit:Length) -> float:
    # Length enum has conversions based on the millimeter, so multiplying by the enum value will always yield millimeters
    return value * (unit.value/targetUnit.value)

def getDimensionsFromString(dimensions):
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

        defaultUnit = Length.fromString(defaultUnit) if defaultUnit else None
        
        parsedDimensions = [Dimension(dimension, defaultUnit) for dimension in dimensionsArray ]
    elif dimensions and type(dimensions) == str:
        parsedDimensions = [Dimension(dimensions)]
    else:
        print("getDimensionsFromString: ", dimensions, " is not a valid input. Cannot parse dimensions.")

    return parsedDimensions

class BlenderLength(Units):
    #metric
    KILOMETERS = Length.kilometer
    METERS = Length.meter
    CENTIMETERS = Length.centimeter
    MILLIMETERS = Length.millimeter
    MICROMETERS = Length.micrometer
    #imperial
    MILES = Length.mile
    FEET = Length.foot
    INCHES = Length.inch
    THOU = Length.thousandthInch

    def getSystem(self):
        if self == self.KILOMETERS or self == self.METERS or self == self.CENTIMETERS or self == self.MILLIMETERS or self == self.MICROMETERS:
            return'METRIC'
        else:
            return'IMPERIAL'

# Use this value to scale any number operations done throughout this implementation
defaultBlenderUnit = BlenderLength.METERS

def convertDimensionsToBlenderUnit(dimensions:list[Dimension]):
    return [
        Dimension(
            float(
                convertToUnit(
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

