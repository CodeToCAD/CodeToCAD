"""
Material interface for CodeToCAD.

This module defines the interface for materials that can be applied to parts,
providing both physical properties for simulation and visual characteristics for rendering.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Tuple
from pathlib import Path
from dataclasses import dataclass


@dataclass
class TextureMaps:
    """Container for texture map file paths."""

    diffuse: Optional[str] = None  # Base color/albedo map
    normal: Optional[str] = None  # Normal/bump map
    roughness: Optional[str] = None  # Surface roughness map
    metallic: Optional[str] = None  # Metallic map
    specular: Optional[str] = None  # Specular map
    emission: Optional[str] = None  # Emission/glow map
    displacement: Optional[str] = None  # Height/displacement map
    ambient_occlusion: Optional[str] = None  # AO map


class MaterialInterface(ABC):
    """Interface for materials with physical and visual properties."""

    def __init__(self):
        # Physical properties
        self.name: str = "default"
        self.density: float = 1000.0  # kg/m³
        self.friction: float = 0.5
        self.restitution: float = 0.1  # bounciness
        self.hardness: float = 5.0  # Mohs scale (1-10)
        self.thermal_conductivity: float = 1.0  # W/(m·K)
        self.electrical_conductivity: float = 0.0  # S/m

        # Visual properties
        self.color: Tuple[float, float, float, float] = (0.8, 0.8, 0.8, 1.0)  # RGBA
        self.metallic: float = 0.0  # 0.0 = dielectric, 1.0 = metallic
        self.roughness: float = 0.5  # 0.0 = mirror, 1.0 = completely rough
        self.specular: float = 0.5  # Specular reflection intensity
        self.emission: Tuple[float, float, float] = (0.0, 0.0, 0.0)  # RGB emission
        self.transparency: float = 0.0  # 0.0 = opaque, 1.0 = transparent
        self.ior: float = 1.5  # Index of refraction

        # Texture maps
        self.textures: TextureMaps = TextureMaps()

        # Additional properties
        self.category: str = "generic"
        self.description: str = ""
        self.tags: list[str] = []
        self.custom_properties: Dict[str, Any] = {}

    def set_name(self, name: str) -> "MaterialInterface":
        """Set the material name."""
        self.name = name
        return self

    def set_physical_properties(
        self,
        density: Optional[float] = None,
        friction: Optional[float] = None,
        restitution: Optional[float] = None,
        hardness: Optional[float] = None,
        thermal_conductivity: Optional[float] = None,
        electrical_conductivity: Optional[float] = None,
    ) -> "MaterialInterface":
        """Set physical properties of the material."""
        if density is not None:
            self.density = density
        if friction is not None:
            self.friction = friction
        if restitution is not None:
            self.restitution = restitution
        if hardness is not None:
            self.hardness = hardness
        if thermal_conductivity is not None:
            self.thermal_conductivity = thermal_conductivity
        if electrical_conductivity is not None:
            self.electrical_conductivity = electrical_conductivity
        return self

    def set_visual_properties(
        self,
        color: Optional[Tuple[float, float, float, float]] = None,
        metallic: Optional[float] = None,
        roughness: Optional[float] = None,
        specular: Optional[float] = None,
        emission: Optional[Tuple[float, float, float]] = None,
        transparency: Optional[float] = None,
        ior: Optional[float] = None,
    ) -> "MaterialInterface":
        """Set visual properties of the material."""
        if color is not None:
            self.color = color
        if metallic is not None:
            self.metallic = metallic
        if roughness is not None:
            self.roughness = roughness
        if specular is not None:
            self.specular = specular
        if emission is not None:
            self.emission = emission
        if transparency is not None:
            self.transparency = transparency
        if ior is not None:
            self.ior = ior
        return self

    def set_textures(
        self,
        diffuse: Optional[str] = None,
        normal: Optional[str] = None,
        roughness: Optional[str] = None,
        metallic: Optional[str] = None,
        specular: Optional[str] = None,
        emission: Optional[str] = None,
        displacement: Optional[str] = None,
        ambient_occlusion: Optional[str] = None,
    ) -> "MaterialInterface":
        """Set texture map file paths."""
        if diffuse is not None:
            self.textures.diffuse = diffuse
        if normal is not None:
            self.textures.normal = normal
        if roughness is not None:
            self.textures.roughness = roughness
        if metallic is not None:
            self.textures.metallic = metallic
        if specular is not None:
            self.textures.specular = specular
        if emission is not None:
            self.textures.emission = emission
        if displacement is not None:
            self.textures.displacement = displacement
        if ambient_occlusion is not None:
            self.textures.ambient_occlusion = ambient_occlusion
        return self

    def set_category(self, category: str) -> "MaterialInterface":
        """Set the material category."""
        self.category = category
        return self

    def set_description(self, description: str) -> "MaterialInterface":
        """Set the material description."""
        self.description = description
        return self

    def add_tag(self, tag: str) -> "MaterialInterface":
        """Add a tag to the material."""
        if tag not in self.tags:
            self.tags.append(tag)
        return self

    def set_custom_property(self, key: str, value: Any) -> "MaterialInterface":
        """Set a custom property."""
        self.custom_properties[key] = value
        return self

    def get_custom_property(self, key: str, default: Any = None) -> Any:
        """Get a custom property."""
        return self.custom_properties.get(key, default)

    def has_textures(self) -> bool:
        """Check if the material has any texture maps."""
        return any(
            [
                self.textures.diffuse,
                self.textures.normal,
                self.textures.roughness,
                self.textures.metallic,
                self.textures.specular,
                self.textures.emission,
                self.textures.displacement,
                self.textures.ambient_occlusion,
            ]
        )

    def get_texture_paths(self) -> list[str]:
        """Get all texture file paths."""
        paths = []
        for texture_path in [
            self.textures.diffuse,
            self.textures.normal,
            self.textures.roughness,
            self.textures.metallic,
            self.textures.specular,
            self.textures.emission,
            self.textures.displacement,
            self.textures.ambient_occlusion,
        ]:
            if texture_path and Path(texture_path).exists():
                paths.append(texture_path)
        return paths

    def validate_textures(self) -> list[str]:
        """Validate texture file paths and return list of missing files."""
        missing = []
        for attr_name, texture_path in [
            ("diffuse", self.textures.diffuse),
            ("normal", self.textures.normal),
            ("roughness", self.textures.roughness),
            ("metallic", self.textures.metallic),
            ("specular", self.textures.specular),
            ("emission", self.textures.emission),
            ("displacement", self.textures.displacement),
            ("ambient_occlusion", self.textures.ambient_occlusion),
        ]:
            if texture_path and not Path(texture_path).exists():
                missing.append(f"{attr_name}: {texture_path}")
        return missing

    @abstractmethod
    def copy(self) -> "MaterialInterface":
        """Create a copy of the material."""
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert material to dictionary representation."""
        pass

    @abstractmethod
    def from_dict(self, data: Dict[str, Any]) -> "MaterialInterface":
        """Load material from dictionary representation."""
        pass

    def __repr__(self) -> str:
        return f"<Material: {self.name}, Category: {self.category}, Density: {self.density} kg/m³>"
