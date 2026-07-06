"""MJCF generation and the MuJoCo-backed Simulation."""

from __future__ import annotations

import tempfile
from pathlib import Path
from xml.etree import ElementTree as ET

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


def build_mjcf(
    links: list[LinkSpec],
    name: str = "codetocad_robot",
    *,
    gravity: tuple[float, float, float] = (0.0, 0.0, -9.81),
    time_step: float = 1.0 / 240.0,
    fixed_base: bool = True,
    actuated: bool = True,
    actuator_kp: float = 100.0,
    lighting: list[Lighting] | None = None,
) -> str:
    """Build an MJCF document from an extracted kinematic tree. Mesh paths
    must already be filled in and be binary STLs in one directory."""
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
    for link in links:
        ET.SubElement(
            asset, "mesh", name=link.name, file=Path(link.mesh_path).name
        )

    worldbody = ET.SubElement(mujoco_el, "worldbody")
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
                joint.set("damping", "0.5")
        ET.SubElement(
            body,
            "geom",
            type="mesh",
            mesh=link.name,
            pos=_fmt(-link.frame),
            rgba=_fmt(link.color_rgba),
        )
        ET.SubElement(
            body,
            "inertial",
            pos=_fmt(link.center_of_mass - link.frame),
            mass=f"{link.mass:.9g}",
            diaginertia=_fmt(link.inertia_diagonal),
        )
        for child in link.children:
            emit_body(child, body)

    emit_body(links[0], worldbody)

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
                ET.SubElement(
                    actuator,
                    "position",
                    name=f"{link.joint.name}_actuator",
                    joint=link.joint.name,
                    kp=f"{actuator_kp:.9g}",
                )
    ET.indent(mujoco_el)
    return ET.tostring(mujoco_el, encoding="unicode")


class MujocoSimulation(Simulation):
    def __init__(
        self,
        root_part: Part3D,
        *,
        output_dir: str | Path | None = None,
        **kwargs,
    ):
        super().__init__(root_part, **kwargs)
        import mujoco

        self._mujoco = mujoco
        self.output_dir = Path(
            output_dir
            if output_dir is not None
            else tempfile.mkdtemp(prefix="codetocad_mujoco_")
        ).resolve()
        export_link_meshes(self.links, self.output_dir)
        for link in self.links:
            ensure_binary_stl(link.mesh_path)  # MuJoCo needs binary STL
        mjcf = build_mjcf(
            self.links,
            name=root_part.name or "codetocad_robot",
            gravity=self.gravity,
            time_step=self.time_step,
            fixed_base=self.fixed_base,
            actuated=self.actuated,
            lighting=self.lighting,
        )
        self.mjcf_path = self.output_dir / "robot.xml"
        self.mjcf_path.write_text(mjcf)

        self.model = mujoco.MjModel.from_xml_path(str(self.mjcf_path))
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

    def set_joint_value(self, name: str, value: float) -> None:
        address = self.model.jnt_qposadr[self._joint_id(name)]
        self.data.qpos[address] = value
        self._mujoco.mj_forward(self.model, self.data)

    def get_joint_value(self, name: str) -> float:
        address = self.model.jnt_qposadr[self._joint_id(name)]
        return float(self.data.qpos[address])

    def launch_viewer(self, key_callback=None) -> None:
        """Open the interactive viewer and step in real time until closed.
        On macOS this must run under ``mjpython``."""
        import time

        import mujoco.viewer

        with mujoco.viewer.launch_passive(
            self.model, self.data, key_callback=key_callback
        ) as viewer:
            while viewer.is_running():
                start = time.time()
                self.step()
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
    output_dir: str | Path | None = None,
) -> MujocoSimulation:
    """Export ``part``'s assembly (meshes + joint constraints) to an MJCF
    model and load it into MuJoCo."""
    return MujocoSimulation(
        part,
        lighting=lighting,
        gravity=gravity,
        time_step=time_step,
        fixed_base=fixed_base,
        actuated=actuated,
        output_dir=output_dir,
    )
