from codetocad.core import Solid, Vertex
from codetocad.integrations.build123d import Shape, Draw
from codetocad.integrations.open3d import show_in_open3d


def main() -> Solid:
    c = 50
    hexagon = Draw.polygon(Vertex(x=0, y=0, z=0), radius=2 * c, sides=6)

    stop = Draw.text("STOP", "Arial", 2 * c)

    hexagon_solid = Shape.extrude(hexagon, height=10)

    pole = Shape.cylinder(Vertex(x=0, y=0, z=-50), radius=1, height=100)

    # stop_sign = Shape.boolean_union(hexagon_solid, pole)

    return hexagon_solid, pole


if __name__ == "__main__":
    main_solid, pole = main()
    show_in_open3d(main_solid)
