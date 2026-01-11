from enum import Enum, auto


class Plane(Enum):
    """Standard planes for mirroring and orientation."""

    XY = auto()  # Z is normal
    XZ = auto()  # Y is normal (also known as ZX)
    YZ = auto()  # X is normal (also known as ZY)

