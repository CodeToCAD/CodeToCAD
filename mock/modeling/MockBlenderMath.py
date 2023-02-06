import math
from typing import Optional

import numpy as np


def getNumpyArrayFromVectorOrMatrix(vectorOrMatrix):
    if isinstance(vectorOrMatrix, Vector):
        return vectorOrMatrix.vector
    if isinstance(vectorOrMatrix, Matrix):
        return vectorOrMatrix.matrix
    return vectorOrMatrix


class Vector:

    def __init__(self, vector: tuple[float, float, float]) -> None:
        self.vector = np.array(vector)

        self.iteratorIndex = 0

    @property
    def x(self):
        return self.vector[0]

    @property
    def y(self):
        return self.vector[1]

    @property
    def z(self):
        return self.vector[2]

    def __iter__(self):
        return self

    def __next__(self):
        if self.iteratorIndex >= 3:
            self.iteratorIndex = 0
            raise StopIteration
        value = self[self.iteratorIndex]
        self.iteratorIndex += 1
        return value

    def toList(self):
        return [self.x, self.y, self.z]

    def to_tuple(self):
        return (self.x, self.y, self.z)

    def __add__(self, other):
        return Vector(np.add(self.vector, getNumpyArrayFromVectorOrMatrix(other)).tolist())

    def __sub__(self, other):
        return Vector(np.subtract(self.vector, getNumpyArrayFromVectorOrMatrix(other)).tolist())

    def __mul__(self, other):
        return Vector(np.multiply(self.vector, getNumpyArrayFromVectorOrMatrix(other)).tolist())

    def __pow__(self, other, mod=None):
        return Vector(np.power(self.vector, getNumpyArrayFromVectorOrMatrix(other)).tolist())

    def __abs__(self):
        return Vector(np.abs(self.vector).tolist())

    def __matmul__(self, other):
        return Vector(np.matmul(self.vector, getNumpyArrayFromVectorOrMatrix(other)).tolist())

    def __copy__(self):
        return self.__deepcopy__()

    def __deepcopy__(self):
        return Vector((self.x, self.y, self.z))

    def copy(self):
        return self.__deepcopy__()

    def __getitem__(self, key):
        return self.vector[key]

    def __str__(self):
        return \
            f"""x   y   z
{self.x}  {self.y}  {self.z}
"""

    def __repr__(self) -> str:
        return self.__str__()


def createTransformationMatrixFromEulerAngles(xInRadians, yInRadians, zInRadians):
    # References https://stackoverflow.com/a/66431815/9824103

    zRotation = np.identity(4)

    zRotation[0, 0] = math.cos(zInRadians)
    zRotation[0, 1] = -math.sin(zInRadians)
    zRotation[1, 0] = math.sin(zInRadians)
    zRotation[1, 1] = math.cos(zInRadians)

    rot_x = np.identity(4)

    rot_x[1, 1] = math.cos(xInRadians)
    rot_x[1, 2] = -math.sin(xInRadians)
    rot_x[2, 1] = math.sin(xInRadians)
    rot_x[2, 2] = math.cos(xInRadians)

    rot_y = np.identity(4)

    rot_y[0, 0] = math.cos(yInRadians)
    rot_y[0, 2] = math.sin(yInRadians)
    rot_y[2, 0] = -math.sin(yInRadians)
    rot_y[2, 2] = math.cos(yInRadians)

    # X * Y * Z multiplication order:
    return np.dot(rot_x, np.dot(rot_y, zRotation))


class Matrix:
    def __init__(self, mat: Optional[np.ndarray] = None) -> None:
        self.matrix = np.identity(4) if mat is None else mat

    @property
    def translation(self):
        return Vector(self.matrix[:3, 3].tolist())

    def to_tuple(self):
        return self.matrix.tolist()

    def translate(self, x, y, z):
        transformMatrix = np.identity(4)
        transformMatrix[0, 3] = x
        transformMatrix[1, 3] = y
        transformMatrix[2, 3] = z

        self.matrix = np.matmul(
            self.matrix, transformMatrix)

        return self

    def scale(self, x, y, z):
        transformMatrix = np.identity(4)
        transformMatrix[0, 0] = x
        transformMatrix[1, 1] = y
        transformMatrix[2, 2] = z

        self.matrix = np.matmul(
            self.matrix, transformMatrix)

        return self

    def rotateByEulerAngle(self, xInRadians, yInRadians, zInRadians):
        self.matrix = np.matmul(
            self.matrix, createTransformationMatrixFromEulerAngles(xInRadians, yInRadians, zInRadians))
        return self

    def __add__(self, other):
        return Matrix(np.add(self.matrix, getNumpyArrayFromVectorOrMatrix(other)))

    def __sub__(self, other):
        return Matrix(np.subtract(self.matrix, getNumpyArrayFromVectorOrMatrix(other)))

    def __mul__(self, other):
        return Matrix(np.multiply(self.matrix, getNumpyArrayFromVectorOrMatrix(other)))

    def __pow__(self, other, mod=None):
        return Matrix(np.power(self.matrix, getNumpyArrayFromVectorOrMatrix(other)))

    def __abs__(self):
        return Matrix(np.abs(self.matrix))

    def __matmul__(self, other):
        other = getNumpyArrayFromVectorOrMatrix(other)
        shapeDifference = self.matrix.shape[1] - other.shape[0]
        if shapeDifference > 0:
            other = np.pad(getNumpyArrayFromVectorOrMatrix(
                other), (0, shapeDifference), constant_values=[1])
        return Matrix(np.matmul(self.matrix, other))
