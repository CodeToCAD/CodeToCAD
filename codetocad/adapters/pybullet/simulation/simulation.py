"""
PyBullet implementation of SimulationInterface.
"""

from typing import TYPE_CHECKING, Sequence
from uuid import uuid4
import pybullet as p
import tempfile
import os

from codetocad.interfaces.simulation.simulation_interface import SimulationInterface
from codetocad.core.dimensions.point import Point
from codetocad.adapters.pybullet.pybullet_actions import simulation_setup
from codetocad.adapters.pybullet.pybullet_actions import body_management
from codetocad.adapters.pybullet.pybullet_actions import file_loading
from codetocad.adapters.pybullet.simulation.simulation_export import (
    PyBulletSimulationExport,
)

if TYPE_CHECKING:
    from codetocad.adapters.pybullet.simulation.simulation_body import SimulationBody
    from codetocad.interfaces.cad.part.part_interface import PartInterface
    from codetocad.interfaces.cad.assembly.assembly_interface import AssemblyInterface


class Simulation(SimulationInterface):
    """PyBullet implementation of SimulationInterface."""

    def __init__(self, name: str | None = None):
        super().__init__()
        self.name = name or f"pybullet_sim_{str(uuid4())[:8]}"
        self.client_id: int | None = None
        self.gui_enabled: bool = False
        self._body_registry: dict[int, "SimulationBody"] = {}

        # Initialize export functionality
        self.export = PyBulletSimulationExport(self)

    def initialize(self, gui: bool = False, **kwargs) -> None:
        """Initialize the PyBullet simulation environment."""
        self.gui_enabled = gui
        self.client_id = simulation_setup.initialize_physics_client(gui, **kwargs)

        # Set default physics parameters
        simulation_setup.set_gravity(self.gravity)
        simulation_setup.set_time_step(self.time_step)

        if gui:
            simulation_setup.configure_debug_visualizer()

    def reset(self) -> None:
        """Reset the simulation to initial state."""
        simulation_setup.reset_simulation()
        self.current_time = 0.0
        self.bodies.clear()
        self._body_registry.clear()

    def step(self, num_steps: int = 1) -> None:
        """Step the simulation forward in time."""
        simulation_setup.step_simulation(num_steps)
        self.current_time += num_steps * self.time_step

    def set_gravity(self, gravity: Point | tuple[float, float, float]) -> None:
        """Set the gravity vector for the simulation."""
        if isinstance(gravity, tuple):
            self.gravity = Point(gravity[0], gravity[1], gravity[2])
        else:
            self.gravity = gravity

        simulation_setup.set_gravity(self.gravity)

    def set_time_step(self, time_step: float) -> None:
        """Set the simulation time step."""
        self.time_step = time_step
        simulation_setup.set_time_step(time_step)

    def add_ground_plane(
        self,
        position: Point | tuple[float, float, float] = (0, 0, 0),
        normal: Point | tuple[float, float, float] = (0, 0, 1),
        **kwargs,
    ) -> "SimulationBody":
        """Add a ground plane to the simulation."""
        from codetocad.adapters.pybullet.simulation.simulation_body import (
            SimulationBody,
        )

        body_id = body_management.create_ground_plane(position, normal, **kwargs)

        sim_body = SimulationBody()
        sim_body.name = "ground_plane"
        sim_body.body_id = body_id
        sim_body.is_static = True

        self.bodies.append(sim_body)
        self._body_registry[body_id] = sim_body

        return sim_body

    def load_urdf(
        self,
        urdf_path: str,
        position: Point | tuple[float, float, float] = (0, 0, 0),
        orientation: tuple[float, float, float, float] = (0, 0, 0, 1),
        **kwargs,
    ) -> "SimulationBody":
        """Load a URDF file into the simulation."""
        from codetocad.adapters.pybullet.simulation.simulation_body import (
            SimulationBody,
        )

        body_id = file_loading.load_urdf_file(
            urdf_path, position, orientation, **kwargs
        )

        sim_body = SimulationBody()
        sim_body.name = f"urdf_body_{str(uuid4())[:8]}"
        sim_body.body_id = body_id

        self.bodies.append(sim_body)
        self._body_registry[body_id] = sim_body

        return sim_body

    def load_stl(
        self,
        stl_path: str,
        position: Point | tuple[float, float, float] = (0, 0, 0),
        orientation: tuple[float, float, float, float] = (0, 0, 0, 1),
        mass: float = 1.0,
        **kwargs,
    ) -> "SimulationBody":
        """Load an STL file as a rigid body."""
        from codetocad.adapters.pybullet.simulation.simulation_body import (
            SimulationBody,
        )

        body_id = file_loading.load_stl_file(
            stl_path, position, orientation, mass, **kwargs
        )

        sim_body = SimulationBody()
        sim_body.name = f"stl_body_{str(uuid4())[:8]}"
        sim_body.body_id = body_id
        sim_body.mass = mass

        self.bodies.append(sim_body)
        self._body_registry[body_id] = sim_body

        return sim_body

    def add_part(
        self,
        part: "PartInterface",
        position: Point | tuple[float, float, float] = (0, 0, 0),
        orientation: tuple[float, float, float, float] = (0, 0, 0, 1),
        mass: float | None = None,
        **kwargs,
    ) -> "SimulationBody":
        """Add a CodeToCAD Part to the simulation using its physical properties."""
        from codetocad.adapters.pybullet.simulation.simulation_body import (
            SimulationBody,
        )

        # Use part's physical properties
        effective_mass = mass if mass is not None else part.get_effective_mass()

        # Create body without material properties (they'll be set after creation)
        body_id = body_management.create_body_from_part(
            part, position, orientation, effective_mass, **kwargs
        )

        # Apply material properties after body creation
        body_management.set_body_friction(body_id, part.friction)
        body_management.set_body_restitution(body_id, part.restitution)

        # Apply visual properties from material
        body_management.apply_material_visual_properties(body_id, part)

        # Set damping if available
        try:
            import pybullet as p

            p.changeDynamics(
                body_id,
                -1,
                linearDamping=part.damping[0],
                angularDamping=part.damping[1],
            )
        except:
            pass  # Ignore if damping setting fails

        sim_body = SimulationBody()
        sim_body.name = part.name or f"part_body_{str(uuid4())[:8]}"
        sim_body.body_id = body_id
        sim_body.mass = effective_mass
        sim_body.original_part = part

        self.bodies.append(sim_body)
        self._body_registry[body_id] = sim_body

        return sim_body

    def add_assembly(
        self,
        assembly: "AssemblyInterface",
        position: Point | tuple[float, float, float] = (0, 0, 0),
        orientation: tuple[float, float, float, float] = (0, 0, 0, 1),
        detect_constraints: bool = True,
        **kwargs,
    ) -> Sequence["SimulationBody"]:
        """Add a CodeToCAD Assembly to the simulation with constraint detection."""
        sim_bodies = []

        # Add all parts first
        for i, part in enumerate(assembly.parts):
            # Offset each part slightly to avoid overlap
            if isinstance(position, Point):
                part_pos = Point(position.x + i * 0.1, position.y, position.z)
            else:
                part_pos = (position[0] + i * 0.1, position[1], position[2])

            sim_body = self.add_part(part, part_pos, orientation, **kwargs)
            sim_bodies.append(sim_body)

        # Add cameras and lights from assembly
        for camera in assembly.cameras:
            self.add_camera(camera)

        for light in assembly.lights:
            self.add_light(light)

        # Detect and create kinematic constraints if requested
        if detect_constraints:
            constraints = self.detect_kinematic_constraints(assembly)
            for constraint in constraints:
                # Find corresponding simulation bodies
                body1_idx = self._find_body_index_for_part(
                    constraint.get("body1"), assembly.parts
                )
                body2_idx = self._find_body_index_for_part(
                    constraint.get("body2"), assembly.parts
                )

                if (
                    body1_idx is not None
                    and body2_idx is not None
                    and body1_idx < len(sim_bodies)
                    and body2_idx < len(sim_bodies)
                ):
                    self.create_joint_from_constraint(
                        constraint, sim_bodies[body1_idx], sim_bodies[body2_idx]
                    )

        return sim_bodies

    def _find_body_index_for_part(self, part, parts_list) -> int | None:
        """Find the index of a part in the parts list."""
        if part is None:
            return None
        try:
            return parts_list.index(part)
        except ValueError:
            return None

    def create_joint_from_constraint(self, constraint: dict, body1, body2):
        """Create a PyBullet joint from a constraint definition."""
        from codetocad.adapters.pybullet.simulation.simulation_joint import (
            SimulationJoint,
        )
        from codetocad.interfaces.simulation.simulation_joint_interface import JointType

        # Map constraint types to PyBullet joint types
        constraint_type = constraint.get("type", "fixed")

        if constraint_type == "fixed":
            joint_type = JointType.FIXED
        elif constraint_type == "revolute":
            joint_type = JointType.REVOLUTE
        elif constraint_type == "prismatic":
            joint_type = JointType.PRISMATIC
        else:
            joint_type = JointType.FIXED  # Default fallback

        # Create joint
        joint = SimulationJoint()
        joint.create_joint(
            body1,
            body2,
            joint_type,
            position=Point(*constraint.get("position", (0, 0, 0))),
            axis=Point(*constraint.get("axis", (0, 0, 1))),
            limits=constraint.get("limits"),
        )

        return joint

    def remove_body(self, body: "SimulationBody") -> None:
        """Remove a body from the simulation."""
        if hasattr(body, "body_id") and body.body_id is not None:
            body_management.remove_body(body.body_id)

            if body.body_id in self._body_registry:
                del self._body_registry[body.body_id]

        if body in self.bodies:
            self.bodies.remove(body)

    def get_body_by_name(self, name: str) -> "SimulationBody | None":
        """Get a body by name."""
        for body in self.bodies:
            if body.name == name:
                return body
        return None

    def start(self) -> None:
        """Start the simulation."""
        self.is_running = True

    def stop(self) -> None:
        """Stop the simulation."""
        self.is_running = False

    def pause(self) -> None:
        """Pause the simulation."""
        self.is_running = False

    def resume(self) -> None:
        """Resume the simulation."""
        self.is_running = True

    def disconnect(self) -> None:
        """Disconnect from the simulation environment."""
        if self.client_id is not None:
            simulation_setup.disconnect_physics_client(self.client_id)
            self.client_id = None
        self.is_running = False

    def __del__(self):
        """Cleanup when simulation is destroyed."""
        try:
            self.disconnect()
        except:
            pass  # Ignore errors during cleanup
