"""
MuJoCo XML generation utilities.
"""

from typing import Dict, Any, List, Tuple, Optional
import xml.etree.ElementTree as ET
from codetocad.core.dimensions.point import Point


def create_basic_xml_structure() -> ET.Element:
    """Create basic MuJoCo XML structure."""
    root = ET.Element("mujoco")

    # Add compiler settings
    compiler = ET.SubElement(root, "compiler")
    compiler.set("angle", "radian")
    compiler.set("coordinate", "local")

    # Add default settings
    default = ET.SubElement(root, "default")

    # Add worldbody
    worldbody = ET.SubElement(root, "worldbody")

    return root


def generate_body_xml(
    name: str,
    position: Point | Tuple[float, float, float] = (0, 0, 0),
    orientation: Tuple[float, float, float, float] = (1, 0, 0, 0),
    mass: float = 1.0,
    **kwargs,
) -> ET.Element:
    """Generate XML for a body."""
    body = ET.Element("body")
    body.set("name", name)

    if isinstance(position, Point):
        pos_str = f"{position.x} {position.y} {position.z}"
    else:
        pos_str = f"{position[0]} {position[1]} {position[2]}"
    body.set("pos", pos_str)

    # Convert quaternion to axis-angle if needed
    quat_str = f"{orientation[0]} {orientation[1]} {orientation[2]} {orientation[3]}"
    body.set("quat", quat_str)

    # Add inertial properties
    inertial = ET.SubElement(body, "inertial")
    inertial.set("mass", str(mass))

    return body


def generate_geom_xml(
    name: str,
    geom_type: str = "box",
    size: Tuple[float, ...] = (1, 1, 1),
    position: Point | Tuple[float, float, float] = (0, 0, 0),
    rgba: Tuple[float, float, float, float] = (0.8, 0.8, 0.8, 1.0),
    **kwargs,
) -> ET.Element:
    """Generate XML for a geometry."""
    geom = ET.Element("geom")
    geom.set("name", name)
    geom.set("type", geom_type)

    # Set size
    size_str = " ".join(str(s) for s in size)
    geom.set("size", size_str)

    # Set position
    if isinstance(position, Point):
        pos_str = f"{position.x} {position.y} {position.z}"
    else:
        pos_str = f"{position[0]} {position[1]} {position[2]}"
    geom.set("pos", pos_str)

    # Set color
    rgba_str = f"{rgba[0]} {rgba[1]} {rgba[2]} {rgba[3]}"
    geom.set("rgba", rgba_str)

    return geom


def generate_joint_xml(
    name: str,
    joint_type: str = "hinge",
    axis: Point | Tuple[float, float, float] = (0, 0, 1),
    position: Point | Tuple[float, float, float] = (0, 0, 0),
    limited: bool = False,
    range_limits: Tuple[float, float] | None = None,
    **kwargs,
) -> ET.Element:
    """Generate XML for a joint."""
    joint = ET.Element("joint")
    joint.set("name", name)
    joint.set("type", joint_type)

    # Set axis
    if isinstance(axis, Point):
        axis_str = f"{axis.x} {axis.y} {axis.z}"
    else:
        axis_str = f"{axis[0]} {axis[1]} {axis[2]}"
    joint.set("axis", axis_str)

    # Set position
    if isinstance(position, Point):
        pos_str = f"{position.x} {position.y} {position.z}"
    else:
        pos_str = f"{position[0]} {position[1]} {position[2]}"
    joint.set("pos", pos_str)

    # Set limits
    if limited and range_limits:
        joint.set("limited", "true")
        joint.set("range", f"{range_limits[0]} {range_limits[1]}")

    return joint


def generate_actuator_xml(
    name: str,
    joint_name: str,
    actuator_type: str = "motor",
    gear: float = 1.0,
    **kwargs,
) -> ET.Element:
    """Generate XML for an actuator."""
    actuator = ET.Element(actuator_type)
    actuator.set("name", name)
    actuator.set("joint", joint_name)
    actuator.set("gear", str(gear))

    return actuator


def generate_sensor_xml(
    name: str,
    sensor_type: str = "jointpos",
    joint_name: str | None = None,
    body_name: str | None = None,
    **kwargs,
) -> ET.Element:
    """Generate XML for a sensor."""
    sensor = ET.Element(sensor_type)
    sensor.set("name", name)

    if joint_name:
        sensor.set("joint", joint_name)
    if body_name:
        sensor.set("body", body_name)

    return sensor


def generate_mesh_xml(
    name: str, filename: str, scale: Tuple[float, float, float] = (1, 1, 1)
) -> ET.Element:
    """Generate XML for a mesh asset."""
    mesh = ET.Element("mesh")
    mesh.set("name", name)
    mesh.set("file", filename)

    scale_str = f"{scale[0]} {scale[1]} {scale[2]}"
    mesh.set("scale", scale_str)

    return mesh


def convert_stl_to_mesh(stl_path: str, mesh_name: str) -> ET.Element:
    """Convert STL file reference to MuJoCo mesh XML."""
    return generate_mesh_xml(mesh_name, stl_path)


def convert_part_to_xml(part: Any, name: str | None = None) -> ET.Element:
    """Convert CodeToCAD Part to MuJoCo XML."""
    part_name = name or part.name or "part"

    # Create body element
    body = generate_body_xml(part_name)

    # Add geometry (simplified - would need actual part geometry)
    geom = generate_geom_xml(f"{part_name}_geom", "box", (0.5, 0.5, 0.5))
    body.append(geom)

    return body


def create_ground_plane_xml() -> ET.Element:
    """Create XML for ground plane."""
    return generate_geom_xml(
        "ground", geom_type="plane", size=(10, 10, 0.1), rgba=(0.8, 0.8, 0.8, 1.0)
    )


def create_robot_xml(
    name: str,
    bodies: List[Dict[str, Any]],
    joints: List[Dict[str, Any]] | None = None,
    actuators: List[Dict[str, Any]] | None = None,
) -> ET.Element:
    """Create XML for a complete robot."""
    root = create_basic_xml_structure()
    worldbody = root.find("worldbody")

    # Add ground plane
    ground = create_ground_plane_xml()
    worldbody.append(ground)

    # Add robot body
    robot_body = ET.SubElement(worldbody, "body")
    robot_body.set("name", name)

    # Add bodies
    for body_info in bodies:
        body_xml = generate_body_xml(**body_info)
        robot_body.append(body_xml)

    # Add actuators section if needed
    if actuators:
        actuator_section = ET.SubElement(root, "actuator")
        for actuator_info in actuators:
            actuator_xml = generate_actuator_xml(**actuator_info)
            actuator_section.append(actuator_xml)

    return root


def xml_to_string(xml_element: ET.Element) -> str:
    """Convert XML element to string."""
    ET.indent(xml_element, space="  ", level=0)
    return ET.tostring(xml_element, encoding="unicode")


def save_xml_to_file(xml_element: ET.Element, filename: str) -> None:
    """Save XML element to file."""
    xml_string = xml_to_string(xml_element)
    with open(filename, "w") as f:
        f.write('<?xml version="1.0"?>\n')
        f.write(xml_string)


def load_xml_from_file(filename: str) -> ET.Element:
    """Load XML from file."""
    tree = ET.parse(filename)
    return tree.getroot()


def validate_xml_structure(xml_element: ET.Element) -> bool:
    """Validate basic XML structure for MuJoCo."""
    if xml_element.tag != "mujoco":
        return False

    # Check for required elements
    worldbody = xml_element.find("worldbody")
    if worldbody is None:
        return False

    return True
