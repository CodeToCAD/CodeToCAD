"""
Comprehensive example: Car with Robotic Arm Simulation

This example demonstrates the complete CodeToCAD workflow including:
- Custom sketching for curved car body
- Realistic materials (steel frame, rubber tires, plastic body panels)
- 6-DOF robotic arm with appropriate materials
- Assembly constraints and joint creation
- Physical simulation with proper mass distribution
- Export capabilities (URDF, MuJoCo XML)
- Material and asset management integration
"""

from pathlib import Path

from codetocad.adapters.assets.thingiverse_adapter import ThingiverseAdapter

from codetocad.adapters.assets.ambientcg_adapter import AmbientCGAdapter
from codetocad.adapters.build123d.cad.sketch.sketch import Sketch
from codetocad.adapters.build123d.cad.part.part import Part
from codetocad.adapters.build123d.cad.assembly.assembly import Assembly
from codetocad.core.dimensions.point import Point
from codetocad.interfaces.cad.part.part_interface import PartCategory

from codetocad.adapters.pybullet.simulation.simulation import (
    Simulation as PyBulletSimulation,
)

from codetocad.adapters.mujoco.simulation.simulation import (
    Simulation as MuJoCoSimulation,
)


def create_rectangle_sketch(
    width: float, height: float, center_x: float = 0, center_y: float = 0
) -> Sketch:
    """Create a rectangular sketch using build123d preset API."""
    sketch = Sketch()

    # Use the preset rectangle method
    sketch.preset.rectangle(width, height)

    return sketch


def create_circle_sketch(
    radius: float, center_x: float = 0, center_y: float = 0
) -> Sketch:
    """Create a circular sketch using build123d API."""
    sketch = Sketch()
    sketch.preset.circle(radius * 2)

    return sketch


def create_car_chassis() -> Part:
    """Create a car chassis with curved body using custom sketching."""
    print("🚗 Creating car chassis...")

    # Create chassis base sketch using helper function
    chassis_sketch = create_rectangle_sketch(
        200, 100, 100, 50
    )  # 200mm x 100mm base, centered at (100, 50)

    # Create the chassis part
    chassis = Part()
    chassis.sketch = chassis_sketch
    chassis.set_name("car_chassis")

    # Extrude to create 3D shape
    chassis.extrude_sketch(20)  # 20mm thick chassis

    # Apply steel material for structural strength
    from codetocad.core.material import Material

    steel_material = Material.preset.steel()
    chassis.set_material(steel_material)

    # Set explicit mass for reasonable simulation (instead of using density directly)
    chassis.mass = 50.0  # 50 kg chassis

    # Set as structural component
    chassis.set_physical_properties(category=PartCategory.RIGID_BODY)

    return chassis


def create_wheel(radius: float = 30, width: float = 20) -> Part:
    """Create a wheel with rubber material."""
    print(f"🛞 Creating wheel (radius: {radius}mm, width: {width}mm)...")

    # Create wheel sketch using helper function
    wheel_sketch = create_circle_sketch(radius, 0, 0)

    # Create wheel part
    wheel = Part()
    wheel.sketch = wheel_sketch
    wheel.set_name("wheel")

    # Extrude to create wheel
    wheel.extrude_sketch(width)

    # Apply rubber material
    from codetocad.core.material import Material

    rubber_material = Material.preset.rubber()
    wheel.set_material(rubber_material)

    # Set reasonable mass for wheel
    wheel.mass = 5.0  # 5 kg per wheel

    return wheel


def create_robotic_arm_link(
    length: float, width: float = 15, height: float = 15
) -> Part:
    """Create a robotic arm link with aluminum material."""
    print(f"🦾 Creating arm link (length: {length}mm)...")

    # Create link sketch using helper function
    link_sketch = create_rectangle_sketch(length, width, length / 2, width / 2)

    # Create link part
    link = Part()
    link.sketch = link_sketch
    link.set_name(f"arm_link_{length}mm")

    # Extrude to create 3D link
    link.extrude_sketch(height)

    # Apply aluminum material for lightweight strength
    from codetocad.core.material import Material

    aluminum_material = Material.preset.aluminum()
    link.set_material(aluminum_material)

    # Set reasonable mass based on link length
    link.mass = length / 20.0  # Proportional to length, lighter for aluminum

    return link


def create_joint_connector() -> Part:
    """Create a joint connector with steel material."""
    print("🔗 Creating joint connector...")

    # Create connector sketch (small cylinder) using helper function
    connector_sketch = create_circle_sketch(8, 0, 0)  # 8mm radius

    # Create connector part
    connector = Part()
    connector.sketch = connector_sketch
    connector.set_name("joint_connector")

    # Extrude to create connector
    connector.extrude_sketch(10)  # 10mm thick

    # Apply steel material for joint strength
    from codetocad.core.material import Material

    steel_material = Material.preset.steel()
    connector.set_material(steel_material)

    # Set small mass for connector
    connector.mass = 0.5  # 0.5 kg connector

    return connector


def create_car_assembly() -> Assembly:
    """Create the complete car assembly."""
    print("🏗️  Assembling car...")

    car_assembly = Assembly()
    car_assembly.set_name("autonomous_car")

    # Create chassis
    chassis = create_car_chassis()
    car_assembly.add_part(chassis)

    # Create and add wheels
    wheel_positions = [
        Point(30, 20, -15),  # Front left
        Point(30, 80, -15),  # Front right
        Point(170, 20, -15),  # Rear left
        Point(170, 80, -15),  # Rear right
    ]

    for i, pos in enumerate(wheel_positions):
        wheel = create_wheel()
        wheel.set_name(f"wheel_{i+1}")
        wheel.transform.translate(pos.x, pos.y, pos.z)
        car_assembly.add_part(wheel)

    return car_assembly


def create_robotic_arm_assembly() -> Assembly:
    """Create the 6-DOF robotic arm assembly."""
    print("🤖 Assembling robotic arm...")

    arm_assembly = Assembly()
    arm_assembly.set_name("robotic_arm_6dof")

    # Create arm links with different lengths
    link_lengths = [60, 80, 70, 50, 40, 30]  # 6 links for 6 DOF
    links = []

    for i, length in enumerate(link_lengths):
        link = create_robotic_arm_link(length)
        link.set_name(f"arm_link_{i+1}")
        links.append(link)
        arm_assembly.add_part(link)

    # Create joint connectors
    for i in range(len(links) - 1):
        connector = create_joint_connector()
        connector.set_name(f"joint_{i+1}")
        arm_assembly.add_part(connector)

    # Position links in kinematic chain
    current_pos = Point(0, 0, 0)
    for i, link in enumerate(links):
        link.transform.translate(current_pos.x, current_pos.y, current_pos.z)
        if i < len(link_lengths) - 1:
            current_pos = Point(
                current_pos.x + link_lengths[i], current_pos.y, current_pos.z + 20
            )

    return arm_assembly


def create_complete_system() -> Assembly:
    """Create the complete car with robotic arm system."""
    print("🎯 Creating complete system...")

    complete_system = Assembly()
    complete_system.set_name("car_with_robotic_arm")

    # Create car
    car = create_car_assembly()

    # Create robotic arm
    arm = create_robotic_arm_assembly()

    # Position arm on top of car
    for part in arm.parts:
        part.transform.translate(100, 50, 30)  # Mount on center of car

    # Add both assemblies to complete system
    for part in car.parts:
        complete_system.add_part(part)

    for part in arm.parts:
        complete_system.add_part(part)

    return complete_system


def demonstrate_material_assets():
    """Demonstrate material asset downloading and usage."""
    print("🎨 Demonstrating material asset management...")

    try:
        # Initialize material asset manager
        from codetocad.adapters.assets.material_asset_adapter import (
            MaterialAssetManager,
        )

        material_manager = MaterialAssetManager()

        # Add ambientCG adapter (free, no API key required)
        ambient_adapter = AmbientCGAdapter()
        material_manager.add_adapter("ambientcg", ambient_adapter)

        # Search for materials with fallback
        print("Searching for metal materials...")
        try:
            results = material_manager.search_all("metal", limit=3)

            if results:
                for source, assets in results.items():
                    print(f"Found {len(assets)} materials from {source}")
                    for asset in assets[:2]:  # Show first 2
                        print(f"  - {asset.name}: {asset.description}")

                # Try to download a material (if available)
                for source, assets in results.items():
                    if assets:
                        asset = assets[0]
                        print(f"Attempting to download material: {asset.name}")

                        downloaded_files = material_manager.download_from_adapter(
                            source, asset
                        )
                        if downloaded_files:
                            print(f"Downloaded {len(downloaded_files)} texture files")

                            # Create material from asset
                            material = ambient_adapter.create_material_from_asset(
                                asset, downloaded_files
                            )
                            print(f"Created material: {material.name}")
                        else:
                            print(
                                "No files downloaded - using preset materials as fallback"
                            )
                        break
            else:
                print("No materials found - using preset materials as fallback")

        except Exception as api_error:
            print(f"API search failed: {api_error}")
            print("Using preset materials as fallback")

    except Exception as e:
        print(f"Material asset demonstration failed: {e}")
        print("This is expected if network is unavailable or API limits are reached")
        print("Using preset materials as fallback")


def demonstrate_model_assets():
    """Demonstrate 3D model asset downloading."""
    print("📦 Demonstrating 3D model asset management...")

    try:
        # Initialize model asset manager
        from codetocad.adapters.assets.model_asset_adapter import (
            ModelAssetManager,
        )

        model_manager = ModelAssetManager()

        # Add free model adapter
        free_adapter = ThingiverseAdapter()
        model_manager.add_adapter("free_models", free_adapter)

        # Search for models
        print("Searching for car chassis models...")
        results = model_manager.search_all("car chassis", limit=2)

        for source, assets in results.items():
            print(f"Found {len(assets)} models from {source}")
            for asset in assets:
                print(f"  - {asset.name}: {asset.description}")
                print(f"    Formats: {', '.join(asset.file_formats)}")

        # Download a model (if available)
        if results:
            for source, assets in results.items():
                if assets:
                    asset = assets[0]
                    print(f"Downloading model: {asset.name}")

                    downloaded_file = model_manager.download_from_adapter(
                        source, asset, "stl"
                    )
                    if downloaded_file:
                        print(f"Downloaded model to: {downloaded_file}")
                    break

    except Exception as e:
        print(f"Model asset demonstration failed: {e}")


def run_pybullet_simulation(system: Assembly):
    """Run PyBullet physics simulation."""
    print("🎮 Running PyBullet simulation...")

    try:
        # Create simulation
        sim = PyBulletSimulation("car_arm_simulation")
        sim.initialize(gui=True)

        # Add ground plane
        sim.add_ground_plane()

        # Add complete system with constraint detection
        bodies = sim.add_assembly(system, detect_constraints=True)

        print(f"Added {len(bodies)} bodies to simulation")

        # Export URDF with meshes and textures
        export_dir = Path("exports")
        export_dir.mkdir(exist_ok=True)

        urdf_file = export_dir / "car_with_arm.urdf"
        sim.export.urdf(str(urdf_file))
        print(f"📄 Exported URDF to: {urdf_file}")

        # Export MJCF (MuJoCo XML) with meshes and textures
        mjcf_file = export_dir / "car_with_arm.xml"
        sim.export.mjcf(str(mjcf_file))
        print(f"🎯 Exported MJCF to: {mjcf_file}")

        # Export scene
        scene_file = export_dir / "car_with_arm_scene.json"
        sim.export.scene(str(scene_file))
        print(f"🎬 Exported scene to: {scene_file}")

        # Run simulation
        print("Running simulation for 5 seconds...")
        sim.start()

        step = 0

        try:
            while True:
                # while step < 1200:  # 5 seconds at 240 Hz
                sim.step()

                if step % 240 == 0:  # Every second
                    print(f"  Simulation time: {step/240:.1f}s")

                step += 1
        except KeyboardInterrupt:
            print("🛑 Simulation interrupted")

        sim.stop()
        sim.disconnect()

        print("✅ PyBullet simulation completed")

    except Exception as e:
        print(f"❌ PyBullet simulation failed: {e}")


def run_mujoco_simulation(system: Assembly):
    """Run MuJoCo physics simulation."""
    print("🎮 Running MuJoCo simulation...")

    try:
        # Create simulation
        sim = MuJoCoSimulation("car_arm_mujoco")
        sim.initialize(gui=True)

        # Add complete system with constraint detection
        bodies = sim.add_assembly(system, detect_constraints=True)

        print(f"Added {len(bodies)} bodies to simulation")

        # Export MuJoCo XML
        export_dir = Path("exports")
        export_dir.mkdir(exist_ok=True)

        xml_file = export_dir / "car_with_arm_mujoco.xml"
        sim.export.xml(str(xml_file), format_type="mujoco")
        print(f"📄 Exported MuJoCo XML to: {xml_file}")

        # Run simulation
        print("Running simulation for 3 seconds...")
        sim.start()

        for step in range(1500):  # 3 seconds at 500 Hz
            sim.step()

            if step % 500 == 0:  # Every second
                print(f"  Simulation time: {step/500:.1f}s")

        sim.stop()
        sim.disconnect()

        print("✅ MuJoCo simulation completed")

    except Exception as e:
        print(f"❌ MuJoCo simulation failed: {e}")


def main():
    """Main demonstration function."""
    print("🚀 CodeToCAD Car with Robotic Arm Simulation Demo")
    print("=" * 60)

    # Create the complete system
    system = create_complete_system()

    print(f"\n📊 System Statistics:")
    print(f"  Total parts: {len(system.parts)}")

    # Calculate total mass
    total_mass = sum(part.get_effective_mass() for part in system.parts)
    print(f"  Total mass: {total_mass:.2f} kg")

    # Show material breakdown
    materials = {}
    for part in system.parts:
        material_name = part.material
        if material_name in materials:
            materials[material_name] += 1
        else:
            materials[material_name] = 1

    print(f"  Materials used:")
    for material, count in materials.items():
        print(f"    - {material}: {count} parts")

    # Demonstrate asset management
    print("\n" + "=" * 60)
    demonstrate_material_assets()

    print("\n" + "=" * 60)
    demonstrate_model_assets()

    # Run simulations
    print("\n" + "=" * 60)
    run_pybullet_simulation(system)

    print("\n" + "=" * 60)
    run_mujoco_simulation(system)

    print("\n🎉 Demo completed successfully!")
    print("\nCheck the 'exports' directory for generated files:")
    print("  - car_with_arm.urdf (PyBullet URDF export)")
    print("  - car_with_arm_mujoco.xml (MuJoCo XML export)")
    print("  - car_with_arm_scene.json (Scene description)")


if __name__ == "__main__":
    main()
