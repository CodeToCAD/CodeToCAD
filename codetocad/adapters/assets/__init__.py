"""
Asset management adapters for CodeToCAD.

This package provides adapters for downloading and managing various types of assets
including materials, textures, and 3D models from online sources.
"""

from codetocad.adapters.assets.material_asset_adapter import (
    MaterialAsset,
    MaterialAssetAdapter,
    AmbientCGAdapter,
    PoliigonAdapter,
    MaterialAssetManager,
)

from codetocad.adapters.assets.model_asset_adapter import (
    ModelAsset,
    ModelAssetAdapter,
    ThingiverseAdapter,
    FreeModelAdapter,
    ModelAssetManager,
)

__all__ = [
    # Material assets
    "MaterialAsset",
    "MaterialAssetAdapter",
    "AmbientCGAdapter",
    "PoliigonAdapter",
    "MaterialAssetManager",
    # Model assets
    "ModelAsset",
    "ModelAssetAdapter",
    "ThingiverseAdapter",
    "FreeModelAdapter",
    "ModelAssetManager",
]
