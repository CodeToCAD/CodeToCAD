class Vector:
    x: float
    y: float
    z: float

    def __init__(self, vector: tuple[float, float, float]) -> None:
        self.x = vector[0]
        self.y = vector[1]
        self.z = vector[2]

        self.iteratorIndex = 0

    def __iter__(self):
        return self

    def __next__(self):
        value = self[self.iteratorIndex]
        self.iteratorIndex += 1
        if self.iteratorIndex > 3:
            self.iteratorIndex = 0
            raise StopIteration
        return value

    def toList(self):
        return [self.x, self.y, self.z]

    def to_tuple(self):
        return (self.x, self.y, self.z)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Vector((x, y, z))

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Vector((x, y, z))

    def __mul__(self, other):
        x = self.x * other.x
        y = self.y * other.y
        z = self.z * other.z
        return Vector((x, y, z))

    def __truediv__(self, other):
        x = self.x / other.x
        y = self.y / other.y
        z = self.z / other.z
        return Vector((x, y, z))

    def __floordiv__(self, other):
        x = self.x // other.x
        y = self.y // other.y
        z = self.z // other.z
        return Vector((x, y, z))

    def __mod__(self, other):
        x = self.x % other.x
        y = self.y % other.y
        z = self.z % other.z
        return Vector((x, y, z))

    def __pow__(self, other, mod=None):
        x = pow(self.x, other.x)
        y = pow(self.y, other.y)
        z = pow(self.z, other.z)
        return Vector((x, y, z))

    def __abs__(self):
        x = abs(self.x)
        y = abs(self.y)
        z = abs(self.z)
        return Vector((x, y, z))

    def __copy__(self):
        return self.__deepcopy__()

    def __deepcopy__(self):
        return Vector((self.x, self.y, self.z))

    def __matmul__(self, other):
        return Vector((0, 0, 0))

    def copy(self):
        return self.__deepcopy__()

    def __getitem__(self, key):
        if (key == 0):
            return self.x
        if (key == 1):
            return self.y
        if (key == 2):
            return self.z

    def __str__(self):
        return \
            f"""x   y   z
{self.x}  {self.y}  {self.z}
"""

    def __repr__(self) -> str:
        return self.__str__()


class Matrix:
    def __init__(self) -> None:
        pass

    @property
    def translation(self):
        return Vector((0, 0, 0))

    def __matmul__(self, other):
        return Vector((0, 0, 0))
