#!/usr/bin/env python3
"""
Basic usage examples for the build123d adapter.

This file demonstrates how to use the build123d adapter with CodeToCAD.
Note: build123d must be installed for these examples to work.
"""


def example_basic_shapes():
    """Example of creating basic shapes with the build123d adapter."""
    try:
        from codetocad.adapters.build123d import (
            Vertex,
            Edge,
            Wire,
            Sketch,
            Part,
            Assembly,
        )

        print("Creating basic shapes with build123d adapter...")

        # Create vertices
        v1 = Vertex(0, 0, 0)
        v2 = Vertex(1, 1, 1)
        print(f"Created vertices: {v1}, {v2}")

        # Create edge
        edge = Edge(v1, v2)
        print(f"Created edge: {edge}")

        # Create a sketch with a rectangle
        sketch = Sketch("example_sketch")
        rect_wire = sketch.preset.rectangle(10, 5)
        print(f"Created sketch with rectangle: {sketch}")

        # Create parts using presets
        cube = Part.preset.cube(2, 2, 2)
        cylinder = Part.preset.cylinder(1, 3)
        sphere = Part.preset.sphere(1.5)
        print(f"Created parts: {cube.name}, {cylinder.name}, {sphere.name}")

        # Create assembly
        assembly = Assembly("example_assembly")
        assembly.add_part(cube)
        assembly.add_part(cylinder)
        assembly.add_part(sphere)
        print(f"Created assembly with {len(assembly)} parts")

        # Boolean operations
        result = cube.boolean.union(cylinder)
        print(f"Boolean union result: {result.name}")

        return assembly

    except ImportError as e:
        print(f"build123d is not installed: {e}")
        print("Install build123d with: pip install build123d")
        return None


def example_sketch_operations():
    """Example of sketch operations with the build123d adapter."""
    try:
        from codetocad.adapters.build123d import Sketch, Part

        print("Creating sketch with drawing operations...")

        # Create a sketch
        sketch = Sketch("drawing_example")

        # Draw lines and shapes
        sketch.draw.line_to(10, 0)
        sketch.draw.line_to(10, 10)
        sketch.draw.line_to(0, 10)
        sketch.draw.close()

        print(f"Created sketch with {len(sketch.wires)} wires")

        # Create a part and extrude the sketch
        part = Part("extruded_part")
        part.sketch = sketch
        part.extrude_sketch(5)

        print(f"Extruded part: {part}")

        return part

    except ImportError as e:
        print(f"build123d is not installed: {e}")
        return None


def example_transformations():
    """Example of transformation operations."""
    try:
        from codetocad.adapters.build123d import Part

        print("Demonstrating transformations...")

        # Create a cube
        cube = Part.preset.cube(2, 2, 2)
        print(f"Original cube: {cube.name}")

        # Apply transformations
        cube.transform.translate(5, 0, 0)
        cube.transform.rotate((0, 0, 1), 45)  # Rotate 45 degrees around Z-axis
        cube.transform.scale(1.5, 1.5, 1.0)

        print(f"Transformed cube volume: {cube.geometry.volume()}")
        print(f"Bounding box: {cube.geometry.bounding_box()}")

        return cube

    except ImportError as e:
        print(f"build123d is not installed: {e}")
        return None


def example_export():
    """Example of exporting parts."""
    try:
        from codetocad.adapters.build123d import Part

        print("Demonstrating export functionality...")

        # Create a part
        part = Part.preset.sphere(2)

        # Export to different formats
        try:
            part.export.step("sphere.step")
            print("Exported to STEP format")
        except Exception as e:
            print(f"STEP export failed: {e}")

        try:
            part.export.stl("sphere.stl")
            print("Exported to STL format")
        except Exception as e:
            print(f"STL export failed: {e}")

        return part

    except ImportError as e:
        print(f"build123d is not installed: {e}")
        return None


if __name__ == "__main__":
    print("build123d Adapter Examples")
    print("=" * 40)

    # Run examples
    assembly = example_basic_shapes()
    part1 = example_sketch_operations()
    part2 = example_transformations()
    part3 = example_export()

    print("\nExamples completed!")
    if assembly:
        print(f"Final assembly has {len(assembly)} parts")
    else:
        print("Examples require build123d to be installed")
        print("Install with: pip install build123d")
