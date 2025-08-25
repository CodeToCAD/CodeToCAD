"""
Camera interface for 3D scenes and simulations.

This module defines the interface for cameras that can be used in assemblies
and simulations for rendering and computer vision applications.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple
from codetocad.core.dimensions.point import Point


class CameraType(Enum):
    """Camera type enumeration."""

    PERSPECTIVE = "perspective"
    ORTHOGRAPHIC = "orthographic"
    FISHEYE = "fisheye"


class CameraInterface(ABC):
    """Interface for 3D cameras."""

    def __init__(self):
        self.name: str | None = None
        self.position: Point = Point(0, 0, 5)
        self.target: Point = Point(0, 0, 0)
        self.up_vector: Point = Point(0, 0, 1)

        # Camera parameters
        self.camera_type: CameraType = CameraType.PERSPECTIVE
        self.field_of_view: float = 45.0  # degrees
        self.aspect_ratio: float = 16.0 / 9.0
        self.near_plane: float = 0.1
        self.far_plane: float = 1000.0

        # Resolution
        self.resolution: tuple[int, int] = (1920, 1080)

        # Orthographic parameters (used when camera_type is ORTHOGRAPHIC)
        self.orthographic_scale: float = 10.0

        # Fisheye parameters (used when camera_type is FISHEYE)
        self.fisheye_strength: float = 1.0

    def set_name(self, name: str) -> "CameraInterface":
        """Set the camera name."""
        self.name = name
        return self

    def set_position(
        self, position: Point | tuple[float, float, float]
    ) -> "CameraInterface":
        """Set camera position."""
        if isinstance(position, tuple):
            self.position = Point(position[0], position[1], position[2])
        else:
            self.position = position
        return self

    def set_target(
        self, target: Point | tuple[float, float, float]
    ) -> "CameraInterface":
        """Set camera target (look-at point)."""
        if isinstance(target, tuple):
            self.target = Point(target[0], target[1], target[2])
        else:
            self.target = target
        return self

    def set_up_vector(
        self, up: Point | tuple[float, float, float]
    ) -> "CameraInterface":
        """Set camera up vector."""
        if isinstance(up, tuple):
            self.up_vector = Point(up[0], up[1], up[2])
        else:
            self.up_vector = up
        return self

    def set_field_of_view(self, fov: float) -> "CameraInterface":
        """Set field of view in degrees."""
        self.field_of_view = fov
        return self

    def set_aspect_ratio(self, aspect: float) -> "CameraInterface":
        """Set aspect ratio (width/height)."""
        self.aspect_ratio = aspect
        return self

    def set_resolution(self, width: int, height: int) -> "CameraInterface":
        """Set camera resolution."""
        self.resolution = (width, height)
        self.aspect_ratio = width / height
        return self

    def set_clipping_planes(self, near: float, far: float) -> "CameraInterface":
        """Set near and far clipping planes."""
        self.near_plane = near
        self.far_plane = far
        return self

    def set_camera_type(self, camera_type: CameraType) -> "CameraInterface":
        """Set camera type."""
        self.camera_type = camera_type
        return self

    def set_orthographic_scale(self, scale: float) -> "CameraInterface":
        """Set orthographic scale (for orthographic cameras)."""
        self.orthographic_scale = scale
        return self

    def set_fisheye_strength(self, strength: float) -> "CameraInterface":
        """Set fisheye distortion strength."""
        self.fisheye_strength = strength
        return self

    def look_at(
        self,
        position: Point | tuple[float, float, float],
        target: Point | tuple[float, float, float],
        up: Point | tuple[float, float, float] = (0, 0, 1),
    ) -> "CameraInterface":
        """Set camera position, target, and up vector in one call."""
        self.set_position(position)
        self.set_target(target)
        self.set_up_vector(up)
        return self

    def get_view_matrix(self) -> tuple[tuple[float, ...], ...]:
        """
        Get the view matrix for this camera.

        Returns:
            4x4 view matrix as tuple of tuples
        """
        # This would be implemented by concrete classes
        # Return identity matrix as placeholder
        return ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))

    def get_projection_matrix(self) -> tuple[tuple[float, ...], ...]:
        """
        Get the projection matrix for this camera.

        Returns:
            4x4 projection matrix as tuple of tuples
        """
        # This would be implemented by concrete classes
        # Return identity matrix as placeholder
        return ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))

    @abstractmethod
    def render(self, output_path: str | None = None) -> bytes | None:
        """
        Render the scene from this camera's perspective.

        Args:
            output_path: Optional path to save the rendered image

        Returns:
            Image data as bytes if output_path is None, otherwise None
        """
        pass

    @abstractmethod
    def get_ray(self, screen_x: float, screen_y: float) -> tuple[Point, Point]:
        """
        Get a ray from the camera through a screen coordinate.

        Args:
            screen_x: Screen X coordinate (0-1)
            screen_y: Screen Y coordinate (0-1)

        Returns:
            Tuple of (ray_origin, ray_direction)
        """
        pass

    def __repr__(self) -> str:
        return f"<Camera: {self.name or 'Unnamed'}, Type: {self.camera_type.value}, FOV: {self.field_of_view}°>"
