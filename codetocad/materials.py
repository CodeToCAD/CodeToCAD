"""Materials and the MaterialMixin."""

from __future__ import annotations

from .units import (
    DensityKilogramsPerCubicMeter,
    DensityWithUnit,
    WeightKilograms,
    WeightWithUnit,
)
from .vectors import Vec4


class MaterialBase:
    def __init__(
        self,
        name: str,
        mass: WeightWithUnit | None = None,
        density: DensityWithUnit | None = None,
        color_rgba: Vec4 | None = None,
        youngs_modulus: float | None = None,
        poissons_ratio: float | None = None,
    ):
        self.name = name
        self.mass = WeightKilograms(mass) if mass is not None else None
        self.density = (
            DensityKilogramsPerCubicMeter(density) if density is not None else None
        )
        self.color_rgba = color_rgba
        self.youngs_modulus = youngs_modulus
        """Young's modulus in pascals (used by FEA integrations)."""
        self.poissons_ratio = poissons_ratio
        """Poisson's ratio (used by FEA integrations)."""

    def __repr__(self):
        return f"MaterialBase(name={self.name!r})"


class MaterialMixin:
    def _init_material(self):
        self.material: MaterialBase | None = None

    def set_material(self, material: MaterialBase):
        self.material = material
        return self

    def get_density(self) -> DensityKilogramsPerCubicMeter:
        if self.material is None or self.material.density is None:
            raise ValueError("No material with a density has been set on this part")
        return self.material.density

    def get_mass(self) -> WeightKilograms:
        if self.material is None:
            raise ValueError("No material has been set on this part")
        if self.material.mass is not None:
            return self.material.mass
        if self.material.density is not None:
            return WeightKilograms(self.material.density.value * self.get_volume())
        raise ValueError(
            "The material has neither a mass nor a density to derive mass from"
        )


def white_material() -> MaterialBase:
    return MaterialBase("white", color_rgba=Vec4(1.0, 1.0, 1.0, 1.0))


def red_material() -> MaterialBase:
    return MaterialBase("red", color_rgba=Vec4(1.0, 0.0, 0.0, 1.0))


def green_material() -> MaterialBase:
    return MaterialBase("green", color_rgba=Vec4(0.0, 1.0, 0.0, 1.0))


def aluminum_material() -> MaterialBase:
    return MaterialBase(
        "aluminum",
        density="2700 kg/m3",
        color_rgba=Vec4(0.77, 0.77, 0.78, 1.0),
        youngs_modulus=69e9,
        poissons_ratio=0.33,
    )


def steel_material() -> MaterialBase:
    return MaterialBase(
        "steel",
        density="7850 kg/m3",
        color_rgba=Vec4(0.55, 0.57, 0.6, 1.0),
        youngs_modulus=210e9,
        poissons_ratio=0.3,
    )
