# Assembly mate interfaces

from .mate_interface import MateInterface, MateType, MateStatus
from .geometric_mate_interface import (
    GeometricMateInterface,
    CoincidentMateInterface,
    ConcentricMateInterface,
    DistanceMateInterface,
    ParallelMateInterface,
    PerpendicularMateInterface,
    TangentMateInterface,
    AngleMateInterface,
)
from .kinematic_mate_interface import (
    KinematicMateInterface,
    RigidMateInterface,
    RevoluteMateInterface,
    LinearMateInterface,
    CylindricalMateInterface,
    BallMateInterface,
)
from .mate_manager_interface import MateManagerInterface

__all__ = [
    # Base interfaces
    "MateInterface",
    "MateType",
    "MateStatus",
    # Geometric mate interfaces
    "GeometricMateInterface",
    "CoincidentMateInterface",
    "ConcentricMateInterface",
    "DistanceMateInterface",
    "ParallelMateInterface",
    "PerpendicularMateInterface",
    "TangentMateInterface",
    "AngleMateInterface",
    # Kinematic mate interfaces
    "KinematicMateInterface",
    "RigidMateInterface",
    "RevoluteMateInterface",
    "LinearMateInterface",
    "CylindricalMateInterface",
    "BallMateInterface",
    # Manager interface
    "MateManagerInterface",
]
