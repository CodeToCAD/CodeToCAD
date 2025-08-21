"""
Example 3: An extruded prismatic solid

CodeToCAD implementation of build123d introductory example 3.
Creates a prismatic solid using extrusion of a sketch with a circle and subtracted rectangle.

Original build123d code:
```python
length, width, thickness = 80.0, 60.0, 10.0

with BuildPart() as ex3:
    with BuildSketch() as ex3_sk:
        Circle(width)
        Rectangle(length / 2, width / 2, mode=Mode.SUBTRACT)
    extrude(amount=2 * thickness)
```

This example demonstrates:
- Creating sketches with multiple shapes
- Boolean operations within sketches (subtraction)
- Extruding sketches to create 3D solids
- Comparing CodeToCAD implementation with original build123d code
"""

from codetocad.adapters.build123d import Part
import build123d as bd


def original():
    """Create the original build123d version for comparison."""
    length, width, thickness = 80.0, 60.0, 10.0

    with bd.BuildPart() as ex3:
        with bd.BuildSketch() as ex3_sk:
            bd.Circle(width)  # This creates a circle with radius=width (60.0)
            bd.Rectangle(length / 2, width / 2, mode=bd.Mode.SUBTRACT)
        bd.extrude(amount=2 * thickness)

    return ex3.part


def create_extruded_prismatic_solid():
    """Create an extruded prismatic solid using CodeToCAD."""
    # Define dimensions
    length, width, thickness = 80.0, 60.0, 10.0

    # Create the base circle part - note: build123d Circle(width) creates a circle with radius=width
    circle_part = Part.preset.cylinder(
        width, 2 * thickness
    )  # Use radius=width to match original
    circle_part.set_name("circle_part")

    # Create the rectangle to subtract
    rect_part = Part.preset.cube(length / 2, width / 2, 2 * thickness)
    rect_part.set_name("rectangle_part")

    # Perform boolean difference
    result = circle_part.boolean.difference(rect_part)
    result.set_name("extruded_prismatic_solid")

    return result


def compare_implementations():
    """Compare CodeToCAD and original build123d implementations."""
    print("Comparing implementations...")

    # Create both versions
    codetocad_part = create_extruded_prismatic_solid()
    original_part = original()

    # Get volumes and bounding boxes
    codetocad_volume = codetocad_part.geometry.volume()
    codetocad_bbox = codetocad_part.geometry.bounding_box()

    original_volume = float(original_part.volume)
    original_bbox = original_part.bounding_box()
    original_bbox_tuple = (
        (original_bbox.min.X, original_bbox.min.Y, original_bbox.min.Z),
        (original_bbox.max.X, original_bbox.max.Y, original_bbox.max.Z),
    )

    # Compare results
    volume_match = abs(codetocad_volume - original_volume) < 1e-6
    bbox_match = (
        abs(codetocad_bbox[0][0] - original_bbox_tuple[0][0]) < 1e-6
        and abs(codetocad_bbox[0][1] - original_bbox_tuple[0][1]) < 1e-6
        and abs(codetocad_bbox[0][2] - original_bbox_tuple[0][2]) < 1e-6
        and abs(codetocad_bbox[1][0] - original_bbox_tuple[1][0]) < 1e-6
        and abs(codetocad_bbox[1][1] - original_bbox_tuple[1][1]) < 1e-6
        and abs(codetocad_bbox[1][2] - original_bbox_tuple[1][2]) < 1e-6
    )

    print(f"CodeToCAD Volume: {codetocad_volume:.6f}")
    print(f"Original Volume: {original_volume:.6f}")
    print(f"Volume Match: {volume_match}")
    print(f"CodeToCAD BBox: {codetocad_bbox}")
    print(f"Original BBox: {original_bbox_tuple}")
    print(f"BBox Match: {bbox_match}")

    return volume_match and bbox_match


def main():
    """Main function to run the example."""
    print("Example 3: An extruded prismatic solid")
    print("Creating an extruded prismatic solid with CodeToCAD...")

    # Create the extruded solid
    solid = create_extruded_prismatic_solid()

    print(f"Created solid: {solid.name}")
    print(f"Volume: {solid.geometry.volume():.2f}")
    print(f"Bounding box: {solid.geometry.bounding_box()}")

    # Compare with original
    print("\n" + "=" * 50)
    match = compare_implementations()
    print(f"Implementations match: {match}")

    return solid


if __name__ == "__main__":
    result = main()
