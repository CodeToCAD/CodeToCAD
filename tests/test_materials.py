"""
Unit tests for the material system.
"""

import unittest
import tempfile
import os
from pathlib import Path

from codetocad.core.material import Material, MaterialPresets
from codetocad.interfaces.cad.material_interface import MaterialInterface, TextureMaps


class TestMaterialInterface(unittest.TestCase):
    """Test the MaterialInterface functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.material = Material()

    def test_material_creation(self):
        """Test basic material creation."""
        self.assertIsInstance(self.material, MaterialInterface)
        self.assertEqual(self.material.name, "default")
        self.assertEqual(self.material.density, 1000.0)
        self.assertEqual(self.material.friction, 0.5)

    def test_set_physical_properties(self):
        """Test setting physical properties."""
        self.material.set_physical_properties(
            density=7850.0, friction=0.7, restitution=0.1, hardness=6.5
        )

        self.assertEqual(self.material.density, 7850.0)
        self.assertEqual(self.material.friction, 0.7)
        self.assertEqual(self.material.restitution, 0.1)
        self.assertEqual(self.material.hardness, 6.5)

    def test_set_visual_properties(self):
        """Test setting visual properties."""
        self.material.set_visual_properties(
            color=(1.0, 0.0, 0.0, 1.0), metallic=1.0, roughness=0.3, specular=0.9
        )

        self.assertEqual(self.material.color, (1.0, 0.0, 0.0, 1.0))
        self.assertEqual(self.material.metallic, 1.0)
        self.assertEqual(self.material.roughness, 0.3)
        self.assertEqual(self.material.specular, 0.9)

    def test_set_textures(self):
        """Test setting texture paths."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create dummy texture files
            diffuse_path = os.path.join(temp_dir, "diffuse.jpg")
            normal_path = os.path.join(temp_dir, "normal.jpg")

            Path(diffuse_path).touch()
            Path(normal_path).touch()

            self.material.set_textures(diffuse=diffuse_path, normal=normal_path)

            self.assertEqual(self.material.textures.diffuse, diffuse_path)
            self.assertEqual(self.material.textures.normal, normal_path)
            self.assertTrue(self.material.has_textures())

    def test_texture_validation(self):
        """Test texture file validation."""
        # Set non-existent texture paths
        self.material.set_textures(
            diffuse="/non/existent/diffuse.jpg", normal="/non/existent/normal.jpg"
        )

        missing = self.material.validate_textures()
        self.assertEqual(len(missing), 2)
        self.assertIn("diffuse:", missing[0])
        self.assertIn("normal:", missing[1])

    def test_material_copy(self):
        """Test material copying."""
        self.material.set_name("Test Material")
        self.material.set_physical_properties(density=2000.0, friction=0.8)
        self.material.set_visual_properties(color=(0.5, 0.5, 0.5, 1.0))
        self.material.add_tag("test")

        copied = self.material.copy()

        self.assertEqual(copied.name, "Test Material")
        self.assertEqual(copied.density, 2000.0)
        self.assertEqual(copied.friction, 0.8)
        self.assertEqual(copied.color, (0.5, 0.5, 0.5, 1.0))
        self.assertIn("test", copied.tags)

        # Ensure it's a deep copy
        self.assertIsNot(copied, self.material)
        self.assertIsNot(copied.tags, self.material.tags)

    def test_material_serialization(self):
        """Test material to/from dictionary conversion."""
        self.material.set_name("Serialization Test")
        self.material.set_physical_properties(density=1500.0)
        self.material.set_visual_properties(metallic=0.5)
        self.material.add_tag("serializable")

        # Convert to dictionary
        data = self.material.to_dict()

        self.assertEqual(data["name"], "Serialization Test")
        self.assertEqual(data["density"], 1500.0)
        self.assertEqual(data["metallic"], 0.5)
        self.assertIn("serializable", data["tags"])

        # Create new material from dictionary
        new_material = Material()
        new_material.from_dict(data)

        self.assertEqual(new_material.name, "Serialization Test")
        self.assertEqual(new_material.density, 1500.0)
        self.assertEqual(new_material.metallic, 0.5)
        self.assertIn("serializable", new_material.tags)

    def test_custom_properties(self):
        """Test custom property management."""
        self.material.set_custom_property("yield_strength", 250e6)  # Pa
        self.material.set_custom_property("melting_point", 1538)  # °C

        self.assertEqual(self.material.get_custom_property("yield_strength"), 250e6)
        self.assertEqual(self.material.get_custom_property("melting_point"), 1538)
        self.assertIsNone(self.material.get_custom_property("non_existent"))
        self.assertEqual(
            self.material.get_custom_property("non_existent", "default"), "default"
        )


class TestMaterialPresets(unittest.TestCase):
    """Test the material preset system."""

    def test_steel_preset(self):
        """Test steel material preset."""
        steel = MaterialPresets.steel()

        self.assertEqual(steel.name, "Steel")
        self.assertEqual(steel.density, 7850.0)
        self.assertEqual(steel.friction, 0.7)
        self.assertEqual(steel.metallic, 1.0)
        self.assertEqual(steel.category, "metal")
        self.assertIn("metal", steel.tags)
        self.assertIn("structural", steel.tags)

    def test_aluminum_preset(self):
        """Test aluminum material preset."""
        aluminum = MaterialPresets.aluminum()

        self.assertEqual(aluminum.name, "Aluminum")
        self.assertEqual(aluminum.density, 2700.0)
        self.assertEqual(aluminum.metallic, 1.0)
        self.assertEqual(aluminum.category, "metal")
        self.assertIn("lightweight", aluminum.tags)

    def test_wood_preset(self):
        """Test wood material preset."""
        wood = MaterialPresets.wood()

        self.assertEqual(wood.name, "Wood")
        self.assertEqual(wood.density, 600.0)
        self.assertEqual(wood.metallic, 0.0)
        self.assertEqual(wood.category, "organic")
        self.assertIn("organic", wood.tags)

    def test_plastic_preset(self):
        """Test plastic material preset."""
        plastic = MaterialPresets.plastic()

        self.assertEqual(plastic.name, "Plastic")
        self.assertEqual(plastic.density, 1050.0)
        self.assertEqual(plastic.metallic, 0.0)
        self.assertEqual(plastic.category, "polymer")
        self.assertIn("polymer", plastic.tags)

    def test_rubber_preset(self):
        """Test rubber material preset."""
        rubber = MaterialPresets.rubber()

        self.assertEqual(rubber.name, "Rubber")
        self.assertEqual(rubber.density, 1200.0)
        self.assertEqual(rubber.restitution, 0.9)  # High bounciness
        self.assertEqual(rubber.category, "polymer")
        self.assertIn("elastic", rubber.tags)

    def test_glass_preset(self):
        """Test glass material preset."""
        glass = MaterialPresets.glass()

        self.assertEqual(glass.name, "Glass")
        self.assertEqual(glass.density, 2500.0)
        self.assertEqual(glass.transparency, 0.9)
        self.assertEqual(glass.ior, 1.52)
        self.assertEqual(glass.category, "ceramic")
        self.assertIn("transparent", glass.tags)

    def test_concrete_preset(self):
        """Test concrete material preset."""
        concrete = MaterialPresets.concrete()

        self.assertEqual(concrete.name, "Concrete")
        self.assertEqual(concrete.density, 2400.0)
        self.assertEqual(concrete.roughness, 0.95)
        self.assertEqual(concrete.category, "composite")
        self.assertIn("structural", concrete.tags)

    def test_preset_access_via_material_class(self):
        """Test accessing presets via Material.preset."""
        steel = Material.preset.steel()
        aluminum = Material.preset.aluminum()

        self.assertIsInstance(steel, Material)
        self.assertIsInstance(aluminum, Material)
        self.assertEqual(steel.name, "Steel")
        self.assertEqual(aluminum.name, "Aluminum")

    def test_preset_independence(self):
        """Test that preset materials are independent instances."""
        steel1 = Material.preset.steel()
        steel2 = Material.preset.steel()

        # Should be different instances
        self.assertIsNot(steel1, steel2)

        # Modifying one shouldn't affect the other
        steel1.set_name("Modified Steel")
        self.assertEqual(steel2.name, "Steel")

    def test_all_presets_available(self):
        """Test that all expected presets are available."""
        presets = [
            "steel",
            "aluminum",
            "wood",
            "plastic",
            "rubber",
            "glass",
            "concrete",
        ]

        for preset_name in presets:
            self.assertTrue(hasattr(Material.preset, preset_name))
            preset_material = getattr(Material.preset, preset_name)()
            self.assertIsInstance(preset_material, Material)


class TestTextureMaps(unittest.TestCase):
    """Test the TextureMaps data class."""

    def test_texture_maps_creation(self):
        """Test TextureMaps creation and default values."""
        textures = TextureMaps()

        self.assertIsNone(textures.diffuse)
        self.assertIsNone(textures.normal)
        self.assertIsNone(textures.roughness)
        self.assertIsNone(textures.metallic)

    def test_texture_maps_with_values(self):
        """Test TextureMaps with provided values."""
        textures = TextureMaps(
            diffuse="diffuse.jpg", normal="normal.jpg", roughness="roughness.jpg"
        )

        self.assertEqual(textures.diffuse, "diffuse.jpg")
        self.assertEqual(textures.normal, "normal.jpg")
        self.assertEqual(textures.roughness, "roughness.jpg")
        self.assertIsNone(textures.metallic)


if __name__ == "__main__":
    unittest.main()
