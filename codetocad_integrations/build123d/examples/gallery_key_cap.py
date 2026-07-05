"""Build123D gallery example: Key Cap.

https://build123d.readthedocs.io/en/stable/examples_1.html

A Cherry MX keyboard key cap: tapered body, spherical dish, hollowed
underside, support ribs and the switch socket. This shape needs the full
Build123D API, so it is a custom CodeToCAD part overriding build_native();
CodeToCAD operations, analysis and export still work on top of it.

The fine features (1mm fillets on a tapered dish) are numerically fragile at
meter scale, so this part is modeled in millimeter numbers and scaled to
meters (CodeToCAD's base unit) on return — a useful pattern for detailed
custom parts.
"""

import build123d as bd

from codetocad_integrations.build123d import Part3D

MM = 0.001


class KeyCap(Part3D):
    def build_native(self) -> bd.Part:
        # Tapered box with a spherical dish on top.
        plan = bd.Rectangle(18, 18)
        key_cap = bd.extrude(plan, amount=10, taper=15)
        key_cap -= bd.Location((0, -3, 47), (90, 0, 0)) * bd.Sphere(40)

        # Round off the edges, then hollow out the underside.
        key_cap = bd.fillet(
            key_cap.edges().filter_by_position(
                bd.Axis.Z, 0, 30, inclusive=(False, True)
            ),
            radius=1,
        )
        key_cap -= bd.scale(key_cap, (0.925, 0.925, 0.85))

        # Support ribs and the switch socket.
        ribs = bd.Rectangle(17.5, 0.5)
        ribs += bd.Rectangle(0.5, 17.5)
        ribs += bd.Circle(radius=5.51 / 2)
        key_cap += bd.extrude(
            bd.Pos(0, 0, 4) * ribs, until=bd.Until.NEXT, target=key_cap
        )

        rib_bottom = key_cap.faces().filter_by_position(bd.Axis.Z, 4, 4)[0]
        socket = bd.Circle(radius=5.5 / 2)
        socket -= bd.Rectangle(4.1, 1.17)
        socket -= bd.Rectangle(1.17, 4.1)
        key_cap += bd.extrude(bd.Plane(rib_bottom) * socket, amount=3.5)

        # Modeled in mm; scale to CodeToCAD's meters.
        return bd.scale(key_cap, MM)


if __name__ == "__main__":
    key_cap = KeyCap(name="key_cap")
    key_cap.export("gallery_key_cap.stl")
    print(f"volume: {key_cap.get_volume() * 1e9:.0f} mm^3")
