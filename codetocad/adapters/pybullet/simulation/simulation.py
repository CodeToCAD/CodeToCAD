"""
PyBullet implementation of SimulationInterface.
"""

from typing import TYPE_CHECKING, Optional, List, Sequence
from uuid import uuid4
import pybullet as p

from codetocad.interfaces.simulation.simulation_interface import SimulationInterface
from codetocad.core.dimensions.point import Point
from codetocad.adapters.pybullet.pybullet_actions import simulation_setup
from codetocad.adapters.pybullet.pybullet_actions import body_management
from codetocad.adapters.pybullet.pybullet_actions import file_loading

if TYPE_CHECKING:
    from codetocad.adapters.pybullet.simulation.simulation_body import SimulationBody
    from codetocad.interfaces.cad.part.part_interface import PartInterface
    from codetocad.interfaces.cad.assembly.assembly_interface import AssemblyInterface


class Simulation(SimulationInterface):
    """PyBullet implementation of SimulationInterface."""

    def __init__(self, name: str | None = None):
        super().__init__()
        self.name = name or f"pybullet_sim_{str(uuid4())[:8]}"
        self.client_id: Optional[int] = None
        self.gui_enabled: bool = False
        self._body_registry: dict[int, "SimulationBody"] = {}

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
        mass: float = 1.0,
        **kwargs,
    ) -> "SimulationBody":
        """Add a CodeToCAD Part to the simulation."""
        from codetocad.adapters.pybullet.simulation.simulation_body import (
            SimulationBody,
        )

        body_id = body_management.create_body_from_part(
            part, position, orientation, mass, **kwargs
        )

        sim_body = SimulationBody()
        sim_body.name = part.name or f"part_body_{str(uuid4())[:8]}"
        sim_body.body_id = body_id
        sim_body.mass = mass
        sim_body.original_part = part

        self.bodies.append(sim_body)
        self._body_registry[body_id] = sim_body

        return sim_body

    def add_assembly(
        self,
        assembly: "AssemblyInterface",
        position: Point | tuple[float, float, float] = (0, 0, 0),
        orientation: tuple[float, float, float, float] = (0, 0, 0, 1),
        **kwargs,
    ) -> Sequence["SimulationBody"]:
        """Add a CodeToCAD Assembly to the simulation."""
        sim_bodies = []

        for i, part in enumerate(assembly.parts):
            # Offset each part slightly to avoid overlap
            if isinstance(position, Point):
                part_pos = Point(position.x + i * 0.1, position.y, position.z)
            else:
                part_pos = (position[0] + i * 0.1, position[1], position[2])

            sim_body = self.add_part(part, part_pos, orientation, **kwargs)
            sim_bodies.append(sim_body)

        return sim_bodies

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
