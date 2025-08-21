# CodeToCAD Physics Simulation System

## Overview

The CodeToCAD Physics Simulation System provides a unified interface for physics simulation that works seamlessly with existing CAD workflows. The system supports multiple physics engines through a common interface, allowing users to easily switch between different simulation backends while maintaining the same API.

## Supported Physics Engines

### PyBullet Adapter
- **High-performance physics simulation** with real-time capabilities
- **Comprehensive joint system** supporting revolute, prismatic, fixed, and spherical joints
- **Advanced sensor integration** for force, position, velocity, and contact detection
- **Robot simulation support** with URDF loading and control systems
- **GUI visualization** for interactive simulation development

### MuJoCo Adapter  
- **State-of-the-art physics engine** optimized for robotics and biomechanics
- **Advanced contact dynamics** with sophisticated collision detection
- **XML model format** with automatic generation from CAD objects
- **High-frequency simulation** with parallel processing capabilities
- **Comprehensive sensor suite** including IMU, force, and vision sensors

## Architecture

The simulation system follows CodeToCAD's established architectural patterns:

```
codetocad/
├── interfaces/cad/simulation/          # Abstract interfaces
│   ├── simulation_interface.py         # Main simulation environment
│   ├── simulation_body_interface.py    # Rigid body interface
│   ├── simulation_joint_interface.py   # Joint and constraint interface
│   ├── simulation_sensor_interface.py  # Sensor interface
│   └── simulation_controller_interface.py # Controller interface
├── adapters/
│   ├── pybullet/                       # PyBullet implementation
│   │   ├── pybullet_actions/           # Modular action functions
│   │   ├── simulation/                 # Interface implementations
│   │   ├── examples/                   # Usage examples
│   │   └── README.md                   # PyBullet-specific docs
│   └── mujoco/                         # MuJoCo implementation
│       ├── mujoco_actions/             # Modular action functions
│       ├── simulation/                 # Interface implementations
│       ├── examples/                   # Usage examples
│       └── README.md                   # MuJoCo-specific docs
└── core/
    └── simulation_integration.py       # CAD-simulation integration
```

## Quick Start

### Installation

```bash
# For PyBullet support
pip install pybullet

# For MuJoCo support  
pip install mujoco

# For development with visualization
pip install pybullet[extras] mujoco[viewer]
```

### Basic Usage

```python
from codetocad.adapters.build123d import Part, Assembly
from codetocad.adapters.pybullet import Simulation  # or mujoco
from codetocad.core.simulation_integration import SimulationIntegrationHelper

# Create CAD objects
cube = Part.preset.cube(1, 1, 1)
sphere = Part.preset.sphere(0.5)

assembly = Assembly("physics_demo")
assembly.add_part(cube)
assembly.add_part(sphere)

# Set up simulation
sim, bodies = SimulationIntegrationHelper.setup_simulation_from_assembly(
    assembly, 
    simulation_type="pybullet",  # or "mujoco"
    gui=True
)

# Position objects
bodies[0].set_position((0, 0, 3))
bodies[1].set_position((2, 0, 2))

# Run simulation
sim.start()
for i in range(1000):
    sim.step()
sim.stop()
```

## Core Features

### 1. Seamless CAD Integration

Convert CodeToCAD Parts and Assemblies directly to physics bodies:

```python
# Direct part conversion
body = sim.add_part(part, position=(0, 0, 1), mass=2.0)

# Assembly conversion with automatic positioning
bodies = sim.add_assembly(assembly, position=(0, 0, 0))

# URDF generation from CAD
from codetocad.core.simulation_integration import CADToSimulationConverter
urdf_path = CADToSimulationConverter.create_urdf_from_assembly(assembly, "robot.urdf")
robot = sim.load_urdf(urdf_path)
```

### 2. Unified Physics Interface

The same API works across all physics engines:

```python
# Works with both PyBullet and MuJoCo
body.set_position((1, 2, 3))
body.apply_force((10, 0, 0))
body.set_mass(5.0)

position = body.get_position()
velocity = body.get_linear_velocity()
contacts = body.get_contact_points()
```

### 3. Advanced Joint System

Create complex mechanical systems:

```python
# Create joints between bodies
joint = sim.create_joint()
joint.create_revolute_joint(
    parent_body=base,
    child_body=arm,
    axis=(0, 0, 1),
    lower_limit=-3.14,
    upper_limit=3.14
)

# Control joint motion
joint.set_position(1.57)  # 90 degrees
joint.apply_force(10.0)   # 10 Nm torque
```

### 4. Comprehensive Sensor System

Monitor simulation state with various sensors:

```python
# Create sensors
force_sensor = sim.create_sensor()
force_sensor.create_force_sensor(body)

position_sensor = sim.create_sensor()
position_sensor.create_position_sensor(body)

imu_sensor = sim.create_sensor()
imu_sensor.create_imu_sensor(body)

# Read sensor data
force = force_sensor.read_force()
position = position_sensor.read_position()
imu_data = imu_sensor.read_data()
```

### 5. Control Systems

Implement sophisticated control algorithms:

```python
# PID controller
controller = sim.create_controller()
controller.create_pid_controller(
    joint=arm_joint,
    kp=100.0, ki=0.1, kd=10.0
)

# Trajectory following
controller.create_trajectory_controller(joints=[joint1, joint2, joint3])
positions = [[0, 0, 0], [1.57, 0, 0], [1.57, 1.57, 0]]
controller.set_trajectory(positions)

# Update controller each step
controller.update(sim.get_time_step())
```

## Engine-Specific Features

### PyBullet Advantages
- **Real-time performance** suitable for interactive applications
- **Extensive URDF support** for robot simulation
- **Built-in GUI** with debug visualization
- **Constraint solver** optimized for real-time use
- **Direct force application** and impulse simulation

### MuJoCo Advantages  
- **High-accuracy physics** with advanced contact modeling
- **Parallel simulation** for batch processing
- **XML model format** with rich feature set
- **Advanced sensors** including cameras and LiDAR
- **Optimization-friendly** for machine learning applications

## Integration Examples

### Robot Arm Simulation

```python
# Create robot arm assembly
base = Part.preset.cylinder(0.2, 0.1)
arm1 = Part.preset.cylinder(0.05, 1.0)
arm2 = Part.preset.cylinder(0.05, 0.8)

robot = Assembly("robot_arm")
robot.add_part(base)
robot.add_part(arm1) 
robot.add_part(arm2)

# Simulate with physics
sim, bodies = SimulationIntegrationHelper.setup_simulation_from_assembly(
    robot, "pybullet", gui=True
)

# Create joints between segments
joint1 = sim.create_joint()
joint1.create_revolute_joint(bodies[0], bodies[1], axis=(0, 0, 1))

joint2 = sim.create_joint()
joint2.create_revolute_joint(bodies[1], bodies[2], axis=(0, 1, 0))

# Add control system
controller = sim.create_controller()
controller.create_trajectory_controller([joint1, joint2])
```

### Multi-Physics Comparison

```python
# Same assembly, different physics engines
assembly = create_test_assembly()

# PyBullet simulation
pybullet_sim, pybullet_bodies = SimulationIntegrationHelper.setup_simulation_from_assembly(
    assembly, "pybullet"
)

# MuJoCo simulation  
mujoco_sim, mujoco_bodies = SimulationIntegrationHelper.setup_simulation_from_assembly(
    assembly, "mujoco"
)

# Compare results
for i in range(1000):
    pybullet_sim.step()
    mujoco_sim.step()
    
    # Log positions for comparison
    pb_pos = pybullet_bodies[0].get_position()
    mj_pos = mujoco_bodies[0].get_position()
```

## Performance Considerations

### PyBullet
- Optimized for **real-time simulation** (240 Hz typical)
- **Memory efficient** for moderate complexity scenes
- **GPU acceleration** available for collision detection
- Best for **interactive applications** and **real-time control**

### MuJoCo
- Optimized for **accuracy and stability** (1000+ Hz possible)
- **Vectorized operations** for maximum performance
- **Parallel simulation** support for batch processing
- Best for **research applications** and **machine learning**

## Error Handling and Debugging

The simulation system provides comprehensive error handling:

```python
try:
    sim = Simulation("test")
    sim.initialize(gui=True)
    body = sim.add_part(part)
except FileNotFoundError as e:
    print(f"File not found: {e}")
except RuntimeError as e:
    print(f"Simulation error: {e}")
finally:
    sim.disconnect()
```

Debug visualization and logging:
```python
# Enable debug output
sim.configure_debug_visualizer(enable_gui=True)

# Add debug markers
sim.add_debug_line(start_pos=(0,0,0), end_pos=(1,1,1), color=(1,0,0))
sim.add_debug_text("Debug Info", position=(0,0,1))
```

## Future Enhancements

- **Additional physics engines** (Bullet3, ODE, etc.)
- **Soft body dynamics** for deformable objects
- **Fluid simulation** integration
- **GPU acceleration** for large-scale simulations
- **Machine learning** integration for control
- **Distributed simulation** across multiple machines

## Contributing

The physics simulation system follows CodeToCAD's contribution guidelines:

1. **Interface-first design** - extend interfaces before implementations
2. **Modular architecture** - separate actions from interface implementations  
3. **Comprehensive testing** - unit tests and integration tests required
4. **Documentation** - examples and API documentation for all features
5. **Performance testing** - benchmark new features against existing implementations

## Support and Resources

- **PyBullet Documentation**: [PyBullet Quickstart Guide](https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdAvK3dsihxVUA)
- **MuJoCo Documentation**: [MuJoCo Documentation](https://mujoco.readthedocs.io/)
- **CodeToCAD Examples**: See `examples/` directories in each adapter
- **Community Support**: CodeToCAD GitHub Discussions

The physics simulation system represents a major advancement in CodeToCAD's capabilities, enabling seamless integration between design and simulation workflows while maintaining the flexibility to choose the best physics engine for each application.
