# PyBullet Physics Simulation Adapter

## Overview

This document describes the PyBullet adapter for CodeToCAD's physics simulation system. The adapter provides PyBullet-specific implementations of the simulation interfaces, enabling realistic physics simulation with PyBullet's physics engine.

## Directory Structure

```
codetocad/adapters/pybullet/
├── __init__.py                    # Module exports
├── README.md                      # This documentation
├── pybullet_actions/              # Modular action functions
│   ├── __init__.py
│   ├── simulation_setup.py        # Simulation initialization and setup
│   ├── body_management.py         # Body creation and management
│   ├── joint_management.py        # Joint creation and control
│   ├── sensor_management.py       # Sensor creation and data reading
│   ├── controller_management.py   # Controller creation and updates
│   └── file_loading.py           # URDF/STL file loading utilities
├── simulation/                    # Interface implementations
│   ├── __init__.py
│   ├── simulation.py             # Main simulation environment
│   ├── simulation_body.py        # Rigid body implementation
│   ├── simulation_joint.py       # Joint implementation
│   ├── simulation_sensor.py      # Sensor implementation
│   └── simulation_controller.py  # Controller implementation
├── cli/                          # CLI utilities
│   ├── __init__.py
│   ├── run_pybullet.py          # Run PyBullet simulations
│   └── config.py                # Configuration management
└── examples/                     # Usage examples
    ├── __init__.py
    ├── basic_simulation.py       # Basic simulation example
    ├── robot_arm_control.py      # Robot arm control example
    └── multi_body_physics.py     # Multi-body physics example
```

## Features

### Core Simulation Capabilities
- **Physics Environment**: Full PyBullet physics simulation with gravity, collision detection, and dynamics
- **GUI Support**: Optional PyBullet GUI for visualization and debugging
- **Time Stepping**: Configurable simulation time steps and real-time execution
- **Scene Management**: Ground planes, lighting, and environment setup

### Body Management
- **URDF Loading**: Load robot models and mechanisms from URDF files
- **STL Import**: Import 3D models from STL files as rigid bodies
- **CAD Integration**: Convert CodeToCAD Parts and Assemblies to simulation bodies
- **Physics Properties**: Mass, inertia, friction, restitution configuration
- **Dynamic Control**: Position, velocity, and force control of bodies

### Joint System
- **Joint Types**: Revolute, prismatic, fixed, spherical, and cylindrical joints
- **Motion Control**: Position, velocity, and force/torque control
- **Limits**: Joint position and velocity limits with enforcement
- **Constraints**: Advanced constraint systems for complex mechanisms

### Sensor Integration
- **Force Sensors**: Measure forces and torques on bodies and joints
- **Position Sensors**: Track body and joint positions and orientations
- **Contact Sensors**: Detect collisions and contact forces
- **IMU Sensors**: Inertial measurement units for acceleration and angular velocity
- **Custom Sensors**: Extensible sensor system for specialized measurements

### Control Systems
- **PID Controllers**: Proportional-integral-derivative control for joints
- **Position Control**: High-level position control with automatic force calculation
- **Velocity Control**: Velocity-based control with force limits
- **Trajectory Control**: Multi-joint trajectory following
- **Force Control**: Direct force and torque application

## Installation

The PyBullet adapter requires the PyBullet package:

```bash
pip install pybullet
```

For development with additional features:
```bash
pip install pybullet[extras]
```

## Basic Usage

### Simple Simulation Setup
```python
from codetocad.adapters.pybullet import Simulation, SimulationBody

# Create and initialize simulation
sim = Simulation("my_simulation")
sim.initialize(gui=True)  # Enable GUI for visualization
sim.set_gravity((0, 0, -9.81))

# Add ground plane
ground = sim.add_ground_plane()

# Load a robot from URDF
robot = sim.load_urdf("path/to/robot.urdf", position=(0, 0, 1))

# Run simulation
sim.start()
for i in range(1000):
    sim.step()
sim.stop()
```

### CAD Integration
```python
from codetocad.adapters.build123d import Part
from codetocad.adapters.pybullet import Simulation

# Create a CAD part
cube = Part.preset.cube(1, 1, 1)

# Add to simulation
sim = Simulation()
sim.initialize()
sim_body = sim.add_part(cube, position=(0, 0, 2), mass=1.0)

# Apply forces
sim_body.apply_force((10, 0, 0))  # Push in X direction
```

### Joint Control
```python
# Create a revolute joint between two bodies
joint = sim.create_joint()
joint.create_revolute_joint(
    parent_body=base_body,
    child_body=arm_body,
    axis=(0, 0, 1),  # Z-axis rotation
    lower_limit=-3.14,
    upper_limit=3.14
)

# Control joint position
joint.set_position(1.57)  # 90 degrees

# Apply joint torque
joint.apply_force(10.0)  # 10 Nm torque
```

### Sensor Usage
```python
# Create sensors
force_sensor = sim.create_sensor()
force_sensor.create_force_sensor(robot_body, position=(0, 0, 0))

position_sensor = sim.create_sensor()
position_sensor.create_position_sensor(robot_body)

# Read sensor data
force_data = force_sensor.read_force()
position_data = position_sensor.read_position()

print(f"Force: {force_data}, Position: {position_data}")
```

### Controller Implementation
```python
# Create PID controller for joint
controller = sim.create_controller()
controller.create_pid_controller(
    joint=arm_joint,
    kp=100.0,  # Proportional gain
    ki=0.1,    # Integral gain
    kd=10.0    # Derivative gain
)

# Set target position
controller.set_target_position(1.57)  # 90 degrees

# Update controller (called each simulation step)
controller.update(sim.get_time_step())
```

## Advanced Features

### Multi-Body Systems
```python
# Load complex robot with multiple bodies
robot_bodies = sim.load_urdf("complex_robot.urdf")

# Create joints between bodies
for i in range(len(robot_bodies) - 1):
    joint = sim.create_joint()
    joint.create_revolute_joint(robot_bodies[i], robot_bodies[i+1])
```

### Trajectory Control
```python
# Define trajectory waypoints
positions = [[0, 0, 0], [1.57, 0, 0], [1.57, 1.57, 0]]
times = [0, 1, 2]  # Time for each waypoint

# Create trajectory controller
traj_controller = sim.create_controller()
traj_controller.create_trajectory_controller(arm_joints)
traj_controller.set_trajectory(positions, times=times)
```

### Contact Detection
```python
# Create contact sensor
contact_sensor = sim.create_sensor()
contact_sensor.create_contact_sensor(gripper_body)

# Check for contacts
contacts = contact_sensor.read_contact_points()
for contact in contacts:
    print(f"Contact with {contact['body_name']} at {contact['position']}")
```

## Integration with Existing Adapters

The PyBullet adapter seamlessly integrates with existing CodeToCAD adapters:

```python
from codetocad.adapters.build123d import Part, Assembly
from codetocad.adapters.pybullet import Simulation

# Create CAD geometry
base = Part.preset.cube(2, 2, 0.1)
arm = Part.preset.cylinder(0.1, 1)

assembly = Assembly("robot_arm")
assembly.add_part(base)
assembly.add_part(arm)

# Simulate the assembly
sim = Simulation()
sim.initialize()
sim_bodies = sim.add_assembly(assembly)

# The CAD geometry is now physics-enabled
```

## Performance Considerations

- **Real-time Simulation**: PyBullet supports real-time physics simulation
- **Batch Operations**: Efficient batch processing of multiple bodies and joints
- **Memory Management**: Automatic cleanup of simulation resources
- **Multithreading**: Support for multi-threaded simulation updates

## Error Handling

The adapter provides comprehensive error handling:
- Graceful failure for invalid URDF files
- Validation of physics parameters
- Automatic recovery from simulation errors
- Detailed error messages for debugging

## Future Enhancements

- Advanced constraint solvers
- Soft body dynamics
- Fluid simulation integration
- GPU acceleration support
- Advanced visualization features
- Machine learning integration for control

## Dependencies

- `pybullet`: Core physics simulation engine
- `numpy`: Numerical computations
- `codetocad.core`: Core CodeToCAD functionality
- `codetocad.interfaces`: Simulation interfaces

The adapter follows the same organizational pattern as other CodeToCAD adapters, with modular action functions and clean interface implementations for maximum maintainability and extensibility.
