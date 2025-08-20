# build123d CAD Adapter

## Overview

This document describes the concrete implementations of CAD interface classes for the build123d adapter in CodeToCAD. These implementations provide build123d-specific functionality while maintaining compatibility with the abstract interface definitions.

## Implementation Structure

### Directory Structure
```
codetocad/adapters/build123d/
├── __init__.py                    # Module exports
├── README.md                      # This documentation
├── build123d_actions/             # Modular action functions
│   ├── __init__.py
│   ├── geometry.py               # Geometry creation functions
│   ├── transformations.py        # Transformation operations
│   ├── export.py                 # Export/import functions
│   └── sketch_operations.py      # Sketch and wire operations
├── cad/                          # Interface implementations
│   ├── __init__.py
│   ├── vertex/
│   │   ├── __init__.py
│   │   └── vertex.py             # Vertex implementation
│   ├── edge/
│   │   ├── __init__.py
│   │   └── edge.py               # Edge implementation
│   ├── wire/
│   │   ├── __init__.py
│   │   ├── wire.py               # Wire implementation
│   │   ├── wire_add.py           # Wire add operations
│   │   └── wire_preset_class_property.py
│   ├── sketch/
│   │   ├── __init__.py
│   │   ├── sketch.py             # Sketch implementation
│   │   └── sketch_get.py         # Sketch get operations
│   ├── part/
│   │   ├── __init__.py
│   │   ├── part.py               # Part implementation
│   │   ├── part_presets.py       # Part preset shapes
│   │   └── part_preset_class_property.py
│   └── assembly/
│       ├── __init__.py
│       └── assembly.py           # Assembly implementation
└── cli/                          # CLI utilities (future)
    └── __init__.py
```

## Class Implementations

### 1. Vertex (`vertex/vertex.py`)
- **Inherits from**: `VertexInterface`
- **build123d Integration**: Creates build123d Vertex objects
- **Key Features**:
  - Position management with build123d coordinates
  - Transformation operations
  - Distance calculations
  - Position getter/setter methods

### 2. Edge (`edge/edge.py`)
- **Inherits from**: `EdgeInterface`
- **build123d Integration**: Creates build123d Edge objects
- **Key Features**:
  - Line edge creation between vertices
  - Length calculations
  - Direction vector operations
  - Parallel/perpendicular checks
  - Edge splitting operations

### 3. Wire (`wire/wire.py`)
- **Inherits from**: `WireInterface`
- **build123d Integration**: Creates build123d Wire objects from edges
- **Key Features**:
  - Edge collection and management
  - Wire closure detection
  - Length calculations
  - Bounding box operations
  - Wire reversal and copying

### 4. Sketch (`sketch/sketch.py`)
- **Inherits from**: `SketchInterface`
- **build123d Integration**: Uses build123d BuildSketch context
- **Key Features**:
  - Wire collection and management
  - Drawing operations through wire.add
  - Face creation from sketches
  - Bounding box calculations
  - Sketch copying and clearing

### 5. Part (`part/part.py`)
- **Inherits from**: `PartInterface`
- **build123d Integration**: Creates build123d Solid objects
- **Key Features**:
  - Sketch extrusion to solids
  - Boolean operations (union, difference, intersection)
  - Transform operations (translate, rotate, scale)
  - Volume and bounding box calculations
  - Export functionality (STEP, STL, BREP)

### 6. Assembly (`assembly/assembly.py`)
- **Inherits from**: `AssemblyInterface`
- **build123d Integration**: Manages collections of build123d Solid objects
- **Key Features**:
  - Part collection and management
  - Collective transform operations
  - Export functionality for multiple parts
  - Bounding box calculations for entire assemblies
  - Union operations across all parts

## Modular Actions

The adapter uses a modular action system where specific build123d API calls are encapsulated in utility functions:

### Geometry Actions (`build123d_actions/geometry.py`)
- Vertex, edge, and wire creation
- Primitive solid creation (cube, cylinder, sphere)
- Boolean operations
- Face creation and extrusion

### Transformation Actions (`build123d_actions/transformations.py`)
- Translation, rotation, and scaling
- Bounding box and center of mass calculations
- Volume and area measurements
- Mirroring operations

### Export Actions (`build123d_actions/export.py`)
- STEP, STL, and BREP export/import
- Multi-object export handling
- File format conversions

### Sketch Operations (`build123d_actions/sketch_operations.py`)
- Sketch context management
- Line, arc, and spline creation
- Rectangle and circle primitives
- Sketch extrusion and revolution

## Usage Examples

### Basic Usage
```python
from codetocad.adapters.build123d import Vertex, Edge, Wire, Sketch, Part, Assembly

# Create vertices
v1 = Vertex(0, 0, 0)
v2 = Vertex(1, 1, 1)

# Create edge
edge = Edge(v1, v2)

# Create part using presets
cube = Part.preset.cube(2, 2, 2)

# Create assembly
assembly = Assembly("my_assembly")
assembly.add_part(cube)
```

### Advanced Operations
```python
# Create a sketch with a rectangle
sketch = Sketch()
rect_wire = sketch.preset.rectangle(10, 5)

# Create a part and extrude the sketch
part = Part("extruded_part")
part.sketch = sketch
part.extrude_sketch(3)

# Boolean operations
cube1 = Part.preset.cube(2, 2, 2)
cube2 = Part.preset.cube(1, 1, 1)
cube2.transform.translate(0.5, 0.5, 0.5)
result = cube1.boolean.difference(cube2)

# Export
result.export_step("result.step")
```

## Dependencies

This adapter requires the `build123d` package to be installed:

```bash
pip install build123d
```

## Notes

- The adapter follows the same organizational pattern as other CodeToCAD adapters
- All interface implementations delegate to modular action functions
- Native build123d objects are stored and managed for direct API access
- Error handling is implemented for common failure cases
- The adapter supports both programmatic creation and preset shapes

## Future Enhancements

- CLI utilities for running build123d scripts
- Advanced constraint solving
- Parametric modeling support
- Additional export formats
- Performance optimizations for large assemblies
