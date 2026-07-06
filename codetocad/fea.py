"""FEA (finite element analysis) primitives.

``FEA`` is the abstract base implemented by FEA integrations (e.g.
``codetocad_integrations.calculix``): fixtures and loads are described with
CodeToCAD Locations on a Part3D, the integration meshes the part's exported
geometry, solves, and returns ``FEAResults``.

Units are SI throughout: meters, newtons, pascals.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import numpy as np

from codetocad.materials import MaterialBase, steel_material

if TYPE_CHECKING:
    from codetocad.location import Location
    from codetocad.parts import Part3D


@dataclass
class FixedSupport:
    location: "Location"
    tolerance: float


@dataclass
class ForceLoad:
    location: "Location"
    force: tuple[float, float, float]
    """Total force in newtons, distributed over the selected nodes."""
    tolerance: float


@dataclass
class FEAResults:
    """Nodal results of a static analysis."""

    node_ids: np.ndarray
    """(N,) original solver node ids."""
    nodes: np.ndarray
    """(N, 3) node coordinates in meters."""
    displacements: np.ndarray
    """(N, 3) nodal displacements in meters."""
    von_mises: np.ndarray
    """(N,) nodal von Mises stress in pascals."""
    surface_triangles: np.ndarray = field(default_factory=lambda: np.empty((0, 3), int))
    """(T, 3) surface triangle corner indices into ``nodes`` (for plotting)."""

    @property
    def displacement_magnitudes(self) -> np.ndarray:
        return np.linalg.norm(self.displacements, axis=1)

    @property
    def max_displacement(self) -> float:
        """Maximum nodal displacement magnitude in meters."""
        return float(self.displacement_magnitudes.max())

    @property
    def max_von_mises(self) -> float:
        """Maximum nodal von Mises stress in pascals."""
        return float(self.von_mises.max())

    def visualize(
        self,
        path: str,
        *,
        field_name: str = "von_mises",
        deform_scale: float | None = None,
        title: str | None = None,
    ) -> str:
        """Render the deformed surface colored by ``field_name`` ("von_mises"
        or "displacement") to an image file. Requires matplotlib."""
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection

        if field_name == "von_mises":
            values = self.von_mises / 1e6
            label = "von Mises stress [MPa]"
        elif field_name == "displacement":
            values = self.displacement_magnitudes * 1000
            label = "displacement [mm]"
        else:
            raise ValueError(f"Unknown field {field_name!r}")

        if deform_scale is None:
            extent = float(np.ptp(self.nodes, axis=0).max())
            max_disp = self.max_displacement
            deform_scale = 0.1 * extent / max_disp if max_disp > 0 else 1.0
        deformed = self.nodes + deform_scale * self.displacements

        triangles = self.surface_triangles
        if len(triangles) == 0:
            raise ValueError("No surface triangles were captured for plotting")
        face_values = values[triangles].mean(axis=1)
        colormap = plt.cm.turbo
        normalize = plt.Normalize(values.min(), values.max())

        figure = plt.figure(figsize=(10, 6))
        axes = figure.add_subplot(projection="3d")
        collection = Poly3DCollection(
            deformed[triangles],
            facecolors=colormap(normalize(face_values)),
            edgecolors="none",
        )
        axes.add_collection3d(collection)
        # Equal aspect box around the deformed shape.
        lower, upper = deformed.min(axis=0), deformed.max(axis=0)
        center, radius = (lower + upper) / 2, float((upper - lower).max()) / 2
        axes.set_xlim(center[0] - radius, center[0] + radius)
        axes.set_ylim(center[1] - radius, center[1] + radius)
        axes.set_zlim(center[2] - radius, center[2] + radius)
        axes.set_xlabel("x [m]")
        axes.set_ylabel("y [m]")
        axes.set_zlabel("z [m]")
        scalar_map = plt.cm.ScalarMappable(norm=normalize, cmap=colormap)
        figure.colorbar(scalar_map, ax=axes, shrink=0.6, label=label)
        axes.set_title(
            title
            or (
                f"max displacement {self.max_displacement * 1000:.3f} mm, "
                f"max von Mises {self.max_von_mises / 1e6:.1f} MPa "
                f"(deformation x{deform_scale:.0f})"
            )
        )
        figure.tight_layout()
        figure.savefig(path, dpi=150)
        plt.close(figure)
        return path


class FEA:
    """Base class for finite element analyses of a Part3D.

    Create one with the ``analyze()`` function of an FEA integration
    (``codetocad_integrations.calculix``)."""

    def __init__(self, part: "Part3D", material: MaterialBase | None = None):
        self.part = part
        self.material = material or getattr(part, "material", None) or steel_material()
        if self.material.youngs_modulus is None or self.material.poissons_ratio is None:
            raise ValueError(
                f"Material {self.material.name!r} has no youngs_modulus/"
                "poissons_ratio; use e.g. steel_material() or set them"
            )
        self.fixed_supports: list[FixedSupport] = []
        self.loads: list[ForceLoad] = []

    def fix(self, location, tolerance: float = 1e-4) -> "FEA":
        """Fully constrain the nodes selected by ``location`` (see
        ``select_node_indices`` for the selection rules)."""
        self.fixed_supports.append(
            FixedSupport(self.part.resolve_location(location), tolerance)
        )
        return self

    def add_force(
        self,
        location,
        force: tuple[float, float, float],
        tolerance: float = 1e-4,
    ) -> "FEA":
        """Apply a total ``force`` (newtons), distributed evenly over the
        nodes selected by ``location``."""
        self.loads.append(
            ForceLoad(
                self.part.resolve_location(location), tuple(force), tolerance
            )
        )
        return self

    def select_node_indices(
        self, coordinates: np.ndarray, location, tolerance: float
    ) -> np.ndarray:
        """Select mesh node indices for a Location.

        If the location's point lies on a face plane of the part's bounding
        box (e.g. ``part.left_center``), all nodes within ``tolerance`` of
        that plane are selected — so cube-location shortcuts select whole
        faces. Otherwise nodes within ``tolerance`` of the point are
        selected."""
        point = np.asarray(location.to_tuple())
        bbox_min, bbox_max = self.part.get_bounding_box()
        bounds = (np.asarray(bbox_min.to_tuple()), np.asarray(bbox_max.to_tuple()))
        for axis in range(3):
            for bound in bounds:
                if abs(point[axis] - bound[axis]) < 1e-9:
                    mask = np.abs(coordinates[:, axis] - bound[axis]) <= tolerance
                    return np.flatnonzero(mask)
        distances = np.linalg.norm(coordinates - point, axis=1)
        return np.flatnonzero(distances <= tolerance)

    def solve(self) -> FEAResults:
        raise NotImplementedError(
            "Use an FEA integration such as codetocad_integrations.calculix"
        )
