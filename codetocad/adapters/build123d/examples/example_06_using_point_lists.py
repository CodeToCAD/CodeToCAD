"""
Example 6: Using Point Lists

CodeToCAD implementation of build123d introductory example 6.
Creates a shape with multiple features positioned at various locations using point lists.

Original build123d code:
```python
a, b, c = 80, 60, 10

with BuildPart() as ex6:
    with BuildSketch() as ex6_sk:
        Circle(a)
        with Locations((b, 0), (0, b), (-b, 0), (0, -b)):
            Circle(c, mode=Mode.SUBTRACT)
    extrude(amount=c)
```

This example demonstrates:
- Creating multiple features at various locations using point lists
- Boolean operations with multiple positioned shapes
- Efficient creation of repeated features
- Comparing CodeToCAD implementation with original build123d code
"""

from codetocad.adapters.build123d import Part
import build123d as bd


def original():
    """Create the original build123d version for comparison."""
    a, b, c = 80, 60, 10

    with bd.BuildPart() as ex6:
        with bd.BuildSketch() as ex6_sk:
            bd.Circle(a)
            with bd.Locations((b, 0), (0, b), (-b, 0), (0, -b)):
                bd.Circle(c, mode=bd.Mode.SUBTRACT)
        bd.extrude(amount=c)

    return ex6.part


def create_using_point_lists():
    """Create a shape with multiple positioned features using CodeToCAD."""
    # Define dimensions
    a, b, c = 80, 60, 10

    # Create the base circle part
    base_circle = Part.preset.cylinder(a, c)  # radius=a, height=c
    base_circle.set_name("base_circle")

    # Define the positions for the holes
    hole_positions = [(b, 0, 0), (0, b, 0), (-b, 0, 0), (0, -b, 0)]

    # Create holes at each position and subtract them
    result = base_circle
    for i, (x, y, z) in enumerate(hole_positions):
        hole = Part.preset.cylinder(c, c)  # radius=c, height=c
        hole.set_name(f"hole_{i}")
        hole.transform.translate(x, y, z)
        result = result.boolean.difference(hole)

    result.set_name("using_point_lists")
    return result


def compare_implementations():
    """Compare CodeToCAD and original build123d implementations."""
    print("Comparing implementations...")

    # Create both versions
    codetocad_part = create_using_point_lists()
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
    print("Example 6: Using Point Lists")
    print("Creating a shape with multiple positioned features using CodeToCAD...")

    # Create the shape
    shape = create_using_point_lists()

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
