"""
Example 1: Simple Rectangular Plate

CodeToCAD implementation of build123d introductory example 1.
Creates a simple rectangular box using CodeToCAD's Part.preset.cube method.

Original build123d code:
```python
length, width, thickness = 80.0, 60.0, 10.0

with BuildPart() as ex1:
    Box(length, width, thickness)
```

This example demonstrates:
- Creating basic geometric primitives using CodeToCAD
- Using Part presets for simple shapes
- Converting build123d Box to CodeToCAD cube
- Comparing CodeToCAD implementation with original build123d code
"""

from codetocad.adapters.build123d import Part
import build123d as bd


def original():
    """Create the original build123d version for comparison."""
    length, width, thickness = 80.0, 60.0, 10.0

    with bd.BuildPart() as ex1:
        bd.Box(length, width, thickness)

    return ex1.part


def create_simple_rectangular_plate():
    """Create a simple rectangular plate using CodeToCAD."""
    # Define dimensions
    length, width, thickness = 80.0, 60.0, 10.0

    # Create the rectangular plate using Part preset
    plate = Part.preset.cube(length, width, thickness)
    plate.set_name("simple_rectangular_plate")

    return plate


def compare_implementations():
    """Compare CodeToCAD and original build123d implementations."""
    print("Comparing implementations...")

    # Create both versions
    codetocad_part = create_simple_rectangular_plate()
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
    print("Example 1: Simple Rectangular Plate")
    print("Creating a rectangular plate with CodeToCAD...")

    # Create the plate
    plate = create_simple_rectangular_plate()

    print(f"Created plate: {plate.name}")
    print(f"Volume: {plate.geometry.volume():.2f}")
    print(f"Bounding box: {plate.geometry.bounding_box()}")

    # Compare with original
    print("\n" + "=" * 50)
    match = compare_implementations()
    print(f"Implementations match: {match}")

    return plate


if __name__ == "__main__":
    result = main()
