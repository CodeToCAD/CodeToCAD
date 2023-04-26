from . import utilities as Utilities
from .external.forbiddenfruit import curse, reverse

# Note: this uses a 3rd party plugin: https://github.com/clarete/forbiddenfruit/tree/master to patch python's built-in string class
# This patch allows users to perform string arithmetics like "2mm" * 2, or "(max - min) / 2"


def _multiply(self, other):
    output = f"{self}*{other}"
    if (self in Utilities.reservedWords or other in Utilities.reservedWords):
        return output
    try:
        output = self.__mul__(other)
    except:
        pass
    try:
        left = Utilities.Dimension.fromString(self)
        right = Utilities.Dimension.fromString(other)
        output = str(left * right)
    except:
        pass
    return output


def _add(self, other):
    print(self, ",", other, "add self and other")
    output = f"{self}+{other}"
    if (self in Utilities.reservedWords or other in Utilities.reservedWords):
        return output
    try:
        output = self.__add__(other)
    except:
        pass
    try:
        left = Utilities.Dimension.fromString(self)
        right = Utilities.Dimension.fromString(other)
        output = str(left + right)
    except:
        pass
    return output


def _subtract(self, other):
    output = f"{self}-{other}"
    if (self in Utilities.reservedWords or other in Utilities.reservedWords):
        return output
    try:
        output = self.__sub__(other)
    except:
        pass
    try:
        left = Utilities.Dimension.fromString(self)
        right = Utilities.Dimension.fromString(other)
        output = str(left - right)
    except:
        pass

    return output


def _divide(self, other):
    output = f"{self}/{other}"
    if (self in Utilities.reservedWords or other in Utilities.reservedWords):
        return output
    try:
        output = self.__div__(other)
    except:
        pass
    try:
        left = Utilities.Dimension.fromString(self)
        right = Utilities.Dimension.fromString(other)
        output = str(left / right)
    except:
        pass

    return output


def applyStringExtensions():
    print("CodeToCAD String extensions loaded.")
    curse(str, "__mul__", _multiply)
    curse(str, "__add__", _add)
    curse(str, "__sub__", _subtract)
    curse(str, "__div__", _divide)


def removeStringExtensions():
    print("CodeToCAD String extensions unloaded.")
    reverse(str, "__mul__")
    reverse(str, "__add__")
    reverse(str, "__sub__")
    reverse(str, "__div__")
