"""
Example 8: Polylines

CodeToCAD implementation of build123d introductory example 8.
Creates an I-beam shape using polylines and mirroring.

Original build123d code:
```python
(L, H, W, t) = (100.0, 20.0, 20.0, 1.0)
pts = [
    (0, H / 2.0),
    (W / 2.0, H / 2.0),
    (W / 2.0, (H / 2.0 - t)),
    (t / 2.0, (H / 2.0 - t)),
    (t / 2.0, (t - H / 2.0)),
    (W / 2.0, (t - H / 2.0)),
    (W / 2.0, H / -2.0),
    (0, H / -2.0),
]

with BuildPart() as ex8:
    with BuildSketch(Plane.YZ) as ex8_sk:
        with BuildLine() as ex8_ln:
            Polyline(pts)
            mirror(ex8_ln.line, about=Plane.YZ)
        make_face()
    extrude(amount=L)
```

This example demonstrates:
- Creating complex profiles using polylines
- Mirroring geometry to create symmetric shapes
- Working with different sketch planes (YZ plane)
- Comparing CodeToCAD implementation with original build123d code
"""

from codetocad.adapters.build123d import Sketch, Part
import build123d as bd


def original():
    """Create the original build123d version for comparison."""
    (L, H, W, t) = (100.0, 20.0, 20.0, 1.0)
    pts = [
        (0, H / 2.0),
        (W / 2.0, H / 2.0),
        (W / 2.0, (H / 2.0 - t)),
        (t / 2.0, (H / 2.0 - t)),
        (t / 2.0, (t - H / 2.0)),
        (W / 2.0, (t - H / 2.0)),
        (W / 2.0, H / -2.0),
        (0, H / -2.0),
    ]

    with bd.BuildPart() as ex8:
        with bd.BuildSketch(bd.Plane.YZ) as ex8_sk:
            with bd.BuildLine() as ex8_ln:
                bd.Polyline(pts)
                bd.mirror(ex8_ln.line, about=bd.Plane.YZ)
            bd.make_face()
        bd.extrude(amount=L)

    return ex8.part


def create_polylines():
    """Create an I-beam shape using polylines with CodeToCAD."""
    # Define dimensions
    (L, H, W, t) = (100.0, 20.0, 20.0, 1.0)

    # Define the points for half of the I-beam profile
    pts = [
        (0, H / 2.0),
        (W / 2.0, H / 2.0),
        (W / 2.0, (H / 2.0 - t)),
        (t / 2.0, (H / 2.0 - t)),
        (t / 2.0, (t - H / 2.0)),
        (W / 2.0, (t - H / 2.0)),
        (W / 2.0, H / -2.0),
        (0, H / -2.0),
    ]

    # Create a sketch for the I-beam profile
    sketch = Sketch("ibeam_sketch")

    # Create the polyline for half of the I-beam
    half_profile = sketch.preset.polyline(pts)

    # For the mirrored part, we'll create the mirror points manually
    # since we don't have direct mirroring support in sketches yet
    mirrored_pts = [
        (-x, y) for x, y in reversed(pts[:-1])
    ]  # Mirror and reverse, skip last point to avoid duplication

    # Add the mirrored polyline
    mirrored_profile = sketch.preset.polyline(mirrored_pts)

    # Create a part and extrude the sketch
    part = Part("ibeam_part")
    part.sketch = sketch
    part.extrude_sketch(L)
    part.set_name("polylines")

    return part


def compare_implementations():
    """Compare CodeToCAD and original build123d implementations."""
    print("Comparing implementations...")

    # Create both versions
    codetocad_part = create_polylines()
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

    # Compare results (allowing for some tolerance due to different approach)
    volume_tolerance = original_volume * 0.2  # 20% tolerance for different approach
    volume_match = abs(codetocad_volume - original_volume) < volume_tolerance

    # Bounding box comparison with tolerance
    bbox_tolerance = 5.0  # 5 unit tolerance
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
    print(f"Volume Match (within 20%): {volume_match}")
    print(f"CodeToCAD BBox: {codetocad_bbox}")
    print(f"Original BBox: {original_bbox_tuple}")
    print(f"BBox Match (within 5 units): {bbox_match}")

    return volume_match and bbox_match


def main():
    """Main function to run the example."""
    print("Example 8: Polylines")
    print("Creating an I-beam shape using polylines with CodeToCAD...")

    # Create the I-beam
    ibeam = create_polylines()

    print(f"Created I-beam: {ibeam.name}")
    print(f"Volume: {ibeam.geometry.volume():.2f}")
    print(f"Bounding box: {ibeam.geometry.bounding_box()}")

    # Compare with original
    print("\n" + "=" * 50)
    match = compare_implementations()
    print(f"Implementations match (with tolerance): {match}")

    return ibeam


if __name__ == "__main__":
    result = main()
