"""
Example 2: Plate with Hole

CodeToCAD implementation of build123d introductory example 2.
Creates a rectangular box with a cylindrical hole cut through it.

Original build123d code:
```python
length, width, thickness = 80.0, 60.0, 10.0
center_hole_dia = 22.0

with BuildPart() as ex2:
    Box(length, width, thickness)
    Cylinder(radius=center_hole_dia / 2, height=thickness, mode=Mode.SUBTRACT)
```

This example demonstrates:
- Creating basic geometric primitives
- Boolean operations (difference/subtraction)
- Combining multiple parts into one
- Comparing CodeToCAD implementation with original build123d code
"""

from codetocad.adapters.build123d import Part
import build123d as bd


def original():
    """Create the original build123d version for comparison."""
    length, width, thickness = 80.0, 60.0, 10.0
    center_hole_dia = 22.0

    with bd.BuildPart() as ex2:
        bd.Box(length, width, thickness)
        bd.Cylinder(radius=center_hole_dia / 2, height=thickness, mode=bd.Mode.SUBTRACT)

    return ex2.part


def create_plate_with_hole():
    """Create a rectangular plate with a hole using CodeToCAD."""
    # Define dimensions
    length, width, thickness = 80.0, 60.0, 10.0
    center_hole_dia = 22.0

    # Create the base plate
    plate = Part.preset.cube(length, width, thickness)
    plate.set_name("base_plate")

    # Create the hole (cylinder to subtract)
    hole = Part.preset.cylinder(center_hole_dia / 2, thickness)
    hole.set_name("hole_cylinder")

    # Perform boolean difference to create the hole
    result = plate.boolean.difference(hole)
    result.set_name("plate_with_hole")

    return result


def compare_implementations():
    """Compare CodeToCAD and original build123d implementations."""
    print("Comparing implementations...")

    # Create both versions
    codetocad_part = create_plate_with_hole()
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
    print("Example 2: Plate with Hole")
    print("Creating a rectangular plate with a hole using CodeToCAD...")

    # Create the plate with hole
    plate = create_plate_with_hole()

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
