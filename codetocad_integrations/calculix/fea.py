"""The CalculiX/pygccx-backed FEA implementation.

Pipeline: Part3D -> STEP/STL export -> gmsh tetrahedral mesh (via pygccx)
-> node sets from CodeToCAD Locations -> CalculiX static solve -> nodal
displacement + von Mises stress results.

Units are SI: meters, newtons, pascals.
"""

from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path

import numpy as np

import codetocad
from codetocad.fea import FEA, FEAResults
from codetocad.parts import Part3D
from codetocad.simulation import export_single_part


def find_ccx() -> str:
    """Locate the CalculiX solver executable."""
    override = os.environ.get("CODETOCAD_CCX")
    if override:
        return override
    for candidate in ("ccx", "ccx_static"):
        found = shutil.which(candidate)
        if found:
            return found
    home_install = Path.home() / ".codetocad" / "ccx" / "bin" / "ccx"
    if home_install.exists():
        return str(home_install)
    raise FileNotFoundError(
        "CalculiX solver (ccx) not found. Set CODETOCAD_CCX to its path, put "
        "ccx on the PATH, or install it with e.g.\n"
        "  micromamba create -p ~/.codetocad/ccx -c conda-forge calculix"
    )


class CalculixFEA(FEA):
    def __init__(
        self,
        part: Part3D,
        material=None,
        *,
        mesh_size: float | None = None,
        element_order: int = 2,
        ccx_path: str | None = None,
        output_dir: str | Path | None = None,
    ):
        super().__init__(part, material)
        self.mesh_size = mesh_size
        self.element_order = element_order
        self.ccx_path = ccx_path
        self.output_dir = Path(
            output_dir
            if output_dir is not None
            else tempfile.mkdtemp(prefix="codetocad_calculix_")
        ).resolve()

    # -- geometry and meshing --

    def _export_geometry(self) -> Path:
        """Export the part as STEP (exact geometry) if the backend supports
        it, else STL."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        name = self.part.name or "part"
        try:
            path = self.output_dir / f"{name}.step"
            export_single_part(self.part, str(path))
            return path
        except (ValueError, NotImplementedError):
            path = self.output_dir / f"{name}.stl"
            export_single_part(self.part, str(path))
            return path

    def _build_gmsh_mesh(self, gmsh, geometry: Path) -> np.ndarray:
        """Mesh the geometry; returns the surface triangle connectivity
        (corner node ids) for visualization."""
        gmsh.option.setNumber("General.Terminal", 0)
        if geometry.suffix.lower() == ".step":
            gmsh.model.occ.importShapes(str(geometry))
            gmsh.model.occ.synchronize()
        else:
            gmsh.merge(str(geometry))
            gmsh.model.mesh.classifySurfaces(np.pi / 4, True, True)
            gmsh.model.mesh.createGeometry()
            surfaces = [s[1] for s in gmsh.model.getEntities(2)]
            loop = gmsh.model.geo.addSurfaceLoop(surfaces)
            gmsh.model.geo.addVolume([loop])
            gmsh.model.geo.synchronize()

        bbox_min, bbox_max = self.part.get_bounding_box()
        extent = float(
            np.linalg.norm(
                np.asarray(bbox_max.to_tuple()) - np.asarray(bbox_min.to_tuple())
            )
        )
        size = self.mesh_size if self.mesh_size is not None else extent / 25
        gmsh.option.setNumber("Mesh.MeshSizeMax", size)
        gmsh.option.setNumber("Mesh.MeshSizeMin", size / 4)

        volumes = [v[1] for v in gmsh.model.getEntities(3)]
        gmsh.model.addPhysicalGroup(3, volumes, name="part")
        gmsh.model.mesh.generate(3)
        if self.element_order == 2:
            gmsh.model.mesh.setOrder(2)

        # Surface triangles (corner nodes only) for result plotting.
        triangle_type = 2 if self.element_order == 1 else 9
        _, node_tags = gmsh.model.mesh.getElementsByType(triangle_type)
        nodes_per_triangle = 3 if self.element_order == 1 else 6
        connectivity = np.array(node_tags, dtype=int).reshape(-1, nodes_per_triangle)
        return connectivity[:, :3]

    # -- solving --

    def solve(self) -> FEAResults:
        from pygccx import enums
        from pygccx import model as ccx_model
        from pygccx import model_keywords as mk
        from pygccx import step_keywords as sk

        ccx = self.ccx_path or find_ccx()
        geometry = self._export_geometry()

        with ccx_model.Model(
            ccx, ccx, jobname="analysis", working_dir=str(self.output_dir)
        ) as model:
            gmsh = model.get_gmsh()
            surface_triangles_ids = self._build_gmsh_mesh(gmsh, geometry)
            model.update_mesh_from_gmsh()
            mesh = model.mesh

            node_ids = np.array(sorted(mesh.nodes), dtype=int)
            coordinates = np.array([mesh.nodes[i] for i in node_ids])

            def node_set(label: str, location, tolerance):
                indices = self.select_node_indices(coordinates, location, tolerance)
                if len(indices) == 0:
                    raise ValueError(
                        f"No mesh nodes selected for {label} at "
                        f"{location.to_tuple()}; increase the tolerance"
                    )
                return mesh.add_set(
                    label, enums.ESetTypes.NODE, [int(i) for i in node_ids[indices]]
                )

            material = mk.Material(self.material.name or "material")
            elastic = mk.Elastic(
                (self.material.youngs_modulus, self.material.poissons_ratio)
            )
            solid_section = mk.SolidSection(
                elset=mesh.get_el_set_by_name("part"), material=material
            )
            model.add_model_keywords(material, elastic, solid_section)
            if self.material.density is not None:
                model.add_model_keywords(mk.Density(self.material.density.value))

            step = sk.Step(nlgeom=False)
            step.add_step_keywords(sk.Static())
            for index, support in enumerate(self.fixed_supports):
                fix_set = node_set(f"FIX{index}", support.location, support.tolerance)
                step.add_step_keywords(sk.Boundary(fix_set, 1, 0, 3))
            for index, load in enumerate(self.loads):
                load_set = node_set(f"LOAD{index}", load.location, load.tolerance)
                node_count = len(load_set.ids)
                for dof, component in enumerate(load.force, start=1):
                    if component:
                        step.add_step_keywords(
                            sk.Cload(load_set, dof, component / node_count)
                        )
            step.add_step_keywords(
                sk.NodeFile([enums.ENodeFileResults.U]),
                sk.ElFile([enums.EElFileResults.S]),
            )
            model.add_steps(step)
            model.solve()
            frd = model.get_frd_result()

        return self._collect_results(
            frd, node_ids, coordinates, surface_triangles_ids
        )

    def _collect_results(
        self, frd, node_ids, coordinates, surface_triangles_ids
    ) -> FEAResults:
        from pygccx import enums

        displacement_set = frd.get_result_sets_by(entity=enums.EFrdEntities.DISP)[-1]
        stress_set = frd.get_result_sets_by(entity=enums.EFrdEntities.STRESS)[-1]

        displacements = np.array(
            [displacement_set.values[i][:3] for i in node_ids]
        )
        stress = np.array([stress_set.values[i] for i in node_ids])
        sxx, syy, szz, sxy, syz, szx = (stress[:, i] for i in range(6))
        von_mises = np.sqrt(
            0.5 * ((sxx - syy) ** 2 + (syy - szz) ** 2 + (szz - sxx) ** 2)
            + 3.0 * (sxy**2 + syz**2 + szx**2)
        )

        id_to_index = {int(node_id): i for i, node_id in enumerate(node_ids)}
        triangles = np.array(
            [
                [id_to_index[int(n)] for n in triangle]
                for triangle in surface_triangles_ids
                if all(int(n) in id_to_index for n in triangle)
            ],
            dtype=int,
        )
        return FEAResults(
            node_ids=node_ids,
            nodes=coordinates,
            displacements=displacements,
            von_mises=von_mises,
            surface_triangles=triangles,
        )


def analyze(
    part: Part3D,
    material=None,
    *,
    mesh_size: float | None = None,
    element_order: int = 2,
    ccx_path: str | None = None,
    output_dir: str | Path | None = None,
) -> CalculixFEA:
    """Create a CalculiX FEA for ``part``. Add fixtures with ``fix()`` and
    loads with ``add_force()``, then call ``solve()``."""
    return CalculixFEA(
        part,
        material,
        mesh_size=mesh_size,
        element_order=element_order,
        ccx_path=ccx_path,
        output_dir=output_dir,
    )
