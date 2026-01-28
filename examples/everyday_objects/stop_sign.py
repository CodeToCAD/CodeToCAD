"""
Stop Sign Example

Creates a complete stop sign with:
- A red hexagonal sign face
- White "STOP" text extruded from the face
- A gray pole supporting the sign

Run with: python examples/everyday_objects/stop_sign.py
"""

import build123d as bd
from codetocad.core import Solid, Vertex
from codetocad.integrations.build123d import Shape, Draw
from codetocad.integrations.open3d import show_in_open3d


def main() -> tuple[Solid, Solid]:
    """Create a complete stop sign.

    Returns:
        A tuple of (stop_sign_body, stop_text) - the main sign with pole
        and the white "STOP" text (display separately with different colors)
    """
    # Dimensions
    sign_radius = 100  # Radius of the hexagonal sign face
    pole_radius = 5
    pole_height = 300
    sign_thickness = 10
    text_height = 2

    # Create the hexagonal sign face
    hexagon = Draw.polygon(
        center=Vertex(x=0, y=0, z=sign_thickness), radius=sign_radius, sides=6
    )
    hexagon_solid = Shape.extrude(hexagon, height=sign_thickness)

    # Create "STOP" text
    # Each letter is a separate wire, so we extrude all of them together
    stop_text_edge = Draw.text("STOP", "Arial", size=sign_radius * 0.5)
    stop_text_solid = Shape.extrude(stop_text_edge, height=text_height)

    # Move the text to position using native build123d
    native_text = stop_text_solid.get_native()
    if native_text is not None:
        # Move text up to be on top of the hexagon face
        native_text.move(bd.Location((0, 0, sign_thickness)))
        stop_text_solid.set_native(native_text)

    # Create the pole (cylinder) - positioned below the sign
    pole = Shape.cylinder(
        center=Vertex(x=0, y=0, z=-pole_height / 2 + sign_thickness),
        radius=pole_radius,
        height=pole_height,
    )

    # Combine the hexagon sign face with the pole
    stop_sign = Shape.union(hexagon_solid, pole)

    return stop_sign, stop_text_solid


if __name__ == "__main__":
    stop_sign, stop_text = main()

    # Show the stop sign body with red color
    show_in_open3d(stop_sign, color=(0.8, 0.0, 0.0))  # Red stop sign

    # Show the text in a separate window (white)
    show_in_open3d(stop_text, color=(1.0, 1.0, 1.0))  # White text
