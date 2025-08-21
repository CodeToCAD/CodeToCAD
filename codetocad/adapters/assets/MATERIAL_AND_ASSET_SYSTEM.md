# Material and Asset Management System

## Overview

The CodeToCAD Material and Asset Management System provides comprehensive support for:
- **Material Management**: Physical and visual properties with preset materials
- **Online Asset Integration**: Download materials and 3D models from various sources
- **Seamless Integration**: Automatic application of material properties to simulation
- **Export Support**: Materials included in URDF, SDF, and MuJoCo exports

## 🎨 Material System

### Material Interface

The `MaterialInterface` provides a comprehensive material definition system:

```python
from codetocad.core.material import Material

# Create custom material
material = Material()
material.set_name("Custom Steel")
material.set_physical_properties(
    density=7850.0,  # kg/m³
    friction=0.7,
    restitution=0.1,
    hardness=6.5,
    thermal_conductivity=50.0,
    electrical_conductivity=1.0e6
)
material.set_visual_properties(
    color=(0.7, 0.7, 0.8, 1.0),  # RGBA
    metallic=1.0,
    roughness=0.3,
    specular=0.9
)
```

### Preset Materials

Access common materials through the preset system:

```python
from codetocad.core.material import Material

# Available presets
steel = Material.preset.steel()
aluminum = Material.preset.aluminum()
wood = Material.preset.wood()
plastic = Material.preset.plastic()
rubber = Material.preset.rubber()
glass = Material.preset.glass()
concrete = Material.preset.concrete()
```

### Applying Materials to Parts

```python
from codetocad.core.part import Part
from codetocad.core.material import Material

part = Part()
part.set_material(Material.preset.aluminum())

# Material properties are automatically applied
print(f"Part density: {part.density} kg/m³")
print(f"Part friction: {part.friction}")
print(f"Part color: {part.color}")
```

## 🌐 Online Asset Integration

### Material Asset Adapters

#### AmbientCG (Free, CC0 Materials)

```python
from codetocad.adapters.assets import AmbientCGAdapter, MaterialAssetManager

# Initialize adapter (no API key required)
adapter = AmbientCGAdapter()
manager = MaterialAssetManager()
manager.add_adapter("ambientcg", adapter)

# Search for materials
results = manager.search_all("metal", limit=5)

# Download and use material
for source, assets in results.items():
    if assets:
        asset = assets[0]
        downloaded_files = manager.download_from_adapter(source, asset)
        
        # Create material from downloaded assets
        material = adapter.create_material_from_asset(asset, downloaded_files)
        
        # Apply to part
        part.set_material(material)
```

#### Poliigon (Premium Service)

```python
from codetocad.adapters.assets import PoliigonAdapter

# Requires API key (set in .env file)
adapter = PoliigonAdapter(api_key="your_api_key")
# Implementation depends on Poliigon API documentation
```

### 3D Model Asset Adapters

#### Thingiverse Integration

```python
from codetocad.adapters.assets import ThingiverseAdapter, ModelAssetManager

# Initialize with API key
adapter = ThingiverseAdapter(api_key="your_thingiverse_api_key")
manager = ModelAssetManager()
manager.add_adapter("thingiverse", adapter)

# Search for models
results = manager.search_all("robotic arm", limit=3)

# Download model
for source, assets in results.items():
    if assets:
        asset = assets[0]
        model_file = manager.download_from_adapter(source, asset, format="stl")
        print(f"Downloaded: {model_file}")
```

#### Free Model Sources

```python
from codetocad.adapters.assets import FreeModelAdapter

# No API key required
adapter = FreeModelAdapter()
results = adapter.search("car chassis", limit=5)
```

## ⚙️ Configuration

### Environment Setup

1. Copy `.env.template` to `.env`:
```bash
cp .env.template .env
```

2. Configure API keys in `.env`:
```env
# Material services
POLIIGON_API_KEY=your_poliigon_api_key_here

# 3D model services  
THINGIVERSE_API_KEY=your_thingiverse_api_key_here

# Cache settings
MATERIAL_CACHE_DIR=/path/to/material/cache
MODEL_CACHE_DIR=/path/to/model/cache
MAX_CACHE_SIZE_MB=1000
```

### Programmatic Configuration

```python
from codetocad.cli.config import get_asset_config, get_material_cache_dir

# Get current configuration
config = get_asset_config()
print(f"Material cache: {get_material_cache_dir()}")
print(f"Auto download: {config.auto_download_materials}")
```

## 🚗 Complete Example: Car with Robotic Arm

See `examples/car_with_arm_simulation.py` for a comprehensive demonstration:

```python
# Create parts with materials
chassis = create_car_chassis()
chassis.set_material(Material.preset.steel())

wheel = create_wheel()
wheel.set_material(Material.preset.rubber())

arm_link = create_robotic_arm_link(80)
arm_link.set_material(Material.preset.aluminum())

# Assemble with automatic constraint detection
system = Assembly()
system.add_part(chassis)
system.add_part(wheel)
system.add_part(arm_link)

# Simulate with material properties
sim = Simulation("car_with_arm")
sim.initialize(gui=True)
bodies = sim.add_assembly(system, detect_constraints=True)

# Export with materials
sim.export.urdf("car_with_arm.urdf")
sim.export.xml("car_with_arm.xml", format_type="mujoco")
```

## 📊 Material Properties Reference

### Physical Properties

| Property | Unit | Description | Steel | Aluminum | Wood | Plastic | Rubber |
|----------|------|-------------|-------|----------|------|---------|--------|
| Density | kg/m³ | Mass per volume | 7850 | 2700 | 600 | 1050 | 1200 |
| Friction | - | Surface friction | 0.7 | 0.6 | 0.8 | 0.4 | 1.2 |
| Restitution | - | Bounciness | 0.1 | 0.2 | 0.3 | 0.5 | 0.9 |
| Hardness | Mohs | Surface hardness | 6.5 | 3.0 | 4.0 | 2.5 | 1.5 |

### Visual Properties

| Property | Range | Description |
|----------|-------|-------------|
| Color | (0-1, 0-1, 0-1, 0-1) | RGBA color values |
| Metallic | 0.0-1.0 | Metallic vs dielectric |
| Roughness | 0.0-1.0 | Surface roughness |
| Specular | 0.0-1.0 | Specular reflection |
| Transparency | 0.0-1.0 | Material transparency |
| IOR | 1.0+ | Index of refraction |

## 🔧 API Reference

### MaterialInterface

```python
class MaterialInterface:
    def set_physical_properties(density, friction, restitution, ...)
    def set_visual_properties(color, metallic, roughness, ...)
    def set_textures(diffuse, normal, roughness, ...)
    def copy() -> MaterialInterface
    def to_dict() -> Dict[str, Any]
    def from_dict(data: Dict[str, Any]) -> MaterialInterface
```

### PartInterface Extensions

```python
class PartInterface:
    def set_material(material: MaterialInterface) -> PartInterface
    def get_material() -> MaterialInterface | None
    def get_effective_mass() -> float
```

### Asset Adapters

```python
class MaterialAssetAdapter:
    def search(query: str, category: str = None, limit: int = 10) -> List[MaterialAsset]
    def download(asset: MaterialAsset, temp_dir: str = None) -> Dict[str, str]
    def save(downloaded_files: Dict[str, str], target_dir: str) -> Dict[str, str]

class ModelAssetAdapter:
    def search(query: str, category: str = None, limit: int = 10) -> List[ModelAsset]
    def download(asset: ModelAsset, format: str = "stl", temp_dir: str = None) -> str
    def save(temp_file: str, target_path: str) -> str
```

## 🧪 Testing

Run the material system tests:

```bash
# Run material tests
python -m pytest tests/test_materials.py

# Run asset adapter tests  
python -m pytest tests/test_asset_adapters.py

# Run integration tests
python -m pytest tests/test_material_integration.py
```

## 🚀 Getting Started

1. **Install dependencies**:
```bash
pip install requests
```

2. **Set up API keys** (optional):
```bash
cp .env.template .env
# Edit .env with your API keys
```

3. **Run the example**:
```bash
python examples/car_with_arm_simulation.py
```

4. **Use in your project**:
```python
from codetocad.core.material import Material
from codetocad.core.part import Part

part = Part()
part.set_material(Material.preset.steel())
```

## 🔗 Free Material Sources

- **ambientCG**: https://ambientcg.com/ (CC0 materials)
- **Poly Haven**: https://polyhaven.com/ (CC0 materials)  
- **Texture Haven**: https://texturehaven.com/ (CC0 materials)

## 🔗 Free 3D Model Sources

- **Printables**: https://www.printables.com/
- **MyMiniFactory**: https://www.myminifactory.com/
- **Cults3D**: https://cults3d.com/
- **GrabCAD**: https://grabcad.com/

## 📝 Notes

- API keys are optional - the system works with free sources
- Materials are automatically applied to simulation physics
- Texture maps are preserved in exports when available
- Cache directories are automatically managed
- Network failures are handled gracefully with fallbacks
