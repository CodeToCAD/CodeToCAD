# Wire Geometric Constraints

This document describes the wire geometric constraint functionality implemented specifically for the build123d adapter.

## Overview

The wire constraint system provides comprehensive geometric constraint functionality for wires, allowing users to create complex geometric relationships such as tangent, parallel, perpendicular, coincident, distance, length, and continuity constraints.

## Architecture

### Interface Layer (`codetocad/interfaces/cad/wire/`)

The interface layer defines abstract base classes for all wire constraint functionality:

- **`WireConstraintInterface`**: Enhanced interface for applying geometric constraints to wires
- **`GeometricConstraint`**: Base class for individual geometric constraints
- **`ConstraintType`**: Enumeration of available constraint types
- **`ConstraintStatus`**: Enumeration of constraint states

### Implementation Layer (`codetocad/adapters/build123d/cad/wire/`)

The build123d adapter provides concrete implementations:

- **`WireConstraint`**: build123d implementation of WireConstraintInterface
- **`Build123dConstraint`**: Concrete geometric constraint implementation for build123d

## Constraint Types

### 1. Tangent Constraints
Create smooth tangent connections between wires and other geometric entities.

```python
tangent_constraint = wire.constraint.tangent_to(
    target_entity=target_curve,
    point=connection_point,
    name="smooth_connection"
)
```

### 2. Parallel Constraints
Maintain parallel relationships between wires and reference entities.

```python
parallel_constraint = wire.constraint.parallel_to(
    reference_entity=reference_line,
    name="parallel_alignment"
)
```

### 3. Perpendicular Constraints
Create perpendicular relationships between wires and reference entities.

```python
perpendicular_constraint = wire.constraint.perpendicular_to(
    reference_entity=reference_line,
    name="right_angle"
)
```

### 4. Coincident Constraints
Ensure wire points coincide with target points.

```python
coincident_constraint = wire.constraint.coincident_points(
    target_point=(x, y, z),
    wire_point="end",  # "start", "end", or parameter value
    name="endpoint_match"
)
```

### 5. Distance Constraints
Maintain specific distances between wires and other entities.

```python
distance_constraint = wire.constraint.distance_from(
    target_entity=target_entity,
    distance_value=5.0,
    name="maintain_clearance"
)
```

### 6. Length Constraints
Control the total length of wires.

```python
length_constraint = wire.constraint.set_length(
    length_value=15.0,
    name="fixed_dimension"
)
```

### 7. Continuity Constraints
Ensure smooth continuity between connected wire segments.

```python
continuity_constraint = wire.constraint.continuous_with(
    other_wire=connecting_wire,
    continuity_order=1,  # 0=position, 1=tangent, 2=curvature
    name="smooth_transition"
)
```

## Usage Examples

### Basic Constraint Application

```python
from codetocad.adapters.build123d import Wire, Sketch

# Create wires
sketch = Sketch("constraint_demo")
main_wire = Wire(sketch, name="main_wire")
reference_wire = Wire(sketch, name="reference_wire")

# Apply parallel constraint
parallel_constraint = main_wire.constraint.parallel_to(
    reference_entity=reference_wire,
    name="parallel_wires"
)

# Apply distance constraint
distance_constraint = main_wire.constraint.distance_from(
    target_entity=reference_wire,
    distance_value=10.0,
    name="maintain_spacing"
)
```

### Constraint Management

```python
# Get all constraints
all_constraints = wire.constraint.get_all_constraints()
print(f"Total constraints: {len(all_constraints)}")

# Validate constraints
validation_results = wire.constraint.validate_constraints()
valid_count = sum(1 for is_valid in validation_results.values() if is_valid)
print(f"Valid constraints: {valid_count}/{len(validation_results)}")

# Solve constraints
solve_success = wire.constraint.solve_constraints()
print(f"Constraint solving: {'succeeded' if solve_success else 'failed'}")

# Remove a constraint
removal_success = wire.constraint.remove_constraint("constraint_name")
print(f"Constraint removal: {'succeeded' if removal_success else 'failed'}")
```

### Constraint Modification

```python
# Update constraint parameters
constraint = wire.constraint.get_constraint("distance_constraint")
if constraint:
    update_success = constraint.update_parameters(distance_value=7.5)
    print(f"Parameter update: {'succeeded' if update_success else 'failed'}")

# Suppress/unsuppress constraints
suppress_success = constraint.suppress()
unsuppress_success = constraint.unsuppress()
```

## Advanced Features

### Constraint Status Management

Constraints can have different statuses:
- **ACTIVE**: Constraint is applied and being solved
- **SUPPRESSED**: Constraint is temporarily disabled
- **FAILED**: Constraint application or solving failed
- **UNDEFINED**: Constraint is not yet applied

### Constraint Validation

The system provides comprehensive validation:
- Parameter validation (required parameters present)
- Geometric validation (entities exist and are compatible)
- Constraint compatibility checking

### Constraint Solving

The constraint solver:
- Applies constraints in dependency order
- Handles constraint conflicts
- Provides feedback on solving success/failure
- Supports iterative solving for complex systems

## Backward Compatibility

The system maintains backward compatibility with existing wire constraint methods:

```python
# Legacy methods still work
wire.constraint.coincident(vertex1, vertex2)
wire.constraint.parallel(edge1, edge2)
wire.constraint.perpendicular(edge1, edge2)
wire.constraint.tangent(wire, edge)
wire.constraint.midpoint(edge, target_vertex)
```

## Integration with build123d

The constraint system integrates seamlessly with build123d:
- Uses build123d's native constraint solving capabilities
- Maintains wire geometry integrity
- Supports complex constraint relationships
- Provides efficient constraint evaluation

## Error Handling

The system provides robust error handling:
- Graceful failure for invalid constraints
- Detailed error messages for debugging
- Rollback capabilities for failed constraint applications
- Validation before constraint application

## Performance Considerations

- Constraints are applied lazily when needed
- Constraint solving is optimized for common cases
- Batch constraint operations are supported
- Memory usage is minimized through efficient data structures

## Future Enhancements

Planned improvements include:
- Advanced constraint types (curvature, area, etc.)
- Constraint dependency analysis
- Visual constraint feedback
- Constraint templates and presets
- Integration with parametric modeling workflows
