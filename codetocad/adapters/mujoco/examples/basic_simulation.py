"""
Basic MuJoCo simulation example.

This example demonstrates how to create a simple physics simulation using
the MuJoCo adapter with CodeToCAD.
"""

from codetocad.adapters.build123d import Part, Assembly
from codetocad.adapters.mujoco import Simulation
from codetocad.core.simulation_integration import SimulationIntegrationHelper
import time


def basic_simulation_example():
    """Demonstrate basic MuJoCo simulation setup."""
    print("🎯 Creating basic MuJoCo simulation...")

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
        print("Setting up MuJoCo simulation...")
        sim, bodies = SimulationIntegrationHelper.setup_simulation_from_assembly(
            assembly,
            simulation_type="mujoco",
            gui=True,  # Enable viewer for visualization
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

        for i in range(1000):  # 5 seconds at 200 Hz (MuJoCo default)
            sim.step()

            # Print positions every second
            if i % 200 == 0:
                for j, body in enumerate(bodies):
                    pos = body.get_position()
                    print(f"  {body.name}: ({pos.x:.2f}, {pos.y:.2f}, {pos.z:.2f})")

            time.sleep(1 / 200)  # Real-time simulation

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


def xml_model_example():
    """Demonstrate creating and using MuJoCo XML models."""
    print("🎯 Demonstrating MuJoCo XML model creation...")

    try:
        # Create a simple assembly
        base = Part.preset.cube(2, 2, 0.2)
        base.set_name("base")

        arm = Part.preset.cylinder(0.1, 1)
        arm.set_name("arm")

        assembly = Assembly("robot_arm")
        assembly.add_part(base)
        assembly.add_part(arm)

        # Create simulation
        sim = Simulation("xml_demo")
        sim.initialize(gui=True)

        # Generate XML from assembly
        xml_content = sim.generate_xml_from_assembly(assembly)
        print("Generated MuJoCo XML:")
        print(xml_content[:200] + "..." if len(xml_content) > 200 else xml_content)

        # Add assembly to simulation
        bodies = sim.add_assembly(assembly)

        print(f"Added {len(bodies)} bodies to simulation")

        # Run brief simulation
        sim.start()
        for i in range(200):
            sim.step()
            time.sleep(1 / 200)

        sim.stop()
        print("✅ XML model demo completed!")

        return sim, bodies

    except Exception as e:
        print(f"❌ Error in XML demo: {e}")
        return None, None
    finally:
        try:
            if "sim" in locals():
                sim.disconnect()
        except:
            pass


def advanced_physics_example():
    """Demonstrate advanced MuJoCo physics features."""
    print("🎯 Demonstrating advanced MuJoCo physics...")

    try:
        # Create multiple objects for complex interactions
        objects = []
        for i in range(3):
            obj = Part.preset.sphere(0.3)
            obj.set_name(f"sphere_{i}")
            objects.append(obj)

        assembly = Assembly("multi_body_system")
        for obj in objects:
            assembly.add_part(obj)

        # Create simulation with custom parameters
        sim = Simulation("advanced_demo")
        sim.initialize(gui=True)
        sim.set_gravity((0, 0, -9.81))
        sim.set_time_step(0.002)  # 2ms timestep for accuracy

        # Add ground plane
        sim.add_ground_plane()

        # Add objects at different positions
        bodies = []
        for i, obj in enumerate(objects):
            body = sim.add_part(
                obj,
                position=(i * 0.8, 0, 2 + i * 0.5),
                mass=1.0 + i * 0.5,  # Different masses
            )
            bodies.append(body)

        # Apply different initial conditions
        bodies[0].set_linear_velocity((1, 0, 0))
        bodies[1].set_linear_velocity((-0.5, 1, 0))
        bodies[2].apply_force((0, 0, 10))

        print("Running advanced physics simulation...")
        sim.start()

        for i in range(1000):
            sim.step()

            # Monitor system energy (simplified)
            if i % 100 == 0:
                total_kinetic = 0
                for body in bodies:
                    vel = body.get_linear_velocity()
                    mass = body.get_mass()
                    kinetic = 0.5 * mass * (vel.x**2 + vel.y**2 + vel.z**2)
                    total_kinetic += kinetic

                print(f"  Step {i}: Total kinetic energy ≈ {total_kinetic:.2f} J")

            time.sleep(1 / 500)  # Faster than real-time

        sim.stop()
        print("✅ Advanced physics demo completed!")

        return sim, bodies

    except Exception as e:
        print(f"❌ Error in advanced demo: {e}")
        return None, None
    finally:
        try:
            if "sim" in locals():
                sim.disconnect()
        except:
            pass


def sensor_integration_example():
    """Demonstrate sensor integration in MuJoCo."""
    print("🎯 Demonstrating MuJoCo sensor integration...")

    try:
        # Create a simple pendulum-like system
        base = Part.preset.cube(0.2, 0.2, 0.2)
        base.set_name("base")

        pendulum = Part.preset.cylinder(0.05, 1)
        pendulum.set_name("pendulum")

        # Create simulation
        sim = Simulation("sensor_demo")
        sim.initialize(gui=True)

        # Add parts
        base_body = sim.add_part(base, position=(0, 0, 2), mass=10.0)
        pendulum_body = sim.add_part(pendulum, position=(0, 0, 1), mass=1.0)

        # Make base static
        base_body.set_static(True)

        # Create sensors
        position_sensor = sim.create_sensor()
        position_sensor.create_position_sensor(pendulum_body)

        velocity_sensor = sim.create_sensor()
        velocity_sensor.create_velocity_sensor(pendulum_body)

        # Give pendulum initial push
        pendulum_body.set_linear_velocity((2, 0, 0))

        print("Monitoring sensor data...")
        sim.start()

        for i in range(500):
            sim.step()

            if i % 50 == 0:
                pos = position_sensor.read_position()
                vel = velocity_sensor.read_velocity()
                print(f"  Position: ({pos.x:.2f}, {pos.y:.2f}, {pos.z:.2f})")
                print(f"  Velocity: ({vel.x:.2f}, {vel.y:.2f}, {vel.z:.2f})")

            time.sleep(1 / 200)

        sim.stop()
        print("✅ Sensor integration demo completed!")

        return sim, [base_body, pendulum_body]

    except Exception as e:
        print(f"❌ Error in sensor demo: {e}")
        return None, None
    finally:
        try:
            if "sim" in locals():
                sim.disconnect()
        except:
            pass


if __name__ == "__main__":
    print("MuJoCo Simulation Examples")
    print("=" * 40)

    # Run examples
    print("\n1. Basic Simulation")
    basic_simulation_example()

    print("\n2. XML Model Creation")
    xml_model_example()

    print("\n3. Advanced Physics")
    advanced_physics_example()

    print("\n4. Sensor Integration")
    sensor_integration_example()

    print("\n🎉 All examples completed!")
