from dataclasses import dataclass
from platform import system
from codetocad.cli.config import get_temp_stl_export_path
from codetocad.core.cad.vertex_edge_solid import Solid, Vertex, Edge
from codetocad.core.dimensions.length_expression import LengthExp
import numpy as np
import open3d as o3d

if system() != "Darwin":
    from open3d.web_visualizer import draw
else:
    # The web visualizer is not available on macOS.
    from open3d.visualization import draw


# Type alias for RGB color as tuple of floats (0.0-1.0)
ColorType = tuple[float, float, float]


@dataclass
class ColoredVertex:
    """A vertex with an associated color for visualization."""

    vertex: Vertex
    color: "ColorType" = (1.0, 0.0, 0.0)  # Default red


@dataclass
class ColoredEdge:
    """An edge with an associated color for visualization."""

    edge: Edge
    color: "ColorType" = (0.0, 1.0, 0.0)  # Default green


@dataclass
class ColoredFace:
    """A face (represented as Edge boundary) with an associated color."""

    face: Edge  # Face boundary as Edge
    color: "ColorType" = (0.0, 0.0, 1.0)  # Default blue


def _get_coord_value(val) -> float:
    """Extract float value from a coordinate (handles float, int, LengthExp, str)."""
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, LengthExp):
        # LengthExp stores meters, but we work in mm for build123d
        return float(val.value) * 1000
    if hasattr(val, "value"):
        return float(val.value)
    return float(val)


def _create_vertex_sphere(
    vertex: Vertex, color: "ColorType", radius: float = 1.0
) -> o3d.geometry.TriangleMesh:
    """Create a small sphere mesh at a vertex position."""
    x = _get_coord_value(vertex.x)
    y = _get_coord_value(vertex.y)
    z = _get_coord_value(vertex.z)

    sphere = o3d.geometry.TriangleMesh.create_sphere(radius=radius)
    sphere.translate([x, y, z])
    sphere.paint_uniform_color(list(color))
    sphere.compute_vertex_normals()
    return sphere


def _create_edge_cylinder(
    edge: Edge, color: "ColorType", radius: float = 0.5
) -> o3d.geometry.TriangleMesh:
    """Create a cylinder mesh along an edge."""
    x1 = _get_coord_value(edge.v1.x)
    y1 = _get_coord_value(edge.v1.y)
    z1 = _get_coord_value(edge.v1.z)
    x2 = _get_coord_value(edge.v2.x)
    y2 = _get_coord_value(edge.v2.y)
    z2 = _get_coord_value(edge.v2.z)

    p1 = np.array([x1, y1, z1])
    p2 = np.array([x2, y2, z2])

    # Calculate length and direction
    direction = p2 - p1
    length = np.linalg.norm(direction)

    if length < 0.001:
        # Degenerate edge, create a sphere instead
        sphere = o3d.geometry.TriangleMesh.create_sphere(radius=radius)
        sphere.translate(p1)
        sphere.paint_uniform_color(list(color))
        sphere.compute_vertex_normals()
        return sphere

    # Create cylinder at origin aligned with Z axis
    cylinder = o3d.geometry.TriangleMesh.create_cylinder(radius=radius, height=length)

    # Calculate rotation to align Z axis with edge direction
    direction_normalized = direction / length
    z_axis = np.array([0, 0, 1])

    # Calculate rotation axis and angle
    dot = np.dot(z_axis, direction_normalized)
    if abs(dot) > 0.9999:
        # Nearly parallel, minimal rotation needed
        if dot < 0:
            # Flip 180 degrees around X axis
            rotation_matrix = np.array(
                [[1, 0, 0], [0, -1, 0], [0, 0, -1]], dtype=np.float64
            )
            cylinder.rotate(rotation_matrix, center=[0, 0, 0])
    else:
        rotation_axis = np.cross(z_axis, direction_normalized)
        rotation_axis = rotation_axis / np.linalg.norm(rotation_axis)
        angle = np.arccos(np.clip(dot, -1.0, 1.0))
        rotation_matrix = o3d.geometry.get_rotation_matrix_from_axis_angle(
            rotation_axis * angle
        )
        cylinder.rotate(rotation_matrix, center=[0, 0, 0])

    # Move to midpoint
    midpoint = (p1 + p2) / 2
    cylinder.translate(midpoint)
    cylinder.paint_uniform_color(list(color))
    cylinder.compute_vertex_normals()
    return cylinder


def _create_coordinate_frame(
    origin: "tuple[float, float, float]",
    size: float = 15.0,
    radius: float = 0.5,
) -> "list[o3d.geometry.TriangleMesh]":
    """Create coordinate frame axes (X=red, Y=green, Z=blue) at the given origin.

    Args:
        origin: (x, y, z) position for the origin of the coordinate frame
        size: Length of each axis arrow
        radius: Radius of the axis cylinders

    Returns:
        List of Open3D meshes representing the coordinate frame
    """
    geometries = []
    ox, oy, oz = origin

    # Colors: X=red, Y=green, Z=blue
    axis_colors = [
        (1.0, 0.0, 0.0),  # X - Red
        (0.0, 1.0, 0.0),  # Y - Green
        (0.0, 0.0, 1.0),  # Z - Blue
    ]
    axis_directions = [
        np.array([1, 0, 0]),  # X
        np.array([0, 1, 0]),  # Y
        np.array([0, 0, 1]),  # Z
    ]

    for color, direction in zip(axis_colors, axis_directions):
        # Create cylinder for axis shaft
        cylinder = o3d.geometry.TriangleMesh.create_cylinder(
            radius=radius, height=size * 0.85
        )
        # Create cone for arrow head
        cone = o3d.geometry.TriangleMesh.create_cone(
            radius=radius * 2.5, height=size * 0.15
        )

        # Rotate to align with axis direction
        z_axis = np.array([0, 0, 1])
        if not np.allclose(direction, z_axis):
            rotation_axis = np.cross(z_axis, direction)
            rotation_axis = rotation_axis / np.linalg.norm(rotation_axis)
            angle = np.arccos(np.dot(z_axis, direction))
            rotation_matrix = o3d.geometry.get_rotation_matrix_from_axis_angle(
                rotation_axis * angle
            )
            cylinder.rotate(rotation_matrix, center=[0, 0, 0])
            cone.rotate(rotation_matrix, center=[0, 0, 0])

        # Position cylinder (centered at half height along axis)
        cylinder.translate(np.array([ox, oy, oz]) + direction * (size * 0.85 / 2))
        # Position cone (at end of cylinder)
        cone.translate(
            np.array([ox, oy, oz]) + direction * (size * 0.85 + size * 0.15 / 2)
        )

        cylinder.paint_uniform_color(list(color))
        cone.paint_uniform_color(list(color))
        cylinder.compute_vertex_normals()
        cone.compute_vertex_normals()

        geometries.append(cylinder)
        geometries.append(cone)

    return geometries


def show_in_open3d(
    shape: Solid,
    color: "ColorType" = (0.5, 0.5, 0.5),
    vertices: "list[ColoredVertex] | None" = None,
    edges: "list[ColoredEdge] | None" = None,
    faces: "list[ColoredFace] | None" = None,
    vertex_radius: float = 1.0,
    edge_radius: float = 0.5,
    show_coordinate_frame: bool = False,
    coordinate_frame_origin: "tuple[float, float, float] | None" = None,
    coordinate_frame_size: float = 15.0,
):
    """Export and visualize a shape with optional colored vertices, edges, and faces.

    Args:
        shape: The solid to visualize
        color: RGB color for the main shape (default gray)
        vertices: List of ColoredVertex objects to highlight
        edges: List of ColoredEdge objects to highlight
        faces: List of ColoredFace objects to highlight (rendered as edge boundaries)
        vertex_radius: Radius of vertex marker spheres
        edge_radius: Radius of edge marker cylinders
        show_coordinate_frame: Whether to show XYZ coordinate frame axes
        coordinate_frame_origin: (x, y, z) position for coordinate frame origin.
            If None, automatically placed outside the shape's bounding box.
        coordinate_frame_size: Size of the coordinate frame axes (default 15mm)
    """
    from codetocad.integrations.build123d.cad.shape import export_file

    export_file(shape, str(get_temp_stl_export_path()))

    mesh = o3d.io.read_triangle_mesh(str(get_temp_stl_export_path()))
    mesh.paint_uniform_color(list(color))
    mesh.compute_vertex_normals()

    # Collect all geometries to display
    geometries = [mesh]

    # Add coordinate frame if requested
    if show_coordinate_frame:
        if coordinate_frame_origin is None:
            # Place coordinate frame outside the bounding box
            bbox = mesh.get_axis_aligned_bounding_box()
            min_bound = bbox.get_min_bound()
            # Place it at the corner minus some offset
            origin = (
                min_bound[0] - coordinate_frame_size * 0.5,
                min_bound[1] - coordinate_frame_size * 0.5,
                min_bound[2] - coordinate_frame_size * 0.5,
            )
        else:
            origin = coordinate_frame_origin
        frame_geoms = _create_coordinate_frame(
            origin, coordinate_frame_size, radius=coordinate_frame_size * 0.03
        )
        geometries.extend(frame_geoms)

    # Add vertex markers
    if vertices:
        for cv in vertices:
            sphere = _create_vertex_sphere(cv.vertex, cv.color, vertex_radius)
            geometries.append(sphere)

    # Add edge markers
    if edges:
        for ce in edges:
            cylinder = _create_edge_cylinder(ce.edge, ce.color, edge_radius)
            geometries.append(cylinder)

    # Add face markers (faces are represented as Edge boundaries)
    # We render the boundary edges of each face
    if faces:
        for cf in faces:
            # If the face has sub_edges, render each sub_edge
            if cf.face.sub_edges:
                for sub_edge in cf.face.sub_edges:
                    cylinder = _create_edge_cylinder(sub_edge, cf.color, edge_radius)
                    geometries.append(cylinder)
            else:
                # Render the main edge
                cylinder = _create_edge_cylinder(cf.face, cf.color, edge_radius)
                geometries.append(cylinder)

    draw(geometries)
