"""
Constraint operations for build123d - assembly constraints and joints.

Note: build123d primarily uses direct positioning rather than parametric constraints.
These functions provide similar functionality through transformations.
"""

import math
import build123d as bd
from codetocad.core.dimensions.length_expression import LengthExp, LengthType
from codetocad.core.dimensions.angle import Angle, AngleType
from codetocad.core.enums.axis import Axis, AxisType


def get_axis_vector(axis: AxisType) -> tuple[float, float, float]:
    """Convert axis type to direction vector."""
    if isinstance(axis, str):
        axis = Axis.from_string(axis)

    if axis == Axis.X:
        return (1, 0, 0)
    elif axis == Axis.Y:
        return (0, 1, 0)
    elif axis == Axis.Z:
        return (0, 0, 1)
    else:
        return (0, 0, 1)


def fix_at_location(
    obj: "bd.Part | bd.Solid",
    target_location: tuple[float, float, float],
    offset: LengthType = 0,
) -> "bd.Part | bd.Solid":
    """Fix an object at a target location with optional offset."""
    off = float(LengthExp(offset))
    # Apply offset along Z axis by default
    loc = bd.Location(
        (target_location[0], target_location[1], target_location[2] + off)
    )
    return obj.moved(loc)


def make_tangent(
    obj: "bd.Part | bd.Solid",
    this_face: bd.Face,
    target_face: bd.Face,
) -> "bd.Part | bd.Solid":
    """Position object so that a face is tangent to another face.

    Note: This is an approximation - true tangent constraints require
    a constraint solver which build123d doesn't natively support.
    """
    # Get face centers and normals
    this_center = this_face.center()
    target_center = target_face.center()

    # Move object so face centers align
    offset = target_center - this_center
    return obj.moved(bd.Location(offset))


def make_parallel(
    obj: "bd.Part | bd.Solid",
    this_edge: bd.Edge,
    target_edge: bd.Edge,
) -> "bd.Part | bd.Solid":
    """Rotate object so that an edge is parallel to another edge.

    Note: This aligns edge directions but doesn't constrain position.
    """
    # Get edge direction vectors
    this_dir = this_edge.tangent_at(0)
    target_dir = target_edge.tangent_at(0)

    # Calculate rotation needed
    # This is a simplified version - full implementation would use quaternions
    angle = this_dir.get_angle(target_dir)
    if abs(angle) > 0.001:  # Only rotate if not already parallel
        axis = this_dir.cross(target_dir)
        if axis.length > 0.001:
            rotation = bd.Rotation(axis, math.degrees(angle))
            return obj.moved(bd.Location(rotation))

    return obj


def make_perpendicular(
    obj: "bd.Part | bd.Solid",
    this_edge: bd.Edge,
    target_edge: bd.Edge,
) -> "bd.Part | bd.Solid":
    """Rotate object so that an edge is perpendicular to another edge."""
    # Get edge direction vectors
    this_dir = this_edge.tangent_at(0)
    target_dir = target_edge.tangent_at(0)

    # Target perpendicular direction
    perp_dir = target_dir.cross(bd.Vector(0, 0, 1))
    if perp_dir.length < 0.001:
        perp_dir = target_dir.cross(bd.Vector(1, 0, 0))

    # Calculate rotation to make this_dir align with perp_dir
    angle = this_dir.get_angle(perp_dir)
    if abs(angle) > 0.001:
        axis = this_dir.cross(perp_dir)
        if axis.length > 0.001:
            rotation = bd.Rotation(axis, math.degrees(angle))
            return obj.moved(bd.Location(rotation))

    return obj


def create_revolute_joint_location(
    center: tuple[float, float, float],
    axis: AxisType,
    angle: AngleType = 0,
) -> bd.Location:
    """Create a location representing a revolute joint position."""
    axis_vec = get_axis_vector(axis)
    angle_deg = math.degrees(Angle(angle).value)

    rotation = bd.Rotation(axis_vec, angle_deg)
    return bd.Location(center, rotation)


def create_prismatic_joint_location(
    center: tuple[float, float, float],
    axis: AxisType,
    offset: LengthType = 0,
) -> bd.Location:
    """Create a location representing a prismatic joint position."""
    axis_vec = get_axis_vector(axis)
    off = float(LengthExp(offset))

    # Apply offset along the axis
    offset_vec = tuple(a * off for a in axis_vec)
    return bd.Location(
        (
            center[0] + offset_vec[0],
            center[1] + offset_vec[1],
            center[2] + offset_vec[2],
        )
    )
