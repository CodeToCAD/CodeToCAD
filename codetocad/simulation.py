"""Simulation and lighting primitives.

``Simulation`` is the abstract base implemented by the pybullet and mujoco
integrations: it extracts the kinematic tree (links + joints) recorded by
Assembly3D constraints on a root Part3D, exports each part's mesh, and
federates them to a physics engine via URDF/MJCF.

Frames convention: parts are modeled in place in world coordinates. Each
link's frame sits at its joint anchor (world origin for the root), so a
joint's origin is ``child_anchor - parent_frame`` and mesh vertices are
offset by ``-frame`` inside their link.
"""

from __future__ import annotations

import re
import struct
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

from .location import quat_rotate_vector

if TYPE_CHECKING:
    from .parts import Part3D

#: Assembly constraint operations recorded on ``Part.operations``. Geometry
#: backends skip these; simulation backends turn them into joints.
CONSTRAINT_OPERATIONS = frozenset(
    {
        "fixed",
        "revolute",
        "prismatic",
        "coincide",
        "parallel",
        "perpendicular",
        "tangent",
    }
)

#: Constraint operations that map to simulated joints.
JOINT_OPERATIONS = frozenset({"fixed", "revolute", "prismatic"})


@dataclass
class Lighting:
    """A light in the simulated scene."""

    name: str = "light"
    light_type: str = "directional"
    """One of "directional", "point" or "spot"."""
    position: tuple[float, float, float] = (0.0, 0.0, 3.0)
    direction: tuple[float, float, float] = (0.0, 0.0, -1.0)
    color: tuple[float, float, float] = (1.0, 1.0, 1.0)
    intensity: float = 1.0

    @property
    def diffuse(self) -> tuple[float, float, float]:
        return tuple(min(1.0, c * self.intensity) for c in self.color)


@dataclass
class JointSpec:
    name: str
    joint_type: str  # "fixed" | "revolute" | "prismatic"
    anchor: np.ndarray  # world coordinates
    axis: np.ndarray  # world coordinates, unit
    lower: float | None = None
    upper: float | None = None


@dataclass
class LinkSpec:
    part: "Part3D"
    name: str
    frame: np.ndarray  # world position of the link frame
    parent: "LinkSpec | None" = None
    joint: JointSpec | None = None  # joint connecting this link to parent
    mesh_path: str | None = None
    children: list["LinkSpec"] = field(default_factory=list)

    @property
    def mass(self) -> float:
        """Mass from the part's material, else water density, else 1 kg."""
        try:
            return float(self.part.get_mass().value)
        except (ValueError, NotImplementedError):
            pass
        try:
            return float(self.part.get_volume()) * 1000.0
        except (ValueError, NotImplementedError):
            return 1.0

    @property
    def center_of_mass(self) -> np.ndarray:
        """World-space center of mass (bounding-box center approximation)."""
        bbox_min, bbox_max = self.part.get_bounding_box()
        return (np.array(bbox_min.to_tuple()) + np.array(bbox_max.to_tuple())) / 2

    @property
    def inertia_diagonal(self) -> np.ndarray:
        """Solid-box inertia about the center of mass, from the bounding box."""
        bbox_min, bbox_max = self.part.get_bounding_box()
        size = np.array(bbox_max.to_tuple()) - np.array(bbox_min.to_tuple())
        mass = self.mass
        inertia = (
            mass
            / 12.0
            * np.array(
                [
                    size[1] ** 2 + size[2] ** 2,
                    size[0] ** 2 + size[2] ** 2,
                    size[0] ** 2 + size[1] ** 2,
                ]
            )
        )
        return np.maximum(inertia, 1e-8)

    @property
    def color_rgba(self) -> tuple[float, float, float, float]:
        material = getattr(self.part, "material", None)
        if material is not None and material.color_rgba is not None:
            return material.color_rgba.to_tuple()
        return (0.7, 0.7, 0.7, 1.0)


def _limit_to_float(value) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if hasattr(value, "z"):  # Vec3 limits: use the joint's single dof (z)
        return float(value.z)
    return float(value)


def extract_links(root: "Part3D") -> list[LinkSpec]:
    """Walk the assembly constraints recorded on ``root`` (and descendants)
    into a kinematic tree. Returns links in breadth-first order, root first."""
    used_names: set[str] = set()

    def unique_name(base: str) -> str:
        name = base
        counter = 1
        while name in used_names:
            counter += 1
            name = f"{base}_{counter}"
        used_names.add(name)
        return name

    root_link = LinkSpec(
        part=root,
        name=unique_name(root.name or "base"),
        frame=np.zeros(3),
    )
    links = [root_link]
    seen_parts = {id(root)}
    queue = [root_link]
    while queue:
        parent_link = queue.pop(0)
        for operation in getattr(parent_link.part, "operations", []):
            if operation["operation"] not in JOINT_OPERATIONS:
                continue
            child_part = operation["other_part"]
            if id(child_part) in seen_parts:
                continue
            seen_parts.add(id(child_part))
            location = parent_link.part.resolve_location(operation["location"])
            anchor = location.to_numpy()
            axis = np.asarray(
                quat_rotate_vector(location.quat, (0.0, 0.0, 1.0))
            )
            if location.inverted:
                axis = -axis
            # Snap float residue from quaternion math (e.g. 6e-17) to zero.
            axis = np.where(np.abs(axis) < 1e-9, 0.0, axis)
            child_name = unique_name(child_part.name or "link")
            joint = JointSpec(
                name=location.name or f"{child_name}_joint",
                joint_type=operation["operation"],
                anchor=anchor,
                axis=axis / np.linalg.norm(axis),
                lower=_limit_to_float(operation.get("min_limits")),
                upper=_limit_to_float(operation.get("max_limits")),
            )
            child_link = LinkSpec(
                part=child_part,
                name=child_name,
                frame=anchor.copy(),
                parent=parent_link,
                joint=joint,
            )
            parent_link.children.append(child_link)
            links.append(child_link)
            queue.append(child_link)
    return links


def export_link_meshes(links: list[LinkSpec], directory: str | Path) -> None:
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    for link in links:
        path = directory / f"{link.name}.stl"
        link.part.export(str(path))
        link.mesh_path = str(path)


def ensure_binary_stl(path: str | Path) -> None:
    """Convert an ASCII STL file to binary in place (some engines, like
    MuJoCo, only load binary STL)."""
    path = Path(path)
    with open(path, "rb") as f:
        head = f.read(6)
    if not head.startswith(b"solid"):
        return
    text = path.read_text(errors="ignore")
    if "facet" not in text:
        return
    vertices = re.findall(
        r"vertex\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)", text
    )
    points = np.array(vertices, dtype=np.float64).reshape(-1, 3, 3)
    normals = np.cross(
        points[:, 1] - points[:, 0], points[:, 2] - points[:, 0]
    )
    lengths = np.linalg.norm(normals, axis=1, keepdims=True)
    normals = normals / np.where(lengths == 0, 1.0, lengths)
    with open(path, "wb") as f:
        f.write(b"\0" * 80)
        f.write(struct.pack("<I", len(points)))
        for normal, triangle in zip(normals, points):
            f.write(struct.pack("<3f", *normal))
            for vertex in triangle:
                f.write(struct.pack("<3f", *vertex))
            f.write(struct.pack("<H", 0))


class Simulation:
    """Base class for physics simulations of a CodeToCAD assembly.

    Create one with the ``simulate()`` function of a simulation integration
    (``codetocad_integrations.pybullet`` or ``codetocad_integrations.mujoco``).
    """

    def __init__(
        self,
        root_part: "Part3D",
        *,
        lighting: list[Lighting] | None = None,
        gravity: tuple[float, float, float] = (0.0, 0.0, -9.81),
        time_step: float = 1.0 / 240.0,
        fixed_base: bool = True,
        actuated: bool = True,
    ):
        self.root_part = root_part
        self.lighting = lighting if lighting is not None else [Lighting()]
        self.gravity = gravity
        self.time_step = time_step
        self.fixed_base = fixed_base
        self.actuated = actuated
        self.links = extract_links(root_part)

    @property
    def joint_names(self) -> list[str]:
        return [
            link.joint.name
            for link in self.links
            if link.joint is not None and link.joint.joint_type != "fixed"
        ]

    # -- interface implemented by integrations --

    def step(self, count: int = 1) -> None:
        raise NotImplementedError

    def set_joint_target(self, name: str, value: float) -> None:
        """Position-control a joint towards ``value`` (radians/meters)."""
        raise NotImplementedError

    def set_joint_value(self, name: str, value: float) -> None:
        """Instantly set a joint's value (teleport; no dynamics)."""
        raise NotImplementedError

    def get_joint_value(self, name: str) -> float:
        raise NotImplementedError

    def run(self, duration: float, realtime: bool = False) -> None:
        """Step the simulation for ``duration`` seconds."""
        import time as _time

        steps = int(round(duration / self.time_step))
        for _ in range(steps):
            self.step()
            if realtime:
                _time.sleep(self.time_step)

    def close(self) -> None:
        pass

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()
        return False
