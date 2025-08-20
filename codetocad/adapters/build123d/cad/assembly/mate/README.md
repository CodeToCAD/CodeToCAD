# Assembly Mates

This document describes the assembly mate functionality implemented specifically for the build123d adapter.

## Overview

The assembly mate system provides a comprehensive framework for defining relationships and constraints between parts in an assembly. It supports both geometric constraints (static positioning) and kinematic joints (motion-based relationships).

## Architecture

### Interface Layer (`codetocad/interfaces/cad/assembly/`)

The interface layer defines abstract base classes for all mate functionality:

- **`MateInterface`**: Base interface for all mates
- **`GeometricMateInterface`**: Interface for static geometric constraints
- **`KinematicMateInterface`**: Interface for motion-based joints
- **`MateManagerInterface`**: Interface for managing collections of mates
- **`AssemblyMateInterface`**: NEW - Fluent API interface for intuitive mate creation

### Implementation Layer (`codetocad/adapters/build123d/cad/assembly/`)

The build123d adapter provides concrete implementations:

- **`Mate`**: Base implementation class
- **`GeometricMate`**: Base for geometric constraints
- **`KinematicMate`**: Base for kinematic joints
- **`MateManager`**: Manages mate collections in assemblies
- **`AssemblyMate`**: NEW - Fluent API implementation for build123d

## NEW Fluent API

The fluent API provides an intuitive, method-based approach to creating mates:

### Benefits of the Fluent API

✅ **More Intuitive**: `assembly.mate.revolute(...)` vs `assembly.create_mate(MateType.REVOLUTE, ...)`
✅ **Type-Specific Parameters**: Each mate method has parameters specific to that mate type
✅ **Required Location Parameters**: Kinematic mates require `location1` and `location2` for proper joint definition
✅ **Better IDE Support**: Autocomplete and type hints work better with specific methods
✅ **CAD Software Conventions**: Follows patterns familiar to CAD users

### API Comparison

```python
# OLD API
revolute_mate = assembly.create_mate(
    MateType.REVOLUTE, part1, part2, name="hinge",
    axis=axis, angle_range=(0, 180)
)

# NEW FLUENT API
revolute_mate = assembly.mate.revolute(
    part1, part2, axis=axis,
    location1=location_on_part1,
    location2=location_on_part2,
    angle_range=(0, 180),
    name="hinge"
)
```

## Mate Types

### Geometric Mates (Static Constraints)

1. **Coincident**: Aligns faces, edges, or points to occupy the same location
2. **Concentric**: Aligns cylindrical/circular features on the same axis
3. **Distance**: Maintains a specific distance between features
4. **Parallel**: Keeps faces or edges parallel
5. **Perpendicular**: Keeps faces or edges perpendicular
6. **Tangent**: Makes surfaces tangent to each other
7. **Angle**: Maintains a specific angle between features

### Kinematic Mates (Motion-Based)

1. **Rigid**: Fixes parts together (0 degrees of freedom)
2. **Revolute**: Allows rotation around an axis (1 DOF)
3. **Linear**: Allows translation along an axis (1 DOF)
4. **Cylindrical**: Allows rotation and translation along an axis (2 DOF)
5. **Ball**: Allows rotation around all three axes (3 DOF)

## Usage Examples

### Basic Assembly with Rigid Mate (NEW FLUENT API)

```python
from codetocad.adapters.build123d import Part, Assembly
import build123d as bd

# Create parts
base = Part.preset.cube(10, 10, 2)
base.set_name("base")

cylinder = Part.preset.cylinder(2, 5)
cylinder.set_name("cylinder")

# Create assembly
assembly = Assembly("example_assembly")
assembly.add_part(base)
assembly.add_part(cylinder)

# Create rigid mate using fluent API
location1 = bd.Location((0, 0, 1))  # Location on base
location2 = bd.Location((0, 0, 0))  # Location on cylinder

rigid_mate = assembly.mate.rigid(
    base,
    cylinder,
    location1=location1,
    location2=location2,
    name="fix_cylinder"
)

print(f"Created mate: {rigid_mate.name}")
print(f"Status: {rigid_mate.status.value}")
```

### Kinematic Assembly with Revolute Mate (NEW FLUENT API)

```python
import build123d as bd

# Create revolute mate for rotation using fluent API
axis = bd.Axis((0, 0, 0), (0, 0, 1))  # Z-axis
location1 = bd.Location((0, 0, 1))    # Location on base
location2 = bd.Location((0, 0, 0))    # Location on cylinder

revolute_mate = assembly.mate.revolute(
    base,
    cylinder,
    axis=axis,
    location1=location1,
    location2=location2,
    angle_range=(0, 180),
    current_angle=45,
    name="rotating_cylinder"
)

# Change the angle
if revolute_mate:
    revolute_mate.set_angle(90)
    print(f"New angle: {revolute_mate.current_angle}°")
```

### Geometric Mates (NEW FLUENT API)

```python
# Coincident mate - align faces
coincident_mate = assembly.mate.coincident(
    part1,
    part2,
    entity1=face_on_part1,  # Specific face reference
    entity2=face_on_part2,  # Specific face reference
    flip_alignment=False,
    name="align_faces"
)

# Distance mate - maintain spacing
distance_mate = assembly.mate.distance(
    part1,
    part2,
    entity1=face_on_part1,
    entity2=face_on_part2,
    distance=5.0,
    name="maintain_distance"
)

# Concentric mate - align cylindrical features
concentric_mate = assembly.mate.concentric(
    part1,
    part2,
    entity1=cylindrical_face1,
    entity2=cylindrical_face2,
    name="align_cylinders"
)
```

### Assembly Management

```python
# Get mate statistics
stats = assembly.get_mate_statistics()
print(f"Total mates: {stats['total']}")
print(f"Active mates: {stats['active']}")

# Validate all mates
validation_results = assembly.validate_mates()
for mate_name, is_valid in validation_results.items():
    print(f"{mate_name}: {'Valid' if is_valid else 'Invalid'}")

# Solve all mates
if assembly.solve_mates():
    print("All mates solved successfully")

# Remove a mate
assembly.remove_mate("fix_cylinder")
```

## Integration with Existing System

The mate system is fully integrated with the existing CodeToCAD assembly hierarchy:

1. **Assembly Class**: Extended with mate management capabilities
2. **Part Class**: Compatible with mate constraints
3. **Interface Pattern**: Follows the established interface/adapter pattern
4. **build123d Integration**: Leverages build123d's joint system where applicable

## Current Implementation Status

### ✅ Completed Features

- [x] Complete interface hierarchy for all mate types
- [x] Base implementation classes with validation and error handling
- [x] Integration with existing assembly system
- [x] Mate manager for collection management
- [x] Basic rigid mate functionality
- [x] Comprehensive enum system for mate types and statuses
- [x] Assembly convenience methods for mate operations
- [x] Example code and basic testing

### 🚧 Partially Implemented

- [x] Kinematic mate interfaces (need full build123d integration)
- [x] Geometric mate interfaces (need constraint solving)
- [x] Mate validation system (basic validation working)

### 📋 Future Enhancements

- [ ] Full build123d joint integration for kinematic mates
- [ ] Geometric constraint solver for static mates
- [ ] Advanced mate features (mate limits, mate references)
- [ ] Mate conflict detection and resolution
- [ ] Mate animation and visualization
- [ ] Import/export of mate definitions
- [ ] Performance optimization for large assemblies

## File Structure

```
codetocad/
├── interfaces/cad/assembly/mate/
│   ├── __init__.py
│   ├── mate_interface.py
│   ├── geometric_mate_interface.py
│   ├── kinematic_mate_interface.py
│   └── mate_manager_interface.py
└── adapters/build123d/cad/assembly/
    ├── assembly.py (updated with mate support)
    └── mate/
        ├── __init__.py
        ├── mate.py
        ├── geometric_mate.py
        ├── kinematic_mate.py
        └── mate_manager.py
```

## Testing

Run the test suite to verify functionality:

```bash
# Basic functionality test
python test_assembly_mates.py

# Comprehensive examples
python codetocad/adapters/build123d/examples/assembly_mates_example.py
```

## Design Principles

1. **Extensibility**: Easy to add new mate types
2. **Consistency**: Follows CodeToCAD's interface patterns
3. **Flexibility**: Supports both geometric and kinematic constraints
4. **Integration**: Works seamlessly with existing assembly system
5. **Validation**: Comprehensive error checking and validation
6. **Performance**: Efficient mate management and solving

## Contributing

When adding new mate types:

1. Define the interface in the appropriate interface module
2. Implement the concrete class in the build123d adapter
3. Add the mate type to the `MateType` enum
4. Update the mate manager's class mapping
5. Add tests and examples
6. Update this documentation

## Dependencies

- Python 3.8+
- CodeToCAD core interfaces
- build123d (for kinematic joint functionality)
- typing (for type hints)

## License

This implementation follows the same license as the CodeToCAD project.
