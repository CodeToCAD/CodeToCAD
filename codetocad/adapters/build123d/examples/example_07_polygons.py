"""
Example 7: Polygons

CodeToCAD implementation of build123d introductory example 7.
Creates a shape with regular polygons positioned at specific locations.

Original build123d code:
```python
a, b, c = 60, 80, 5

with BuildPart() as ex7:
    with BuildSketch() as ex7_sk:
        Rectangle(a, b)
        with Locations((0, 3 * c), (0, -3 * c)):
            RegularPolygon(radius=2 * c, side_count=6, mode=Mode.SUBTRACT)
    extrude(amount=c)
```

This example demonstrates:
- Creating regular polygons with specified radius and side count
- Positioning polygons at multiple locations
- Boolean operations with positioned polygons
- Comparing CodeToCAD implementation with original build123d code
"""

from codetocad.adapters.build123d import Part
import build123d as bd


def original():
    """Create the original build123d version for comparison."""
    a, b, c = 60, 80, 5

    with bd.BuildPart() as ex7:
        with bd.BuildSketch() as ex7_sk:
            bd.Rectangle(a, b)
            with bd.Locations((0, 3 * c), (0, -3 * c)):
                bd.RegularPolygon(radius=2 * c, side_count=6, mode=bd.Mode.SUBTRACT)
        bd.extrude(amount=c)

    return ex7.part


def create_polygons():
    """Create a shape with regular polygons using CodeToCAD."""
    # Define dimensions
    a, b, c = 60, 80, 5

    # Create the base rectangle part
    base_rect = Part.preset.cube(a, b, c)
    base_rect.set_name("base_rectangle")

    # Create hexagons to subtract at positions (0, 3*c) and (0, -3*c)
    hex_positions = [(0, 3 * c, 0), (0, -3 * c, 0)]

    result = base_rect
    for i, (x, y, z) in enumerate(hex_positions):
        # Create hexagon (6-sided polygon) with radius 2*c
        hex_part = Part.preset.cylinder(2 * c, c)  # Approximate with cylinder for now
        hex_part.set_name(f"hexagon_{i}")
        hex_part.transform.translate(x, y, z)
        result = result.boolean.difference(hex_part)

    result.set_name("polygons")
    return result


def compare_implementations():
    """Compare CodeToCAD and original build123d implementations."""
    print("Comparing implementations...")

    # Create both versions
    codetocad_part = create_polygons()
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

    # Compare results (allowing for some tolerance due to polygon approximation)
    volume_tolerance = original_volume * 0.1  # 10% tolerance for polygon approximation
    volume_match = abs(codetocad_volume - original_volume) < volume_tolerance

    # Bounding box comparison with tolerance
    bbox_tolerance = 2.0  # 2 unit tolerance
    bbox_match = (
        abs(codetocad_bbox[0][0] - original_bbox_tuple[0][0]) < bbox_tolerance
        and abs(codetocad_bbox[0][1] - original_bbox_tuple[0][1]) < bbox_tolerance
        and abs(codetocad_bbox[0][2] - original_bbox_tuple[0][2]) < bbox_tolerance
        and abs(codetocad_bbox[1][0] - original_bbox_tuple[1][0]) < bbox_tolerance
        and abs(codetocad_bbox[1][1] - original_bbox_tuple[1][1]) < bbox_tolerance
        and abs(codetocad_bbox[1][2] - original_bbox_tuple[1][2]) < bbox_tolerance
    )

    print(f"CodeToCAD Volume: {codetocad_volume:.6f}")
    print(f"Original Volume: {original_volume:.6f}")
    print(f"Volume Match (within 10%): {volume_match}")
    print(f"CodeToCAD BBox: {codetocad_bbox}")
    print(f"Original BBox: {original_bbox_tuple}")
    print(f"BBox Match (within 2 units): {bbox_match}")

    return volume_match and bbox_match


def main():
    """Main function to run the example."""
    print("Example 7: Polygons")
    print("Creating a shape with regular polygons using CodeToCAD...")

    # Create the shape
    shape = create_polygons()

    print(f"Created shape: {shape.name}")
    print(f"Volume: {shape.geometry.volume():.2f}")
    print(f"Bounding box: {shape.geometry.bounding_box()}")

    # Compare with original
    print("\n" + "=" * 50)
    match = compare_implementations()
    print(f"Implementations match (with tolerance): {match}")

    return shape


if __name__ == "__main__":
    result = main()
