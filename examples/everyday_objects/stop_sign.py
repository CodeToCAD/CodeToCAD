"""
Stop Sign Example

Creates a complete stop sign with:
- A red hexagonal sign face
- White "STOP" text extruded from the face
- A gray pole supporting the sign

Run with: python examples/everyday_objects/stop_sign.py
"""

from codetocad.core import Solid, Vertex
from codetocad.core.enums.plane import Plane
from codetocad.integrations.build123d import Shape, Draw
from codetocad.integrations.open3d import show_in_open3d


def main() -> Solid:
    """Create a complete stop sign.

    Returns:
        A tuple of (stop_sign_body, stop_text) - the main sign with pole
        and the white "STOP" text (display separately with different colors)
    """
    # Dimensions
    sign_radius = 100  # Radius of the hexagonal sign face
    pole_radius = 10
    pole_height = 300
    sign_thickness = 10
    text_height = 20

    # Create the hexagonal sign face on the XZ plane (vertical orientation)
    hexagon = Draw.polygon(
        center=Vertex(x=0, y=0, z=sign_thickness / 2),
        radius=sign_radius,
        sides=6,
        # plane=Plane.XZ,
    )
    hexagon_solid = Shape.extrude(hexagon, height=sign_thickness)

    # Create "STOP" text on the XZ plane, positioned on the front face of the sign
    # The text is centered at z = sign_thickness (on the front face)
    stop_text_edge = Draw.text(
        "STOP",
        "Arial",
        size=sign_radius * 0.4,
        center=Vertex(x=0, y=0, z=sign_thickness + text_height / 2),
        # plane=Plane.XZ,
    )
    stop_text_solid = Shape.extrude(stop_text_edge, height=text_height)

    # Create the pole (cylinder) extending downward from the sign
    # The pole is on the XZ plane so it extends along the Y axis (downward)
    pole = Shape.cylinder(
        center=Vertex(x=0, y=0, z=-sign_thickness / 2),
        radius=pole_radius,
        height=pole_height,
        plane=Plane.XZ,
    )
    # pole = Shape.rotate(pole, x="90deg")

    # Combine the hexagon sign face with the pole
    stop_sign = Shape.union(hexagon_solid, pole)
    stop_sign = Shape.union(stop_sign, stop_text_solid)

    return stop_sign


if __name__ == "__main__":
    stop_sign = main()

    Shape.export_file(stop_sign, "./stop_sign.stl")

    # Show the stop sign body with red color
    show_in_open3d(stop_sign, color=(0.8, 0.0, 0.0))  # Red stop sign
