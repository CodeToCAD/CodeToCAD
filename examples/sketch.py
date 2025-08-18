from codetocad.adapters.blender import *


def create_custom_sketch_part():
    """Create a part from a custom sketch."""

    print("✏️ Creating custom sketch part...")

    # Create a custom sketch
    sketch = Sketch("custom_shape")

    # Create vertices for a pentagon
    import math

    vertices = []
    for i in range(5):
        angle = i * 2 * math.pi / 5
        x = 2 * math.cos(angle)
        y = 2 * math.sin(angle)
        vertex = Vertex(x, y, 0, name=f"pentagon_vertex_{i}")
        vertices.append(vertex)

    # Create wire connecting the vertices
    wire = Wire(sketch, name="pentagon_wire")
    for i in range(5):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % 5]  # Connect to next vertex (wrap around)
        edge = Edge(v1, v2, name=f"pentagon_edge_{i}")
        wire.edges.append(edge)

    # Close the wire
    wire.close()
    sketch.add(wire)

    # Create part from sketch
    part = Part("pentagon_part")
    part.sketch = sketch
    part.create_from_sketch()
    part.extrude(1.0)  # Extrude 1 unit

    print(f"✅ Custom sketch part completed!")
    print(f"   Part: {part}")
    print(f"   Sketch: {sketch}")

    return part


if __name__ == "__main__":
    run(entry_function=create_custom_sketch_part, background=False)
