"""
Example 5: Moving the current working point

CodeToCAD implementation of build123d introductory example 5.
Creates a shape with multiple features positioned at different locations.

Original build123d code:
```python
a, b, c, d = 90, 45, 15, 7.5

with BuildPart() as ex5:
    with BuildSketch() as ex5_sk:
        Circle(a)
        with Locations((b, 0.0)):
            Rectangle(c, c, mode=Mode.SUBTRACT)
        with Locations((0, b)):
            Circle(d, mode=Mode.SUBTRACT)
    extrude(amount=c)
```

This example demonstrates:
- Creating base shapes and positioning additional features
- Using boolean operations within sketches
- Positioning shapes at specific locations
- Comparing CodeToCAD implementation with original build123d code
"""

from codetocad.adapters.build123d import Part
import build123d as bd


def original():
    """Create the original build123d version for comparison."""
    a, b, c, d = 90, 45, 15, 7.5

    with bd.BuildPart() as ex5:
        with bd.BuildSketch() as ex5_sk:
            bd.Circle(a)
            with bd.Locations((b, 0.0)):
                bd.Rectangle(c, c, mode=bd.Mode.SUBTRACT)
            with bd.Locations((0, b)):
                bd.Circle(d, mode=bd.Mode.SUBTRACT)
        bd.extrude(amount=c)

    return ex5.part


def create_moving_current_working_point():
    """Create a shape with positioned features using CodeToCAD."""
    # Define dimensions
    a, b, c, d = 90, 45, 15, 7.5

    # Create the base circle part
    base_circle = Part.preset.cylinder(a, c)  # radius=a, height=c
    base_circle.set_name("base_circle")

    # Create the rectangle to subtract at position (b, 0.0)
    rect_part = Part.preset.cube(c, c, c)
    rect_part.set_name("rectangle_part")
    rect_part.transform.translate(b, 0.0, 0)  # Move to position (b, 0, 0)

    # Create the small circle to subtract at position (0, b)
    small_circle = Part.preset.cylinder(d, c)  # radius=d, height=c
    small_circle.set_name("small_circle")
    small_circle.transform.translate(0, b, 0)  # Move to position (0, b, 0)

    # Perform boolean operations
    result = base_circle.boolean.difference(rect_part)
    result = result.boolean.difference(small_circle)
    result.set_name("moving_current_working_point")

    return result


def compare_implementations():
    """Compare CodeToCAD and original build123d implementations."""
    print("Comparing implementations...")

    # Create both versions
    codetocad_part = create_moving_current_working_point()
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
    print("Example 5: Moving the current working point")
    print("Creating a shape with positioned features using CodeToCAD...")

    # Create the shape
    shape = create_moving_current_working_point()

    print(f"Created shape: {shape.name}")
    print(f"Volume: {shape.geometry.volume():.2f}")
    print(f"Bounding box: {shape.geometry.bounding_box()}")

    # Compare with original
    print("\n" + "=" * 50)
    match = compare_implementations()
    print(f"Implementations match: {match}")

    return shape


if __name__ == "__main__":
    result = main()
