"""
Interface for physics simulation environments.

This interface defines the core functionality for physics simulation systems,
providing methods to set up simulation scenes, manage time stepping, and
configure simulation parameters.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Optional, Sequence
from codetocad.core.dimensions.length_expression import LengthType
from codetocad.core.dimensions.point import Point

if TYPE_CHECKING:
    from codetocad.interfaces.simulation.simulation_body_interface import (
        SimulationBodyInterface,
    )
    from codetocad.interfaces.cad.part.part_interface import PartInterface
    from codetocad.interfaces.cad.assembly.assembly_interface import AssemblyInterface


class SimulationInterface(ABC):
    """
    Base interface for physics simulation environments.

    This interface provides methods for setting up and managing physics
    simulations, including scene configuration, time stepping, and
    body management.
    """

    def __init__(self):
        """Initialize the simulation interface."""
        self.name: str | None = None
        self.is_running: bool = False
        self.current_time: float = 0.0
        self.time_step: float = 1.0 / 240.0  # Default 240 Hz
        self.gravity: Point = Point(0, 0, -9.81)  # Default Earth gravity
        self.bodies: list["SimulationBodyInterface"] = []

    def set_name(self, name: str):
        """Set the simulation name."""
        self.name = name

    @abstractmethod
    def initialize(self, gui: bool = False, **kwargs) -> None:
        """
        Initialize the simulation environment.

        Args:
            gui: Whether to enable GUI/visualization mode
            **kwargs: Additional simulation-specific parameters
        """
        ...

    @abstractmethod
    def reset(self) -> None:
        """Reset the simulation to initial state."""
        ...

    @abstractmethod
    def step(self, num_steps: int = 1) -> None:
        """
        Step the simulation forward in time.

        Args:
            num_steps: Number of simulation steps to execute
        """
        ...

    @abstractmethod
    def set_gravity(self, gravity: Point | tuple[float, float, float]) -> None:
        """
        Set the gravity vector for the simulation.

        Args:
            gravity: Gravity vector as Point or (x, y, z) tuple
        """
        ...

    @abstractmethod
    def set_time_step(self, time_step: float) -> None:
        """
        Set the simulation time step.

        Args:
            time_step: Time step in seconds
        """
        ...

    @abstractmethod
    def add_ground_plane(
        self,
        position: Point | tuple[float, float, float] = (0, 0, 0),
        normal: Point | tuple[float, float, float] = (0, 0, 1),
        **kwargs,
    ) -> "SimulationBodyInterface":
        """
        Add a ground plane to the simulation.

        Args:
            position: Position of the ground plane
            normal: Normal vector of the ground plane
            **kwargs: Additional ground plane parameters

        Returns:
            The created ground plane body
        """
        ...

    @abstractmethod
    def load_urdf(
        self,
        urdf_path: str,
        position: Point | tuple[float, float, float] = (0, 0, 0),
        orientation: tuple[float, float, float, float] = (0, 0, 0, 1),
        **kwargs,
    ) -> "SimulationBodyInterface":
        """
        Load a URDF file into the simulation.

        Args:
            urdf_path: Path to the URDF file
            position: Initial position as Point or (x, y, z) tuple
            orientation: Initial orientation as quaternion (x, y, z, w)
            **kwargs: Additional loading parameters

        Returns:
            The loaded simulation body
        """
        ...

    @abstractmethod
    def load_stl(
        self,
        stl_path: str,
        position: Point | tuple[float, float, float] = (0, 0, 0),
        orientation: tuple[float, float, float, float] = (0, 0, 0, 1),
        mass: float = 1.0,
        **kwargs,
    ) -> "SimulationBodyInterface":
        """
        Load an STL file as a rigid body.

        Args:
            stl_path: Path to the STL file
            position: Initial position as Point or (x, y, z) tuple
            orientation: Initial orientation as quaternion (x, y, z, w)
            mass: Mass of the body in kg
            **kwargs: Additional loading parameters

        Returns:
            The loaded simulation body
        """
        ...

    @abstractmethod
    def add_part(
        self,
        part: "PartInterface",
        position: Point | tuple[float, float, float] = (0, 0, 0),
        orientation: tuple[float, float, float, float] = (0, 0, 0, 1),
        mass: float = 1.0,
        **kwargs,
    ) -> "SimulationBodyInterface":
        """
        Add a CodeToCAD Part to the simulation.

        Args:
            part: The Part instance to add
            position: Initial position as Point or (x, y, z) tuple
            orientation: Initial orientation as quaternion (x, y, z, w)
            mass: Mass of the body in kg
            **kwargs: Additional parameters

        Returns:
            The created simulation body
        """
        ...

    @abstractmethod
    def add_assembly(
        self,
        assembly: "AssemblyInterface",
        position: Point | tuple[float, float, float] = (0, 0, 0),
        orientation: tuple[float, float, float, float] = (0, 0, 0, 1),
        **kwargs,
    ) -> Sequence["SimulationBodyInterface"]:
        """
        Add a CodeToCAD Assembly to the simulation.

        Args:
            assembly: The Assembly instance to add
            position: Initial position as Point or (x, y, z) tuple
            orientation: Initial orientation as quaternion (x, y, z, w)
            **kwargs: Additional parameters

        Returns:
            List of created simulation bodies
        """
        ...

    @abstractmethod
    def remove_body(self, body: "SimulationBodyInterface") -> None:
        """
        Remove a body from the simulation.

        Args:
            body: The body to remove
        """
        ...

    @abstractmethod
    def get_body_by_name(self, name: str) -> "SimulationBodyInterface | None":
        """
        Get a body by name.

        Args:
            name: Name of the body to find

        Returns:
            The body if found, None otherwise
        """
        ...

    @abstractmethod
    def start(self) -> None:
        """Start the simulation."""
        ...

    @abstractmethod
    def stop(self) -> None:
        """Stop the simulation."""
        ...

    @abstractmethod
    def pause(self) -> None:
        """Pause the simulation."""
        ...

    @abstractmethod
    def resume(self) -> None:
        """Resume the simulation."""
        ...

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from the simulation environment."""
        ...

    def get_current_time(self) -> float:
        """Get the current simulation time."""
        return self.current_time

    def get_time_step(self) -> float:
        """Get the simulation time step."""
        return self.time_step

    def get_gravity(self) -> Point:
        """Get the current gravity vector."""
        return self.gravity

    def get_bodies(self) -> list["SimulationBodyInterface"]:
        """Get all bodies in the simulation."""
        return self.bodies.copy()

    def __len__(self) -> int:
        """Return the number of bodies in the simulation."""
        return len(self.bodies)

    def __repr__(self) -> str:
        return f"<Simulation: {self.name or 'Unnamed'}, Bodies: {len(self.bodies)}>"
