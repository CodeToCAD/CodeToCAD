from enum import Enum


class ConstraintTypes(Enum):
    # Translation locked between specified start and end points in all axes.
    LimitLocation = 0
    # Rotation locked between specified start and end angles in all axes.
    LimitRotation = 1
    # Rotation locked between specified start and end angles in all axes, but rotation origin is offset.
    Pivot = 2
    # Rotation of one object is a percentage of another's in a specified axis.
    Gear = 3
    # Fixed position:
    FixedPosition = 4
    # Fixed rotation:
    FixedRotation = 5
