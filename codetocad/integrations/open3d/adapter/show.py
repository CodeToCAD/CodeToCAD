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
    label: "str | None" = None  # Optional text label (e.g., cardinal direction name)


@dataclass
class ColoredEdge:
    """An edge with an associated color for visualization."""

    edge: Edge
    color: "ColorType" = (0.0, 1.0, 0.0)  # Default green
    label: "str | None" = None  # Optional text label (e.g., cardinal direction name)


@dataclass
class ColoredFace:
    """A face (represented as Edge boundary) with an associated color."""

    face: Edge  # Face boundary as Edge
    color: "ColorType" = (0.0, 0.0, 1.0)  # Default blue
    label: "str | None" = None  # Optional text label


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


def _create_text_label(
    text: str,
    position: "tuple[float, float, float]",
    color: "ColorType" = (1.0, 1.0, 1.0),
    size: float = 2.0,
) -> "o3d.geometry.TriangleMesh | None":
    """Create a 3D text label at the given position.

    Args:
        text: The text to display
        position: (x, y, z) position for the text
        color: RGB color for the text
        size: Size/scale of the text

    Returns:
        Open3D TriangleMesh representing the text, or None if text creation fails
    """
    try:
        # Try to create 3D text using Open3D's tensor geometry
        text_mesh = o3d.t.geometry.TriangleMesh.create_text(text, depth=size * 0.1)
        # Convert to legacy TriangleMesh
        text_mesh_legacy = text_mesh.to_legacy()
        # Scale and position the text
        text_mesh_legacy.scale(size, center=(0, 0, 0))
        text_mesh_legacy.translate(position)
        text_mesh_legacy.paint_uniform_color(list(color))
        text_mesh_legacy.compute_vertex_normals()
        return text_mesh_legacy
    except Exception:
        # If text creation fails (not supported in this Open3D version), return None
        return None


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
    show_labels: bool = True,
    label_size: float = 2.0,
    show_coordinates: bool = False,
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
        show_labels: Whether to show text labels for vertices and edges
        label_size: Size of the text labels (default 2.0mm)
        show_coordinates: Whether to show coordinates in labels (default False).
            If True, shows coordinates. If False, shows the label from ColoredVertex/ColoredEdge.
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

            # Add text label for vertex if enabled
            if show_labels:
                x = _get_coord_value(cv.vertex.x)
                y = _get_coord_value(cv.vertex.y)
                z = _get_coord_value(cv.vertex.z)

                # Determine label text: use custom label if provided, otherwise coordinates
                if show_coordinates:
                    label_text = f"({x:.1f}, {y:.1f}, {z:.1f})"
                elif cv.label:
                    label_text = cv.label
                else:
                    label_text = f"({x:.1f}, {y:.1f}, {z:.1f})"

                # Position label slightly offset from vertex
                label_pos = (x + label_size, y + label_size, z + label_size)
                text_mesh = _create_text_label(
                    label_text, label_pos, cv.color, label_size
                )
                if text_mesh:
                    geometries.append(text_mesh)

    # Add edge markers
    if edges:
        for ce in edges:
            cylinder = _create_edge_cylinder(ce.edge, ce.color, edge_radius)
            geometries.append(cylinder)

            # Add text label for edge if enabled
            if show_labels:
                x1 = _get_coord_value(ce.edge.v1.x)
                y1 = _get_coord_value(ce.edge.v1.y)
                z1 = _get_coord_value(ce.edge.v1.z)
                x2 = _get_coord_value(ce.edge.v2.x)
                y2 = _get_coord_value(ce.edge.v2.y)
                z2 = _get_coord_value(ce.edge.v2.z)
                # Position label at edge midpoint
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                mid_z = (z1 + z2) / 2

                # Determine label text: use custom label if provided, otherwise coordinates
                if show_coordinates:
                    label_text = (
                        f"({x1:.1f},{y1:.1f},{z1:.1f})-({x2:.1f},{y2:.1f},{z2:.1f})"
                    )
                elif ce.label:
                    label_text = ce.label
                else:
                    label_text = (
                        f"({x1:.1f},{y1:.1f},{z1:.1f})-({x2:.1f},{y2:.1f},{z2:.1f})"
                    )

                label_pos = (mid_x + label_size, mid_y + label_size, mid_z + label_size)
                text_mesh = _create_text_label(
                    label_text, label_pos, ce.color, label_size
                )
                if text_mesh:
                    geometries.append(text_mesh)

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

    # Set up camera with Z-axis pointing up
    # Get bounding box to position camera appropriately
    bbox = mesh.get_axis_aligned_bounding_box()
    center = bbox.get_center()
    extent = bbox.get_extent()
    max_extent = max(extent)

    # Position camera to look at the object from front-right-top
    # Eye position: in front (-Y), to the right (+X), and above (+Z)
    eye = center + np.array([max_extent * 1.5, -max_extent * 1.5, max_extent * 1.0])
    lookat = center
    up = np.array([0, 0, 1])  # Z-axis points up

    draw(geometries, lookat=lookat, eye=eye, up=up)
