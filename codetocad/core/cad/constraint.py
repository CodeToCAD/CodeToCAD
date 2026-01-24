from codetocad.core.cad.vertex_edge_solid import Edge, Vertex
from codetocad.core.dimensions.angle import AngleType
from codetocad.core.dimensions.length_expression import LengthType
from codetocad.core.enums.axis import AxisType

class Constraint:
    """Common joint or mate constraint methods."""

    def __new__(cls, *args, **kwargs):
        raise TypeError(
            f"Do not instantiate a {cls.__name__} class, use its methods instead."
        )

    @staticmethod
    def fix(this: "Vertex|Edge", at: "Vertex|Edge", offset_x: "LengthType" = 0, offset_y: "LengthType" = 0, offset_z: "LengthType" = 0,
    ) -> None:
        """Fix this to at. Same as, coincide."""
        raise NotImplementedError("Method not implemented.")

    @staticmethod
    def tangent(this: "Edge", at: "Edge") -> None:
        """Make this edge tangent to at."""
        raise NotImplementedError("Method not implemented.")

    @staticmethod
    def parallel(this: "Edge", at: "Edge") -> None:
        """Make this edge parallel to at."""
        raise NotImplementedError("Method not implemented.")

    @staticmethod
    def perpendicular(this: "Edge", at: "Edge") -> None:
        """Make this edge perpendicular to at."""
        raise NotImplementedError("Method not implemented.")

    @staticmethod
    def revolute(
        this: "Edge",
        at: "Edge",
        axis: "AxisType" = "z",
        limit_min_x: "AngleType|None" = None,
        limit_max_x: "AngleType|None" = None,
        limit_min_y: "AngleType|None" = None,
        limit_max_y: "AngleType|None" = None,
        limit_min_z: "AngleType|None" = None,
        limit_max_z: "AngleType|None" = None,
    ) -> None:
        """Create a revolute joint (hinge) between this and at.

        Component rotates around axis like a hinge.
        """
        raise NotImplementedError("Method not implemented.")

    @staticmethod
    def prismatic(
        this: "Edge",
        at: "Edge",
        limit_min_x: "LengthType|None" = None,
        limit_max_x: "LengthType|None" = None,
        limit_min_y: "LengthType|None" = None,
        limit_max_y: "LengthType|None" = None,
        limit_min_z: "LengthType|None" = None,
        limit_max_z: "LengthType|None" = None,
    ) -> None:
        """Create a prismatic joint (linear/sliding) between this and at.

        Component moves along a single axis.
        """
        raise NotImplementedError("Method not implemented.")

    @staticmethod
    def ball(
        this: "Vertex|Edge",
        at: "Vertex|Edge",
        angular_range_x: tuple["AngleType", "AngleType"] | None = None,
        angular_range_y: tuple["AngleType", "AngleType"] | None = None,
        angular_range_z: tuple["AngleType", "AngleType"] | None = None,
    ) -> None:
        """Create a ball joint (gimbal) between this and at.

        Component rotates around all 3 axes using a gimbal system.
        """
        raise NotImplementedError("Method not implemented.")

    @staticmethod
    def rigid(this: "Vertex|Edge", at: "Vertex|Edge") -> None:
        """Create a rigid joint (fixed) between this and at.

        Fixes two components to one another with no freedom of movement.
        """
        raise NotImplementedError("Method not implemented.")
