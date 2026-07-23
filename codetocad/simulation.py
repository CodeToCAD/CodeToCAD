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

import inspect
import math
import re
import struct
import tempfile
import zlib
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

from codetocad.location import quat_multiply, quat_rotate_vector
from codetocad.units import LengthMeters

if TYPE_CHECKING:
    from codetocad import Joint
    from codetocad.location import Location
    from codetocad.units import LengthWithUnit


def _axis_angle_quat(axis, angle: float) -> tuple[float, float, float, float]:
    """Quaternion ``(x, y, z, w)`` for a rotation of ``angle`` radians about
    ``axis``."""
    axis = np.asarray(axis, dtype=float)
    norm = float(np.linalg.norm(axis))
    if norm < 1e-12 or abs(angle) < 1e-12:
        return (0.0, 0.0, 0.0, 1.0)
    axis = axis / norm
    sin_half = math.sin(angle / 2.0)
    return (
        float(axis[0] * sin_half),
        float(axis[1] * sin_half),
        float(axis[2] * sin_half),
        float(math.cos(angle / 2.0)),
    )


def _quat_to_matrix(quat: tuple[float, float, float, float]) -> np.ndarray:
    """3x3 rotation matrix from a quaternion ``(x, y, z, w)``."""
    x, y, z, w = quat
    return np.array(
        [
            [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
        ]
    )


def _matrix_to_quat(m: np.ndarray) -> tuple[float, float, float, float]:
    """Quaternion ``(x, y, z, w)`` from a 3x3 rotation matrix."""
    m = np.asarray(m, dtype=float)
    trace = m[0, 0] + m[1, 1] + m[2, 2]
    if trace > 0.0:
        s = math.sqrt(trace + 1.0) * 2.0
        w = 0.25 * s
        x = (m[2, 1] - m[1, 2]) / s
        y = (m[0, 2] - m[2, 0]) / s
        z = (m[1, 0] - m[0, 1]) / s
    elif m[0, 0] > m[1, 1] and m[0, 0] > m[2, 2]:
        s = math.sqrt(1.0 + m[0, 0] - m[1, 1] - m[2, 2]) * 2.0
        w = (m[2, 1] - m[1, 2]) / s
        x = 0.25 * s
        y = (m[0, 1] + m[1, 0]) / s
        z = (m[0, 2] + m[2, 0]) / s
    elif m[1, 1] > m[2, 2]:
        s = math.sqrt(1.0 + m[1, 1] - m[0, 0] - m[2, 2]) * 2.0
        w = (m[0, 2] - m[2, 0]) / s
        x = (m[0, 1] + m[1, 0]) / s
        y = 0.25 * s
        z = (m[1, 2] + m[2, 1]) / s
    else:
        s = math.sqrt(1.0 + m[2, 2] - m[0, 0] - m[1, 1]) * 2.0
        w = (m[1, 0] - m[0, 1]) / s
        x = (m[0, 2] + m[2, 0]) / s
        y = (m[1, 2] + m[2, 1]) / s
        z = 0.25 * s
    return (float(x), float(y), float(z), float(w))

if TYPE_CHECKING:
    from codetocad.parts import Part3D

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
    position: tuple[LengthWithUnit, LengthWithUnit, LengthWithUnit] = (
        0.0,
        0.0,
        3.0,
    )
    """World position, in the usual CodeToCAD length units — floats are meters,
    strings such as ``"30cm"`` are parsed. Stored as :class:`LengthMeters`; read
    :attr:`position_meters` for plain floats."""
    direction: tuple[float, float, float] = (0.0, 0.0, -1.0)
    color: tuple[float, float, float] = (1.0, 1.0, 1.0)
    intensity: float = 1.0

    def __post_init__(self) -> None:
        x, y, z = self.position
        self.position = (LengthMeters(x), LengthMeters(y), LengthMeters(z))

    @property
    def position_meters(self) -> tuple[float, float, float]:
        """The light's position as plain meters, for engine bindings."""
        x, y, z = self.position
        return (float(x), float(y), float(z))

    @property
    def diffuse(self) -> tuple[float, float, float]:
        return tuple(min(1.0, c * self.intensity) for c in self.color)


@dataclass
class Camera:
    """The overview camera every simulation renders from — the viewpoint
    ``capture_image()`` / ``record_gif()`` and the live GUI/viewer use.

    The camera's pose is a :class:`~codetocad.Location`, uniform with the rest
    of CodeToCAD: it sits at the location's position and looks along the
    location's local **+Z** axis, with local **+Y** up — the same
    "+Z is the direction" convention as joint axes and face normals. Leave
    ``location`` ``None`` to auto-frame the whole assembly.

    Aim it without doing quaternion math with :meth:`look_at`::

        Camera.look_at(eye=(2, -2, 1.5), target=(0, 0, 0.3))

    or place it on a part's face — ``Camera(location=part.front_center)`` —
    since a face location's +Z already points along its outward normal. Pass a
    camera to ``simulate(camera=...)`` or set it live with ``sim.set_camera``.
    """

    location: "Location | None" = None
    fov: float = 60.0
    """Vertical field of view in degrees."""

    @classmethod
    def look_at(
        cls,
        eye: tuple[float, float, float],
        target: tuple[float, float, float],
        up: tuple[float, float, float] = (0.0, 0.0, 1.0),
        *,
        fov: float = 60.0,
        name: str | None = None,
    ) -> "Camera":
        """A camera at ``eye`` looking toward ``target``, ``up`` roughly up —
        the ergonomic way to aim the overview camera. Builds the ``Location``
        (local +Z toward ``target``, local +Y up) for you."""
        from codetocad.location import Location

        eye_arr = np.asarray(eye, dtype=float)
        forward = np.asarray(target, dtype=float) - eye_arr
        norm = float(np.linalg.norm(forward))
        if norm < 1e-12:
            raise ValueError("Camera.look_at: eye and target coincide")
        forward = forward / norm
        up_vec = np.asarray(up, dtype=float)
        right = np.cross(up_vec, forward)
        if float(np.linalg.norm(right)) < 1e-9:  # up parallel to the view ray
            fallback = (0.0, 0.0, 1.0) if abs(forward[2]) < 0.9 else (0.0, 1.0, 0.0)
            right = np.cross(np.asarray(fallback), forward)
        right = right / np.linalg.norm(right)
        true_up = np.cross(forward, right)
        # Columns = world directions of the camera's local +X/+Y/+Z axes.
        rotation = np.column_stack((right, true_up, forward))
        quat = _matrix_to_quat(rotation)
        return cls(
            location=Location(
                float(eye_arr[0]), float(eye_arr[1]), float(eye_arr[2]),
                *quat, name=name,
            ),
            fov=fov,
        )

    def resolve(
        self, center, default_distance: float
    ) -> "tuple[np.ndarray, np.ndarray, np.ndarray]":
        """Return ``(eye, target, up)`` in world coordinates — ``target`` a
        point one unit along the view ray. With no ``location`` set, an
        elevated three-quarter view of ``center`` at ``default_distance``."""
        if self.location is not None:
            eye = self.location.to_numpy()
            forward = np.asarray(
                quat_rotate_vector(self.location.quat, (0.0, 0.0, 1.0)), dtype=float
            )
            up = np.asarray(
                quat_rotate_vector(self.location.quat, (0.0, 1.0, 0.0)), dtype=float
            )
            return eye, eye + forward, up
        center = np.asarray(center, dtype=float)
        # Default view direction: yaw 45deg, pitch -35deg (looking down).
        direction = np.array([0.5792279, -0.5792279, -0.5735764])
        direction = direction / np.linalg.norm(direction)
        return center - direction * default_distance, center, np.array(
            [0.0, 0.0, 1.0]
        )


@dataclass
class JointSpec:
    name: str
    joint_type: str  # "fixed" | "revolute" | "prismatic"
    anchor: np.ndarray  # world coordinates
    axis: np.ndarray  # world coordinates, unit
    lower: float | None = None
    upper: float | None = None
    #: Joint value (radians/meters) to apply at simulation start, from
    #: ``starting_angle`` / ``starting_pos``. ``None`` leaves it at zero.
    initial_value: float | None = None
    #: The user-facing ``Joint`` returned by ``.revolute()``/etc, so a
    #: simulation can bind it back for ``joint.move_to(...)`` control.
    joint_obj: Joint | None = None


@dataclass
class LinkSpec:
    part: "Part3D"
    name: str
    frame: np.ndarray  # world position of the (kinematic) link frame
    parent: "LinkSpec | None" = None
    joint: JointSpec | None = None  # joint connecting this link to parent
    mesh_path: str | None = None
    children: list["LinkSpec"] = field(default_factory=list)
    #: World point in the part's *modeled* pose that maps onto the link
    #: origin. Equals ``frame`` for parts modeled in place; differs when a
    #: constraint's ``other_location`` snaps the child into position. Backends
    #: place geometry/inertia relative to this, not ``frame``.
    mesh_frame: np.ndarray | None = None
    #: Net translation applied to this link's modeled geometry to assemble it
    #: (accumulated from ancestor snaps). Descendants inherit it so a snapped
    #: sub-tree stays rigid.
    shift: np.ndarray | None = None
    #: Rigid pose that maps this link's *modeled* geometry to its *assembled
    #: and initially-posed* placement — the translation ``shift`` plus the
    #: rotation/slide of every ancestor joint's ``starting_angle`` /
    #: ``starting_pos``. Geometry export/preview apply this so a design shows
    #: its joints at their starting pose; simulation ignores it (it applies
    #: the starting value as live joint state instead). With no starting
    #: values anywhere, it reduces to ``shift`` (identity rotation).
    pose_rotation: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)
    pose_offset: np.ndarray | None = None

    def __post_init__(self):
        if self.mesh_frame is None:
            self.mesh_frame = self.frame
        if self.shift is None:
            self.shift = np.zeros(3)
        if self.pose_offset is None:
            self.pose_offset = np.asarray(self.shift, dtype=float).copy()

    @property
    def assembly_matrix(self) -> np.ndarray:
        """The 4x4 form of ``(pose_rotation, pose_offset)`` — for backends that
        apply a homogeneous transform (open3d, Blender)."""
        matrix = np.eye(4)
        matrix[:3, :3] = _quat_to_matrix(self.pose_rotation)
        matrix[:3, 3] = self.pose_offset
        return matrix

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
            # Joint anchor in assembled world: the parent's location, carried
            # by whatever shift already assembled the parent.
            anchor = location.to_numpy() + parent_link.shift
            axis = np.asarray(
                quat_rotate_vector(location.quat, (0.0, 0.0, 1.0))
            )
            if location.inverted:
                axis = -axis
            # Snap float residue from quaternion math (e.g. 6e-17) to zero.
            axis = np.where(np.abs(axis) < 1e-9, 0.0, axis)
            # The child snaps so its ``other_location`` (in its modeled pose)
            # lands on the joint anchor; with no other_location it is taken as
            # already in place at the parent's location.
            other_location = operation.get("other_location")
            if other_location is not None:
                mesh_frame = child_part.resolve_location(other_location).to_numpy()
            else:
                mesh_frame = location.to_numpy()
            child_name = unique_name(child_part.name or "link")
            joint = JointSpec(
                name=location.name or f"{child_name}_joint",
                joint_type=operation["operation"],
                anchor=anchor,
                axis=axis / np.linalg.norm(axis),
                lower=_limit_to_float(operation.get("min_limits")),
                upper=_limit_to_float(operation.get("max_limits")),
                initial_value=operation.get("initial_value"),
                joint_obj=operation.get("joint_obj"),
            )
            child_link = LinkSpec(
                part=child_part,
                name=child_name,
                frame=anchor.copy(),
                parent=parent_link,
                joint=joint,
                mesh_frame=mesh_frame,
                shift=anchor - mesh_frame,
            )
            parent_link.children.append(child_link)
            links.append(child_link)
            queue.append(child_link)
    _assign_assembly_poses(links)
    return links


def _assign_assembly_poses(links: list[LinkSpec]) -> None:
    """Bake each joint's ``starting_angle``/``starting_pos`` into a rigid
    ``(pose_rotation, pose_offset)`` per link, so geometry export/preview show
    the assembly at its starting pose. A joint rotates (revolute) or slides
    (prismatic) its whole sub-tree about its anchor; descendants inherit their
    ancestors' motion. ``links`` are breadth-first (parents before children)."""
    # (q, t): the rotation applied to already-assembled geometry and the
    # translation it carries, excluding the link's own ``shift``.
    outer: dict[str, tuple[tuple[float, float, float, float], np.ndarray]] = {}
    for link in links:
        if link.parent is None:
            rotation, translation = (0.0, 0.0, 0.0, 1.0), np.zeros(3)
        else:
            joint = link.joint
            value = joint.initial_value if joint is not None else None
            if joint and value and joint.joint_type == "revolute":
                local_q = _axis_angle_quat(joint.axis, value)
                anchor = np.asarray(link.frame, dtype=float)
                local_t = anchor - quat_rotate_vector(local_q, anchor)
            elif joint and value and joint.joint_type == "prismatic":
                local_q = (0.0, 0.0, 0.0, 1.0)
                local_t = np.asarray(joint.axis, dtype=float) * value
            else:
                local_q, local_t = (0.0, 0.0, 0.0, 1.0), np.zeros(3)
            parent_q, parent_t = outer[link.parent.name]
            rotation = quat_multiply(parent_q, local_q)
            translation = quat_rotate_vector(parent_q, local_t) + parent_t
        outer[link.name] = (rotation, translation)
        link.pose_rotation = rotation
        link.pose_offset = quat_rotate_vector(rotation, link.shift) + translation


def rigid_group_ids(links: list[LinkSpec]) -> dict[str, int]:
    """Map each link name to a rigid-group id. Links welded together by
    ``fixed`` joints share a group: they move as one body and touch by
    construction, so collision between them is meaningless (and would
    fight the weld constraint). A movable joint starts a new group."""
    groups: dict[str, int] = {}
    next_id = 0
    for link in links:  # breadth-first, parents before children
        if (
            link.parent is not None
            and link.joint is not None
            and link.joint.joint_type == "fixed"
        ):
            groups[link.name] = groups[link.parent.name]
        else:
            groups[link.name] = next_id
            next_id += 1
    return groups


def welded_link_pairs(links: list[LinkSpec]) -> list[tuple[str, str]]:
    """Name pairs of links in the same rigid group — the pairs a
    self-colliding simulation must still exclude from contact."""
    groups = rigid_group_ids(links)
    return [
        (first.name, second.name)
        for i, first in enumerate(links)
        for second in links[i + 1 :]
        if groups[first.name] == groups[second.name]
    ]


def extract_scene_links(
    parts: list["Part3D"], taken: set[str] | None = None
) -> list[LinkSpec]:
    """LinkSpecs for free-floating scene bodies (no parent, no joint): loose
    objects a robot can interact with, e.g. something to pick up. Each
    link's frame sits at the part's (bounding-box) center, so the free
    body's pose is the object's pose."""
    taken = set(taken or ())
    links = []
    for part in parts:
        base = part.name or "scene_part"
        name, counter = base, 1
        while name in taken:
            counter += 1
            name = f"{base}_{counter}"
        taken.add(name)
        bbox_min, bbox_max = part.get_bounding_box()
        center = (np.array(bbox_min.to_tuple()) + np.array(bbox_max.to_tuple())) / 2
        links.append(LinkSpec(part=part, name=name, frame=center))
    return links


def export_single_part(part: "Part3D", location: str) -> str:
    """Export just ``part``'s own geometry, without the parts joined to it
    (``export()`` includes the whole assembly by default). Tolerates
    ``export()`` overrides that don't take ``include_assembly``."""
    try:
        parameters = inspect.signature(part.export).parameters
    except (TypeError, ValueError):
        parameters = {}
    if "include_assembly" in parameters:
        return part.export(location, include_assembly=False)
    return part.export(location)


def export_link_meshes(links: list[LinkSpec], directory: str | Path) -> None:
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    for link in links:
        path = directory / f"{link.name}.stl"
        export_single_part(link.part, str(path))
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


def encode_png(pixels: np.ndarray) -> bytes:
    """Encode an (H, W, 3) RGB or (H, W) grayscale uint8 array as a PNG
    (stdlib only) — e.g. a simulated camera frame for telemetry: base64
    the result and show it with ``app.add_image``."""
    pixels = np.ascontiguousarray(pixels, dtype=np.uint8)
    if pixels.ndim == 2:
        color_type = 0  # grayscale
    elif pixels.ndim == 3 and pixels.shape[2] == 3:
        color_type = 2  # RGB
    else:
        raise ValueError("Expected an (H, W) or (H, W, 3) uint8 array")
    height, width = pixels.shape[:2]
    rows = pixels.reshape(height, -1)
    # Each scanline starts with a filter byte (0 = unfiltered).
    raw = np.zeros((height, rows.shape[1] + 1), dtype=np.uint8)
    raw[:, 1:] = rows

    def chunk(tag: bytes, payload: bytes) -> bytes:
        return (
            struct.pack(">I", len(payload))
            + tag
            + payload
            + struct.pack(">I", zlib.crc32(tag + payload))
        )

    header = struct.pack(">IIBBBBB", width, height, 8, color_type, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", zlib.compress(raw.tobytes(), 6))
        + chunk(b"IEND", b"")
    )


def _web_safe_palette() -> bytes:
    """A 216-color 6x6x6 RGB cube, padded to 256 entries — the global color
    table an animated GIF quantizes frames into."""
    table = bytearray()
    for red in range(6):
        for green in range(6):
            for blue in range(6):
                table += bytes((red * 51, green * 51, blue * 51))
    table += bytes(3 * (256 - 216))
    return bytes(table)


def _quantize_to_web_safe(frame: np.ndarray) -> np.ndarray:
    """Map an (H, W, 3) uint8 RGB frame to indices into the 6x6x6 cube."""
    frame = np.ascontiguousarray(frame, dtype=np.uint8)
    if frame.ndim == 2:  # grayscale -> gray RGB
        frame = np.repeat(frame[:, :, None], 3, axis=2)
    levels = np.round(frame.astype(np.float64) / 255.0 * 5.0).astype(np.int64)
    return (36 * levels[:, :, 0] + 6 * levels[:, :, 1] + levels[:, :, 2]).astype(
        np.uint8
    )


def _lzw_encode(indices: np.ndarray, min_code_size: int) -> bytes:
    """GIF variable-width LZW compression of a flat array of palette indices."""
    clear_code = 1 << min_code_size
    end_code = clear_code + 1
    code_size = min_code_size + 1
    dictionary: dict[tuple[int, ...], int] = {}

    def reset() -> int:
        dictionary.clear()
        for value in range(clear_code):
            dictionary[(value,)] = value
        return clear_code + 2

    out = bytearray()
    bit_buffer = 0
    bit_count = 0

    def write(code: int, width: int) -> None:
        nonlocal bit_buffer, bit_count
        bit_buffer |= code << bit_count
        bit_count += width
        while bit_count >= 8:
            out.append(bit_buffer & 0xFF)
            bit_buffer >>= 8
            bit_count -= 8

    next_code = reset()
    write(clear_code, code_size)
    current: tuple[int, ...] = ()
    for value in indices.tolist():
        candidate = current + (value,)
        if candidate in dictionary:
            current = candidate
            continue
        write(dictionary[current], code_size)
        dictionary[candidate] = next_code
        next_code += 1
        if next_code > (1 << code_size) and code_size < 12:
            code_size += 1
        if next_code >= 4096:
            write(clear_code, code_size)
            next_code = reset()
            code_size = min_code_size + 1
        current = (value,)
    if current:
        write(dictionary[current], code_size)
    write(end_code, code_size)
    if bit_count > 0:
        out.append(bit_buffer & 0xFF)
    return bytes(out)


def _to_sub_blocks(data: bytes) -> bytes:
    """Split LZW data into GIF sub-blocks (<=255 bytes, zero terminator)."""
    out = bytearray()
    for start in range(0, len(data), 255):
        chunk = data[start : start + 255]
        out.append(len(chunk))
        out += chunk
    out.append(0)
    return bytes(out)


def encode_gif(
    frames: "list[np.ndarray]", *, fps: int = 20, loop: int = 0
) -> bytes:
    """Encode a list of (H, W, 3) uint8 RGB frames as an animated GIF89a
    (stdlib + numpy only). ``fps`` is the playback rate; ``loop`` the repeat
    count (0 = loop forever). Frames are quantized to a 216-color web-safe
    palette — plenty for simulation renders."""
    if not frames:
        raise ValueError("encode_gif needs at least one frame")
    height, width = np.asarray(frames[0]).shape[:2]
    delay = max(1, round(100.0 / fps))  # hundredths of a second
    palette = _web_safe_palette()

    out = bytearray(b"GIF89a")
    # Logical screen descriptor: global color table, 8-bit, 256 entries.
    out += struct.pack("<HH", width, height)
    out += bytes((0xF7, 0, 0))  # packed(GCT|res|size=7), background, aspect
    out += palette
    # NETSCAPE2.0 looping extension.
    out += b"\x21\xff\x0bNETSCAPE2.0\x03\x01"
    out += struct.pack("<H", loop)
    out += b"\x00"
    for frame in frames:
        indices = _quantize_to_web_safe(np.asarray(frame))
        out += b"\x21\xf9\x04\x00" + struct.pack("<H", delay) + b"\x00\x00"
        out += b"\x2c" + struct.pack("<HHHH", 0, 0, width, height) + b"\x00"
        min_code_size = 8
        out += bytes((min_code_size,))
        out += _to_sub_blocks(_lzw_encode(indices.reshape(-1), min_code_size))
    out += b"\x3b"
    return bytes(out)


class Simulation:
    """Base class for physics simulations of a CodeToCAD assembly.

    Create one with the ``simulate()`` function of a simulation integration
    (``codetocad_integrations.pybullet`` or ``codetocad_integrations.mujoco``).
    """

    # The parameters below are shared by every backend. Backends forward them
    # to this base constructor (via ``**kwargs``) and declare only their own
    # extras (e.g. pybullet's ``gui``, mujoco's ``actuator_types``), so this
    # signature is the single source of truth for the common simulate() API.
    def __init__(
        self,
        root_part: "Part3D",
        *,
        lighting: list[Lighting] | None = None,
        camera: Camera | None = None,
        gravity: tuple[float, float, float] = (0.0, 0.0, -9.81),
        time_step: float = 1.0 / 240.0,
        fixed_base: bool = True,
        actuated: bool = True,
        scene_parts: list["Part3D"] | None = None,
        ground_plane: bool = False,
        self_collision: bool = True,
        collision_exclusions: list[tuple["Part3D | str", "Part3D | str"]]
        | None = None,
        output_dir: str | Path | None = None,
    ):
        self.root_part = root_part
        self.lighting = lighting if lighting is not None else [Lighting()]
        #: Overview camera for capture_image()/record_gif() and the live
        #: GUI/viewer. ``None`` means each backend frames the scene itself;
        #: set one with ``set_camera(...)``.
        self.camera = camera
        self.gravity = gravity
        self.time_step = time_step
        self.fixed_base = fixed_base
        self.actuated = actuated
        self.ground_plane = ground_plane
        #: Collide assembly parts against each other, except parts welded
        #: together by fixed joints (they move as one body). Pairs that
        #: overlap by construction — e.g. a rod modeled into its base at a
        #: joint, which would bleed energy or jam — are opted out via
        #: ``collision_exclusions``.
        self.self_collision = self_collision
        self.output_dir = Path(
            output_dir
            if output_dir is not None
            else tempfile.mkdtemp(prefix="codetocad_sim_")
        ).resolve()
        self.links = extract_links(root_part)
        self.scene_links = extract_scene_links(
            scene_parts or [], taken={link.name for link in self.links}
        )
        #: ``collision_exclusions`` resolved to pairs of link names.
        self.collision_exclusions = [
            (self._resolve_link_name(first), self._resolve_link_name(second))
            for first, second in collision_exclusions or []
        ]
        # Map each movable child part to its joint's name, so callers can
        # reference a joint by the part they joined instead of the joint name.
        self._joint_name_by_part = {
            id(link.part): link.joint.name
            for link in self.links
            if link.joint is not None and link.joint.joint_type != "fixed"
        }
        #: Most recent commanded position target per joint name — the state a
        #: ``set_keyframe()`` snapshots.
        self._joint_targets: dict[str, float] = {}
        #: Recorded keyframes as ``(time_seconds, {joint_name: target})``.
        self._keyframes: list[tuple[float, dict[str, float]]] = []
        #: The user-facing ``Joint`` objects, bound to this simulation so
        #: ``joint.move_to(...)`` drives the live model.
        self.joints: list = []
        self._joint_by_name: dict[str, Joint] = {}
        for link in self.links:
            if link.joint is not None and link.joint.joint_obj is not None:
                link.joint.joint_obj._bind(self, link.joint.name)
                self.joints.append(link.joint.joint_obj)
                self._joint_by_name[link.joint.name] = link.joint.joint_obj

    def get_joint(self, joint: "str | Part3D") -> Joint:
        """The :class:`~codetocad.joints.Joint` object for a joint name or the
        child ``Part3D`` that was joined."""
        name = self._resolve_joint_name(joint)
        try:
            return self._joint_by_name[name]
        except KeyError:
            raise KeyError(
                f"No joint object for {name!r}; joints are "
                f"{sorted(self._joint_by_name)}"
            ) from None

    def _apply_initial_joint_values(self) -> None:
        """Set each joint to its ``starting_angle``/``starting_pos``. Backends
        call this once their model and state are ready."""
        for link in self.links:
            joint = link.joint
            if joint is not None and joint.initial_value is not None:
                self.set_joint_value(joint.name, joint.initial_value)
                self._joint_targets[joint.name] = joint.initial_value

    def _resolve_link_name(self, part: "str | Part3D") -> str:
        """Accept a link name or the ``Part3D`` behind it, returning the
        link name (for ``collision_exclusions`` entries)."""
        names = [link.name for link in self.links]
        if isinstance(part, str):
            if part not in names:
                raise KeyError(
                    f"Unknown part {part!r} in collision_exclusions; "
                    f"assembly parts are {names}"
                )
            return part
        for link in self.links:
            if link.part is part:
                return link.name
        raise KeyError(
            f"{part!r} in collision_exclusions is not part of this "
            f"assembly; assembly parts are {names}"
        )

    @property
    def joint_names(self) -> list[str]:
        return [
            link.joint.name
            for link in self.links
            if link.joint is not None and link.joint.joint_type != "fixed"
        ]

    def _resolve_joint_name(self, joint: "str | Part3D") -> str:
        """Accept either a joint name or the child ``Part3D`` that was joined
        (via ``.revolute()``/``.prismatic()``/...), returning the joint name."""
        if isinstance(joint, str):
            return joint
        name = self._joint_name_by_part.get(id(joint))
        if name is None:
            raise KeyError(
                f"{joint!r} is not joined to this assembly by a movable joint; "
                f"movable joints are {self.joint_names}"
            )
        return name

    # -- interface implemented by integrations --

    def step(self, count: int = 1) -> None:
        raise NotImplementedError

    def _command_joint_target(
        self, joint: "str | Part3D", value: float, **kwargs
    ) -> None:
        """Position-control a joint towards ``value`` (radians/meters) and
        remember the target so ``set_keyframe()`` can snapshot it. This is the
        engine behind ``RevoluteJoint``/``PrismaticJoint``'s ``move_to`` /
        ``move_by``; drive joints through those (``sim.get_joint(name)`` gets a
        joint by name), or ``set_joint_value`` to teleport."""
        name = self._resolve_joint_name(joint)
        self._joint_targets[name] = value
        self._set_joint_target(name, value, **kwargs)

    def _set_joint_target(self, name: str, value: float, **kwargs) -> None:
        """Backend hook: drive the actuator of the (already-resolved) joint."""
        raise NotImplementedError

    def set_joint_velocity(self, joint: "str | Part3D", value: float) -> None:
        """Velocity-control a joint at ``value`` (rad/s or m/s). ``joint`` is a
        joint name or the child part that was joined."""
        self._set_joint_velocity(self._resolve_joint_name(joint), value)

    def _set_joint_velocity(self, name: str, value: float) -> None:
        raise NotImplementedError(
            "This backend does not support velocity control"
        )

    def set_joint_value(self, joint: "str | Part3D", value: float) -> None:
        """Instantly set a joint's value (teleport; no dynamics). ``joint`` is
        a joint name or the child part that was joined."""
        raise NotImplementedError

    def get_joint_value(self, joint: "str | Part3D") -> float:
        raise NotImplementedError

    def capture_image(self, **kwargs) -> np.ndarray:
        """Render the current scene to an ``(H, W, 3)`` uint8 RGB array from
        the overview :attr:`camera`. Backends implement this; encode it with
        :func:`encode_png` for telemetry."""
        raise NotImplementedError(
            "This backend does not support capture_image()"
        )

    # -- camera & lighting --

    def set_camera(self, camera: Camera | None = None, **fields) -> Camera:
        """Set the overview :class:`Camera` used by ``capture_image()`` /
        ``record_gif()`` and the live GUI/viewer. Pass a ``Camera`` (build one
        with ``Camera.look_at(eye=..., target=...)``), or just the fields to
        change (``sim.set_camera(fov=35)`` keeps the current pose). Returns the
        active camera."""
        if camera is None:
            camera = self.camera or Camera()
        if fields:
            camera = replace(camera, **fields)
        self.camera = camera
        self._apply_camera()
        return camera

    def set_lighting(self, lighting: list[Lighting]) -> None:
        """Replace the scene lights and push them to the live view (where the
        backend supports it)."""
        self.lighting = list(lighting)
        self._apply_lighting()

    def _apply_camera(self) -> None:
        """Backend hook: push :attr:`camera` to a live GUI/viewer. Offscreen
        backends read :attr:`camera` in ``capture_image`` and need no-op here."""

    def _apply_lighting(self) -> None:
        """Backend hook: push :attr:`lighting` to the live scene."""

    def _camera_framing(self) -> "tuple[np.ndarray, float]":
        """``(center, extent)`` of the assembly's link frames — the point to
        look at and the diagonal spread a backend sizes the orbit distance
        from."""
        frames = np.array([link.frame for link in self.links])
        center = frames.mean(axis=0)
        extent = float(np.linalg.norm(frames.max(axis=0) - frames.min(axis=0)))
        return center, extent

    def run(self, duration: float, realtime: bool = False) -> None:
        """Step the simulation for ``duration`` seconds."""
        import time as _time

        steps = int(round(duration / self.time_step))
        for _ in range(steps):
            self.step()
            if realtime:
                _time.sleep(self.time_step)

    # -- keyframes --

    def set_keyframe(self, time: float | None = None) -> float:
        """Record the joints' currently commanded position targets as a
        keyframe held at ``time`` seconds. With ``time=None`` the keyframe
        lands one second after the previous one (or at t=0 for the first).
        Command the joints first (``joint.move_to(...)``), then call this to
        pin those positions.
        Replay with :meth:`play_keyframes` or :meth:`record_gif`."""
        if time is None:
            time = self._keyframes[-1][0] + 1.0 if self._keyframes else 0.0
        self._keyframes.append((float(time), dict(self._joint_targets)))
        return time

    def clear_keyframes(self) -> None:
        self._keyframes = []

    def play_keyframes(
        self,
        *,
        fps: int = 30,
        realtime: bool = False,
        on_frame=None,
    ) -> None:
        """Step the simulation through the recorded keyframes, interpolating
        each joint's target between them and driving the actuators there.
        ``on_frame(self)`` is called once per rendered frame."""
        import time as _time

        for targets in self._keyframe_frames(fps):
            for name, value in targets.items():
                self._command_joint_target(name, value)
            self.step(max(1, round(1.0 / fps / self.time_step)))
            if on_frame is not None:
                on_frame(self)
            if realtime:
                _time.sleep(1.0 / fps)

    def _keyframe_frames(self, fps: int):
        """Yield the interpolated ``{joint: target}`` map for each frame of the
        keyframe timeline, at ``fps`` frames per second."""
        keyframes = sorted(self._keyframes, key=lambda item: item[0])
        if not keyframes:
            return
        names = sorted({name for _, targets in keyframes for name in targets})
        start_time = keyframes[0][0]
        end_time = keyframes[-1][0]
        frame_count = max(1, int(round((end_time - start_time) * fps)))
        last_seen = {name: keyframes[0][1].get(name, 0.0) for name in names}

        def sample(name: str, at: float) -> float:
            previous = None
            for moment, targets in keyframes:
                if name not in targets:
                    continue
                if moment <= at:
                    previous = (moment, targets[name])
                else:
                    if previous is None:
                        return targets[name]
                    (t0, v0), (t1, v1) = previous, (moment, targets[name])
                    ratio = (at - t0) / (t1 - t0) if t1 > t0 else 1.0
                    return v0 + (v1 - v0) * ratio
            return previous[1] if previous is not None else last_seen[name]

        for frame in range(frame_count + 1):
            at = start_time + (end_time - start_time) * frame / frame_count
            yield {name: sample(name, at) for name in names}

    # -- recording --

    def record_gif(
        self,
        path: str | Path | None = None,
        *,
        duration: float | None = None,
        fps: int = 20,
        keyframes: bool = False,
        realtime: bool = False,
        loop: int = 0,
        **capture_kwargs,
    ) -> bytes:
        """Render the simulation to an animated GIF and return its bytes
        (also written to ``path`` if given). With ``keyframes=True`` it plays
        the recorded keyframe timeline; otherwise it steps for ``duration``
        seconds. ``fps`` sets the frame rate, ``loop`` the repeat count
        (0 = forever). ``capture_kwargs`` pass through to
        :meth:`capture_image` (e.g. ``width``/``height``)."""
        frames: list[np.ndarray] = []
        frames.append(self.capture_image(**capture_kwargs))
        if keyframes:
            self.play_keyframes(
                fps=fps,
                realtime=realtime,
                on_frame=lambda sim: frames.append(sim.capture_image(**capture_kwargs)),
            )
        else:
            if duration is None:
                raise ValueError("record_gif needs duration=... (or keyframes=True)")
            steps_per_frame = max(1, round(1.0 / fps / self.time_step))
            import time as _time

            for _ in range(int(round(duration * fps))):
                self.step(steps_per_frame)
                frames.append(self.capture_image(**capture_kwargs))
                if realtime:
                    _time.sleep(1.0 / fps)
        data = encode_gif(frames, fps=fps, loop=loop)
        if path is not None:
            Path(path).write_bytes(data)
        return data

    def close(self) -> None:
        pass

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()
        return False
