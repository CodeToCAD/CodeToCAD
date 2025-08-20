from codetocad.adapters.blender import *


def create_room():
    """Create a simple architectural model using codetocad in Blender."""

    print("🏛️ Creating architectural model...")

    # Create main assembly
    building = Assembly("architectural_model")

    # 1. Create foundation
    print("   📐 Creating foundation...")
    foundation = Part.preset.cube(10, 8, 1)
    foundation.set_name("foundation")
    foundation.move(0, 0, -0.5)  # Lower it slightly
    building.add(foundation)

    # 2. Create walls using sketches
    print("   🧱 Creating walls...")

    # Front wall
    front_wall = Part.preset.cube(10, 0.3, 3)
    front_wall.set_name("front_wall")
    front_wall.move(0, -4, 1.5)
    building.add(front_wall)

    # Back wall
    back_wall = Part.preset.cube(10, 0.3, 3)
    back_wall.set_name("back_wall")
    back_wall.move(0, 4, 1.5)
    building.add(back_wall)

    # Left wall
    left_wall = Part.preset.cube(0.3, 8, 3)
    left_wall.set_name("left_wall")
    left_wall.move(-5, 0, 1.5)
    building.add(left_wall)

    # Right wall
    right_wall = Part.preset.cube(0.3, 8, 3)
    right_wall.set_name("right_wall")
    right_wall.move(5, 0, 1.5)
    building.add(right_wall)

    # 3. Create columns
    print("   🏛️ Creating columns...")
    column_positions = [(-3, -2), (3, -2), (-3, 2), (3, 2)]

    for i, (x, y) in enumerate(column_positions):
        column = Part.preset.cylinder(0.3, 4)
        column.set_name(f"column_{i+1}")
        column.move(x, y, 2)
        building.add(column)

    # 4. Create roof
    print("   🏠 Creating roof...")
    roof = Part.preset.cube(12, 10, 0.5)
    roof.set_name("roof")
    roof.move(0, 0, 4.25)
    building.add(roof)

    # 5. Create decorative elements
    print("   ✨ Adding decorative elements...")

    # Central dome
    dome = Part.preset.sphere(1.5)
    dome.set_name("dome")
    dome.move(0, 0, 5.5)
    building.add(dome)

    # Corner spheres
    corner_positions = [(-4, -3), (4, -3), (-4, 3), (4, 3)]
    for i, (x, y) in enumerate(corner_positions):
        sphere = Part.preset.sphere(0.5)
        sphere.set_name(f"corner_sphere_{i+1}")
        sphere.move(x, y, 4.5)
        building.add(sphere)

    print(f"✅ Architectural model completed!")
    print(f"   Building contains {len(building.parts)} parts")
    print(f"   Assembly: {building}")

    return building


if __name__ == "__main__":
    run_blender(create_room, background=False, debugger=True)
