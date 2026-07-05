"""Ledgers: most operations are saved in ledgers to be able to build geometry
easily in the federated application."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .location import Location


@dataclass
class BooleanLedger:
    """Stores information about CSG operations."""

    intersected_parts: list[Any] = field(default_factory=list)
    unioned_parts: list[Any] = field(default_factory=list)
    subtracted_parts: list[Any] = field(default_factory=list)

    @property
    def all_parts(self) -> list[Any]:
        return list(
            set(self.intersected_parts)
            | set(self.unioned_parts)
            | set(self.subtracted_parts)
        )


@dataclass
class AssemblyLedger:
    # Assembly2D constraints
    coincide_constraints: list[Any] = field(default_factory=list)
    parallel_constraints: list[Any] = field(default_factory=list)
    perpendicular_constraints: list[Any] = field(default_factory=list)
    tangent_constraints: list[Any] = field(default_factory=list)

    # Assembly3D constraints
    fixed_constraints: list[Any] = field(default_factory=list)
    revolute_constraints: list[Any] = field(default_factory=list)
    prismatic_constraints: list[Any] = field(default_factory=list)

    transformations: list["Location"] = field(default_factory=list)

    @property
    def all_parts(self) -> list[Any]:
        return list(
            set(self.coincide_constraints)
            | set(self.parallel_constraints)
            | set(self.perpendicular_constraints)
            | set(self.tangent_constraints)
            | set(self.fixed_constraints)
            | set(self.revolute_constraints)
            | set(self.prismatic_constraints)
        )
