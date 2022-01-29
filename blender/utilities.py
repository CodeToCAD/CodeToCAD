from enum import Enum
import re

class Units(Enum):
  millimeter = 1
  centimeter = 10
  meter = 1000
  inches = 25.4
  feet = 304.8

  def fromString(fromString:str):
      aliases = {
          "millimeter": Units.millimeter,
          "centimeter": Units.centimeter,
          "meter": Units.meter,
          "inch": Units.inches,
          "inches": Units.inches,
          "foot": Units.feet,
          "feet": Units.feet,
          "mm": Units.millimeter,
          "cm": Units.centimeter,
          "m": Units.meter,
          "in": Units.inches,
          "ft": Units.feet,
      }
      return aliases[fromString]


class Dimension():

  # fromString: takes a string with a math operation and an optional unit of measurement
  # Default unit is mm if unit not passed
  # examples: "1m", "1.5ft", "3/8in", "1", "1-(3/4)cm" 
  def __init__(self, fromString:str, defaultUnit:Units = None):
      
      # python is frustrating and auto-converts a "100" to 100(int) when passed as a parameter.
      fromString = ""+fromString

      fromString = fromString.replace(" ", "")

      unit = re.search('[A-Za-z]+$', fromString)

      if unit:
          value = fromString[0:-1*len(unit[0])]

          self.unit = Units.fromString(unit[0])
      else:
          value = fromString

          self.unit =  defaultUnit or None
      
      # Make sure our value only contains math operations and numbers as a weak safety check before passing it to `eval`
      if re.match("[+\-*\/%\d]+", value):
          self.value = eval(value)
      else:
          self.value = None
      
      if self.unit:
          self.value = Dimension.convertToMillimeters(self.value, self.unit)
        
      self.value = self.value or 1
    
  def convertToMillimeters(value, unit:Units):
      return value * unit.value / 1000 # units are meters by default


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

        defaultUnit = Units.fromString(defaultUnit) if defaultUnit else None
        
        parsedDimensions = [Dimension(dimension, defaultUnit) for dimension in dimensionsArray ]
    elif dimensions and type(dimensions) == str:
        parsedDimensions = [Dimension(dimensions)]
    else:
        print("getDimensionsFromString: ", dimensions, " is not a valid input. Cannot parse dimensions.")

    return parsedDimensions
