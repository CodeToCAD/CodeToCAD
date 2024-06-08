from enum import Enum


class BooleanOperation(str, Enum):
    UNION = "union"
    INTERSECT = "intersect"
    SUBTRACt = "subtract"
