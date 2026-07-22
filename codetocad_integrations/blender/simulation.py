"""Blender-backed simulation of a CodeToCAD assembly.

Unlike the pybullet/mujoco backends (which federate to a physics engine),
this backend realizes the assembly's joints natively in Blender: each part is
built as a Blender object and every joint becomes an *empty* placed at the
joint anchor, oriented so its local Z is the joint axis. Parts are parented to
their joint empty, and empties chain parent-to-child, so rotating (revolute) or
sliding (prismatic) an empty carries its whole sub-tree — a live articulated
rig. Joint limits are enforced with Blender **Limit Rotation / Limit Location
constraints**, and commanded poses are held with Blender's **native
keyframing** (``set_keyframe``), which the interactive viewer plays back.

Run inside Blender (call ``ensure_blender()`` first). ``sim.launch_viewer()``
opens a Blender GUI on the assembly and plays the keyframed animation.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import numpy as np

from codetocad.parts import Part3D
from codetocad.simulation import LinkSpec, Simulation

try:
    import bpy
    from mathutils import Matrix, Quaternion, Vector

    INSIDE_BLENDER = True
except ImportError:  # pragma: no cover - exercised only outside Blender
    INSIDE_BLENDER = False


def _axis_quaternion(axis: np.ndarray) -> "Quaternion":
    """A rotation mapping +Z onto ``axis`` — orients a joint empty so its
    local Z is the joint axis."""
    return Vector((0.0, 0.0, 1.0)).rotation_difference(Vector(tuple(axis)))


class BlenderSimulation(Simulation):
    """A live articulated Blender rig built from the assembly's joints.

    Joints are driven kinematically (position/velocity commands pose the rig
    directly); pair commands with :meth:`set_keyframe` to record an animation
    the viewer plays back."""

    def __init__(self, root_part: Part3D, *, fps: int = 24, **kwargs):
        if not INSIDE_BLENDER:
            raise RuntimeError(
                "BlenderSimulation requires Blender's Python (bpy). Call "
                "ensure_blender() at the start of your script so it relaunches "
                "under Blender."
            )
        # The base extracts links, resolves scene/collision info and binds the
        # Joint objects returned by .revolute()/.prismatic()/.fixed().
        super().__init__(root_part, **kwargs)
        self.fps = fps
        # One physics/keyframe step advances one Blender frame, so the shared
        # play_keyframes / record_gif stepping paces to the frame rate.
        self.time_step = 1.0 / fps
        self._frame = 1
        #: Current commanded value (rad/m) per joint name.
        self._joint_values: dict[str, float] = {}
        #: Ongoing velocity (rad/s or m/s) per joint name, advanced each step.
        self._joint_velocities: dict[str, float] = {}
        #: The Blender empty acting as each joint; the object controlled by a
        #: parent link (root's control is the root object itself).
        self._joint_empty: dict[str, object] = {}
        self._control: dict[str, object] = {}
        #: Rest (zero-value) world matrix of each joint empty.
        self._joint_rest: dict[str, Matrix] = {}

        scene = bpy.context.scene
        scene.render.fps = fps
        scene.frame_start = 1
        scene.frame_end = 1
        self._build_rig()

    # -- rig construction --

    def _build_rig(self) -> None:
        from codetocad_integrations.blender.parts import adapt

        for link in self.links:
            obj = adapt(link.part).get_native()
            if np.any(link.shift):
                obj.location = tuple(
                    np.asarray(obj.location, dtype=float) + np.asarray(link.shift)
                )
            bpy.context.view_layer.update()
            if link.parent is None:
                self._control[link.name] = obj
                continue
            parent_control = self._control[link.parent.name]
            empty = self._make_joint_empty(link, parent_control)
            self._parent_keep_world(obj, empty, Matrix(obj.matrix_world))
            self._control[link.name] = empty
            self._joint_empty[link.joint.name] = empty
            self._joint_values[link.joint.name] = link.joint.initial_value or 0.0
        bpy.context.view_layer.update()
        self._apply_initial_joint_values()

    def _make_joint_empty(self, link: LinkSpec, parent_control) -> object:
        joint = link.joint
        empty = bpy.data.objects.new(f"{joint.name}__joint", None)
        empty.empty_display_type = "ARROWS"
        empty.empty_display_size = 0.05
        bpy.context.collection.objects.link(empty)
        rotation = (
            _axis_quaternion(joint.axis)
            if joint.joint_type != "fixed"
            else Quaternion()
        )
        world_rest = Matrix.Translation(Vector(tuple(joint.anchor))) @ rotation.to_matrix().to_4x4()
        self._joint_rest[joint.name] = world_rest
        self._parent_keep_world(empty, parent_control, world_rest)
        empty.rotation_mode = "QUATERNION"
        self._add_limit_constraint(empty, joint)
        # Flush the empty's transform so its matrix_world is current before the
        # child part is parented under it (which reads empty.matrix_world to
        # keep its own world pose) -- otherwise the child inherits a stale
        # parent frame and flies off.
        bpy.context.view_layer.update()
        return empty

    @staticmethod
    def _parent_keep_world(child, parent, world_rest: "Matrix") -> None:
        """Parent ``child`` under ``parent`` so its world matrix is
        ``world_rest``. With ``matrix_parent_inverse`` set to the parent's
        (rest) inverse, ``world = matrix_basis``, so a later
        ``matrix_basis = world_rest @ delta`` applies ``delta`` about the
        joint's own local frame."""
        child.parent = parent
        child.matrix_parent_inverse = parent.matrix_world.inverted()
        child.matrix_basis = world_rest

    @staticmethod
    def _add_limit_constraint(empty, joint) -> None:
        if joint.lower is None and joint.upper is None:
            return
        lower = joint.lower if joint.lower is not None else joint.upper
        upper = joint.upper if joint.upper is not None else joint.lower
        if joint.joint_type == "revolute":
            constraint = empty.constraints.new("LIMIT_ROTATION")
            constraint.owner_space = "LOCAL"
            constraint.use_limit_z = True
            constraint.min_z = lower
            constraint.max_z = upper
        elif joint.joint_type == "prismatic":
            constraint = empty.constraints.new("LIMIT_LOCATION")
            constraint.owner_space = "LOCAL"
            constraint.use_min_z = True
            constraint.use_max_z = True
            constraint.min_z = lower
            constraint.max_z = upper

    def _delta_matrix(self, joint_type: str, value: float) -> "Matrix":
        if joint_type == "prismatic":
            return Matrix.Translation(Vector((0.0, 0.0, value)))
        return Matrix.Rotation(value, 4, "Z")

    def _pose_joint(self, name: str, value: float) -> None:
        empty = self._joint_empty[name]
        joint_type = self._joint_type(name)
        empty.matrix_basis = self._joint_rest[name] @ self._delta_matrix(
            joint_type, value
        )
        self._joint_values[name] = value

    def _joint_type(self, name: str) -> str:
        for link in self.links:
            if link.joint is not None and link.joint.name == name:
                return link.joint.joint_type
        raise KeyError(f"Unknown joint {name!r}; joints are {self.joint_names}")

    # -- Simulation interface --

    def step(self, count: int = 1) -> None:
        """Advance the animation by ``count`` frames, integrating any joint
        velocities and playing back keyframes."""
        dt = 1.0 / self.fps
        for _ in range(count):
            for name, velocity in self._joint_velocities.items():
                if velocity:
                    self._pose_joint(name, self._joint_values[name] + velocity * dt)
            self._frame += 1
            bpy.context.scene.frame_end = max(
                bpy.context.scene.frame_end, self._frame
            )
            bpy.context.scene.frame_set(self._frame)
            bpy.context.view_layer.update()

    def _set_joint_target(self, name: str, value: float, **_) -> None:
        self._pose_joint(name, value)
        bpy.context.view_layer.update()

    def _set_joint_velocity(self, name: str, value: float) -> None:
        self._joint_velocities[name] = value

    def set_joint_value(self, joint, value: float) -> None:
        self._pose_joint(self._resolve_joint_name(joint), value)
        bpy.context.view_layer.update()

    def get_joint_value(self, joint) -> float:
        return float(self._joint_values[self._resolve_joint_name(joint)])

    def set_keyframe(self, time: float | None = None) -> float:
        """Hold the joints' currently commanded positions as a Blender
        keyframe at ``time`` seconds (native ``keyframe_insert``). The
        interactive viewer and :meth:`record_gif` play these back."""
        time = super().set_keyframe(time)
        frame = 1 + round(time * self.fps)
        bpy.context.scene.frame_end = max(bpy.context.scene.frame_end, frame)
        for name, empty in self._joint_empty.items():
            self._pose_joint(name, self._joint_targets.get(name, self._joint_values[name]))
            data_path = (
                "location"
                if self._joint_type(name) == "prismatic"
                else "rotation_quaternion"
            )
            empty.keyframe_insert(data_path=data_path, frame=frame)
        return time

    # -- rendering --

    def _ensure_camera(self):
        scene = bpy.context.scene
        if scene.camera is not None:
            return scene.camera
        corners = []
        for link in self.links:
            obj = self._control_object(link)
            corners.extend(obj.matrix_world @ Vector(c) for c in obj.bound_box)
        points = np.array([tuple(c) for c in corners]) if corners else np.zeros((1, 3))
        center = Vector(tuple(points.mean(axis=0)))
        radius = float(np.linalg.norm(points.max(axis=0) - points.min(axis=0))) or 1.0
        camera_data = bpy.data.cameras.new("sim_camera")
        camera = bpy.data.objects.new("sim_camera", camera_data)
        bpy.context.collection.objects.link(camera)
        offset = Vector((1.0, -1.0, 0.8)).normalized() * (radius * 1.6 + 0.5)
        camera.location = center + offset
        direction = (center - camera.location).normalized()
        camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
        scene.camera = camera
        return camera

    def _control_object(self, link: LinkSpec):
        from codetocad_integrations.blender.parts import adapt

        return adapt(link.part).get_native()

    def capture_image(self, width: int = 640, height: int = 480) -> np.ndarray:
        """Render an overview of the current pose to an (height, width, 3)
        uint8 RGB array (Workbench engine, an auto-framed camera)."""
        scene = bpy.context.scene
        self._ensure_camera()
        scene.render.engine = "BLENDER_WORKBENCH"
        scene.render.resolution_x = width
        scene.render.resolution_y = height
        scene.render.image_settings.file_format = "PNG"
        scene.render.image_settings.color_mode = "RGBA"
        path = str(self.output_dir / "_capture.png")
        scene.render.filepath = path
        bpy.ops.render.render(write_still=True)
        image = bpy.data.images.load(path, check_existing=False)
        pixels = np.array(image.pixels[:], dtype=np.float32).reshape(
            image.size[1], image.size[0], image.channels
        )
        bpy.data.images.remove(image)
        # Blender pixels are bottom-up float RGBA; flip to top-down uint8 RGB.
        rgb = np.flipud(pixels[:, :, :3])
        return (np.clip(rgb, 0.0, 1.0) * 255.0).astype(np.uint8)

    # -- viewer --

    def save(self, path: str | Path | None = None) -> Path:
        """Save the assembled rig to a .blend file (defaults to the sim's
        output directory)."""
        path = Path(path) if path is not None else self.output_dir / "scene.blend"
        bpy.ops.wm.save_as_mainfile(filepath=str(path))
        return path

    def launch_viewer(self, *, play: bool = True, block: bool = False) -> "Path":
        """Open a Blender GUI on the assembly. Saves the current rig to a
        .blend and launches Blender on it, starting animation playback so the
        recorded keyframes run. Returns the saved .blend path. ``block=True``
        waits for the viewer to close."""
        from codetocad_integrations.blender.launcher import _blender_executable

        blend_path = self.save()
        command = [_blender_executable(), str(blend_path)]
        if play:
            command += [
                "--python-expr",
                "import bpy; bpy.ops.screen.animation_play()",
            ]
        runner = subprocess.run if block else subprocess.Popen
        runner(command)
        return blend_path


def simulate(part: Part3D, *, fps: int = 24, **kwargs) -> BlenderSimulation:
    """Build ``part``'s assembly as a live articulated rig in Blender, its
    joints realized with empties + Blender Limit constraints. Command the
    joints (``joint.move_to(...)``, ``sim.get_joint(name)`` for name access),
    pin poses with ``sim.set_keyframe()``, open it with ``sim.launch_viewer()``.
    Run inside Blender (call ``ensure_blender()`` first)."""
    return BlenderSimulation(part, fps=fps, **kwargs)
