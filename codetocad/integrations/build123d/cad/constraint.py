"""
Build123d implementation of Constraint class for assembly constraints.

Note: build123d uses direct positioning rather than parametric constraints.
These methods provide similar functionality through transformations, but
won't maintain constraint relationships after initial application.
"""

import build123d as bd

from codetocad.core.cad.assembly import Constraint as BaseConstraint
from codetocad.core.cad.vertex_edge_solid import Edge, Vertex
from codetocad.core.dimensions.angle import AngleType
from codetocad.core.dimensions.length_expression import LengthType
from codetocad.core.enums.axis import AxisType

from codetocad.integrations.build123d.adapter.constraints import (
    fix_at_location,
    make_tangent,
    make_parallel,
    make_perpendicular,
    create_revolute_joint_location,
    create_prismatic_joint_location,
)


class Constraint(BaseConstraint):
    """Build123d implementation of Constraint operations.

    Note: build123d doesn't have native parametric constraints like
    traditional CAD systems. These methods apply transformations to
    achieve the constraint effect, but the constraints won't update
    if geometry changes.
    """

    def __new__(cls, *args, **kwargs):
        raise TypeError("Do not instantiate a Constraint class, use its methods instead.")

    @staticmethod
    def fix(this: "Vertex|Edge", at: "Vertex|Edge", offset: LengthType = 0) -> None:
        """Fix this to at. Same as coincide.
        
        Note: This modifies the native object in place by moving it
        to the target location.
        """
        # Get the target location
        if isinstance(at, Vertex):
            target = at.to_tuple()
        else:
            # Use the edge's first vertex
            target = at.v1.to_tuple()
        
        # Get the native object to move
        native = this.native
        if native is None:
            raise ValueError("Object has no native build123d object")
        
        # Apply the fix constraint (move to location)
        result = fix_at_location(native, target, offset)
        this.native = result

    @staticmethod
    def tangent(this: Edge, at: Edge) -> None:
        """Make this edge tangent to at.
        
        Note: This is an approximation - build123d doesn't support
        true parametric tangent constraints.
        """
        native_this = this.native
        native_at = at.native
        
        if native_this is None or native_at is None:
            raise ValueError("Edges have no native build123d objects")
        
        # For tangent constraint, we need faces. If dealing with edges,
        # we can try to get associated faces or use edge tangent alignment
        # This is a simplified implementation
        raise NotImplementedError(
            "Tangent constraints are not fully supported in build123d. "
            "Consider using direct positioning instead."
        )

    @staticmethod
    def parallel(this: Edge, at: Edge) -> None:
        """Make this edge parallel to at.
        
        Note: This rotates the object but doesn't maintain the constraint.
        """
        native_this = this.native
        native_at = at.native
        
        if native_this is None or native_at is None:
            raise ValueError("Edges have no native build123d objects")
        
        if isinstance(native_this, bd.Edge) and isinstance(native_at, bd.Edge):
            result = make_parallel(native_this, native_this, native_at)
            this.native = result
        else:
            raise NotImplementedError(
                "Parallel constraint requires native build123d Edge objects"
            )

    @staticmethod
    def perpendicular(this: Edge, at: Edge) -> None:
        """Make this edge perpendicular to at.
        
        Note: This rotates the object but doesn't maintain the constraint.
        """
        native_this = this.native
        native_at = at.native
        
        if native_this is None or native_at is None:
            raise ValueError("Edges have no native build123d objects")
        
        if isinstance(native_this, bd.Edge) and isinstance(native_at, bd.Edge):
            result = make_perpendicular(native_this, native_this, native_at)
            this.native = result
        else:
            raise NotImplementedError(
                "Perpendicular constraint requires native build123d Edge objects"
            )

    @staticmethod
    def revolute(
        this: Edge,
        at: Edge,
        axis: AxisType = "z",
        limit_min: "AngleType|None" = None,
        limit_max: "AngleType|None" = None,
    ) -> None:
        """Create a revolute joint between this and at.
        
        Note: build123d doesn't have native joint support. This creates
        a positioning that represents the joint, but doesn't create
        an actual kinematic constraint.
        """
        # Get the joint center from the 'at' edge
        center = at.v1.to_tuple()
        
        # Create the joint location
        location = create_revolute_joint_location(center, axis)
        
        native = this.native
        if native is None:
            raise ValueError("Edge has no native build123d object")
        
        # Move to joint location
        this.native = native.moved(location)

    @staticmethod
    def prismatic(
        this: Edge,
        at: Edge,
        axis: AxisType = "z",
        limit_min: "LengthType|None" = None,
        limit_max: "LengthType|None" = None,
    ) -> None:
        """Create a prismatic joint between this and at.
        
        Note: build123d doesn't have native joint support. This creates
        a positioning that represents the joint.
        """
        # Get the joint center from the 'at' edge
        center = at.v1.to_tuple()
        
        # Create the joint location
        location = create_prismatic_joint_location(center, axis)
        
        native = this.native
        if native is None:
            raise ValueError("Edge has no native build123d object")
        
        # Move to joint location
        this.native = native.moved(location)

