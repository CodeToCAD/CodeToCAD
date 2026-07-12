"""URDF generation and the PyBullet-backed Simulation."""

from __future__ import annotations

import tempfile
from pathlib import Path
from xml.etree import ElementTree as ET

import numpy as np

from codetocad.parts import Part3D
from codetocad.simulation import (
    Lighting,
    LinkSpec,
    Simulation,
    export_link_meshes,
    extract_links,
)


def _fmt(vector) -> str:
    return " ".join(f"{float(v):.9g}" for v in vector)


def build_urdf(links: list[LinkSpec], name: str = "codetocad_robot") -> str:
    """Build a URDF document from an extracted kinematic tree. Mesh paths
    must already be filled in (relative paths are resolved by pybullet
    against the URDF's directory)."""
    robot = ET.Element("robot", name=name)
    for link in links:
        element = ET.SubElement(robot, "link", name=link.name)
        mesh_offset = -link.frame
        for tag in ("visual", "collision"):
            section = ET.SubElement(element, tag)
            ET.SubElement(section, "origin", xyz=_fmt(mesh_offset), rpy="0 0 0")
            geometry = ET.SubElement(section, "geometry")
            ET.SubElement(
                geometry, "mesh", filename=Path(link.mesh_path).name
            )
            if tag == "visual":
                material = ET.SubElement(
                    section, "material", name=f"{link.name}_material"
                )
                ET.SubElement(material, "color", rgba=_fmt(link.color_rgba))
        inertial = ET.SubElement(element, "inertial")
        ET.SubElement(
            inertial,
            "origin",
            xyz=_fmt(link.center_of_mass - link.frame),
            rpy="0 0 0",
        )
        ET.SubElement(inertial, "mass", value=f"{link.mass:.9g}")
        ixx, iyy, izz = link.inertia_diagonal
        ET.SubElement(
            inertial,
            "inertia",
            ixx=f"{ixx:.9g}",
            iyy=f"{iyy:.9g}",
            izz=f"{izz:.9g}",
            ixy="0",
            ixz="0",
            iyz="0",
        )

    for link in links:
        joint_spec = link.joint
        if joint_spec is None:
            continue
        if joint_spec.joint_type == "fixed":
            joint_type = "fixed"
        elif joint_spec.joint_type == "prismatic":
            joint_type = "prismatic"
        elif joint_spec.lower is None and joint_spec.upper is None:
            joint_type = "continuous"
        else:
            joint_type = "revolute"
        joint = ET.SubElement(
            robot, "joint", name=joint_spec.name, type=joint_type
        )
        ET.SubElement(joint, "parent", link=link.parent.name)
        ET.SubElement(joint, "child", link=link.name)
        ET.SubElement(
            joint,
            "origin",
            xyz=_fmt(joint_spec.anchor - link.parent.frame),
            rpy="0 0 0",
        )
        if joint_type != "fixed":
            ET.SubElement(joint, "axis", xyz=_fmt(joint_spec.axis))
            limit = ET.SubElement(joint, "limit", effort="100", velocity="10")
            if joint_type in ("revolute", "prismatic"):
                limit.set("lower", f"{joint_spec.lower or 0:.9g}")
                limit.set("upper", f"{joint_spec.upper or 0:.9g}")
    ET.indent(robot)
    return ET.tostring(robot, encoding="unicode")


class PyBulletSimulation(Simulation):
    def __init__(
        self,
        root_part: Part3D,
        *,
        gui: bool = False,
        ground_plane: bool = False,
        output_dir: str | Path | None = None,
        **kwargs,
    ):
        super().__init__(root_part, **kwargs)
        import pybullet as p

        self._p = p
        self.ground_plane = ground_plane
        self.output_dir = Path(
            output_dir
            if output_dir is not None
            else tempfile.mkdtemp(prefix="codetocad_pybullet_")
        ).resolve()
        export_link_meshes(self.links + self.scene_links, self.output_dir)
        urdf = build_urdf(self.links, name=root_part.name or "codetocad_robot")
        self.urdf_path = self.output_dir / "robot.urdf"
        self.urdf_path.write_text(urdf)

        self.client = p.connect(p.GUI if gui else p.DIRECT)
        p.setGravity(*self.gravity, physicsClientId=self.client)
        p.setTimeStep(self.time_step, physicsClientId=self.client)
        if gui and self.lighting:
            light = self.lighting[0]
            p.configureDebugVisualizer(
                lightPosition=light.position, physicsClientId=self.client
            )
        if ground_plane:
            import pybullet_data

            p.setAdditionalSearchPath(pybullet_data.getDataPath())
            p.loadURDF("plane.urdf", physicsClientId=self.client)
        self.body = p.loadURDF(
            str(self.urdf_path),
            useFixedBase=self.fixed_base,
            physicsClientId=self.client,
        )
        # Each scene part is its own free body in a one-link URDF, so it
        # collides with the robot (self-collision within the robot's URDF
        # stays disabled, loadURDF's default).
        self.scene_bodies: dict[str, int] = {}
        for link in self.scene_links:
            path = self.output_dir / f"{link.name}.urdf"
            path.write_text(build_urdf([link], name=link.name))
            self.scene_bodies[link.name] = p.loadURDF(
                str(path),
                basePosition=tuple(link.frame),
                useFixedBase=False,
                physicsClientId=self.client,
            )
        self._joint_indices: dict[str, int] = {}
        for index in range(p.getNumJoints(self.body, physicsClientId=self.client)):
            info = p.getJointInfo(self.body, index, physicsClientId=self.client)
            if info[2] != p.JOINT_FIXED:
                self._joint_indices[info[1].decode()] = index
        # PyBullet enables velocity motors by default; release them so
        # unactuated joints swing freely until a target is set.
        for index in self._joint_indices.values():
            p.setJointMotorControl2(
                self.body,
                index,
                p.VELOCITY_CONTROL,
                force=0,
                physicsClientId=self.client,
            )

    def _joint(self, name: str) -> int:
        try:
            return self._joint_indices[name]
        except KeyError:
            raise KeyError(
                f"Unknown joint {name!r}; joints are {sorted(self._joint_indices)}"
            ) from None

    def step(self, count: int = 1) -> None:
        for _ in range(count):
            self._p.stepSimulation(physicsClientId=self.client)

    def set_joint_target(self, name: str, value: float, force: float = 100.0) -> None:
        """Position-control a joint towards ``value``. ``force`` caps the
        motor's torque (N*m) or thrust (N) — e.g. a gripper's grip force."""
        self._p.setJointMotorControl2(
            self.body,
            self._joint(name),
            self._p.POSITION_CONTROL,
            targetPosition=value,
            force=force,
            physicsClientId=self.client,
        )

    def set_joint_value(self, name: str, value: float) -> None:
        self._p.resetJointState(
            self.body, self._joint(name), value, physicsClientId=self.client
        )

    def get_joint_value(self, name: str) -> float:
        state = self._p.getJointState(
            self.body, self._joint(name), physicsClientId=self.client
        )
        return float(state[0])

    def get_body_pose(self, name: str) -> tuple[tuple[float, ...], tuple[float, ...]]:
        """World position and quaternion (w, x, y, z) of a scene body or of
        the robot's root link."""
        if name in self.scene_bodies:
            body = self.scene_bodies[name]
        elif name == self.links[0].name:
            body = self.body
        else:
            known = [self.links[0].name, *self.scene_bodies]
            raise KeyError(f"Unknown body {name!r}; bodies are {known}")
        position, (x, y, z, w) = self._p.getBasePositionAndOrientation(
            body, physicsClientId=self.client
        )
        return tuple(map(float, position)), (w, x, y, z)

    def get_keyboard_events(self) -> dict:
        """PyBullet GUI keyboard events (key code -> state)."""
        return self._p.getKeyboardEvents(physicsClientId=self.client)

    def is_connected(self) -> bool:
        return bool(self._p.isConnected(self.client))

    def close(self) -> None:
        if self._p.isConnected(self.client):
            self._p.disconnect(physicsClientId=self.client)


def simulate(
    part: Part3D,
    *,
    gui: bool = False,
    lighting: list[Lighting] | None = None,
    gravity: tuple[float, float, float] = (0.0, 0.0, -9.81),
    time_step: float = 1.0 / 240.0,
    fixed_base: bool = True,
    actuated: bool = True,
    ground_plane: bool = False,
    scene_parts: list[Part3D] | None = None,
    output_dir: str | Path | None = None,
) -> PyBulletSimulation:
    """Export ``part``'s assembly (meshes + joint constraints) to a URDF and
    load it into PyBullet. Joints are passive until ``set_joint_target`` is
    called. ``ground_plane`` adds a static floor at z=0. ``scene_parts``
    are loose, free-floating bodies the robot can collide with (e.g. an
    object to pick up) — pair them with ``ground_plane=True`` so they have
    a floor to rest on."""
    return PyBulletSimulation(
        part,
        gui=gui,
        lighting=lighting,
        gravity=gravity,
        time_step=time_step,
        fixed_base=fixed_base,
        actuated=actuated,
        ground_plane=ground_plane,
        scene_parts=scene_parts,
        output_dir=output_dir,
    )
