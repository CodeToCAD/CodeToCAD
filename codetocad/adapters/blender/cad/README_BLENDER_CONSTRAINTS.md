# Blender Kinematic and Geometric Constraints

This document describes the Blender constraint functionality implemented specifically for the Blender adapter in the CodeToCAD project.

## Overview

The Blender constraint system provides comprehensive kinematic and geometric constraint functionality for Blender objects, allowing users to create complex relationships such as location copying, rotation tracking, distance maintenance, path following, and hierarchical transformations.

## Architecture

### Interface Layer (`codetocad/interfaces/cad/`)

The interface layer defines abstract base classes for all Blender constraint functionality:

- **`BlenderConstraintInterface`**: Abstract interface for applying constraints to Blender objects
- **`BlenderConstraint`**: Base class for individual constraint implementations
- **`BlenderConstraintType`**: Enumeration of available constraint types
- **`BlenderConstraintStatus`**: Enumeration of constraint states

### Implementation Layer (`codetocad/adapters/blender/cad/`)

The Blender adapter provides concrete implementations:

- **`BlenderObjectConstraint`**: Blender implementation of BlenderConstraintInterface
- **`BlenderObjectConstraintImpl`**: Concrete constraint implementation for Blender objects
- **Integration**: Seamless integration with existing Blender constraint actions

## Constraint Types

### 1. Kinematic Constraints

#### Copy Location
Copy the location (position) from another object.

```python
constraint = part.constraints.copy_location(
    target_object=target.get_blender_object(),
    use_x=True,
    use_y=True,
    use_z=False,
    use_offset=False,
    influence=1.0,
    name="follow_xy"
)
```

#### Copy Rotation
Copy the rotation from another object.

```python
constraint = part.constraints.copy_rotation(
    target_object=target.get_blender_object(),
    use_x=True,
    use_y=True,
    use_z=True,
    use_offset=False,
    influence=0.8,
    name="match_rotation"
)
```

#### Copy Scale
Copy the scale from another object.

```python
constraint = part.constraints.copy_scale(
    target_object=target.get_blender_object(),
    use_x=True,
    use_y=True,
    use_z=True,
    influence=1.0,
    name="match_scale"
)
```

#### Limit Location
Restrict object movement within specified bounds.

```python
constraint = part.constraints.limit_location(
    min_x=-5.0,
    max_x=5.0,
    min_y=-3.0,
    max_y=3.0,
    min_z=0.0,
    max_z=10.0,
    name="movement_bounds"
)
```

#### Track To
Make the object point toward another object.

```python
constraint = part.constraints.track_to(
    target_object=target.get_blender_object(),
    track_axis="TRACK_NEGATIVE_Z",
    up_axis="UP_Y",
    influence=1.0,
    name="look_at_target"
)
```

### 2. Geometric Constraints

#### Maintain Distance
Keep a specific distance from another object.

```python
constraint = part.constraints.maintain_distance(
    target_object=reference.get_blender_object(),
    distance=2.5,
    name="keep_distance"
)
```

#### Follow Path
Make the object follow a curve path.

```python
constraint = part.constraints.follow_path(
    curve_object=path_curve.get_blender_object(),
    offset=0.0,
    forward_axis="FORWARD_Y",
    up_axis="UP_Z",
    name="follow_curve"
)
```

### 3. Transformation Constraints

#### Child Of
Create a parent-child relationship with another object.

```python
constraint = part.constraints.child_of(
    parent_object=parent.get_blender_object(),
    influence=1.0,
    name="parent_relationship"
)
```

#### Floor Constraint
Keep the object above a floor surface.

```python
constraint = part.constraints.floor_constraint(
    target_object=floor.get_blender_object(),
    floor_location="FLOOR_NEGATIVE_Y",
    use_rotation=False,
    name="stay_on_floor"
)
```

## Usage Examples

### Basic Constraint Application

```python
from codetocad.adapters.blender import Part

# Create parts
part1 = Part("moving_part")
part2 = Part("target_part")

# Create Blender objects (this would typically be done through modeling)
part1.create_from_sketch()  # or other creation method
part2.create_from_sketch()

# Apply copy location constraint
copy_constraint = part1.constraints.copy_location(
    target_object=part2.get_blender_object(),
    use_x=True,
    use_y=True,
    use_z=False,
    name="follow_target"
)

# Apply limit location constraint
limit_constraint = part1.constraints.limit_location(
    min_x=-10.0,
    max_x=10.0,
    min_y=-5.0,
    max_y=5.0,
    name="movement_limits"
)
```

### Constraint Management

```python
# Get all constraints
all_constraints = part1.constraints.get_all_constraints()
print(f"Total constraints: {len(all_constraints)}")

# Get specific constraint
follow_constraint = part1.constraints.get_constraint("follow_target")
if follow_constraint:
    print(f"Constraint status: {follow_constraint.status.value}")

# Modify constraint properties
if follow_constraint:
    follow_constraint.set_influence(0.5)
    follow_constraint.mute()

# Remove a constraint
removal_success = part1.constraints.remove_constraint("movement_limits")
print(f"Constraint removal: {'succeeded' if removal_success else 'failed'}")

# Clear all constraints
part1.constraints.clear_all_constraints()
```

### Animation and Rigging

```python
# Create a camera that tracks a target
camera = Part("camera")
target = Part("target")

# Make camera look at target
track_constraint = camera.constraints.track_to(
    target_object=target.get_blender_object(),
    track_axis="TRACK_NEGATIVE_Z",
    up_axis="UP_Y",
    name="camera_tracking"
)

# Create an object that follows a path
follower = Part("follower")
path_curve = Part("path")  # Assume this is a curve

follow_constraint = follower.constraints.follow_path(
    curve_object=path_curve.get_blender_object(),
    offset=0.0,
    forward_axis="FORWARD_Y",
    name="path_following"
)
```

## Advanced Features

### Constraint Status Management

Constraints can have different statuses:
- **ACTIVE**: Constraint is applied and functioning
- **MUTED**: Constraint is temporarily disabled
- **DISABLED**: Constraint is permanently disabled
- **ERROR**: Constraint application failed
- **UNDEFINED**: Constraint is not yet applied

### Constraint Influence

All constraints support influence control (0.0 to 1.0):

```python
constraint = part.constraints.copy_location(target, name="copy_loc")
if constraint:
    constraint.set_influence(0.5)  # 50% influence
```

### Constraint Muting

Constraints can be temporarily disabled:

```python
constraint.mute()    # Disable constraint
constraint.unmute()  # Re-enable constraint
```

## Integration with Blender

### Native Blender Constraints

The system integrates seamlessly with Blender's native constraint system:
- Uses `bpy.types.Constraint` objects
- Integrates with Blender's dependency graph
- Supports Blender's animation system
- Works with existing Blender constraint actions

### Existing Blender Actions

The implementation leverages existing Blender constraint actions where available:
- `apply_copy_location_constraint()`
- `apply_copy_rotation_constraint()`
- `apply_limit_location_constraint()`
- `apply_limit_rotation_constraint()`
- `apply_pivot_constraint()`

### New Constraint Types

For constraint types not covered by existing actions, the system uses direct Blender API calls:
- Copy Scale constraints
- Track To constraints
- Follow Path constraints
- Floor constraints
- Child Of constraints

## Blender-Specific Considerations

### Object Hierarchy

The constraint system respects Blender's object hierarchy:
- Parent-child relationships
- Bone constraints for armatures
- Collection-based organization

### Dependency Graph

Constraints integrate with Blender's dependency graph:
- Automatic evaluation order
- Efficient constraint solving
- Animation system compatibility

### Animation Support

Constraints work seamlessly with Blender's animation system:
- Keyframe animation of constraint properties
- Driver-based constraint control
- Timeline-based constraint activation

## Performance Considerations

- Constraints are applied lazily when needed
- Constraint evaluation is optimized through Blender's dependency graph
- Batch constraint operations are supported
- Memory usage is minimized through efficient data structures

## Error Handling

The system provides robust error handling:
- Graceful failure for invalid constraints
- Detailed error messages for debugging
- Validation before constraint application
- Automatic cleanup of failed constraints

## Future Enhancements

Planned improvements include:
- Additional constraint types (IK, spline IK, etc.)
- Constraint templates and presets
- Visual constraint feedback in Blender viewport
- Advanced constraint dependency analysis
- Integration with Blender's geometry nodes
