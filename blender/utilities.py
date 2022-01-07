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

          self.unit =  defaultUnit or Units.millimeter
      
      # Make sure our value only contains math operations and numbers as a weak safety check before passing it to `eval`
      if re.match("[+\-*\/%\d]+", value):
          value = eval(value)
      else:
          value = None
      
      if value:
          self.value = Dimension.convertToMillimeters(value, self.unit)
    
  def convertToMillimeters(value, unit:Units):
      return value * unit.value


def getDimensionsFromString(dimensions):
    parsedDimensions = None
    if "," in dimensions:
        dimensionsArray = dimensions.split(',')

        # we accept a 4th input as a the default value
        # e.g. 1,1,1,m => default value meter
        defaultUnit = dimensionsArray.pop().strip() if len(dimensionsArray) == 4 else None
        
        defaultUnit = Units.fromString(defaultUnit) if defaultUnit else None
        
        parsedDimensions = [Dimension(dimension, defaultUnit).value for dimension in dimensionsArray ]

    return parsedDimensions
