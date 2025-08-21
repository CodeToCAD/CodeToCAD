"""
Basic PyBullet simulation example.

This example demonstrates how to create a simple physics simulation using
the PyBullet adapter with CodeToCAD.
"""

from codetocad.adapters.build123d import Part, Assembly
from codetocad.adapters.pybullet import Simulation
from codetocad.core.simulation_integration import SimulationIntegrationHelper
import time


def basic_simulation_example():
    """Demonstrate basic PyBullet simulation setup."""
    print("🎯 Creating basic PyBullet simulation...")

    try:
        # Create CAD objects
        print("Creating CAD objects...")
        cube = Part.preset.cube(1, 1, 1)
        cube.set_name("falling_cube")

        sphere = Part.preset.sphere(0.5)
        sphere.set_name("rolling_sphere")

        # Create assembly
        assembly = Assembly("physics_demo")
        assembly.add_part(cube)
        assembly.add_part(sphere)

        print(f"Created assembly with {len(assembly.parts)} parts")

        # Set up simulation
        print("Setting up PyBullet simulation...")
        sim, bodies = SimulationIntegrationHelper.setup_simulation_from_assembly(
            assembly,
            simulation_type="pybullet",
            gui=True,  # Enable GUI for visualization
        )

        print(f"Created simulation with {len(bodies)} bodies")

        # Position objects
        if len(bodies) >= 2:
            bodies[0].set_position((0, 0, 3))  # Cube at height 3
            bodies[1].set_position((2, 0, 2))  # Sphere at height 2

            # Give sphere initial velocity
            bodies[1].set_linear_velocity((0, 1, 0))

        # Run simulation
        print("Running simulation for 5 seconds...")
        sim.start()

        for i in range(1200):  # 5 seconds at 240 Hz
            sim.step()

            # Print positions every second
            if i % 240 == 0:
                for j, body in enumerate(bodies):
                    pos = body.get_position()
                    print(f"  {body.name}: ({pos.x:.2f}, {pos.y:.2f}, {pos.z:.2f})")

            time.sleep(1 / 240)  # Real-time simulation

        sim.stop()
        print("✅ Simulation completed successfully!")

        return sim, bodies

    except Exception as e:
        print(f"❌ Error in simulation: {e}")
        import traceback

        traceback.print_exc()
        return None, None
    finally:
        # Cleanup
        try:
            if "sim" in locals():
                sim.disconnect()
        except:
            pass


def force_application_example():
    """Demonstrate applying forces to bodies."""
    print("🎯 Demonstrating force application...")

    try:
        # Create a simple cube
        cube = Part.preset.cube(1, 1, 1)
        cube.set_name("force_cube")

        # Create simulation
        sim = Simulation("force_demo")
        sim.initialize(gui=True)
        sim.add_ground_plane()

        # Add cube to simulation
        body = sim.add_part(cube, position=(0, 0, 2), mass=2.0)

        print("Applying forces to cube...")
        sim.start()

        for i in range(600):  # 2.5 seconds
            # Apply upward force for first second
            if i < 240:
                body.apply_force((0, 0, 20))  # Upward force
            # Apply sideways force for next second
            elif i < 480:
                body.apply_force((10, 0, 0))  # Sideways force

            sim.step()

            if i % 60 == 0:  # Print every 0.25 seconds
                pos = body.get_position()
                vel = body.get_linear_velocity()
                print(f"  Position: ({pos.x:.2f}, {pos.y:.2f}, {pos.z:.2f})")
                print(f"  Velocity: ({vel.x:.2f}, {vel.y:.2f}, {vel.z:.2f})")

            time.sleep(1 / 240)

        sim.stop()
        print("✅ Force application demo completed!")

        return sim, body

    except Exception as e:
        print(f"❌ Error in force demo: {e}")
        return None, None
    finally:
        try:
            if "sim" in locals():
                sim.disconnect()
        except:
            pass


def contact_detection_example():
    """Demonstrate contact detection between objects."""
    print("🎯 Demonstrating contact detection...")

    try:
        # Create two cubes
        cube1 = Part.preset.cube(1, 1, 1)
        cube1.set_name("cube1")

        cube2 = Part.preset.cube(1, 1, 1)
        cube2.set_name("cube2")

        # Create simulation
        sim = Simulation("contact_demo")
        sim.initialize(gui=True)
        sim.add_ground_plane()

        # Add cubes
        body1 = sim.add_part(cube1, position=(0, 0, 3), mass=1.0)
        body2 = sim.add_part(cube2, position=(0, 0, 1), mass=1.0)

        # Make second cube static
        body2.set_static(True)

        print("Monitoring contacts...")
        sim.start()

        contact_detected = False
        for i in range(600):
            sim.step()

            # Check for contacts
            contacts = body1.get_contact_points()
            if contacts and not contact_detected:
                print("🔥 Contact detected!")
                for contact in contacts:
                    print(f"  Contact force: {contact.get('normal_force', 0):.2f}")
                contact_detected = True

            if i % 60 == 0:
                pos1 = body1.get_position()
                print(f"  Cube1 height: {pos1.z:.2f}")

            time.sleep(1 / 240)

        sim.stop()
        print("✅ Contact detection demo completed!")

        return sim, [body1, body2]

    except Exception as e:
        print(f"❌ Error in contact demo: {e}")
        return None, None
    finally:
        try:
            if "sim" in locals():
                sim.disconnect()
        except:
            pass


if __name__ == "__main__":
    print("PyBullet Simulation Examples")
    print("=" * 40)

    # Run examples
    print("\n1. Basic Simulation")
    basic_simulation_example()

    print("\n2. Force Application")
    force_application_example()

    print("\n3. Contact Detection")
    contact_detection_example()

    print("\n🎉 All examples completed!")
