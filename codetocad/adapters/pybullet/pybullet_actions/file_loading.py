"""
PyBullet file loading and export functions.
"""

from typing import Optional, Tuple, Dict, Any
import pybullet as p
import os
import tempfile
from codetocad.core.dimensions.point import Point


def load_urdf_file(
    urdf_path: str,
    position: Point | Tuple[float, float, float] = (0, 0, 0),
    orientation: Tuple[float, float, float, float] = (0, 0, 0, 1),
    use_fixed_base: bool = False,
    **kwargs,
) -> int:
    """Load a URDF file into the simulation."""
    if not os.path.exists(urdf_path):
        raise FileNotFoundError(f"URDF file not found: {urdf_path}")

    if isinstance(position, Point):
        pos = (position.x, position.y, position.z)
    else:
        pos = position

    body_id = p.loadURDF(
        urdf_path,
        basePosition=pos,
        baseOrientation=orientation,
        useFixedBase=use_fixed_base,
        **kwargs,
    )

    return body_id


def load_stl_file(
    stl_path: str,
    position: Point | Tuple[float, float, float] = (0, 0, 0),
    orientation: Tuple[float, float, float, float] = (0, 0, 0, 1),
    mass: float = 1.0,
    scale: Tuple[float, float, float] = (1, 1, 1),
    **kwargs,
) -> int:
    """Load an STL file as a rigid body."""
    if not os.path.exists(stl_path):
        raise FileNotFoundError(f"STL file not found: {stl_path}")

    if isinstance(position, Point):
        pos = (position.x, position.y, position.z)
    else:
        pos = position

    # Create collision shape from mesh
    collision_shape = p.createCollisionShape(
        p.GEOM_MESH, fileName=stl_path, meshScale=scale, **kwargs
    )

    # Create visual shape from mesh
    visual_shape = p.createVisualShape(
        p.GEOM_MESH, fileName=stl_path, meshScale=scale, **kwargs
    )

    # Create multi-body
    body_id = p.createMultiBody(
        baseMass=mass,
        baseCollisionShapeIndex=collision_shape,
        baseVisualShapeIndex=visual_shape,
        basePosition=pos,
        baseOrientation=orientation,
    )

    return body_id


def load_obj_file(
    obj_path: str,
    position: Point | Tuple[float, float, float] = (0, 0, 0),
    orientation: Tuple[float, float, float, float] = (0, 0, 0, 1),
    mass: float = 1.0,
    scale: Tuple[float, float, float] = (1, 1, 1),
    **kwargs,
) -> int:
    """Load an OBJ file as a rigid body."""
    if not os.path.exists(obj_path):
        raise FileNotFoundError(f"OBJ file not found: {obj_path}")

    if isinstance(position, Point):
        pos = (position.x, position.y, position.z)
    else:
        pos = position

    # Create collision shape from mesh
    collision_shape = p.createCollisionShape(
        p.GEOM_MESH, fileName=obj_path, meshScale=scale, **kwargs
    )

    # Create visual shape from mesh
    visual_shape = p.createVisualShape(
        p.GEOM_MESH, fileName=obj_path, meshScale=scale, **kwargs
    )

    # Create multi-body
    body_id = p.createMultiBody(
        baseMass=mass,
        baseCollisionShapeIndex=collision_shape,
        baseVisualShapeIndex=visual_shape,
        basePosition=pos,
        baseOrientation=orientation,
    )

    return body_id


def export_simulation_state(filename: str) -> None:
    """Export the current simulation state."""
    p.saveWorld(filename)


def restore_simulation_state(filename: str) -> None:
    """Restore simulation state from file."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"State file not found: {filename}")

    p.restoreState(fileName=filename)


def save_body_as_urdf(body_id: int, filename: str) -> None:
    """Save a body as URDF file (limited functionality)."""
    # PyBullet doesn't have direct URDF export, this is a placeholder
    # In practice, you'd need to construct the URDF manually
    pass


def create_urdf_from_part(part: Any, filename: str) -> str:
    """Create a URDF file from a CodeToCAD Part."""
    # Export part to STL first
    stl_filename = filename.replace(".urdf", ".stl")
    part.export.stl(stl_filename)

    # Create basic URDF content
    urdf_content = f"""<?xml version="1.0"?>
<robot name="{part.name or 'part'}">
  <link name="base_link">
    <visual>
      <geometry>
        <mesh filename="{os.path.basename(stl_filename)}"/>
      </geometry>
      <material name="default">
        <color rgba="0.8 0.8 0.8 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <mesh filename="{os.path.basename(stl_filename)}"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
    </inertial>
  </link>
</robot>"""

    # Write URDF file
    with open(filename, "w") as f:
        f.write(urdf_content)

    return filename


def create_urdf_from_assembly(assembly: Any, filename: str) -> str:
    """Create a URDF file from a CodeToCAD Assembly."""
    # This is a simplified implementation
    # In practice, you'd need to handle joints between parts

    urdf_content = f"""<?xml version="1.0"?>
<robot name="{assembly.name or 'assembly'}">
"""

    # Add each part as a link
    for i, part in enumerate(assembly.parts):
        stl_filename = f"{assembly.name or 'assembly'}_part_{i}.stl"
        part.export.stl(stl_filename)

        urdf_content += f"""  <link name="link_{i}">
    <visual>
      <geometry>
        <mesh filename="{os.path.basename(stl_filename)}"/>
      </geometry>
      <material name="default">
        <color rgba="0.8 0.8 0.8 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <mesh filename="{os.path.basename(stl_filename)}"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
    </inertial>
  </link>
"""

        # Add fixed joint to previous link (simplified)
        if i > 0:
            urdf_content += f"""  <joint name="joint_{i}" type="fixed">
    <parent link="link_{i-1}"/>
    <child link="link_{i}"/>
    <origin xyz="0 0 0" rpy="0 0 0"/>
  </joint>
"""

    urdf_content += "</robot>"

    # Write URDF file
    with open(filename, "w") as f:
        f.write(urdf_content)

    return filename


def get_supported_file_formats() -> Dict[str, str]:
    """Get supported file formats for loading."""
    return {
        "urdf": "Unified Robot Description Format",
        "stl": "STereoLithography format",
        "obj": "Wavefront OBJ format",
        "dae": "COLLADA format (limited support)",
        "bullet": "PyBullet native format",
    }


def validate_file_format(filename: str) -> bool:
    """Validate if file format is supported."""
    ext = os.path.splitext(filename)[1].lower().lstrip(".")
    return ext in get_supported_file_formats()


def get_file_info(filename: str) -> Dict[str, Any]:
    """Get information about a file."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")

    stat = os.stat(filename)
    ext = os.path.splitext(filename)[1].lower().lstrip(".")

    return {
        "filename": filename,
        "extension": ext,
        "size": stat.st_size,
        "supported": validate_file_format(filename),
        "format_description": get_supported_file_formats().get(ext, "Unknown format"),
    }
