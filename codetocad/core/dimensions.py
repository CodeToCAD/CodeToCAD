from codetocad.core.dimension import Dimension
from codetocad.core.point import Point


class Dimensions:
    def __init__(self, x: Dimension, y: Dimension, z: Dimension) -> None:
        self.point = Point(x, y, z)

    def to_list(self):
        return self.point.to_list()

    @staticmethod
    def from_point(point: Point) -> "Dimensions":
        return Dimensions(point.x, point.y, point.z)

    @classmethod
    def from_list(cls, dimensions_list: list[Dimension]):
        assert (
            len(dimensions_list) == 3
        ), "Dimensions list must contain three Dimensions."
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
        if key == 0:
            return self.x
        if key == 1:
            return self.y
        if key == 2:
            return self.z
        if key == "radius":
            return self.radius
        if key == "width":
            return self.width
        if key == "length":
            return self.length
        if key == "height":
            return self.height
