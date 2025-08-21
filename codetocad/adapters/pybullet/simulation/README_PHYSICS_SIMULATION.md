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

## 1. Architecture

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

## 2. Physical Properties Enhancement ✅

### New Part Properties
Added comprehensive physical properties to `PartInterface`:

```python
class PartInterface:
    # Physical properties for simulation
    category: PartCategory = PartCategory.RIGID_BODY
    mass: float | None = None  # kg, None means use density * volume
    inertia: tuple[float, float, float] | None = None  # Ixx, Iyy, Izz
    material: str = "default"
    color: tuple[float, float, float, float] = (0.8, 0.8, 0.8, 1.0)  # RGBA
    friction: float = 0.5
    restitution: float = 0.1  # bounciness
    density: float = 1000.0  # kg/m³
    damping: tuple[float, float] = (0.1, 0.1)  # linear, angular
```

### Part Categories
```python
class PartCategory(Enum):
    RIGID_BODY = "rigid_body"
    SOFT_BODY = "soft_body"
    FLUID = "fluid"
    SENSOR = "sensor"
    ACTUATOR = "actuator"
    PARTICLE_SYSTEM = "particle_system"
```

### Property Management Methods
- `set_physical_properties()` - Set multiple properties at once
- `get_effective_mass()` - Calculate mass from density if not explicitly set

## 3. Kinematic Constraint Detection ✅

### Enhanced add_assembly Method
```python
def add_assembly(
    self,
    assembly: "AssemblyInterface",
    position: Point | tuple[float, float, float] = (0, 0, 0),
    orientation: tuple[float, float, float, float] = (0, 0, 0, 1),
    detect_constraints: bool = True,  # NEW PARAMETER
    **kwargs,
) -> Sequence["SimulationBodyInterface"]:
```

### Constraint Detection Pipeline
1. **Assembly Analysis** - `detect_kinematic_constraints(assembly)`
2. **Mate Conversion** - `_mate_to_constraint(mate)`
3. **Joint Creation** - `create_joint_from_constraint(constraint, body1, body2)`

### Supported Constraint Types
- Fixed joints
- Revolute joints
- Prismatic joints
- Custom constraint parameters (position, axis, limits)

## 4. Export Functionality ✅

### New Export Interface
Created `SimulationExportInterface` with comprehensive export capabilities:

```python
class SimulationExportInterface:
    def urdf(filename, include_visuals=True, include_collisions=True, include_inertials=True)
    def sdf(filename, version="1.7", include_physics=True)
    def xml(filename, format_type="mujoco")
    def state(filename, format="json", include_velocities=True, include_forces=False)
    def trajectory(filename, format="csv", bodies=None)
    def scene(filename, include_cameras=True, include_lights=True)
```

### Export Implementations
- **PyBullet**: `PyBulletSimulationExport`
- **MuJoCo**: `MuJoCoSimulationExport`

### Usage
```python
# Export simulation model to URDF
simulation.export.urdf("robot.urdf")

# Export to MuJoCo XML format
simulation.export.xml("model.xml", format_type="mujoco")

# Export current simulation state
simulation.export.state("state.json", include_velocities=True)

# Export complete scene with cameras and lights
simulation.export.scene("scene.json")
```

## 5. Camera and Light Support ✅

### New Interfaces
- **CameraInterface** - Comprehensive camera system
- **LightInterface** - Advanced lighting system

### Camera Features
```python
class CameraInterface:
    # Camera types: PERSPECTIVE, ORTHOGRAPHIC, FISHEYE
    # Properties: position, target, up_vector, field_of_view, aspect_ratio
    # Resolution control, clipping planes
    # View and projection matrix calculation
    # Ray casting for computer vision
```

### Light Features
```python
class LightInterface:
    # Light types: DIRECTIONAL, POINT, SPOT, AREA, AMBIENT
    # Properties: position, direction, intensity, color
    # Attenuation parameters, shadow control
    # Spot light parameters, area light sizing
```

### Assembly Integration
```python
class AssemblyInterface:
    cameras: list["CameraInterface"] = []
    lights: list["LightInterface"] = []
    
    def add_camera(camera)
    def add_light(light)
    def get_camera_by_name(name)
    def get_light_by_name(name)
```

### Simulation Integration
```python
class SimulationInterface:
    cameras: list["CameraInterface"] = []
    lights: list["LightInterface"] = []
    
    # Automatic transfer from assemblies
    # Export support in all formats
```

## 6. Implementation Details

### PyBullet Adapter ✅
- **Enhanced** `add_part()` to use physical properties from parts
- **Updated** `add_assembly()` with constraint detection
- **Added** `PyBulletSimulationExport` with URDF, SDF, XML, state export
- **Integrated** camera and light support
- **Implemented** joint creation from constraints

### MuJoCo Adapter ✅
- **Enhanced** `add_part()` to use physical properties from parts
- **Updated** `add_assembly()` with constraint detection
- **Added** `MuJoCoSimulationExport` with native XML export
- **Integrated** camera and light support in XML generation
- **Implemented** joint creation from constraints

## 7. Usage Examples

### Setting Physical Properties
```python
part = Part()
part.set_physical_properties(
    category=PartCategory.RIGID_BODY,
    mass=2.5,
    friction=0.8,
    restitution=0.3,
    color=(0.9, 0.1, 0.1, 1.0),  # Red
    material="steel"
)
```

### Creating Assembly with Cameras and Lights
```python
assembly = Assembly()
assembly.add_part(part1)
assembly.add_part(part2)

# Add camera
camera = Camera()
camera.set_name("main_camera")
camera.look_at(
    position=(5, 5, 5),
    target=(0, 0, 0),
    up=(0, 0, 1)
)
assembly.add_camera(camera)

# Add light
light = Light()
light.create_point_light(
    position=(3, 3, 3),
    intensity=1.0,
    color=(1.0, 1.0, 1.0)
)
assembly.add_light(light)
```

### Running Simulation with Enhanced Features
```python
# Create simulation
sim = Simulation("enhanced_simulation")
sim.initialize(gui=True)

# Add assembly with automatic constraint detection
bodies = sim.add_assembly(assembly, detect_constraints=True)

# Export various formats
sim.export.urdf("model.urdf")
sim.export.xml("model.xml", format_type="mujoco")
sim.export.scene("scene.json", include_cameras=True, include_lights=True)

# Run simulation
sim.start()
for _ in range(1000):
    sim.step()
sim.stop()

# Export final state and trajectory
sim.export.state("final_state.json")
sim.export.trajectory("trajectory.csv")
```

## 8. Benefits

### For Users
- **Simplified workflow** from CAD to simulation
- **Automatic constraint detection** from assembly mates
- **Rich physical properties** for realistic simulation
- **Comprehensive export options** for various tools
- **Camera and lighting support** for visualization

### For Developers
- **Cleaner architecture** with reduced redundancy
- **Extensible export system** for new formats
- **Consistent interface** across physics engines
- **Better separation of concerns** between CAD and simulation

### For Integration
- **Seamless CAD-to-simulation** conversion
- **Automatic joint creation** from assembly constraints
- **Multi-format export** for tool interoperability
- **Scene description** with cameras and lights

## 9. Future Enhancements

### Potential Additions
- **Soft body simulation** support
- **Fluid dynamics** integration
- **Advanced materials** with temperature, conductivity
- **Sensor simulation** (cameras, LIDAR, IMU)
- **Actuator modeling** (motors, servos)
- **Real-time visualization** improvements
- **Trajectory optimization** tools
- **Multi-physics coupling** (thermal, electromagnetic)

This refactoring provides a solid foundation for advanced physics simulation capabilities while maintaining clean, extensible architecture.
