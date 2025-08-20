"""
build123d-specific part presets.
"""

from typing import TYPE_CHECKING
from uuid import uuid4

from codetocad.interfaces.cad.part.part_presets import PartPresetsInterface
from codetocad.core.dimensions.length_expression import LengthType
from codetocad.adapters.build123d.build123d_actions.geometry import (
    create_cube,
    create_cylinder,
    create_sphere,
)

if TYPE_CHECKING:
    from codetocad.adapters.build123d.cad.assembly.assembly import Assembly
    from codetocad.adapters.build123d.cad.part.part import Part


class PartPresets(PartPresetsInterface):
    """build123d-specific part presets."""

    def __init__(self, assembly: "Assembly|None" = None):
        self.assembly = assembly

    def _post_creation_do_this(self, part: "Part"):
        """Post-creation setup for parts."""
        if self.assembly:
            self.assembly.parts.append(part)

    def cube(self, x: LengthType, y: LengthType, z: LengthType) -> "Part":
        """Create a cube part using build123d primitives."""
        from codetocad.adapters.build123d.cad.part.part import Part

        part = Part()
        part.set_name(f"cube_{str(uuid4())[:8]}")

        # Create cube using build123d
        part.native_instance = create_cube(x, y, z)

        self._post_creation_do_this(part)

        return part

    def cylinder(self, radius: LengthType, height: LengthType) -> "Part":
        """Create a cylinder part using build123d primitives."""
        from codetocad.adapters.build123d.cad.part.part import Part

        part = Part()
        part.set_name(f"cylinder_{str(uuid4())[:8]}")

        # Create cylinder using build123d
        part.native_instance = create_cylinder(radius, height)

        self._post_creation_do_this(part)

        return part

    def sphere(self, radius: LengthType) -> "Part":
        """Create a sphere part using build123d primitives."""
        from codetocad.adapters.build123d.cad.part.part import Part

        part = Part()
        part.set_name(f"sphere_{str(uuid4())[:8]}")

        # Create sphere using build123d
        part.native_instance = create_sphere(radius)

        self._post_creation_do_this(part)

        return part

    def cone(
        self, bottom_radius: LengthType, top_radius: LengthType, height: LengthType
    ) -> "Part":
        """Create a cone part using build123d primitives."""
        from codetocad.adapters.build123d.cad.part.part import Part
        import build123d as bd
        from codetocad.core.dimensions.length_expression import LengthExpression

        part = Part()
        part.set_name(f"cone_{str(uuid4())[:8]}")

        # Create cone using build123d
        bottom_r = float(LengthExpression(bottom_radius))
        top_r = float(LengthExpression(top_radius))
        h = float(LengthExpression(height))

        part.native_instance = bd.Solid.make_cone(bottom_r, top_r, h)

        self._post_creation_do_this(part)

        return part

    def torus(self, major_radius: LengthType, minor_radius: LengthType) -> "Part":
        """Create a torus part using build123d primitives."""
        from codetocad.adapters.build123d.cad.part.part import Part
        import build123d as bd
        from codetocad.core.dimensions.length_expression import LengthExpression

        part = Part()
        part.set_name(f"torus_{str(uuid4())[:8]}")

        # Create torus using build123d
        major_r = float(LengthExpression(major_radius))
        minor_r = float(LengthExpression(minor_radius))

        part.native_instance = bd.Solid.make_torus(major_r, minor_r)

        self._post_creation_do_this(part)

        return part
