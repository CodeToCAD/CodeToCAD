"""
Integration utilities for CAD and simulation systems.

This module provides utilities for converting between CAD objects (Parts, Assemblies)
and simulation objects (Bodies, Joints, etc.), enabling seamless integration between
design and physics simulation.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple
import tempfile
import os
from codetocad.core.dimensions.point import Point

if TYPE_CHECKING:
    from codetocad.interfaces.cad.part.part_interface import PartInterface
    from codetocad.interfaces.cad.assembly.assembly_interface import AssemblyInterface
    from codetocad.interfaces.simulation.simulation_interface import SimulationInterface
    from codetocad.interfaces.simulation.simulation_body_interface import (
        SimulationBodyInterface,
    )


class CADToSimulationConverter:
    """Utility class for converting CAD objects to simulation objects."""

    @staticmethod
    def part_to_simulation_body(
        part: "PartInterface",
        simulation: "SimulationInterface",
        position: Point | Tuple[float, float, float] = (0, 0, 0),
        orientation: Tuple[float, float, float, float] = (0, 0, 0, 1),
        mass: float = 1.0,
        **kwargs,
    ) -> "SimulationBodyInterface":
        """
        Convert a CAD Part to a simulation body.

        Args:
            part: The Part to convert
            simulation: The simulation to add the body to
            position: Initial position of the body
            orientation: Initial orientation as quaternion (x, y, z, w)
            mass: Mass of the body in kg
            **kwargs: Additional simulation-specific parameters

        Returns:
            The created simulation body
        """
        return simulation.add_part(part, position, orientation, mass, **kwargs)

    @staticmethod
    def assembly_to_simulation_bodies(
        assembly: "AssemblyInterface",
        simulation: "SimulationInterface",
        position: Point | Tuple[float, float, float] = (0, 0, 0),
        orientation: Tuple[float, float, float, float] = (0, 0, 0, 1),
        **kwargs,
    ) -> List["SimulationBodyInterface"]:
        """
        Convert a CAD Assembly to simulation bodies.

        Args:
            assembly: The Assembly to convert
            simulation: The simulation to add the bodies to
            position: Base position for the assembly
            orientation: Base orientation as quaternion (x, y, z, w)
            **kwargs: Additional simulation-specific parameters

        Returns:
            List of created simulation bodies
        """
        return simulation.add_assembly(assembly, position, orientation, **kwargs)

    @staticmethod
    def export_part_to_stl(part: "PartInterface", filename: str | None = None) -> str:
        """
        Export a Part to STL file for simulation use.

        Args:
            part: The Part to export
            filename: Output filename (None for temporary file)

        Returns:
            Path to the exported STL file
        """
        if filename is None:
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix=".stl", delete=False) as tmp_file:
                filename = tmp_file.name

        part.export.stl(filename)
        return filename

    @staticmethod
    def export_assembly_to_stl_files(
        assembly: "AssemblyInterface", base_filename: str | None = None
    ) -> List[str]:
        """
        Export an Assembly to multiple STL files.

        Args:
            assembly: The Assembly to export
            base_filename: Base filename pattern (None for temporary files)

        Returns:
            List of paths to exported STL files
        """
        stl_files = []

        for i, part in enumerate(assembly.parts):
            if base_filename:
                filename = f"{base_filename}_part_{i}.stl"
            else:
                filename = None

            stl_path = CADToSimulationConverter.export_part_to_stl(part, filename)
            stl_files.append(stl_path)

        return stl_files

    @staticmethod
    def create_urdf_from_part(
        part: "PartInterface", urdf_filename: str, mass: float = 1.0, **kwargs
    ) -> str:
        """
        Create a URDF file from a CAD Part.

        Args:
            part: The Part to convert
            urdf_filename: Output URDF filename
            mass: Mass of the part in kg
            **kwargs: Additional URDF parameters

        Returns:
            Path to the created URDF file
        """
        # Export part to STL
        stl_filename = urdf_filename.replace(".urdf", ".stl")
        CADToSimulationConverter.export_part_to_stl(part, stl_filename)

        # Create URDF content
        part_name = part.name or "part"
        urdf_content = f"""<?xml version="1.0"?>
<robot name="{part_name}">
  <link name="base_link">
    <visual>
      <geometry>
        <mesh filename="{os.path.basename(stl_filename)}"/>
      </geometry>
      <material name="default">
        <color rgba="0.8 0.8 0.8 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <mesh filename="{os.path.basename(stl_filename)}"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="{mass}"/>
      <inertia ixx="{mass}" ixy="0.0" ixz="0.0" iyy="{mass}" iyz="0.0" izz="{mass}"/>
    </inertial>
  </link>
</robot>"""

        # Write URDF file
        with open(urdf_filename, "w") as f:
            f.write(urdf_content)

        return urdf_filename

    @staticmethod
    def create_urdf_from_assembly(
        assembly: "AssemblyInterface", urdf_filename: str, **kwargs
    ) -> str:
        """
        Create a URDF file from a CAD Assembly.

        Args:
            assembly: The Assembly to convert
            urdf_filename: Output URDF filename
            **kwargs: Additional URDF parameters

        Returns:
            Path to the created URDF file
        """
        assembly_name = assembly.name or "assembly"

        urdf_content = f"""<?xml version="1.0"?>
<robot name="{assembly_name}">
"""

        # Export each part and add to URDF
        for i, part in enumerate(assembly.parts):
            part_name = part.name or f"part_{i}"
            stl_filename = f"{assembly_name}_{part_name}.stl"
            CADToSimulationConverter.export_part_to_stl(part, stl_filename)

            urdf_content += f"""  <link name="{part_name}">
    <visual>
      <geometry>
        <mesh filename="{os.path.basename(stl_filename)}"/>
      </geometry>
      <material name="default">
        <color rgba="0.8 0.8 0.8 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <mesh filename="{os.path.basename(stl_filename)}"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
    </inertial>
  </link>
"""

            # Add fixed joint to previous part (simplified)
            if i > 0:
                prev_part_name = assembly.parts[i - 1].name or f"part_{i-1}"
                urdf_content += f"""  <joint name="joint_{i}" type="fixed">
    <parent link="{prev_part_name}"/>
    <child link="{part_name}"/>
    <origin xyz="0 0 0" rpy="0 0 0"/>
  </joint>
"""

        urdf_content += "</robot>"

        # Write URDF file
        with open(urdf_filename, "w") as f:
            f.write(urdf_content)

        return urdf_filename


class SimulationToCADConverter:
    """Utility class for converting simulation objects back to CAD objects."""

    @staticmethod
    def simulation_body_to_part_data(body: "SimulationBodyInterface") -> Dict[str, Any]:
        """
        Extract CAD-relevant data from a simulation body.

        Args:
            body: The simulation body

        Returns:
            Dictionary containing CAD-relevant data
        """
        return {
            "name": body.name,
            "position": body.get_position(),
            "orientation": body.get_orientation(),
            "mass": body.get_mass(),
            "original_part": getattr(body, "original_part", None),
        }


class SimulationIntegrationHelper:
    """Helper class for simulation integration tasks."""

    @staticmethod
    def setup_simulation_from_assembly(
        assembly: "AssemblyInterface", simulation_type: str = "pybullet", **kwargs
    ) -> Tuple["SimulationInterface", List["SimulationBodyInterface"]]:
        """
        Set up a complete simulation from a CAD Assembly.

        Args:
            assembly: The Assembly to simulate
            simulation_type: Type of simulation ("pybullet" or "mujoco")
            **kwargs: Additional simulation parameters

        Returns:
            Tuple of (simulation, list of bodies)
        """
        if simulation_type.lower() == "pybullet":
            from codetocad.adapters.pybullet import Simulation
        elif simulation_type.lower() == "mujoco":
            from codetocad.adapters.mujoco import Simulation
        else:
            raise ValueError(f"Unsupported simulation type: {simulation_type}")

        # Create and initialize simulation
        sim = Simulation(f"{assembly.name or 'assembly'}_simulation")
        sim.initialize(**kwargs)

        # Add ground plane
        sim.add_ground_plane()

        # Convert assembly to simulation bodies
        bodies = CADToSimulationConverter.assembly_to_simulation_bodies(assembly, sim)

        return sim, bodies

    @staticmethod
    def cleanup_temporary_files(file_paths: List[str]) -> None:
        """
        Clean up temporary files created during conversion.

        Args:
            file_paths: List of file paths to clean up
        """
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            except Exception:
                pass  # Ignore cleanup errors

    @staticmethod
    def validate_simulation_compatibility(
        part: "PartInterface", simulation_type: str
    ) -> bool:
        """
        Validate if a Part is compatible with a simulation type.

        Args:
            part: The Part to validate
            simulation_type: Type of simulation to validate against

        Returns:
            True if compatible, False otherwise
        """
        # Check if part has export capabilities
        if not hasattr(part, "export") or not hasattr(part.export, "stl"):
            return False

        # Additional validation could be added here
        return True
