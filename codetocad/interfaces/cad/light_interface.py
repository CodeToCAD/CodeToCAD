"""
Light interface for 3D scenes and simulations.

This module defines the interface for lights that can be used in assemblies
and simulations for realistic rendering and visualization.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple
from codetocad.core.dimensions.point import Point


class LightType(Enum):
    """Light type enumeration."""

    DIRECTIONAL = "directional"
    POINT = "point"
    SPOT = "spot"
    AREA = "area"
    AMBIENT = "ambient"


class LightInterface(ABC):
    """Interface for 3D lights."""

    def __init__(self):
        self.name: str | None = None
        self.position: Point = Point(0, 0, 5)
        self.direction: Point = Point(0, 0, -1)

        # Light parameters
        self.light_type: LightType = LightType.POINT
        self.intensity: float = 1.0
        self.color: Tuple[float, float, float] = (1.0, 1.0, 1.0)  # RGB
        self.enabled: bool = True

        # Attenuation (for point and spot lights)
        self.constant_attenuation: float = 1.0
        self.linear_attenuation: float = 0.0
        self.quadratic_attenuation: float = 0.0

        # Spot light parameters
        self.spot_inner_angle: float = 30.0  # degrees
        self.spot_outer_angle: float = 45.0  # degrees
        self.spot_falloff: float = 1.0

        # Area light parameters
        self.area_width: float = 1.0
        self.area_height: float = 1.0

        # Shadow parameters
        self.cast_shadows: bool = True
        self.shadow_resolution: int = 1024
        self.shadow_bias: float = 0.001

    def set_name(self, name: str) -> "LightInterface":
        """Set the light name."""
        self.name = name
        return self

    def set_position(
        self, position: Point | Tuple[float, float, float]
    ) -> "LightInterface":
        """Set light position."""
        if isinstance(position, tuple):
            self.position = Point(position[0], position[1], position[2])
        else:
            self.position = position
        return self

    def set_direction(
        self, direction: Point | Tuple[float, float, float]
    ) -> "LightInterface":
        """Set light direction (for directional and spot lights)."""
        if isinstance(direction, tuple):
            self.direction = Point(direction[0], direction[1], direction[2])
        else:
            self.direction = direction
        return self

    def set_light_type(self, light_type: LightType) -> "LightInterface":
        """Set light type."""
        self.light_type = light_type
        return self

    def set_intensity(self, intensity: float) -> "LightInterface":
        """Set light intensity."""
        self.intensity = intensity
        return self

    def set_color(self, color: Tuple[float, float, float]) -> "LightInterface":
        """Set light color (RGB values 0-1)."""
        self.color = color
        return self

    def set_enabled(self, enabled: bool) -> "LightInterface":
        """Enable or disable the light."""
        self.enabled = enabled
        return self

    def set_attenuation(
        self, constant: float = 1.0, linear: float = 0.0, quadratic: float = 0.0
    ) -> "LightInterface":
        """Set light attenuation parameters."""
        self.constant_attenuation = constant
        self.linear_attenuation = linear
        self.quadratic_attenuation = quadratic
        return self

    def set_spot_parameters(
        self, inner_angle: float, outer_angle: float, falloff: float = 1.0
    ) -> "LightInterface":
        """Set spot light parameters."""
        self.spot_inner_angle = inner_angle
        self.spot_outer_angle = outer_angle
        self.spot_falloff = falloff
        return self

    def set_area_size(self, width: float, height: float) -> "LightInterface":
        """Set area light size."""
        self.area_width = width
        self.area_height = height
        return self

    def set_shadow_parameters(
        self, cast_shadows: bool = True, resolution: int = 1024, bias: float = 0.001
    ) -> "LightInterface":
        """Set shadow parameters."""
        self.cast_shadows = cast_shadows
        self.shadow_resolution = resolution
        self.shadow_bias = bias
        return self

    def create_directional_light(
        self,
        direction: Point | Tuple[float, float, float],
        intensity: float = 1.0,
        color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
    ) -> "LightInterface":
        """Configure as directional light."""
        self.light_type = LightType.DIRECTIONAL
        self.set_direction(direction)
        self.set_intensity(intensity)
        self.set_color(color)
        return self

    def create_point_light(
        self,
        position: Point | Tuple[float, float, float],
        intensity: float = 1.0,
        color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
        attenuation: Tuple[float, float, float] = (1.0, 0.0, 0.0),
    ) -> "LightInterface":
        """Configure as point light."""
        self.light_type = LightType.POINT
        self.set_position(position)
        self.set_intensity(intensity)
        self.set_color(color)
        self.set_attenuation(*attenuation)
        return self

    def create_spot_light(
        self,
        position: Point | Tuple[float, float, float],
        direction: Point | Tuple[float, float, float],
        inner_angle: float = 30.0,
        outer_angle: float = 45.0,
        intensity: float = 1.0,
        color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
    ) -> "LightInterface":
        """Configure as spot light."""
        self.light_type = LightType.SPOT
        self.set_position(position)
        self.set_direction(direction)
        self.set_spot_parameters(inner_angle, outer_angle)
        self.set_intensity(intensity)
        self.set_color(color)
        return self

    def create_area_light(
        self,
        position: Point | Tuple[float, float, float],
        width: float = 1.0,
        height: float = 1.0,
        intensity: float = 1.0,
        color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
    ) -> "LightInterface":
        """Configure as area light."""
        self.light_type = LightType.AREA
        self.set_position(position)
        self.set_area_size(width, height)
        self.set_intensity(intensity)
        self.set_color(color)
        return self

    @abstractmethod
    def get_illumination_at_point(
        self, point: Point
    ) -> Tuple[float, Tuple[float, float, float]]:
        """
        Calculate illumination at a given point.

        Args:
            point: Point to calculate illumination for

        Returns:
            Tuple of (intensity, color) at the point
        """
        pass

    @abstractmethod
    def get_shadow_factor(self, point: Point, scene_objects: list) -> float:
        """
        Calculate shadow factor at a given point.

        Args:
            point: Point to calculate shadow for
            scene_objects: List of objects that can cast shadows

        Returns:
            Shadow factor (0 = full shadow, 1 = no shadow)
        """
        pass

    def __repr__(self) -> str:
        return f"<Light: {self.name or 'Unnamed'}, Type: {self.light_type.value}, Intensity: {self.intensity}>"
