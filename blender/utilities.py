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

  def __init__(self, fromString:str):
      
      # python is frustrating and auto-converts a "100" to 100(int) when passed as a parameter.
      fromString = ""+fromString

      fromString = fromString.replace(" ", "")

      value = re.search('\d+', fromString)

      unit = re.search('\D+', fromString)

      self.unit = Units.fromString(unit[0]) if unit else Units.millimeter
      
      if value:
          self.value = Dimension.convertToMillimeters(int(value[0]), self.unit)
    
  def convertToMillimeters(value, unit:Units):
      return value * unit.value


def getDimensionsFromString(dimensions):
    parsedDimensions = None
    if "," in dimensions:
        parsedDimensions = [Dimension(dimension).value for dimension in dimensions.split(',') ]

    return parsedDimensions
