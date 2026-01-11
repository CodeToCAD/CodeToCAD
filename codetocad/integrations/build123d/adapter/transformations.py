"""
Transformation functions for build123d objects.
"""

from typing import Union
import build123d as bd
from codetocad.core.dimensions.length_expression import LengthType, LengthExp


def translate_object(
    obj: Union[bd.Vertex, bd.Edge, bd.Wire, bd.Face, bd.Solid],
    dx: LengthType,
    dy: LengthType,
    dz: LengthType = 0,
) -> Union[bd.Vertex, bd.Edge, bd.Wire, bd.Face, bd.Solid]:
    """Translate a build123d object."""
    dx_val = float(LengthExp(dx))
    dy_val = float(LengthExp(dy))
    dz_val = float(LengthExp(dz))

    translation = bd.Vector(dx_val, dy_val, dz_val)
    return obj.moved(bd.Location(translation))


def rotate_object(
    obj: Union[bd.Vertex, bd.Edge, bd.Wire, bd.Face, bd.Solid],
    axis: bd.Vector,
    angle: float,
) -> Union[bd.Vertex, bd.Edge, bd.Wire, bd.Face, bd.Solid]:
    """Rotate a build123d object around an axis."""
    rotation = bd.Rotation(axis, angle)
    return obj.moved(bd.Location(rotation))


def scale_object(
    obj: Union[bd.Vertex, bd.Edge, bd.Wire, bd.Face, bd.Solid],
    scale_x: float,
    scale_y: float,
    scale_z: float = 1.0,
) -> Union[bd.Vertex, bd.Edge, bd.Wire, bd.Face, bd.Solid]:
    """Scale a build123d object."""
    return bd.scale(obj, (scale_x, scale_y, scale_z))


def mirror_object(
    obj: Union[bd.Vertex, bd.Edge, bd.Wire, bd.Face, bd.Solid],
    plane_normal: bd.Vector,
    plane_point: bd.Vector = bd.Vector(0, 0, 0),
) -> Union[bd.Vertex, bd.Edge, bd.Wire, bd.Face, bd.Solid]:
    """Mirror a build123d object across a plane."""
    # Create a plane for mirroring
    plane = bd.Plane(plane_point, plane_normal)
    return obj.mirror(plane)


def get_bounding_box(obj: Union[bd.Edge, bd.Wire, bd.Face, bd.Solid]) -> bd.BoundBox:
    """Get the bounding box of a build123d object."""
    return obj.bounding_box()


def get_center_of_mass(obj: Union[bd.Face, bd.Solid]) -> bd.Vector:
    """Get the center of mass of a build123d object."""
    return obj.center_of_mass


def get_volume(solid: bd.Solid) -> float:
    """Get the volume of a solid."""
    return solid.volume


def get_area(face: bd.Face) -> float:
    """Get the area of a face."""
    return face.area


def get_length(edge: bd.Edge) -> float:
    """Get the length of an edge."""
    return edge.length
