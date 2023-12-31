import math
from typing import Optional, Union

import numpy as np


def get_numpy_array_from_vector_or_matrix(vector_or_matrix):
    if isinstance(vector_or_matrix, Vector):
        return vector_or_matrix.vector
    if isinstance(vector_or_matrix, Matrix):
        return vector_or_matrix.matrix
    if isinstance(vector_or_matrix, Quaternion):
        return vector_or_matrix.to_vector().vector
    return vector_or_matrix


class Vector:
    vector: np.ndarray

    def __init__(
        self,
        vector: Union[tuple[float, float, float], tuple[float, float, float, float]],
    ) -> None:
        self.vector = np.array(vector, dtype=float)

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

    @property
    def xyz(self):
        return Vector(self.vector.tolist()[:2])

    @property
    def length(self):
        sum = 0
        for value in self.vector.tolist():
            sum += pow(value, 2)
        return pow(sum, 1 / 2)

    def to_1x4(self):
        vector = np.ones((1, 4))
        vector[0, : self.vector.shape[0]] = self.vector
        return Vector(vector.tolist())

    def to_1x3(self):
        self.vector = self.vector[0, :3]
        return self

    def __iter__(self):
        return self

    def __next__(self):
        if self.iteratorIndex >= 3:
            self.iteratorIndex = 0
            raise StopIteration
        value = self[self.iteratorIndex]
        self.iteratorIndex += 1
        return value

    def tolist(self):
        return [self.x, self.y, self.z]

    def to_tuple(self):
        return (self.x, self.y, self.z)

    def __sizeof__(self) -> int:
        return self.vector.size

    def __len__(self) -> int:
        return self.__sizeof__()

    def __add__(self, other):
        return Vector(
            np.add(self.vector, get_numpy_array_from_vector_or_matrix(other)).tolist()
        )

    def __sub__(self, other):
        return Vector(
            np.subtract(
                self.vector, get_numpy_array_from_vector_or_matrix(other)
            ).tolist()
        )

    def __mul__(self, other):
        return Vector(
            np.multiply(
                self.vector, get_numpy_array_from_vector_or_matrix(other)
            ).tolist()
        )

    def __pow__(self, other, mod=None):
        return Vector(
            np.power(self.vector, get_numpy_array_from_vector_or_matrix(other)).tolist()
        )

    def __abs__(self):
        return Vector(np.abs(self.vector).tolist())

    def __matmul__(self, other):
        return Vector(
            np.matmul(
                self.vector, get_numpy_array_from_vector_or_matrix(other)
            ).tolist()
        )

    def __copy__(self):
        return self.__deepcopy__()

    def __deepcopy__(self):
        return Vector((self.x, self.y, self.z))

    def copy(self):
        return self.__deepcopy__()

    def __getitem__(self, key):
        return self.vector[key]

    def rotate(self, quat: "Quaternion"):
        self.vector = (self @ quat.to_matrix()).vector

    def __str__(self):
        return f"""x   y   z
{self.x}  {self.y}  {self.z}
"""

    def __repr__(self) -> str:
        return self.__str__()


def create_transformation_matrix_from_euler_angles(
    x_in_radians, y_in_radians, z_in_radians
):
    # References https://stackoverflow.com/a/66431815/9824103

    zRotation = np.identity(4)

    zRotation[0, 0] = math.cos(z_in_radians)
    zRotation[0, 1] = -math.sin(z_in_radians)
    zRotation[1, 0] = math.sin(z_in_radians)
    zRotation[1, 1] = math.cos(z_in_radians)

    rot_x = np.identity(4)

    rot_x[1, 1] = math.cos(x_in_radians)
    rot_x[1, 2] = -math.sin(x_in_radians)
    rot_x[2, 1] = math.sin(x_in_radians)
    rot_x[2, 2] = math.cos(x_in_radians)

    rot_y = np.identity(4)

    rot_y[0, 0] = math.cos(y_in_radians)
    rot_y[0, 2] = math.sin(y_in_radians)
    rot_y[2, 0] = -math.sin(y_in_radians)
    rot_y[2, 2] = math.cos(y_in_radians)

    # X * Y * Z multiplication order:
    return np.dot(rot_x, np.dot(rot_y, zRotation))


class Quaternion:
    def __init__(self, quat: tuple[float, float, float, float]) -> None:
        self.q0 = quat[0]
        self.q1 = quat[1]
        self.q2 = quat[2]
        self.q3 = quat[3]

    def inverted(self):
        return Quaternion((self.q0, self.q1 * -1, self.q2 * -1, self.q3 * -1))

    def __mul__(self, other):
        return Quaternion(
            np.multiply(
                self.to_vector().vector, get_numpy_array_from_vector_or_matrix(other)
            ).tolist()
        )

    def to_vector(self):
        return Vector((self.q0, self.q1, self.q2, self.q3))

    def to_euler(self):
        # references https://automaticaddison.com/how-to-convert-a-quaternion-into-euler-angles-in-python/
        q0 = self.q0
        q1 = self.q1
        q2 = self.q2
        q3 = self.q3
        t0 = +2.0 * (q0 * q1 + q2 * q3)
        t1 = +1.0 - 2.0 * (q1 * q1 + q2 * q2)
        x = math.atan2(t0, t1)

        t2 = +2.0 * (q0 * q2 - q3 * q1)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        y = math.asin(t2)

        t3 = +2.0 * (q0 * q3 + q1 * q2)
        t4 = +1.0 - 2.0 * (q2 * q2 + q3 * q3)
        z = math.atan2(t3, t4)

        return x, y, z  # in radians

    def to_matrix(self):
        # references https://automaticaddison.com/how-to-convert-a-quaternion-to-a-rotation-matrix/
        q0 = self.q0
        q1 = self.q1
        q2 = self.q2
        q3 = self.q3

        # First row of the rotation matrix
        r00 = 2 * (q0 * q0 + q1 * q1) + 1
        r01 = 2 * (q1 * q2 - q0 * q3)
        r02 = 2 * (q1 * q3 + q0 * q2)

        # Second row of the rotation matrix
        r10 = 2 * (q1 * q2 + q0 * q3)
        r11 = 2 * (q0 * q0 + q2 * q2) + 1
        r12 = 2 * (q2 * q3 - q0 * q1)

        # Third row of the rotation matrix
        r20 = 2 * (q1 * q3 - q0 * q2)
        r21 = 2 * (q2 * q3 + q0 * q1)
        r22 = 2 * (q0 * q0 + q3 * q3) - 1

        # 3x3 rotation matrix
        rot_matrix = np.array([[r00, r01, r02], [r10, r11, r12], [r20, r21, r22]])

        return Matrix(rot_matrix)


class Matrix:
    def __init__(self, mat: Optional[np.ndarray] = None) -> None:
        self.matrix = np.identity(4) if mat is None else mat

    @property
    def translation(self):
        return Vector(self.matrix[:3, 3].tolist())

    @property
    def rotation(
        self,
    ):
        return self.get_rotation()

    def get_rotation(self):
        # references https://answers.ros.org/question/388140/converting-a-rotation-matrix-to-quaternions-in-python/?answer=388168#post-id-388168
        m = self.to_3x3().matrix / self.scale_vector.vector
        t = m.trace()
        q = np.asarray([0.0, 0.0, 0.0, 0.0], dtype=np.float64)

        if t > 0:
            t = np.sqrt(t + 1)
            q[3] = 0.5 * t
            t = 0.5 / t
            q[0] = (m[2, 1] - m[1, 2]) * t
            q[1] = (m[0, 2] - m[2, 0]) * t
            q[2] = (m[1, 0] - m[0, 1]) * t

        else:
            i = 0
            if m[1, 1] > m[0, 0]:
                i = 1
            if m[2, 2] > m[i, i]:
                i = 2
            j = (i + 1) % 3
            k = (j + 1) % 3

            t = np.sqrt(m[i, i] - m[j, j] - m[k, k] + 1)
            q[i] = 0.5 * t
            t = 0.5 / t
            q[3] = (m[k, j] - m[j, k]) * t
            q[j] = (m[j, i] + m[i, j]) * t
            q[k] = (m[k, i] + m[i, k]) * t

        return Quaternion(q.tolist())

    @property
    def scale_vector(self):
        x: float = np.linalg.norm(self.matrix[:3, 0], ord=1)
        y: float = np.linalg.norm(self.matrix[:3, 1], ord=1)
        z: float = np.linalg.norm(self.matrix[:3, 2], ord=1)
        return Vector((x, y, z))

    def to_tuple(self):
        return self.matrix.tolist()

    def decompose(self):
        return [self.translation, self.get_rotation(), self.scale_vector]

    def to_4x4(self):
        fourByFour = np.identity(4)
        [rows, cols] = self.matrix.shape
        maxRow = 4 if rows > 4 else rows
        maxCol = 4 if cols > 4 else cols
        fourByFour[:maxRow, :maxCol] = self.matrix
        return Matrix(fourByFour)

    def to_3x3(self):
        return Matrix(self.matrix[:3, :3])

    def to_3x1_vector(self):
        return Vector(self.matrix[:3].tolist())

    @staticmethod
    def Translation(translation: Vector):
        transformMatrix = np.identity(4)

        transformMatrix[0, 3] = translation.x
        transformMatrix[1, 3] = translation.y
        transformMatrix[2, 3] = translation.z
        return Matrix(transformMatrix)

    def translate(self, x, y, z):
        self.matrix = np.add(self.matrix, Matrix.Translation(Vector((x, y, z))).matrix)

        return self

    @staticmethod
    def Diagonal(diagonal: Vector):
        transformMatrix = np.identity(4)

        transformMatrix[0, 0] = diagonal.x
        transformMatrix[1, 1] = diagonal.y
        transformMatrix[2, 2] = diagonal.z
        return Matrix(transformMatrix)

    def scale(self, x, y, z):
        self.matrix = np.matmul(self.matrix, Matrix.Diagonal(Vector((x, y, z))).matrix)

        return self

    def rotate_by_euler_angle(self, x_in_radians, y_in_radians, z_in_radians):
        currenttranslation = self.translation
        self.matrix = np.subtract(
            self.matrix, Matrix.Translation(currenttranslation).matrix
        )
        self.matrix = np.matmul(
            self.matrix,
            create_transformation_matrix_from_euler_angles(
                x_in_radians, y_in_radians, z_in_radians
            ),
        )
        self.matrix = np.add(self.matrix, Matrix.Translation(currenttranslation).matrix)
        return self

    def __add__(self, other):
        return Matrix(np.add(self.matrix, get_numpy_array_from_vector_or_matrix(other)))

    def __sub__(self, other):
        return Matrix(
            np.subtract(self.matrix, get_numpy_array_from_vector_or_matrix(other))
        )

    def __mul__(self, other):
        return Matrix(
            np.multiply(self.matrix, get_numpy_array_from_vector_or_matrix(other))
        )

    def __pow__(self, other, mod=None):
        return Matrix(
            np.power(self.matrix, get_numpy_array_from_vector_or_matrix(other))
        )

    def __abs__(self):
        return Matrix(np.abs(self.matrix))

    def __matmul__(self, other):
        other = get_numpy_array_from_vector_or_matrix(other)
        shapeDifference = self.matrix.shape[1] - other.shape[0]
        if shapeDifference > 0:
            other = np.pad(
                get_numpy_array_from_vector_or_matrix(other),
                (0, shapeDifference),
                constant_values=[1],
            )
        return Matrix(np.matmul(self.matrix, other))
