"""
Material implementation with preset materials.
"""

import copy
from typing import Dict, Any
from abc import ABCMeta
from codetocad.interfaces.cad.material_interface import MaterialInterface, TextureMaps


class _MaterialPresetClassProperty(ABCMeta):
    """Metaclass to provide Material.preset class property."""

    @property
    def preset(cls):
        """Access to material presets."""
        return MaterialPresets()


class Material(MaterialInterface, metaclass=_MaterialPresetClassProperty):
    """Concrete implementation of MaterialInterface."""

    def copy(self) -> "Material":
        """Create a copy of the material."""
        new_material = Material()

        # Copy all attributes
        new_material.name = self.name
        new_material.density = self.density
        new_material.friction = self.friction
        new_material.restitution = self.restitution
        new_material.hardness = self.hardness
        new_material.thermal_conductivity = self.thermal_conductivity
        new_material.electrical_conductivity = self.electrical_conductivity

        new_material.color = self.color
        new_material.metallic = self.metallic
        new_material.roughness = self.roughness
        new_material.specular = self.specular
        new_material.emission = self.emission
        new_material.transparency = self.transparency
        new_material.ior = self.ior

        new_material.textures = copy.deepcopy(self.textures)
        new_material.category = self.category
        new_material.description = self.description
        new_material.tags = self.tags.copy()
        new_material.custom_properties = self.custom_properties.copy()

        return new_material

    def to_dict(self) -> Dict[str, Any]:
        """Convert material to dictionary representation."""
        return {
            "name": self.name,
            "density": self.density,
            "friction": self.friction,
            "restitution": self.restitution,
            "hardness": self.hardness,
            "thermal_conductivity": self.thermal_conductivity,
            "electrical_conductivity": self.electrical_conductivity,
            "color": self.color,
            "metallic": self.metallic,
            "roughness": self.roughness,
            "specular": self.specular,
            "emission": self.emission,
            "transparency": self.transparency,
            "ior": self.ior,
            "textures": {
                "diffuse": self.textures.diffuse,
                "normal": self.textures.normal,
                "roughness": self.textures.roughness,
                "metallic": self.textures.metallic,
                "specular": self.textures.specular,
                "emission": self.textures.emission,
                "displacement": self.textures.displacement,
                "ambient_occlusion": self.textures.ambient_occlusion,
            },
            "category": self.category,
            "description": self.description,
            "tags": self.tags,
            "custom_properties": self.custom_properties,
        }

    def from_dict(self, data: Dict[str, Any]) -> "Material":
        """Load material from dictionary representation."""
        self.name = data.get("name", "default")
        self.density = data.get("density", 1000.0)
        self.friction = data.get("friction", 0.5)
        self.restitution = data.get("restitution", 0.1)
        self.hardness = data.get("hardness", 5.0)
        self.thermal_conductivity = data.get("thermal_conductivity", 1.0)
        self.electrical_conductivity = data.get("electrical_conductivity", 0.0)

        self.color = tuple(data.get("color", (0.8, 0.8, 0.8, 1.0)))
        self.metallic = data.get("metallic", 0.0)
        self.roughness = data.get("roughness", 0.5)
        self.specular = data.get("specular", 0.5)
        self.emission = tuple(data.get("emission", (0.0, 0.0, 0.0)))
        self.transparency = data.get("transparency", 0.0)
        self.ior = data.get("ior", 1.5)

        textures_data = data.get("textures", {})
        self.textures = TextureMaps(
            diffuse=textures_data.get("diffuse"),
            normal=textures_data.get("normal"),
            roughness=textures_data.get("roughness"),
            metallic=textures_data.get("metallic"),
            specular=textures_data.get("specular"),
            emission=textures_data.get("emission"),
            displacement=textures_data.get("displacement"),
            ambient_occlusion=textures_data.get("ambient_occlusion"),
        )

        self.category = data.get("category", "generic")
        self.description = data.get("description", "")
        self.tags = data.get("tags", [])
        self.custom_properties = data.get("custom_properties", {})

        return self


class MaterialPresets:
    """Preset materials for common use cases."""

    @staticmethod
    def steel() -> Material:
        """Create a steel material."""
        material = Material()
        material.set_name("Steel")
        material.set_physical_properties(
            density=7850.0,  # kg/m³
            friction=0.7,
            restitution=0.1,
            hardness=6.5,
            thermal_conductivity=50.0,
            electrical_conductivity=1.0e6,
        )
        material.set_visual_properties(
            color=(0.7, 0.7, 0.8, 1.0), metallic=1.0, roughness=0.3, specular=0.9
        )
        material.set_category("metal")
        material.set_description("High-strength structural steel")
        material.add_tag("metal").add_tag("structural").add_tag("conductive")
        return material

    @staticmethod
    def aluminum() -> Material:
        """Create an aluminum material."""
        material = Material()
        material.set_name("Aluminum")
        material.set_physical_properties(
            density=2700.0,  # kg/m³
            friction=0.6,
            restitution=0.2,
            hardness=3.0,
            thermal_conductivity=237.0,
            electrical_conductivity=3.5e7,
        )
        material.set_visual_properties(
            color=(0.9, 0.9, 0.95, 1.0), metallic=1.0, roughness=0.2, specular=0.95
        )
        material.set_category("metal")
        material.set_description("Lightweight aluminum alloy")
        material.add_tag("metal").add_tag("lightweight").add_tag("conductive")
        return material

    @staticmethod
    def wood() -> Material:
        """Create a wood material."""
        material = Material()
        material.set_name("Wood")
        material.set_physical_properties(
            density=600.0,  # kg/m³ (oak)
            friction=0.8,
            restitution=0.3,
            hardness=4.0,
            thermal_conductivity=0.17,
            electrical_conductivity=1e-16,
        )
        material.set_visual_properties(
            color=(0.6, 0.4, 0.2, 1.0), metallic=0.0, roughness=0.8, specular=0.1
        )
        material.set_category("organic")
        material.set_description("Natural hardwood")
        material.add_tag("organic").add_tag("insulator").add_tag("renewable")
        return material

    @staticmethod
    def plastic() -> Material:
        """Create a plastic material (ABS)."""
        material = Material()
        material.set_name("Plastic")
        material.set_physical_properties(
            density=1050.0,  # kg/m³ (ABS)
            friction=0.4,
            restitution=0.5,
            hardness=2.5,
            thermal_conductivity=0.2,
            electrical_conductivity=1e-16,
        )
        material.set_visual_properties(
            color=(0.2, 0.2, 0.8, 1.0), metallic=0.0, roughness=0.6, specular=0.3
        )
        material.set_category("polymer")
        material.set_description("ABS thermoplastic")
        material.add_tag("polymer").add_tag("insulator").add_tag("moldable")
        return material

    @staticmethod
    def rubber() -> Material:
        """Create a rubber material."""
        material = Material()
        material.set_name("Rubber")
        material.set_physical_properties(
            density=1200.0,  # kg/m³
            friction=1.2,
            restitution=0.9,
            hardness=1.5,
            thermal_conductivity=0.16,
            electrical_conductivity=1e-15,
        )
        material.set_visual_properties(
            color=(0.1, 0.1, 0.1, 1.0), metallic=0.0, roughness=0.9, specular=0.05
        )
        material.set_category("polymer")
        material.set_description("Natural rubber compound")
        material.add_tag("polymer").add_tag("elastic").add_tag("insulator")
        return material

    @staticmethod
    def glass() -> Material:
        """Create a glass material."""
        material = Material()
        material.set_name("Glass")
        material.set_physical_properties(
            density=2500.0,  # kg/m³
            friction=0.3,
            restitution=0.1,
            hardness=6.0,
            thermal_conductivity=1.0,
            electrical_conductivity=1e-15,
        )
        material.set_visual_properties(
            color=(0.9, 0.9, 1.0, 0.1),
            metallic=0.0,
            roughness=0.0,
            specular=1.0,
            transparency=0.9,
            ior=1.52,
        )
        material.set_category("ceramic")
        material.set_description("Transparent soda-lime glass")
        material.add_tag("ceramic").add_tag("transparent").add_tag("brittle")
        return material

    @staticmethod
    def concrete() -> Material:
        """Create a concrete material."""
        material = Material()
        material.set_name("Concrete")
        material.set_physical_properties(
            density=2400.0,  # kg/m³
            friction=0.9,
            restitution=0.05,
            hardness=4.5,
            thermal_conductivity=1.7,
            electrical_conductivity=1e-6,
        )
        material.set_visual_properties(
            color=(0.6, 0.6, 0.6, 1.0), metallic=0.0, roughness=0.95, specular=0.05
        )
        material.set_category("composite")
        material.set_description("Portland cement concrete")
        material.add_tag("composite").add_tag("structural").add_tag("durable")
        return material


# Material.preset is now available via the metaclass
