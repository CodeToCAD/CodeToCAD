# CodeToCAD Configuration System

This document describes the programmatic configuration system for CodeToCAD adapters and settings.

## Overview

CodeToCAD uses a JSON-based configuration system stored in `~/.codetocad/config.json`. Instead of manually editing environment files, you can use the programmatic configuration methods to set up adapters and customize behavior.

## Configuration Methods

### Blender Adapter Configuration

```python
from codetocad.cli.config import (
    set_blender_executable_path,
    set_blender_gpu_rendering
)

# Set path to Blender executable
set_blender_executable_path("/Applications/Blender.app/Contents/MacOS/Blender")

# Enable GPU rendering for faster performance
set_blender_gpu_rendering(True)
```

### PyBullet Simulation Configuration

```python
from codetocad.cli.config import (
    set_pybullet_gui_enabled,
    set_pybullet_time_step,
    set_pybullet_gravity
)

# Enable GUI by default for PyBullet simulations
set_pybullet_gui_enabled(True)

# Set simulation time step (smaller = more accurate, slower)
set_pybullet_time_step(0.004166667)  # ~240 Hz

# Set gravity vector (x, y, z)
set_pybullet_gravity(0, 0, -9.81)  # Standard Earth gravity
```

### MuJoCo Simulation Configuration

```python
from codetocad.cli.config import (
    set_mujoco_viewer_enabled,
    set_mujoco_time_step
)

# Enable viewer by default for MuJoCo simulations
set_mujoco_viewer_enabled(True)

# Set simulation time step
set_mujoco_time_step(0.002)  # 500 Hz
```

### Build123d CAD Configuration

```python
from codetocad.cli.config import (
    set_build123d_installation_path,
    set_build123d_default_units
)

# Set Build123d installation path (if not auto-detected)
set_build123d_installation_path("/usr/local/lib/python3.11/site-packages/build123d")

# Set default units for CAD operations
set_build123d_default_units("mm")  # Options: mm, cm, m, in, ft
```

### Asset Management Configuration

```python
from codetocad.cli.config import (
    set_material_cache_dir,
    set_model_cache_dir,
    set_thingiverse_api_key,
    set_poliigon_api_key,
    set_auto_download_materials
)

# Set cache directories
set_material_cache_dir("/path/to/material/cache")
set_model_cache_dir("/path/to/model/cache")

# Configure API keys for premium services
set_thingiverse_api_key("your_thingiverse_api_key")
set_poliigon_api_key("your_poliigon_api_key")

# Enable automatic material downloads
set_auto_download_materials(True)
```

### Export Configuration

```python
from codetocad.cli.config import (
    set_stl_export_quality,
    set_default_export_units
)

# Set STL export quality
set_stl_export_quality("high")  # Options: low, medium, high

# Set default export units
set_default_export_units("mm")  # Options: mm, cm, m, in, ft
```

## Reading Configuration

You can also read current configuration values:

```python
from codetocad.cli.config import (
    get_pybullet_config,
    get_mujoco_config,
    get_blender_config,
    get_build123d_config,
    get_asset_config,
    get_export_config
)

# Get current PyBullet settings
pybullet_config = get_pybullet_config()
print(f"GUI enabled: {pybullet_config.default_gui}")
print(f"Time step: {pybullet_config.default_time_step}")

# Get current asset settings
asset_config = get_asset_config()
print(f"Material cache: {asset_config.material_cache_dir}")
print(f"Auto download: {asset_config.auto_download_materials}")
```

## Configuration File Location

The configuration is stored in:
- **Linux/macOS**: `~/.codetocad/config.json`
- **Windows**: `%USERPROFILE%\.codetocad\config.json`

## Example Configuration File

```json
{
    "providers": {},
    "assets": {
        "material_cache_dir": "/Users/username/.codetocad/material_cache",
        "model_cache_dir": "/Users/username/.codetocad/model_cache",
        "thingiverse_api_key": "",
        "poliigon_api_key": "",
        "auto_download_materials": true,
        "auto_download_models": false,
        "max_cache_size_mb": 1000
    },
    "pybullet": {
        "default_gui": true,
        "default_time_step": 0.004166667,
        "default_gravity": [0, 0, -9.81],
        "enable_debug_visualizer": false
    },
    "mujoco": {
        "default_viewer": true,
        "default_time_step": 0.002,
        "default_gravity": [0, 0, -9.81]
    },
    "blender": {
        "executable_path": "",
        "default_scene_cleanup": true,
        "enable_gpu_rendering": false
    },
    "build123d": {
        "installation_path": "",
        "default_units": "mm",
        "precision": 1e-06
    },
    "export": {
        "stl_quality": "medium",
        "default_units": "mm",
        "auto_cleanup_temp_files": true
    }
}
```

## Migration from .env Files

If you were previously using `.env` files, you can migrate to the new system:

1. **Remove** your `.env` file
2. **Use the configuration methods** above to set your preferences
3. **Verify** settings with the getter functions

## Benefits of Programmatic Configuration

1. **Type Safety**: Configuration values are validated
2. **IDE Support**: Auto-completion and documentation
3. **Centralized**: All settings in one JSON file
4. **Persistent**: Settings survive across sessions
5. **Programmatic**: Can be set from code or scripts
6. **User-Friendly**: Clear feedback when settings are changed

## Complete Configuration Example

```python
# Complete setup for a robotics project
from codetocad.cli.config import *

# Configure simulation
set_pybullet_gui_enabled(True)
set_pybullet_time_step(0.004166667)  # 240 Hz for robotics
set_pybullet_gravity(0, 0, -9.81)

# Configure CAD
set_build123d_default_units("mm")  # Millimeters for precision

# Configure assets
set_material_cache_dir("./project_cache/materials")
set_auto_download_materials(True)

# Configure exports
set_stl_export_quality("high")
set_default_export_units("mm")

print("CodeToCAD configured for robotics project!")
```

This programmatic approach provides a much more user-friendly and maintainable way to configure CodeToCAD compared to manual environment file editing.
