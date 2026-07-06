"""Everyday object example: Perforated baking pan.

This example models a simple baking pan based on a 2D drawing
using CodeToCAD primitives (Shape/Draw) on top of build123d.

Dimensions are taken from the drawing but simplified slightly
for clarity rather than exact manufacturing accuracy.
"""

from codetocad.core import Solid, Vertex
from codetocad.core.enums import CardinalDirection
from codetocad.integrations.build123d import Shape
from codetocad.integrations.build123d.cad.selectors import find_edge
from codetocad.integrations.open3d import show_in_open3d


# Overall pan dimensions (from drawing, in millimetres)
LENGTH = 290.0  # long side
WIDTH = 210.0  # short side
HEIGHT = 33.5  # overall depth

# Sheet / wall parameters (simplified)
WALL_THICKNESS = 3.5
FLANGE_WIDTH = 20.0  # horizontal lip around the pan
OUTER_CORNER_RADIUS = 12.0
BOTTOM_FILLET_RADIUS = 2.0

# Perforation parameters (holes in the base)
HOLE_DIAMETER = 12.0
HOLE_ROWS = 7
HOLE_COLS = 9
HOLE_MARGIN_X = 25.0  # distance from outer edge to first/last hole (long side)
HOLE_MARGIN_Y = 25.0  # distance from outer edge to first/last hole (short side)


def _create_pan_body() -> Solid:
    """Create the basic tray shape with outer fillets and inner cavity."""

    # Start from a simple rectangular block representing the outer envelope.
    base_center = Vertex(x=0, y=0, z=0)
    outer = Shape.cuboid(base_center, width=LENGTH, height=WIDTH, depth=HEIGHT)

    # Round the four vertical corner edges using cardinal-direction edge selectors.
    corner_edge_directions = (
        CardinalDirection.FRONT_LEFT,
        CardinalDirection.FRONT_RIGHT,
        CardinalDirection.BACK_LEFT,
        CardinalDirection.BACK_RIGHT,
    )
    vertical_edges = []
    for direction in corner_edge_directions:
        edges_at_direction = find_edge(outer, direction)
        if edges_at_direction:
            # Take the closest edge to the ideal cardinal position
            vertical_edges.append(edges_at_direction[0])
    outer = Shape.fillet(outer, radius=OUTER_CORNER_RADIUS, edges=vertical_edges)

    # Create the inner cavity: inset from the outer edges by wall + flange,
    # and starting above the bottom to leave a solid base thickness.
    inner_length = LENGTH - 2 * (FLANGE_WIDTH + WALL_THICKNESS)
    inner_width = WIDTH - 2 * (FLANGE_WIDTH + WALL_THICKNESS)

    cavity_base = Vertex(x=0, y=0, z=WALL_THICKNESS)
    cavity = Shape.cuboid(
        cavity_base,
        width=inner_length,
        height=inner_width,
        depth=HEIGHT - WALL_THICKNESS,
    )

    pan = Shape.subtract(outer, cavity)

    # Soften the bottom outer edges with a small fillet radius using selectors.
    bottom_edge_directions = (
        CardinalDirection.BOTTOM_FRONT,
        CardinalDirection.BOTTOM_BACK,
        CardinalDirection.BOTTOM_LEFT,
        CardinalDirection.BOTTOM_RIGHT,
    )
    bottom_edges = []
    for direction in bottom_edge_directions:
        edges_at_direction = find_edge(pan, direction)
        if edges_at_direction:
            bottom_edges.append(edges_at_direction[0])
    pan = Shape.fillet(pan, radius=BOTTOM_FILLET_RADIUS, edges=bottom_edges)

    return pan


def _add_perforations(pan: Solid) -> Solid:
    """Drill an evenly spaced grid of through-holes in the base of the pan."""

    hole_radius = HOLE_DIAMETER / 2.0

    # Define usable area for the perforation pattern so the holes stay
    # comfortably inside the side walls.
    usable_length = LENGTH - 2 * HOLE_MARGIN_X
    usable_width = WIDTH - 2 * HOLE_MARGIN_Y

    # Compute spacing between holes along each direction.
    spacing_x = usable_length / (HOLE_COLS - 1) if HOLE_COLS > 1 else 0.0
    spacing_y = usable_width / (HOLE_ROWS - 1) if HOLE_ROWS > 1 else 0.0

    # Place cylinders starting from the bottom of the pan so they cut through
    # the base completely when subtracted.
    for row in range(HOLE_ROWS):
        for col in range(HOLE_COLS):
            x = -usable_length / 2.0 + col * spacing_x
            y = -usable_width / 2.0 + row * spacing_y

            center = Vertex(x=x, y=y, z=0.0)
            hole = Shape.cylinder(center, radius=hole_radius, height=HEIGHT)
            pan = Shape.subtract(pan, hole)

    return pan


def main() -> Solid:
    """Build the perforated baking pan and return it as a Solid."""

    pan = _create_pan_body()
    pan = _add_perforations(pan)
    return pan


if __name__ == "__main__":
    baking_pan = main()
    show_in_open3d(baking_pan)
