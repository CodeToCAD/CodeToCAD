"""
MuJoCo implementation of SimulationInterface.
"""

from typing import TYPE_CHECKING, Optional, List
from uuid import uuid4
import mujoco as mj
import tempfile
import os

from codetocad.interfaces.simulation.simulation_interface import SimulationInterface
from codetocad.core.dimensions.point import Point
from codetocad.adapters.mujoco.mujoco_actions import simulation_setup
from codetocad.adapters.mujoco.mujoco_actions import xml_generation

if TYPE_CHECKING:
    from codetocad.adapters.mujoco.simulation.simulation_body import SimulationBody
    from codetocad.interfaces.cad.part.part_interface import PartInterface
    from codetocad.interfaces.cad.assembly.assembly_interface import AssemblyInterface


class Simulation(SimulationInterface):
    """MuJoCo implementation of SimulationInterface."""

    def __init__(self, name: str | None = None):
        super().__init__()
        self.name = name or f"mujoco_sim_{str(uuid4())[:8]}"
        self.model: Optional[mj.MjModel] = None
        self.data: Optional[mj.MjData] = None
        self.viewer: Optional[Any] = None
        self.gui_enabled: bool = False
        self._body_registry: dict[str, "SimulationBody"] = {}

    def initialize(self, gui: bool = False, **kwargs) -> None:
        """Initialize the MuJoCo simulation environment."""
        self.gui_enabled = gui

        # Create default model if none provided
        xml_string = kwargs.get("xml_string")
        xml_path = kwargs.get("xml_path")

        if not xml_string and not xml_path:
            # Create basic model with ground plane
            root = xml_generation.create_basic_xml_structure()
            worldbody = root.find("worldbody")
            ground = xml_generation.create_ground_plane_xml()
            worldbody.append(ground)
            xml_string = xml_generation.xml_to_string(root)

        self.model = simulation_setup.initialize_mujoco_model(xml_string, xml_path)
        self.data = simulation_setup.create_mujoco_data(self.model)

        # Set default physics parameters
        simulation_setup.set_mujoco_gravity(self.model, self.gravity)
        simulation_setup.set_mujoco_timestep(self.model, self.time_step)

        if gui:
            try:
                import mujoco.viewer

                self.viewer = mujoco.viewer.launch_passive(self.model, self.data)
            except ImportError:
                print("MuJoCo viewer not available")

    def reset(self) -> None:
        """Reset the simulation to initial state."""
        if self.model and self.data:
            simulation_setup.reset_mujoco_simulation(self.model, self.data)
            self.current_time = 0.0
            self.bodies.clear()
            self._body_registry.clear()

    def step(self, num_steps: int = 1) -> None:
        """Step the simulation forward in time."""
        if self.model and self.data:
            simulation_setup.step_mujoco_simulation(self.model, self.data, num_steps)
            self.current_time = simulation_setup.get_simulation_time(self.data)

            if self.viewer:
                self.viewer.sync()

    def set_gravity(self, gravity: Point | tuple[float, float, float]) -> None:
        """Set the gravity vector for the simulation."""
        if isinstance(gravity, tuple):
            self.gravity = Point(gravity[0], gravity[1], gravity[2])
        else:
            self.gravity = gravity

        if self.model:
            simulation_setup.set_mujoco_gravity(self.model, self.gravity)

    def set_time_step(self, time_step: float) -> None:
        """Set the simulation time step."""
        self.time_step = time_step
        if self.model:
            simulation_setup.set_mujoco_timestep(self.model, time_step)

    def add_ground_plane(
        self,
        position: Point | tuple[float, float, float] = (0, 0, 0),
        normal: Point | tuple[float, float, float] = (0, 0, 1),
        **kwargs,
    ) -> "SimulationBody":
        """Add a ground plane to the simulation."""
        from codetocad.adapters.mujoco.simulation.simulation_body import SimulationBody

        # Ground plane is typically part of the initial model
        # For now, return a placeholder body
        sim_body = SimulationBody()
        sim_body.name = "ground_plane"
        sim_body.body_name = "ground"
        sim_body.is_static = True

        self.bodies.append(sim_body)
        self._body_registry["ground"] = sim_body

        return sim_body

    def load_urdf(
        self,
        urdf_path: str,
        position: Point | tuple[float, float, float] = (0, 0, 0),
        orientation: tuple[float, float, float, float] = (0, 0, 0, 1),
        **kwargs,
    ) -> "SimulationBody":
        """Load a URDF file into the simulation."""
        # MuJoCo doesn't directly support URDF - would need conversion
        # This is a placeholder implementation
        from codetocad.adapters.mujoco.simulation.simulation_body import SimulationBody

        sim_body = SimulationBody()
        sim_body.name = f"urdf_body_{str(uuid4())[:8]}"
        sim_body.body_name = sim_body.name

        self.bodies.append(sim_body)
        self._body_registry[sim_body.name] = sim_body

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
        from codetocad.adapters.mujoco.simulation.simulation_body import SimulationBody

        # Create XML with mesh
        body_name = f"stl_body_{str(uuid4())[:8]}"
        mesh_name = f"{body_name}_mesh"

        # Generate XML for the body with mesh
        body_xml = xml_generation.generate_body_xml(
            body_name, position, orientation, mass
        )
        mesh_xml = xml_generation.convert_stl_to_mesh(stl_path, mesh_name)

        # This would require recompiling the model with the new body
        # For now, create a placeholder body
        sim_body = SimulationBody()
        sim_body.name = body_name
        sim_body.body_name = body_name
        sim_body.mass = mass

        self.bodies.append(sim_body)
        self._body_registry[body_name] = sim_body

        return sim_body

    def load_xml(self, xml_path: str) -> "SimulationBody":
        """Load a MuJoCo XML file."""
        # Reload the entire model with the new XML
        self.model = simulation_setup.initialize_mujoco_model(xml_path=xml_path)
        self.data = simulation_setup.create_mujoco_data(self.model)

        from codetocad.adapters.mujoco.simulation.simulation_body import SimulationBody

        sim_body = SimulationBody()
        sim_body.name = f"xml_body_{str(uuid4())[:8]}"
        sim_body.body_name = sim_body.name

        self.bodies.append(sim_body)
        self._body_registry[sim_body.name] = sim_body

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
        from codetocad.adapters.mujoco.simulation.simulation_body import SimulationBody

        # Export part to temporary STL and create body
        with tempfile.NamedTemporaryFile(suffix=".stl", delete=False) as tmp_file:
            tmp_path = tmp_file.name

        try:
            part.export.stl(tmp_path)
            sim_body = self.load_stl(tmp_path, position, orientation, mass, **kwargs)
            sim_body.name = part.name or sim_body.name
            sim_body.original_part = part
            return sim_body
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def add_assembly(
        self,
        assembly: "AssemblyInterface",
        position: Point | tuple[float, float, float] = (0, 0, 0),
        orientation: tuple[float, float, float, float] = (0, 0, 0, 1),
        **kwargs,
    ) -> List["SimulationBody"]:
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
        # MuJoCo requires model recompilation to remove bodies
        # This is a placeholder implementation
        if body.name and body.name in self._body_registry:
            del self._body_registry[body.name]

        if body in self.bodies:
            self.bodies.remove(body)

    def get_body_by_name(self, name: str) -> "SimulationBody | None":
        """Get a body by name."""
        return self._body_registry.get(name)

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
        if self.viewer:
            self.viewer.close()
            self.viewer = None
        self.is_running = False

    def generate_xml_from_assembly(self, assembly: "AssemblyInterface") -> str:
        """Generate MuJoCo XML from a CodeToCAD Assembly."""
        bodies = []
        for i, part in enumerate(assembly.parts):
            body_info = {
                "name": part.name or f"part_{i}",
                "mass": 1.0,
                "position": (i * 0.1, 0, 0),  # Simple offset
            }
            bodies.append(body_info)

        robot_xml = xml_generation.create_robot_xml(assembly.name or "assembly", bodies)
        return xml_generation.xml_to_string(robot_xml)

    def __del__(self):
        """Cleanup when simulation is destroyed."""
        try:
            self.disconnect()
        except:
            pass  # Ignore errors during cleanup
