from typing import TYPE_CHECKING
from abc import ABC, abstractmethod, ABCMeta
from enum import Enum
from codetocad.interfaces.cad.part.part_presets import PartPresetsInterface
from codetocad.interfaces.cad.part.part_transform_interface import (
    PartTransformInterface,
)
from codetocad.interfaces.cad.part.part_export_interface import PartExportInterface
from codetocad.interfaces.cad.part.part_boolean_interface import PartBooleanInterface
from codetocad.interfaces.cad.part.part_geometry_interface import PartGeometryInterface
from codetocad.core.dimensions.length_expression import LengthType


class PartCategory(Enum):
    """Enumeration of part categories for physics simulation."""

    RIGID_BODY = "rigid_body"
    SOFT_BODY = "soft_body"
    FLUID = "fluid"
    SENSOR = "sensor"
    ACTUATOR = "actuator"
    PARTICLE_SYSTEM = "particle_system"


if TYPE_CHECKING:
    from codetocad.interfaces.cad.assembly.assembly_interface import AssemblyInterface
    from codetocad.interfaces.cad.material_interface import MaterialInterface


class _PartPresetClassPropertyInterface(ABCMeta):
    @property
    def preset(self):
        return PartPresetsInterface()


class PartInterface(ABC, metaclass=_PartPresetClassPropertyInterface):
    def __init__(self):
        self.member_assemblies: list[AssemblyInterface] = []

        from codetocad.interfaces.cad.sketch.sketch_interface import SketchInterface

        self.sketch: SketchInterface = SketchInterface()
        self.name: str | None = None

        # Physical properties for simulation
        self.category: PartCategory = PartCategory.RIGID_BODY
        self.mass: float | None = None  # kg, None means use density * volume
        self.inertia: tuple[float, float, float] | None = None  # Ixx, Iyy, Izz
        self.material: str = "default"
        self.color: tuple[float, float, float, float] = (0.8, 0.8, 0.8, 1.0)  # RGBA
        self.friction: float = 0.5
        self.restitution: float = 0.1  # bounciness
        self.density: float = 1000.0  # kg/m³
        self.damping: tuple[float, float] = (0.1, 0.1)  # linear, angular

        # Material reference
        self._material_object: "MaterialInterface | None" = None

        # Method group properties
        self.transform = PartTransformInterface(self)
        self.export = PartExportInterface(self)
        self.boolean = PartBooleanInterface(self)
        self.geometry = PartGeometryInterface(self)

    def set_name(self, name: str):
        """Set the part name."""
        self.name = name

    def set_physical_properties(
        self,
        category: PartCategory | None = None,
        mass: float | None = None,
        inertia: tuple[float, float, float] | None = None,
        material: str | None = None,
        color: tuple[float, float, float, float] | None = None,
        friction: float | None = None,
        restitution: float | None = None,
        density: float | None = None,
        damping: tuple[float, float] | None = None,
    ) -> "PartInterface":
        """
        Set physical properties for simulation.

        Args:
            category: Part category (rigid_body, soft_body, etc.)
            mass: Mass in kg (overrides density calculation)
            inertia: Inertia tensor diagonal (Ixx, Iyy, Izz)
            material: Material identifier
            color: RGBA color values (0-1)
            friction: Coefficient of friction
            restitution: Coefficient of restitution (bounciness)
            density: Density in kg/m³ (used if mass not specified)
            damping: Linear and angular damping coefficients

        Returns:
            Self for method chaining
        """
        if category is not None:
            self.category = category
        if mass is not None:
            self.mass = mass
        if inertia is not None:
            self.inertia = inertia
        if material is not None:
            self.material = material
        if color is not None:
            self.color = color
        if friction is not None:
            self.friction = friction
        if restitution is not None:
            self.restitution = restitution
        if density is not None:
            self.density = density
        if damping is not None:
            self.damping = damping

        return self

    def set_material(self, material: "MaterialInterface") -> "PartInterface":
        """
        Set the material for this part, applying both physical and visual properties.

        Args:
            material: Material to apply to this part

        Returns:
            Self for method chaining
        """
        self._material_object = material

        # Apply physical properties from material
        self.density = material.density
        self.friction = material.friction
        self.restitution = material.restitution
        self.material = material.name
        self.color = material.color

        # Store material reference for texture access
        return self

    def get_material(self) -> "MaterialInterface | None":
        """
        Get the material object applied to this part.

        Returns:
            Material object or None if no material is set
        """
        return self._material_object

    def get_effective_mass(self) -> float:
        """
        Get the effective mass of the part.

        Returns mass if set, otherwise calculates from density and volume.
        """
        if self.mass is not None:
            return self.mass

        # Calculate volume and multiply by density
        # This would need to be implemented by concrete classes
        # For now, return a default based on density
        return self.density  # Placeholder - should be density * volume

    @classmethod
    @abstractmethod
    def get_by_name(cls, name: str) -> "PartInterface| None":
        """Get a part by name."""
        ...

    def extrude_sketch(self, _distance: LengthType) -> "PartInterface":
        """Extrude the part's sketch to create a solid."""
        return self

    def copy(self) -> "PartInterface":
        """Create a copy of the part."""
        # This method should be implemented by concrete classes
        # as it requires creating new instances of the specific part type
        raise NotImplementedError("copy must be implemented by concrete classes")

    def hide(self):
        """Hide the part."""
        pass

    def show(self):
        """Show the part."""
        pass

    def delete(self):
        """Delete the part."""
        pass

    def __repr__(self):
        return f"<Part: {self.name or 'Unnamed'}. {self.sketch}>"
