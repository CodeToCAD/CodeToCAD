# MuJoCo Physics Simulation Adapter

## Overview

This document describes the MuJoCo adapter for CodeToCAD's physics simulation system. The adapter provides MuJoCo-specific implementations of the simulation interfaces, enabling high-performance physics simulation with MuJoCo's advanced physics engine.

## Directory Structure

```
codetocad/adapters/mujoco/
├── __init__.py                    # Module exports
├── README.md                      # This documentation
├── mujoco_actions/                # Modular action functions
│   ├── __init__.py
│   ├── simulation_setup.py        # Simulation initialization and setup
│   ├── body_management.py         # Body creation and management
│   ├── joint_management.py        # Joint creation and control
│   ├── sensor_management.py       # Sensor creation and data reading
│   ├── controller_management.py   # Controller creation and updates
│   ├── file_loading.py           # XML file loading utilities
│   └── xml_generation.py         # XML model generation utilities
├── simulation/                    # Interface implementations
│   ├── __init__.py
│   ├── simulation.py             # Main simulation environment
│   ├── simulation_body.py        # Rigid body implementation
│   ├── simulation_joint.py       # Joint implementation
│   ├── simulation_sensor.py      # Sensor implementation
│   └── simulation_controller.py  # Controller implementation
├── cli/                          # CLI utilities
│   ├── __init__.py
│   ├── run_mujoco.py            # Run MuJoCo simulations
│   └── config.py                # Configuration management
└── examples/                     # Usage examples
    ├── __init__.py
    ├── basic_simulation.py       # Basic simulation example
    ├── robot_control.py          # Robot control example
    ├── humanoid_simulation.py    # Humanoid robot example
    └── contact_dynamics.py       # Contact dynamics example
```

## Features

### Core Simulation Capabilities
- **High-Performance Physics**: MuJoCo's optimized physics engine for fast, accurate simulation
- **Advanced Contact Dynamics**: Sophisticated contact modeling and collision detection
- **Visualization**: Built-in viewer for real-time simulation visualization
- **XML Model Format**: Native MuJoCo XML model format with automatic generation
- **Parallel Simulation**: Support for parallel simulation instances

### Body Management
- **XML Model Loading**: Load complex models from MuJoCo XML files
- **STL Integration**: Convert STL files to MuJoCo mesh assets
- **CAD Integration**: Convert CodeToCAD Parts and Assemblies to MuJoCo bodies
- **Advanced Materials**: Comprehensive material property specification
- **Composite Bodies**: Support for complex multi-body systems

### Joint System
- **Comprehensive Joint Types**: All MuJoCo joint types including ball, slide, hinge, and free joints
- **Actuator System**: Advanced actuator models for motors, cylinders, and muscles
- **Constraint Solving**: High-performance constraint solver for complex mechanisms
- **Joint Limits**: Position, velocity, and force limits with smooth enforcement
- **Gear Ratios**: Support for gear trains and transmission systems

### Sensor Integration
- **Rich Sensor Suite**: Force, torque, position, velocity, acceleration, and gyroscope sensors
- **Contact Sensors**: Detailed contact force and pressure measurements
- **Vision Sensors**: Camera sensors for computer vision applications
- **Custom Sensors**: Extensible sensor framework for specialized measurements
- **High-Frequency Sampling**: Support for high-frequency sensor data collection

### Control Systems
- **Actuator Control**: Direct control of MuJoCo actuators with various control modes
- **PID Controllers**: Built-in PID control with automatic tuning capabilities
- **Model Predictive Control**: Advanced MPC implementations for optimal control
- **Inverse Dynamics**: Computed torque control using MuJoCo's inverse dynamics
- **Trajectory Optimization**: Integration with trajectory optimization algorithms

## Installation

The MuJoCo adapter requires the MuJoCo package:

```bash
pip install mujoco
```

For development with visualization:
```bash
pip install mujoco[viewer]
```

## Basic Usage

### Simple Simulation Setup
```python
from codetocad.adapters.mujoco import Simulation, SimulationBody

# Create and initialize simulation
sim = Simulation("my_simulation")
sim.initialize(gui=True)  # Enable viewer for visualization
sim.set_gravity((0, 0, -9.81))

# Add ground plane
ground = sim.add_ground_plane()

# Load a robot from XML
robot = sim.load_xml("path/to/robot.xml")

# Run simulation
sim.start()
for i in range(1000):
    sim.step()
sim.stop()
```

### CAD Integration
```python
from codetocad.adapters.build123d import Part
from codetocad.adapters.mujoco import Simulation

# Create a CAD part
sphere = Part.preset.sphere(0.5)

# Add to simulation
sim = Simulation()
sim.initialize()
sim_body = sim.add_part(sphere, position=(0, 0, 2), mass=1.0)

# Apply forces
sim_body.apply_force((10, 0, 0))  # Push in X direction
```

### Advanced Joint Control
```python
# Create a hinge joint with actuator
joint = sim.create_joint()
joint.create_revolute_joint(
    parent_body=base_body,
    child_body=arm_body,
    axis=(0, 0, 1),  # Z-axis rotation
    lower_limit=-3.14,
    upper_limit=3.14
)

# Create actuator for the joint
actuator = sim.create_actuator(joint, actuator_type="motor")

# Control joint with actuator
actuator.set_control(10.0)  # Apply 10 Nm torque
```

### Sensor Usage
```python
# Create advanced sensors
force_sensor = sim.create_sensor()
force_sensor.create_force_sensor(robot_body, position=(0, 0, 0))

accelerometer = sim.create_sensor()
accelerometer.create_accelerometer(robot_body)

gyroscope = sim.create_sensor()
gyroscope.create_gyro(robot_body)

# Read sensor data
force_data = force_sensor.read_force()
accel_data = accelerometer.read_acceleration()
gyro_data = gyroscope.read_angular_velocity()
```

### Model Predictive Control
```python
# Create MPC controller
controller = sim.create_controller()
controller.create_mpc_controller(
    joints=arm_joints,
    horizon=10,  # 10-step prediction horizon
    cost_weights={'position': 1.0, 'velocity': 0.1, 'control': 0.01}
)

# Set target trajectory
target_positions = [[0, 0, 0], [1.57, 0, 0], [1.57, 1.57, 0]]
controller.set_target_trajectory(target_positions)

# Update controller
controller.update(sim.get_time_step())
```

## Advanced Features

### XML Model Generation
```python
# Generate XML model from CAD assembly
from codetocad.adapters.build123d import Assembly

assembly = Assembly("robot")
# ... add parts to assembly

# Convert to MuJoCo XML
xml_model = sim.generate_xml_from_assembly(assembly)
sim.load_xml_string(xml_model)
```

### Contact Dynamics
```python
# Configure contact parameters
sim.set_contact_parameters(
    friction=0.8,
    restitution=0.1,
    contact_stiffness=1000,
    contact_damping=10
)

# Monitor contact forces
contact_sensor = sim.create_sensor()
contact_sensor.create_contact_sensor(gripper_body)

contacts = contact_sensor.read_contact_points()
for contact in contacts:
    print(f"Contact force: {contact['force']}")
```

### Parallel Simulation
```python
# Create multiple simulation instances
simulations = []
for i in range(4):
    sim = Simulation(f"sim_{i}")
    sim.initialize()
    simulations.append(sim)

# Run simulations in parallel
import concurrent.futures

def run_simulation(sim):
    for _ in range(1000):
        sim.step()
    return sim.get_simulation_data()

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(run_simulation, simulations)
```

## Integration with Existing Adapters

The MuJoCo adapter seamlessly integrates with existing CodeToCAD adapters:

```python
from codetocad.adapters.build123d import Part, Assembly
from codetocad.adapters.mujoco import Simulation

# Create complex CAD geometry
base = Part.preset.cube(2, 2, 0.1)
arm1 = Part.preset.cylinder(0.1, 1)
arm2 = Part.preset.cylinder(0.1, 0.8)

assembly = Assembly("robot_arm")
assembly.add_part(base)
assembly.add_part(arm1)
assembly.add_part(arm2)

# Convert to high-performance MuJoCo simulation
sim = Simulation()
sim.initialize()
sim_bodies = sim.add_assembly(assembly)

# The CAD geometry is now physics-enabled with MuJoCo's advanced features
```

## Performance Considerations

- **Vectorized Operations**: MuJoCo's vectorized computations for maximum performance
- **GPU Acceleration**: Optional GPU acceleration for large-scale simulations
- **Memory Efficiency**: Optimized memory usage for complex models
- **Batch Processing**: Efficient batch processing of multiple simulation instances
- **Real-time Capability**: Real-time simulation for interactive applications

## Error Handling

The adapter provides comprehensive error handling:
- Validation of XML model files
- Automatic model compilation and error reporting
- Graceful handling of simulation instabilities
- Detailed error messages with suggestions for fixes

## Future Enhancements

- Machine learning integration for control
- Advanced visualization features
- Soft body dynamics
- Fluid-structure interaction
- Distributed simulation across multiple machines
- Integration with reinforcement learning frameworks

## Dependencies

- `mujoco`: Core physics simulation engine
- `numpy`: Numerical computations
- `xml.etree.ElementTree`: XML parsing and generation
- `codetocad.core`: Core CodeToCAD functionality
- `codetocad.interfaces`: Simulation interfaces

The adapter follows the same organizational pattern as other CodeToCAD adapters, with modular action functions and clean interface implementations optimized for MuJoCo's unique capabilities and performance characteristics.
