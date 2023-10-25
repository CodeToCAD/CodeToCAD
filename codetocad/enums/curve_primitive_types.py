from enum import Enum


class CurvePrimitiveTypes(Enum):
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
