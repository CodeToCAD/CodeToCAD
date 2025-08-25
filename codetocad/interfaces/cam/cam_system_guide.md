# CodeToCAD CAM System Guide

The CodeToCAD CAM (Computer-Aided Manufacturing) system provides comprehensive CNC machining capabilities, allowing you to transition seamlessly from CAD design to manufacturing-ready G-code.

## Overview

The CAM system includes:

- **Tool Management**: Comprehensive tool library with presets for common cutting tools
- **Toolpath Generation**: Support for 2D/3D milling, drilling, and specialty operations
- **Work Coordinate Systems**: Flexible workpiece setup and origin management
- **Post-Processing**: G-code generation for various CNC controllers
- **Simulation**: Basic collision detection and material removal preview
- **Job Management**: Complete workflow organization and optimization

## Quick Start

### 1. Basic Tool Usage

```python
from codetocad.core.cam.tool import Tool

# Use preset tools
end_mill = Tool.preset.end_mill.flat_carbide_6mm()
drill = Tool.preset.drill.twist_drill_hss_5mm()
ball_mill = Tool.preset.ball_mill.ball_mill_carbide_3mm()

# Create custom tool
custom_tool = Tool()
custom_tool.set_name("Custom End Mill")
custom_tool.set_tool_number(1)

# Set geometry
from codetocad.interfaces.cam.tool_interface import ToolGeometry
geometry = ToolGeometry(
    diameter=8.0,
    length=75.0,
    cutting_length=25.0,
    shank_diameter=8.0,
    flute_count=3
)
custom_tool.set_geometry(geometry)
```

### 2. Tool Library Management

```python
from codetocad.core.cam.tool_library import ToolLibrary

# Create library
library = ToolLibrary()
library.set_name("My CNC Tools")

# Add tools
library.add_tool(Tool.preset.end_mill.flat_carbide_6mm(tool_number=1))
library.add_tool(Tool.preset.drill.twist_drill_hss_5mm(tool_number=2))

# Find tools
carbide_tools = library.get_tools_by_type("FLAT_END_MILL")
small_tools = library.get_tools_by_diameter_range(0, 5)

# Save/load library
library.save_to_file("my_tools.json")
library.export_to_format("my_tools.csv", "csv")
```

### 3. Toolpath Creation

```python
from codetocad.core.cam.toolpath import Toolpath
from codetocad.interfaces.cam.toolpath_interface import (
    ToolpathOperation, ToolpathStrategy, CuttingParameters
)

# Create toolpath
toolpath = Toolpath()
toolpath.set_name("Profile Cut")
toolpath.set_operation(ToolpathOperation.FINISHING)
toolpath.set_strategy(ToolpathStrategy.PROFILE)
toolpath.set_tool(end_mill)

# Set cutting parameters
cutting_params = CuttingParameters(
    depth_of_cut=5.0,
    step_down=1.0,
    step_over=0.5,
    feed_rate=1200,
    spindle_speed=18000,
    plunge_rate=300
)
toolpath.set_cutting_parameters(cutting_params)

# Generate drilling pattern
drill_points = [(10, 10), (50, 10), (50, 50), (10, 50)]
drilling_toolpath = Toolpath()
drilling_toolpath.set_tool(drill)
drilling_toolpath.generate_drilling_pattern(drill_points, depth=15.0)
```

### 4. Work Coordinate System Setup

```python
from codetocad.core.cam.work_coordinate_system import WorkCoordinateSystem
from codetocad.interfaces.cam.work_coordinate_system_interface import (
    WCSOrigin, WorkpieceSetup
)

# Create WCS
wcs = WorkCoordinateSystem()
wcs.set_name("Main WCS")

# Define workpiece
workpiece = WorkpieceSetup(
    length=100.0,
    width=50.0,
    height=20.0,
    stock_to_leave=0.5,
    fixture_height=5.0
)
wcs.set_workpiece_setup(workpiece)

# Set origin
wcs.set_origin_from_preset(WCSOrigin.BOTTOM_LEFT_FRONT)

# Transform coordinates
machine_point = wcs.transform_point_to_machine((10, 10, -5))
```

## Tool Presets

The system includes comprehensive tool presets:

### End Mills
- `Tool.preset.end_mill.flat_hss_3mm()` - 3mm HSS flat end mill
- `Tool.preset.end_mill.flat_carbide_6mm()` - 6mm carbide flat end mill
- `Tool.preset.end_mill.roughing_carbide_10mm()` - 10mm carbide roughing mill
- `Tool.preset.end_mill.finishing_carbide_3mm()` - 3mm carbide finishing mill

### Drills
- `Tool.preset.drill.twist_drill_hss_5mm()` - 5mm HSS twist drill
- `Tool.preset.drill.center_drill_60_degree()` - 60° center drill
- `Tool.preset.drill.spot_drill_90_degree_6mm()` - 6mm spot drill

### Ball Mills
- `Tool.preset.ball_mill.ball_mill_carbide_3mm()` - 3mm carbide ball mill
- `Tool.preset.ball_mill.ball_mill_carbide_6mm()` - 6mm carbide ball mill

### V-Bits
- `Tool.preset.v_bit.engraving_90_degree()` - 90° engraving V-bit
- `Tool.preset.v_bit.chamfer_45_degree()` - 45° chamfer mill

## Toolpath Strategies

### 2D Operations
- **PROFILE**: Follow part contours
- **POCKET**: Clear enclosed areas
- **DRILLING**: Point drilling operations
- **ENGRAVING**: Surface engraving

### 2.5D Operations
- **ADAPTIVE_CLEARING**: Intelligent roughing
- **CONVENTIONAL_CLEARING**: Traditional roughing

### 3D Operations
- **WATERLINE**: Constant Z-level passes
- **SURFACE_FINISHING**: 3D surface finishing
- **SPIRAL**: Spiral toolpaths

## Integration with CAD

```python
from codetocad.integrations.cam_integration import cam_integration

# Create CAM job from CAD part
cam_job = cam_integration.create_cam_job_from_part(my_part, "Machining Job")

# Get tool recommendations based on material
recommended_tools = cam_integration.recommend_tools_for_material(my_part.material)

# Get suggested operations
operations = cam_integration.suggest_machining_operations(my_part)

# Optimize toolpath sequence
optimized_toolpaths = cam_integration.optimize_tool_sequence(toolpaths)
```

## Adapters

### FreeCAD Path Adapter
```python
from codetocad.adapters.freecad.cam.toolpath import Toolpath as FreeCADToolpath

# Create FreeCAD-specific toolpath
freecad_toolpath = FreeCADToolpath()
freecad_toolpath.set_freecad_job(freecad_job)
freecad_toolpath.generate_from_part(cad_part)
```

### PyCAM Adapter
```python
from codetocad.adapters.pycam.cam.toolpath import Toolpath as PyCAMToolpath

# Create PyCAM-specific toolpath
pycam_toolpath = PyCAMToolpath()
pycam_toolpath.generate_from_part(cad_part)
```

## Post-Processing

```python
from codetocad.core.cam.post_processor import PostProcessor
from codetocad.interfaces.cam.post_processor_interface import (
    PostProcessorSettings, GCodeDialect, MachineConfiguration
)

# Configure post processor
post_processor = PostProcessor()
settings = PostProcessorSettings(
    dialect=GCodeDialect.GRBL,
    include_comments=True,
    decimal_places=3
)
post_processor.set_settings(settings)

# Generate G-code
gcode_lines = post_processor.process_multiple_toolpaths(toolpaths)

# Export to file
post_processor.export_to_file(toolpaths, "output.nc")
```

## Simulation

```python
from codetocad.core.cam.simulation import Simulation

# Create simulator
simulator = Simulation()
simulator.set_workpiece(cad_part)

# Check for collisions
collisions = simulator.check_multiple_toolpaths(toolpaths)

# Simulate material removal
preview = simulator.simulate_material_removal(toolpaths)
print(f"Volume removed: {preview.volume_removed:.2f} mm³")
print(f"Estimated surface roughness: {preview.roughness_estimate:.1f} μm")
```

## Complete Workflow Example

```python
from codetocad.core.cam.cam_job import CAMJob
from codetocad.interfaces.cam.cam_job_interface import JobSetup, MachiningStrategy

# Create complete CAM job
job = CAMJob()
job.set_name("Complete Machining Job")
job.set_workpiece(my_part)
job.set_tool_library(library)
job.set_work_coordinate_system(wcs)

# Set up job
setup = JobSetup(
    name="Aluminum Part",
    strategy=MachiningStrategy.ROUGHING_FINISHING,
    material=my_part.material,
    tolerance=0.1
)
job.set_setup(setup)

# Generate toolpaths
job.generate_toolpaths()

# Optimize
job.optimize_toolpaths()

# Simulate
job.simulate_job()

# Post-process
job.post_process()

# Export G-code
job.export_gcode("final_program.nc")

# Save job
job.save_job("machining_job.json")
```

## Best Practices

1. **Tool Selection**: Use appropriate tools for materials and operations
2. **Cutting Parameters**: Start conservative and optimize based on results
3. **Work Holding**: Consider fixture clearance in toolpath planning
4. **Tool Changes**: Minimize tool changes for efficiency
5. **Simulation**: Always simulate before machining
6. **Documentation**: Keep detailed records of successful parameters

## Troubleshooting

### Common Issues

1. **Tool Validation Errors**: Check geometry and cutting data completeness
2. **Collision Warnings**: Review clearance heights and fixture setup
3. **Long Machining Times**: Optimize feeds/speeds and toolpath strategies
4. **Poor Surface Finish**: Reduce step-over and increase spindle speed

### Performance Tips

1. Use adaptive clearing for roughing operations
2. Minimize tool changes by grouping operations
3. Optimize toolpath order to reduce rapid moves
4. Use appropriate step-over percentages for finish quality

## Next Steps

- Explore FreeCAD Path Workbench integration for advanced features
- Implement custom post-processors for specific machines
- Add advanced simulation capabilities
- Integrate with CAM software APIs

For more examples, see the `examples/` directory in the CodeToCAD repository.
