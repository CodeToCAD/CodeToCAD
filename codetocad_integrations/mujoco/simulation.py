"""MJCF generation and the MuJoCo-backed Simulation."""

from __future__ import annotations

import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from xml.etree import ElementTree as ET

import numpy as np

from codetocad.parts import Part3D
from codetocad.simulation import (
    Lighting,
    LinkSpec,
    Simulation,
    ensure_binary_stl,
    export_link_meshes,
    extract_links,
)


def _fmt(vector) -> str:
    return " ".join(f"{float(v):.9g}" for v in vector)


@dataclass
class CameraSpec:
    """A fixed camera mounted on one of the robot's links.

    ``position`` is in world coordinates with the robot in its modeled
    pose (the same convention as parts and joint anchors). ``xyaxes`` are
    the camera frame's X (image right) and Y (image up) axes; the camera
    looks along -Z. The default looks towards +X with +Z up — a
    forward-facing camera on a mobile robot."""

    name: str = "camera"
    link: str | None = None  # link (body) to mount on; None = the root link
    position: tuple[float, float, float] = (0.0, 0.0, 0.1)
    xyaxes: tuple[float, float, float, float, float, float] = (0, -1, 0, 0, 0, 1)
    fovy: float = 60.0  # vertical field of view, degrees
    resolution: tuple[int, int] = (320, 240)  # (width, height) pixels


@dataclass
class TerrainSpec:
    """A heightfield floor for the robot to drive on.

    ``heights`` is an (nrow, ncol) array of elevations in meters (>= 0);
    row r maps to y and column c to x across ``extent``, so
    ``heights[0, 0]`` is the corner at ``position - extent/2``. The
    heightfield sits at z=0, on top of a thin base slab."""

    heights: np.ndarray = field(default_factory=lambda: np.zeros((2, 2)))
    extent: tuple[float, float] = (5.0, 5.0)  # total x/y size, meters
    position: tuple[float, float] = (0.0, 0.0)  # center of the field
    base_thickness: float = 0.01
    rgba: tuple[float, float, float, float] = (0.5, 0.55, 0.4, 1.0)
    #: Second checker color; the two-tone grid gives cameras and the
    #: viewer a sense of scale and motion. None renders flat ``rgba``.
    checker_rgba: tuple[float, float, float, float] | None = (0.42, 0.47, 0.33, 1.0)

    @property
    def max_height(self) -> float:
        return max(float(np.max(self.heights)), 1e-6)

    @property
    def normalized(self) -> np.ndarray:
        """Elevation data scaled to [0, 1], as MuJoCo stores it."""
        return np.asarray(self.heights, dtype=np.float64) / self.max_height


def build_mjcf(
    links: list[LinkSpec],
    name: str = "codetocad_robot",
    *,
    gravity: tuple[float, float, float] = (0.0, 0.0, -9.81),
    time_step: float = 1.0 / 240.0,
    fixed_base: bool = True,
    actuated: bool = True,
    actuator_kp: float = 100.0,
    actuator_kv: float = 0.5,
    actuator_types: dict[str, str] | None = None,
    actuator_forcerange: dict[str, float] | None = None,
    joint_damping: float | dict[str, float] = 0.5,
    joint_armature: float | dict[str, float] = 0.0,
    ground_plane: bool = False,
    geom_friction: dict[str, tuple[float, float, float]] | None = None,
    lighting: list[Lighting] | None = None,
    scene_links: list[LinkSpec] | None = None,
    cameras: list[CameraSpec] | None = None,
    terrain: TerrainSpec | None = None,
) -> str:
    """Build an MJCF document from an extracted kinematic tree. Mesh paths
    must already be filled in and be binary STLs in one directory.

    ``actuator_types`` overrides the actuator per joint name: ``"position"``
    (servo towards an angle, gain ``actuator_kp``) or ``"velocity"``
    (servo towards an angular rate, gain ``actuator_kv``) — wheels of a
    mobile robot want velocity. ``actuator_forcerange`` caps an actuator's
    torque/force at ± the given value per joint name (a motor's stall
    torque). ``joint_damping`` sets passive joint damping, per joint name
    with a dict; the 0.5 default suits arm-sized joints and is far too
    much for small wheels. ``joint_armature`` adds a geared motor's
    reflected rotor inertia to a joint — without it, light joints under
    strong gains oscillate at coarse time steps. ``ground_plane`` adds a
    static floor at z=0
    (use with ``fixed_base=False`` so the robot can drive on it), and
    ``geom_friction`` overrides contact friction (slide, spin, roll) per
    link name — e.g. a low-slide caster ball. ``scene_links`` are
    free-floating bodies (a ``freejoint`` each) that collide with the
    robot — loose objects it can push or pick up. ``cameras`` mounts
    fixed cameras on links (render them with
    ``MujocoSimulation.get_camera_image``); ``terrain`` adds a
    heightfield floor (elevation data is uploaded after model load, so
    load this MJCF via ``MujocoSimulation`` for a non-flat field)."""
    actuator_types = actuator_types or {}
    actuator_forcerange = actuator_forcerange or {}
    scene_links = scene_links or []
    cameras = cameras or []

    def damping_for(joint_name: str) -> float:
        if isinstance(joint_damping, dict):
            return joint_damping.get(joint_name, 0.5)
        return joint_damping

    def armature_for(joint_name: str) -> float:
        if isinstance(joint_armature, dict):
            return joint_armature.get(joint_name, 0.0)
        return joint_armature
    mujoco_el = ET.Element("mujoco", model=name)
    mesh_dir = str(Path(links[0].mesh_path).parent)
    ET.SubElement(mujoco_el, "compiler", meshdir=mesh_dir, angle="radian")
    ET.SubElement(
        mujoco_el,
        "option",
        gravity=_fmt(gravity),
        timestep=f"{time_step:.9g}",
    )
    asset = ET.SubElement(mujoco_el, "asset")
    for link in links + scene_links:
        ET.SubElement(
            asset, "mesh", name=link.name, file=Path(link.mesh_path).name
        )
    if terrain is not None:
        nrow, ncol = np.asarray(terrain.heights).shape
        ET.SubElement(
            asset,
            "hfield",
            name="terrain",
            nrow=str(nrow),
            ncol=str(ncol),
            size=_fmt(
                (
                    terrain.extent[0] / 2,
                    terrain.extent[1] / 2,
                    terrain.max_height,
                    terrain.base_thickness,
                )
            ),
        )
        if terrain.checker_rgba is not None:
            ET.SubElement(
                asset,
                "texture",
                name="terrain_checker",
                type="2d",
                builtin="checker",
                rgb1=_fmt(terrain.rgba[:3]),
                rgb2=_fmt(terrain.checker_rgba[:3]),
                width="512",
                height="512",
            )
            ET.SubElement(
                asset,
                "material",
                name="terrain_material",
                texture="terrain_checker",
                texrepeat=_fmt((terrain.extent[0] * 2, terrain.extent[1] * 2)),
            )
    if cameras:
        # Size the offscreen framebuffer for the largest camera.
        visual = ET.SubElement(mujoco_el, "visual")
        ET.SubElement(
            visual,
            "global",
            offwidth=str(max(c.resolution[0] for c in cameras)),
            offheight=str(max(c.resolution[1] for c in cameras)),
        )

    worldbody = ET.SubElement(mujoco_el, "worldbody")
    if terrain is not None:
        terrain_geom = ET.SubElement(
            worldbody,
            "geom",
            name="terrain",
            type="hfield",
            hfield="terrain",
            pos=_fmt((*terrain.position, 0.0)),
            rgba=_fmt(terrain.rgba),
        )
        if terrain.checker_rgba is not None:
            terrain_geom.set("material", "terrain_material")
            terrain_geom.set("rgba", "1 1 1 1")  # let the texture color it
    if ground_plane:
        floor = ET.SubElement(
            worldbody,
            "geom",
            name="floor",
            type="plane",
            size="20 20 0.1",
            rgba="0.85 0.85 0.85 1",
        )
        if terrain is not None:
            # Sink the plane below the heightfield so zero-elevation
            # terrain (a launch pad, wave troughs) doesn't z-fight it.
            floor.set("pos", "0 0 -0.005")
    for light in lighting or []:
        ET.SubElement(
            worldbody,
            "light",
            name=light.name,
            pos=_fmt(light.position),
            dir=_fmt(light.direction),
            diffuse=_fmt(light.diffuse),
            directional="true" if light.light_type == "directional" else "false",
        )

    def emit_geom_and_inertial(body: ET.Element, link: LinkSpec) -> None:
        geom = ET.SubElement(
            body,
            "geom",
            type="mesh",
            mesh=link.name,
            pos=_fmt(-link.frame),
            rgba=_fmt(link.color_rgba),
        )
        if geom_friction and link.name in geom_friction:
            geom.set("friction", _fmt(geom_friction[link.name]))
        ET.SubElement(
            body,
            "inertial",
            pos=_fmt(link.center_of_mass - link.frame),
            mass=f"{link.mass:.9g}",
            diaginertia=_fmt(link.inertia_diagonal),
        )

    def emit_body(link: LinkSpec, parent_element: ET.Element) -> None:
        parent_frame = link.parent.frame if link.parent is not None else None
        pos = link.frame - parent_frame if parent_frame is not None else link.frame
        body = ET.SubElement(
            parent_element, "body", name=link.name, pos=_fmt(pos)
        )
        joint_spec = link.joint
        if link.parent is None:
            if not fixed_base:
                ET.SubElement(body, "freejoint")
        elif joint_spec is not None and joint_spec.joint_type != "fixed":
            joint = ET.SubElement(
                body,
                "joint",
                name=joint_spec.name,
                type="hinge" if joint_spec.joint_type == "revolute" else "slide",
                pos="0 0 0",
                axis=_fmt(joint_spec.axis),
            )
            if joint_spec.lower is not None or joint_spec.upper is not None:
                joint.set("limited", "true")
                joint.set(
                    "range",
                    f"{joint_spec.lower or 0:.9g} {joint_spec.upper or 0:.9g}",
                )
            if actuated:
                joint.set("damping", f"{damping_for(joint_spec.name):.9g}")
            armature = armature_for(joint_spec.name)
            if armature > 0:
                joint.set("armature", f"{armature:.9g}")
        emit_geom_and_inertial(body, link)
        for camera in cameras:
            if (camera.link or links[0].name) == link.name:
                ET.SubElement(
                    body,
                    "camera",
                    name=camera.name,
                    pos=_fmt(np.asarray(camera.position, dtype=float) - link.frame),
                    xyaxes=_fmt(camera.xyaxes),
                    fovy=f"{camera.fovy:.9g}",
                )
        for child in link.children:
            emit_body(child, body)

    emit_body(links[0], worldbody)
    for link in scene_links:
        body = ET.SubElement(
            worldbody, "body", name=link.name, pos=_fmt(link.frame)
        )
        ET.SubElement(body, "freejoint", name=f"{link.name}_free")
        emit_geom_and_inertial(body, link)

    # Parts touch at their joint anchors by construction; exclude all
    # self-collisions within the assembly (matching PyBullet's loadURDF
    # default) so joints move freely.
    contact = ET.SubElement(mujoco_el, "contact")
    for i, first in enumerate(links):
        for second in links[i + 1 :]:
            ET.SubElement(
                contact, "exclude", body1=first.name, body2=second.name
            )

    if actuated:
        actuator = ET.SubElement(mujoco_el, "actuator")
        for link in links:
            if link.joint is not None and link.joint.joint_type != "fixed":
                kind = actuator_types.get(link.joint.name, "position")
                if kind == "velocity":
                    element = ET.SubElement(
                        actuator,
                        "velocity",
                        name=f"{link.joint.name}_actuator",
                        joint=link.joint.name,
                        kv=f"{actuator_kv:.9g}",
                    )
                elif kind == "position":
                    element = ET.SubElement(
                        actuator,
                        "position",
                        name=f"{link.joint.name}_actuator",
                        joint=link.joint.name,
                        kp=f"{actuator_kp:.9g}",
                    )
                else:
                    raise ValueError(
                        f"Unknown actuator type {kind!r} for joint "
                        f"{link.joint.name!r}; use 'position' or 'velocity'"
                    )
                limit = actuator_forcerange.get(link.joint.name)
                if limit is not None:
                    element.set("forcerange", f"{-limit:.9g} {limit:.9g}")
    ET.indent(mujoco_el)
    return ET.tostring(mujoco_el, encoding="unicode")


class MujocoSimulation(Simulation):
    def __init__(
        self,
        root_part: Part3D,
        *,
        output_dir: str | Path | None = None,
        actuator_types: dict[str, str] | None = None,
        actuator_forcerange: dict[str, float] | None = None,
        joint_damping: float | dict[str, float] = 0.5,
        joint_armature: float | dict[str, float] = 0.0,
        ground_plane: bool = False,
        geom_friction: dict[str, tuple[float, float, float]] | None = None,
        cameras: list[CameraSpec] | None = None,
        terrain: TerrainSpec | None = None,
        **kwargs,
    ):
        super().__init__(root_part, **kwargs)
        import mujoco

        self._mujoco = mujoco
        self.cameras = {camera.name: camera for camera in cameras or []}
        self.terrain = terrain
        self._renderers: dict[tuple[int, int], object] = {}
        self.output_dir = Path(
            output_dir
            if output_dir is not None
            else tempfile.mkdtemp(prefix="codetocad_mujoco_")
        ).resolve()
        export_link_meshes(self.links + self.scene_links, self.output_dir)
        for link in self.links + self.scene_links:
            ensure_binary_stl(link.mesh_path)  # MuJoCo needs binary STL
        mjcf = build_mjcf(
            self.links,
            scene_links=self.scene_links,
            name=root_part.name or "codetocad_robot",
            gravity=self.gravity,
            time_step=self.time_step,
            fixed_base=self.fixed_base,
            actuated=self.actuated,
            actuator_types=actuator_types,
            actuator_forcerange=actuator_forcerange,
            joint_damping=joint_damping,
            joint_armature=joint_armature,
            ground_plane=ground_plane,
            geom_friction=geom_friction,
            lighting=self.lighting,
            cameras=cameras,
            terrain=terrain,
        )
        self.mjcf_path = self.output_dir / "robot.xml"
        self.mjcf_path.write_text(mjcf)

        self.model = mujoco.MjModel.from_xml_path(str(self.mjcf_path))
        if terrain is not None:
            # The MJCF declares the heightfield's shape; the elevation
            # data (normalized to [0, 1]) is uploaded here.
            self.model.hfield("terrain").data[:] = terrain.normalized
        self.data = mujoco.MjData(self.model)
        mujoco.mj_forward(self.model, self.data)

    def _joint_id(self, name: str) -> int:
        joint_id = self._mujoco.mj_name2id(
            self.model, self._mujoco.mjtObj.mjOBJ_JOINT, name
        )
        if joint_id < 0:
            raise KeyError(
                f"Unknown joint {name!r}; joints are {self.joint_names}"
            )
        return joint_id

    def step(self, count: int = 1) -> None:
        for _ in range(count):
            self._mujoco.mj_step(self.model, self.data)

    def set_joint_target(self, name: str, value: float) -> None:
        """Drive the joint's actuator towards ``value``: an angle for
        position actuators, an angular rate (rad/s) for velocity ones."""
        if not self.actuated:
            raise RuntimeError(
                "This simulation was created with actuated=False; recreate "
                "it with actuated=True to position-control joints"
            )
        actuator_id = self._mujoco.mj_name2id(
            self.model, self._mujoco.mjtObj.mjOBJ_ACTUATOR, f"{name}_actuator"
        )
        if actuator_id < 0:
            raise KeyError(f"No actuator for joint {name!r}")
        self.data.ctrl[actuator_id] = value

    def set_joint_velocity_target(self, name: str, value: float) -> None:
        """Alias of ``set_joint_target`` for joints declared with
        ``actuator_types={name: "velocity"}`` (target in rad/s)."""
        self.set_joint_target(name, value)

    def set_joint_value(self, name: str, value: float) -> None:
        address = self.model.jnt_qposadr[self._joint_id(name)]
        self.data.qpos[address] = value
        self._mujoco.mj_forward(self.model, self.data)

    def get_joint_value(self, name: str) -> float:
        address = self.model.jnt_qposadr[self._joint_id(name)]
        return float(self.data.qpos[address])

    def get_joint_velocity(self, name: str) -> float:
        """The joint's angular (rad/s) or linear (m/s) velocity."""
        address = self.model.jnt_dofadr[self._joint_id(name)]
        return float(self.data.qvel[address])

    def get_body_pose(self, name: str) -> tuple[tuple[float, ...], tuple[float, ...]]:
        """World position and quaternion (w, x, y, z) of a link's body."""
        body = self.data.body(name)
        return tuple(map(float, body.xpos)), tuple(map(float, body.xquat))

    def get_camera_image(
        self,
        camera: str | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> np.ndarray:
        """Render a mounted camera offscreen: an (height, width, 3) uint8
        RGB array of what the robot sees right now. ``camera`` defaults to
        the first declared camera; ``width``/``height`` default to the
        camera's ``resolution``."""
        if not self.cameras:
            raise RuntimeError(
                "No cameras mounted; pass cameras=[CameraSpec(...)] to simulate()"
            )
        if camera is None:
            camera = next(iter(self.cameras))
        spec = self.cameras.get(camera)
        if spec is None:
            raise KeyError(
                f"Unknown camera {camera!r}; cameras are {list(self.cameras)}"
            )
        width = width or spec.resolution[0]
        height = height or spec.resolution[1]
        renderer = self._renderers.get((width, height))
        if renderer is None:
            renderer = self._mujoco.Renderer(self.model, height=height, width=width)
            self._renderers[(width, height)] = renderer
        renderer.update_scene(self.data, camera=camera)
        return renderer.render()

    def close(self) -> None:
        for renderer in self._renderers.values():
            renderer.close()
        self._renderers.clear()

    def launch_viewer(self, key_callback=None, on_step=None) -> None:
        """Open the interactive viewer and step in real time until closed.
        On macOS this must run under ``mjpython``. ``on_step`` is called
        after every physics step (e.g. to pump an emulated
        microcontroller)."""
        import time

        import mujoco.viewer

        with mujoco.viewer.launch_passive(
            self.model, self.data, key_callback=key_callback
        ) as viewer:
            while viewer.is_running():
                start = time.time()
                self.step()
                if on_step is not None:
                    on_step()
                viewer.sync()
                remainder = self.time_step - (time.time() - start)
                if remainder > 0:
                    time.sleep(remainder)


def simulate(
    part: Part3D,
    *,
    lighting: list[Lighting] | None = None,
    gravity: tuple[float, float, float] = (0.0, 0.0, -9.81),
    time_step: float = 1.0 / 240.0,
    fixed_base: bool = True,
    actuated: bool = True,
    actuator_types: dict[str, str] | None = None,
    actuator_forcerange: dict[str, float] | None = None,
    joint_damping: float | dict[str, float] = 0.5,
    joint_armature: float | dict[str, float] = 0.0,
    ground_plane: bool = False,
    geom_friction: dict[str, tuple[float, float, float]] | None = None,
    scene_parts: list[Part3D] | None = None,
    cameras: list[CameraSpec] | None = None,
    terrain: TerrainSpec | None = None,
    output_dir: str | Path | None = None,
) -> MujocoSimulation:
    """Export ``part``'s assembly (meshes + joint constraints) to an MJCF
    model and load it into MuJoCo. For mobile robots pass
    ``fixed_base=False, ground_plane=True``, declare the wheel joints in
    ``actuator_types={...: "velocity"}``, and give the wheels small
    ``joint_damping`` and the motor's stall torque as
    ``actuator_forcerange``. ``scene_parts`` are loose, free-floating
    bodies the robot can collide with (e.g. an object to pick up) — pair
    them with ``ground_plane=True`` so they have a floor to rest on.
    ``cameras`` mounts fixed ``CameraSpec`` cameras on links, rendered
    with ``sim.get_camera_image()``; ``terrain`` adds a ``TerrainSpec``
    heightfield floor to drive on."""
    return MujocoSimulation(
        part,
        lighting=lighting,
        scene_parts=scene_parts,
        cameras=cameras,
        terrain=terrain,
        gravity=gravity,
        time_step=time_step,
        fixed_base=fixed_base,
        actuated=actuated,
        actuator_types=actuator_types,
        actuator_forcerange=actuator_forcerange,
        joint_damping=joint_damping,
        joint_armature=joint_armature,
        ground_plane=ground_plane,
        geom_friction=geom_friction,
        output_dir=output_dir,
    )
