import pytest

"""
Test script for Blender CAD implementations.
"""


@pytest.mark.skipif(
    "bpy" not in locals(), reason="This test can only be run in Blender"
)
def test_blender_cad_implementations():
    """Test the Blender CAD implementations."""

    # Import the Blender CAD implementations
    from codetocad.adapters.blender import Vertex, Edge, Wire, Sketch, Part, Assembly

    print("🔧 Testing Blender CAD Implementations")
    print("=" * 50)

    # Test 1: Create vertices
    print("\n1. Creating vertices...")
    v1 = Vertex(0, 0, 0, name="origin")
    v2 = Vertex(1, 0, 0, name="x_axis")
    v3 = Vertex(1, 1, 0, name="corner")
    v4 = Vertex(0, 1, 0, name="y_axis")
    print(f"   Created vertices: {v1}, {v2}, {v3}, {v4}")

    # Test 2: Create edges
    print("\n2. Creating edges...")
    e1 = Edge(v1, v2, name="bottom_edge")
    e2 = Edge(v2, v3, name="right_edge")
    e3 = Edge(v3, v4, name="top_edge")
    e4 = Edge(v4, v1, name="left_edge")
    print(f"   Created edges: {e1}, {e2}, {e3}, {e4}")

    # Test 3: Create a wire (rectangle)
    print("\n3. Creating a wire...")
    sketch = Sketch(name="rectangle_sketch")
    wire = Wire(sketch, name="rectangle_wire")

    # Add edges to wire
    wire.edges.extend([e1, e2, e3, e4])
    wire._update_blender_curve()
    print(f"   Created wire: {wire}")

    # Test 4: Create a sketch with preset
    print("\n4. Creating sketch with preset...")
    sketch2 = Sketch(name="preset_sketch")
    rect_wire = sketch2.preset.rectangle(2, 1)
    print(f"   Created preset rectangle: {rect_wire}")

    # Test 5: Create a part
    print("\n5. Creating a part...")
    part = Part(name="test_part")
    part.sketch = sketch
    print(f"   Created part: {part}")

    # Test 6: Create parts using presets
    print("\n6. Creating parts with presets...")
    cube_part = Part.preset.cube(1, 1, 1)
    cylinder_part = Part.preset.cylinder(0.5, 2)
    sphere_part = Part.preset.sphere(0.75)
    print(f"   Created cube: {cube_part}")
    print(f"   Created cylinder: {cylinder_part}")
    print(f"   Created sphere: {sphere_part}")

    # Test 7: Create an assembly
    print("\n7. Creating an assembly...")
    assembly = Assembly(name="test_assembly")
    assembly.add(part)
    assembly.add(cube_part)
    assembly.add(cylinder_part)
    assembly.add(sphere_part)
    print(f"   Created assembly: {assembly}")

    # Test 8: Test assembly operations
    print("\n8. Testing assembly operations...")
    assembly.move(0, 0, 1)  # Move assembly up
    assembly.scale(1.5)  # Scale assembly
    print(f"   Assembly moved and scaled")

    print("\n✅ All Blender CAD implementation tests completed successfully!")
    print(f"   Final assembly contains {len(assembly.parts)} parts")

    return assembly


@pytest.mark.skipif(
    "bpy" not in locals(), reason="This test can only be run in Blender"
)
def create_cube():
    """Simple function to create a cube using Blender CAD implementations."""
    from codetocad.adapters.blender import Part

    print("🎯 Creating a cube using Blender CAD implementation...")

    # Create a cube part
    cube = Part.preset.cube(2, 2, 2)
    cube.set_name("my_test_cube")

    print(f"✅ Created cube: {cube}")
    return cube


@pytest.mark.skipif(
    "bpy" not in locals(), reason="This test can only be run in Blender"
)
def create_complex_assembly():
    """Create a more complex assembly to test functionality."""
    from codetocad.adapters.blender import Assembly, Part, Sketch

    print("🏗️ Creating a complex assembly...")

    # Create an assembly
    assembly = Assembly("complex_assembly")

    # Create multiple parts
    base = Part.preset.cube(4, 4, 0.5)
    base.set_name("base_plate")

    pillar1 = Part.preset.cylinder(0.2, 3)
    pillar1.set_name("pillar_1")
    pillar1.move(-1.5, -1.5, 0.5)

    pillar2 = Part.preset.cylinder(0.2, 3)
    pillar2.set_name("pillar_2")
    pillar2.move(1.5, -1.5, 0.5)

    pillar3 = Part.preset.cylinder(0.2, 3)
    pillar3.set_name("pillar_3")
    pillar3.move(1.5, 1.5, 0.5)

    pillar4 = Part.preset.cylinder(0.2, 3)
    pillar4.set_name("pillar_4")
    pillar4.move(-1.5, 1.5, 0.5)

    top = Part.preset.cube(4, 4, 0.5)
    top.set_name("top_plate")
    top.move(0, 0, 3.5)

    # Add parts to assembly
    assembly.add(base)
    assembly.add(pillar1)
    assembly.add(pillar2)
    assembly.add(pillar3)
    assembly.add(pillar4)
    assembly.add(top)

    print(f"✅ Created complex assembly: {assembly}")
    return assembly
