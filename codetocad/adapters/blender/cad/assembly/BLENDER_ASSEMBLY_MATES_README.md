# Blender Assembly Kinematic Constraint System

This document describes the Blender assembly mate functionality implemented specifically for the Blender adapter in the CodeToCAD project.

## Overview

The Blender assembly mate system provides comprehensive kinematic and geometric constraint functionality for assemblies, allowing users to create complex mechanical relationships such as hinges, sliders, ball joints, and geometric alignments between parts using Blender's native constraint system.

## Architecture

### Interface Layer (`codetocad/interfaces/cad/assembly/mate/`)

The interface layer defines abstract base classes for all assembly mate functionality:

- **`AssemblyMateInterface`**: Abstract interface for creating mates between parts
- **`MateManagerInterface`**: Interface for managing collections of mates
- **`KinematicMateInterface`**: Base interfaces for kinematic mates (rigid, revolute, linear, etc.)
- **`GeometricMateInterface`**: Base interfaces for geometric mates (coincident, distance, etc.)

### Implementation Layer (`codetocad/adapters/blender/cad/assembly/mate/`)

The Blender adapter provides concrete implementations:

- **`BlenderAssemblyMate`**: Blender implementation of AssemblyMateInterface
- **`BlenderMateManager`**: Manages mate creation and lifecycle
- **`BlenderKinematicMate`**: Kinematic mate implementations using Blender constraints
- **`BlenderGeometricMate`**: Geometric mate implementations using Blender constraints

## Mate Types

### 1. Kinematic Mates

#### Rigid Mate
Creates a fixed connection between two parts using Child Of constraint.

```python
rigid_mate = assembly.mate.rigid(
    part1=base_part,
    part2=connected_part,
    location1=connection_point1,
    location2=connection_point2,
    name="rigid_connection"
)
```

#### Revolute Mate
Creates a hinge-like rotational joint with angle limits.

```python
revolute_mate = assembly.mate.revolute(
    part1=base_part,
    part2=rotating_part,
    axis=rotation_axis,
    location1=hinge_point1,
    location2=hinge_point2,
    angle_range=(-90, 90),
    current_angle=0,
    name="hinge_joint"
)
```

#### Linear Mate
Creates a sliding joint with position limits.

```python
linear_mate = assembly.mate.linear(
    part1=base_part,
    part2=sliding_part,
    axis=slide_axis,
    location1=slide_start,
    location2=slider_mount,
    position_range=(0, 100),
    current_position=0,
    name="slider_joint"
)
```

#### Cylindrical Mate
Creates a screw-like joint allowing both rotation and translation.

```python
cylindrical_mate = assembly.mate.cylindrical(
    part1=base_part,
    part2=moving_part,
    axis=screw_axis,
    location1=screw_base,
    location2=screw_mount,
    position_range=(0, 50),
    angle_range=(0, 720),
    current_position=0,
    current_angle=0,
    name="screw_joint"
)
```

#### Ball Mate
Creates a spherical joint allowing multi-axis rotation.

```python
ball_mate = assembly.mate.ball(
    part1=base_part,
    part2=rotating_part,
    center_point=ball_center,
    location1=socket_point,
    location2=ball_point,
    angle_ranges=((-45, 45), (-45, 45), (-180, 180)),
    current_angles=(0, 0, 0),
    name="ball_joint"
)
```

### 2. Geometric Mates

#### Coincident Mate
Aligns geometric entities (faces, edges, vertices) between parts.

```python
coincident_mate = assembly.mate.coincident(
    part1=part1,
    part2=part2,
    entity1=face1,
    entity2=face2,
    flip_alignment=False,
    name="face_alignment"
)
```

#### Concentric Mate
Aligns cylindrical or circular features to share the same axis.

```python
concentric_mate = assembly.mate.concentric(
    part1=part1,
    part2=part2,
    entity1=hole1,
    entity2=shaft2,
    name="shaft_alignment"
)
```

#### Distance Mate
Maintains a specific distance between geometric entities.

```python
distance_mate = assembly.mate.distance(
    part1=part1,
    part2=part2,
    entity1=surface1,
    entity2=surface2,
    distance=5.0,
    name="spacing_constraint"
)
```

#### Parallel Mate
Keeps planar faces or linear edges parallel.

```python
parallel_mate = assembly.mate.parallel(
    part1=part1,
    part2=part2,
    entity1=face1,
    entity2=face2,
    name="parallel_surfaces"
)
```

#### Perpendicular Mate
Keeps planar faces or linear edges perpendicular.

```python
perpendicular_mate = assembly.mate.perpendicular(
    part1=part1,
    part2=part2,
    entity1=face1,
    entity2=face2,
    name="perpendicular_surfaces"
)
```

#### Tangent Mate
Creates tangent relationships between curved surfaces.

```python
tangent_mate = assembly.mate.tangent(
    part1=part1,
    part2=part2,
    entity1=curved_surface1,
    entity2=curved_surface2,
    name="tangent_contact"
)
```

#### Angle Mate
Maintains a specific angle between planar faces or linear edges.

```python
angle_mate = assembly.mate.angle(
    part1=part1,
    part2=part2,
    entity1=face1,
    entity2=face2,
    angle=45.0,
    name="angled_surfaces"
)
```

## Usage Examples

### Basic Assembly with Kinematic Mates

```python
from codetocad.adapters.blender import Assembly, Part

# Create assembly and parts
assembly = Assembly("mechanical_system")
base = Part("base")
arm = Part("rotating_arm")
slider = Part("sliding_part")

# Add parts to assembly
assembly.add.part(base)
assembly.add.part(arm)
assembly.add.part(slider)

# Create kinematic chain
# 1. Rigid connection between base and assembly frame
rigid_mate = assembly.mate.rigid(
    base, assembly_frame,
    location1=base_mount,
    location2=frame_mount,
    name="base_connection"
)

# 2. Revolute joint for rotating arm
revolute_mate = assembly.mate.revolute(
    base, arm,
    axis=Vector(0, 0, 1),
    location1=hinge_point,
    location2=arm_pivot,
    angle_range=(-90, 90),
    name="arm_hinge"
)

# 3. Linear joint for slider on arm
linear_mate = assembly.mate.linear(
    arm, slider,
    axis=Vector(1, 0, 0),
    location1=slide_start,
    location2=slider_mount,
    position_range=(0, 100),
    name="arm_slider"
)
```

### Geometric Alignment

```python
# Align surfaces between parts
coincident_mate = assembly.mate.coincident(
    part1, part2,
    entity1=part1.get_face("top"),
    entity2=part2.get_face("bottom"),
    name="surface_alignment"
)

# Maintain specific spacing
distance_mate = assembly.mate.distance(
    part1, part2,
    entity1=part1.get_face("side"),
    entity2=part2.get_face("side"),
    distance=10.0,
    name="side_spacing"
)

# Keep features concentric
concentric_mate = assembly.mate.concentric(
    shaft_part, bearing_part,
    entity1=shaft_part.get_edge("outer_diameter"),
    entity2=bearing_part.get_edge("inner_diameter"),
    name="bearing_alignment"
)
```

### Animation and Control

```python
# Control joint positions
revolute_mate.set_angle(45.0)  # Rotate to 45 degrees
linear_mate.set_position(25.0)  # Move to 25mm position

# Query current states
current_angle = revolute_mate.get_angle()
current_position = linear_mate.get_position()
degrees_of_freedom = revolute_mate.get_degrees_of_freedom()

# Animate over time
import bpy

def animate_mechanism(frame):
    angle = frame * 2.0  # 2 degrees per frame
    position = 50 * (1 + math.sin(frame * 0.1))  # Sinusoidal motion
    
    revolute_mate.set_angle(angle)
    linear_mate.set_position(position)

# Set up animation handler
bpy.app.handlers.frame_change_pre.append(animate_mechanism)
```

## Advanced Features

### Mate Management

```python
# Get all mates in assembly
all_mates = assembly.mate._mate_manager.get_all_mates()
print(f"Total mates: {len(all_mates)}")

# Get specific mate
hinge_mate = assembly.mate._mate_manager.get_mate("arm_hinge")
if hinge_mate:
    print(f"Hinge angle: {hinge_mate.get_angle()}")

# Remove a mate
removal_success = assembly.mate._mate_manager.remove_mate("old_constraint")

# Validate all mates
validation_results = assembly.mate._mate_manager.validate_mates()
for mate_name, is_valid in validation_results.items():
    print(f"Mate {mate_name}: {'Valid' if is_valid else 'Invalid'}")

# Solve constraint system
solve_success = assembly.mate._mate_manager.solve_mates()
```

### Constraint Customization

```python
# Access underlying Blender constraints
revolute_mate = assembly.mate.revolute(base, arm, axis, loc1, loc2)
blender_constraints = revolute_mate.constraints

for constraint in blender_constraints:
    print(f"Constraint: {constraint.name}, Type: {constraint.type}")
    
    # Modify constraint properties
    if constraint.type == 'LIMIT_ROTATION':
        constraint.influence = 0.8  # Reduce influence
        constraint.use_limit_x = False  # Remove X-axis limit
```

## Integration with Blender

### Native Blender Constraints

The mate system uses Blender's native constraint types:

- **Child Of**: For rigid connections and hierarchical relationships
- **Copy Location/Rotation**: For kinematic relationships
- **Limit Location/Rotation**: For joint constraints and limits
- **Limit Distance**: For spacing and distance constraints
- **Shrinkwrap**: For surface contact and tangent relationships

### Dependency Graph Integration

Mates integrate seamlessly with Blender's dependency graph:
- Automatic constraint evaluation order
- Efficient constraint solving
- Real-time updates during animation
- Proper handling of constraint dependencies

### Animation System Compatibility

The mate system works with Blender's animation features:
- Keyframe animation of joint parameters
- Driver-based constraint control
- Timeline-based mate activation/deactivation
- Integration with Blender's physics system

## Performance Considerations

- Mates are applied lazily when created
- Constraint evaluation is optimized through Blender's dependency graph
- Batch mate operations are supported for efficiency
- Memory usage is minimized through efficient constraint management

## Error Handling

The system provides robust error handling:
- Graceful failure for invalid mate configurations
- Detailed error messages for debugging
- Validation before mate application
- Automatic cleanup of failed mates

## Future Enhancements

Planned improvements include:
- Advanced kinematic solvers for complex assemblies
- Mate templates and presets for common mechanisms
- Visual feedback for mate relationships in Blender viewport
- Integration with Blender's geometry nodes for procedural assemblies
- Support for flexible and compliant joints
