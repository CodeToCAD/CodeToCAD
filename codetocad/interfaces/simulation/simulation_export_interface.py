"""
Simulation export interface.

This module defines the interface for exporting simulation models and states
to various formats like URDF, SDF, XML, etc.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class SimulationExportInterface(ABC):
    """Interface for simulation export functionality."""

    def __init__(self, simulation):
        self.simulation = simulation

    @abstractmethod
    def urdf(
        self,
        filename: str,
        include_visuals: bool = True,
        include_collisions: bool = True,
        include_inertials: bool = True,
        **kwargs,
    ) -> str:
        """
        Export simulation to URDF format.

        Args:
            filename: Output filename
            include_visuals: Include visual elements
            include_collisions: Include collision elements
            include_inertials: Include inertial properties
            **kwargs: Additional export options

        Returns:
            Path to exported file
        """
        pass

    @abstractmethod
    def sdf(
        self,
        filename: str,
        version: str = "1.7",
        include_physics: bool = True,
        **kwargs,
    ) -> str:
        """
        Export simulation to SDF (Simulation Description Format) for Gazebo.

        Args:
            filename: Output filename
            version: SDF version
            include_physics: Include physics parameters
            **kwargs: Additional export options

        Returns:
            Path to exported file
        """
        pass

    @abstractmethod
    def xml(self, filename: str, format_type: str = "mujoco", **kwargs) -> str:
        """
        Export simulation to XML format.

        Args:
            filename: Output filename
            format_type: XML format type ("mujoco", "generic")
            **kwargs: Additional export options

        Returns:
            Path to exported file
        """
        pass

    @abstractmethod
    def mjcf(self, filename: str, **kwargs) -> str:
        """
        Export simulation to MuJoCo MJCF XML format.

        Args:
            filename: Output filename
            **kwargs: Additional export options

        Returns:
            Path to exported file
        """
        pass

    @abstractmethod
    def state(
        self,
        filename: str,
        format: str = "json",
        include_velocities: bool = True,
        include_forces: bool = False,
        **kwargs,
    ) -> str:
        """
        Export current simulation state.

        Args:
            filename: Output filename
            format: Export format ("json", "yaml", "binary")
            include_velocities: Include velocity data
            include_forces: Include force data
            **kwargs: Additional export options

        Returns:
            Path to exported file
        """
        pass

    @abstractmethod
    def trajectory(
        self,
        filename: str,
        format: str = "csv",
        bodies: list | None = None,
        **kwargs,
    ) -> str:
        """
        Export trajectory data.

        Args:
            filename: Output filename
            format: Export format ("csv", "json", "hdf5")
            bodies: List of bodies to export (None for all)
            **kwargs: Additional export options

        Returns:
            Path to exported file
        """
        pass

    @abstractmethod
    def scene(
        self,
        filename: str,
        include_cameras: bool = True,
        include_lights: bool = True,
        **kwargs,
    ) -> str:
        """
        Export complete scene description.

        Args:
            filename: Output filename
            include_cameras: Include camera definitions
            include_lights: Include light definitions
            **kwargs: Additional export options

        Returns:
            Path to exported file
        """
        pass

    def get_supported_formats(self) -> dict[str, list[str]]:
        """
        Get supported export formats.

        Returns:
            Dictionary mapping export types to supported formats
        """
        return {
            "model": ["urdf", "sdf", "xml"],
            "state": ["json", "yaml", "binary"],
            "trajectory": ["csv", "json", "hdf5"],
            "scene": ["json", "xml"],
        }
