"""
Wire Presets Showcase Example

This example demonstrates the enhanced Wire preset capabilities in CodeToCAD,
showcasing the comprehensive set of wire/edge creation methods that match
build123d's 1D and 2D objects.
"""


def showcase_arc_presets():
    """Demonstrate arc preset methods."""
    print("🎯 Arc Presets Showcase")
    print("=" * 40)

    try:
        from codetocad.adapters.build123d import Sketch

        sketch = Sketch("arc_showcase")

        # Center Arc - most common arc type
        center_arc = sketch.preset.center_arc(
            center=(0, 0, 0), radius=5, start_angle=0, arc_size=90
        )
        print(f"✓ Center Arc: {center_arc}")

        # Three Point Arc - intuitive arc creation
        three_point_arc = sketch.preset.three_point_arc(
            start=(10, 0, 0), mid=(12, 2, 0), end=(14, 0, 0)
        )
        print(f"✓ Three Point Arc: {three_point_arc}")

        # Radius Arc - arc defined by endpoints and radius
        radius_arc = sketch.preset.radius_arc(
            start_point=(0, 10, 0), end_point=(5, 10, 0), radius=3
        )
        print(f"✓ Radius Arc: {radius_arc}")

        # Tangent Arc - arc with tangent constraint
        tangent_arc = sketch.preset.tangent_arc(
            start=(10, 10, 0), end=(15, 12, 0), tangent=(1, 0, 0)
        )
        print(f"✓ Tangent Arc: {tangent_arc}")

        return sketch

    except Exception as e:
        print(f"✗ Arc showcase failed: {e}")
        return None


def showcase_curve_presets():
    """Demonstrate curve preset methods."""
    print("\n🌊 Curve Presets Showcase")
    print("=" * 40)

    try:
        from codetocad.adapters.build123d import Sketch

        sketch = Sketch("curve_showcase")

        # Spline - smooth curve through points
        spline_points = [(0, 0, 0), (2, 3, 0), (5, 2, 0), (8, 4, 0)]
        spline = sketch.preset.spline(spline_points)
        print(f"✓ Spline: {spline}")

        # Spline with tangent constraints
        tangent_spline = sketch.preset.spline(
            points=[(0, 10, 0), (3, 12, 0), (6, 10, 0)],
            tangents=[(1, 0, 0), (-1, 0, 0)],  # Horizontal tangents at ends
        )
        print(f"✓ Tangent Spline: {tangent_spline}")

        # Periodic (closed) spline
        periodic_spline = sketch.preset.spline(
            points=[(10, 0, 0), (12, 2, 0), (14, 0, 0), (12, -2, 0)], periodic=True
        )
        print(f"✓ Periodic Spline: {periodic_spline}")

        # Bezier curve - precise control with control points
        control_points = [(0, 20, 0), (2, 25, 0), (6, 25, 0), (8, 20, 0)]
        bezier = sketch.preset.bezier(control_points)
        print(f"✓ Bezier Curve: {bezier}")

        # Weighted Bezier curve - rational bezier with weights
        weights = [
            1.0,
            3.0,
            3.0,
            1.0,
        ]  # Higher weights pull curve toward control points
        weighted_bezier = sketch.preset.bezier(control_points, weights=weights)
        print(f"✓ Weighted Bezier: {weighted_bezier}")

        return sketch

    except Exception as e:
        print(f"✗ Curve showcase failed: {e}")
        return None


def showcase_line_presets():
    """Demonstrate line preset methods."""
    print("\n📏 Line Presets Showcase")
    print("=" * 40)

    try:
        from codetocad.adapters.build123d import Sketch

        sketch = Sketch("line_showcase")

        # Polar Line - line defined by angle and length
        polar_line = sketch.preset.polar_line(start=(0, 0, 0), length=5, angle=45)
        print(f"✓ Polar Line (45°): {polar_line}")

        # Another polar line at different angle
        polar_line_2 = sketch.preset.polar_line(start=(10, 0, 0), length=3, angle=120)
        print(f"✓ Polar Line (120°): {polar_line_2}")

        # Fillet Polyline - polyline with rounded corners
        sharp_points = [(0, 10, 0), (5, 10, 0), (5, 15, 0), (0, 15, 0)]
        fillet_polyline = sketch.preset.fillet_polyline(points=sharp_points, radius=1.0)
        print(f"✓ Fillet Polyline: {fillet_polyline}")

        # Closed fillet polyline
        closed_fillet = sketch.preset.fillet_polyline(
            points=[(10, 10, 0), (15, 10, 0), (15, 15, 0), (10, 15, 0)],
            radius=0.5,
            close=True,
        )
        print(f"✓ Closed Fillet Polyline: {closed_fillet}")

        return sketch

    except Exception as e:
        print(f"✗ Line showcase failed: {e}")
        return None


def showcase_2d_shape_presets():
    """Demonstrate 2D shape preset methods."""
    print("\n🔷 2D Shape Presets Showcase")
    print("=" * 40)

    try:
        from codetocad.adapters.build123d import Sketch

        sketch = Sketch("shape_showcase")

        # Ellipse - oval shape with different radii
        ellipse = sketch.preset.ellipse(x_radius=4, y_radius=2, rotation=30)
        print(f"✓ Ellipse (rotated 30°): {ellipse}")

        # Polygon - custom shape from points
        pentagon_points = [(0, 0, 0), (2, 0, 0), (3, 1.5, 0), (1, 2.5, 0), (-1, 1.5, 0)]
        polygon = sketch.preset.polygon(pentagon_points)
        print(f"✓ Custom Polygon: {polygon}")

        # Rounded Rectangle - rectangle with filleted corners
        rounded_rect = sketch.preset.rectangle_rounded(width=6, height=4, radius=0.8)
        print(f"✓ Rounded Rectangle: {rounded_rect}")

        # Triangle - defined by sides and angles
        right_triangle = sketch.preset.triangle(a=3, b=4, c=5)  # 3-4-5 right triangle
        print(f"✓ Right Triangle: {right_triangle}")

        # Triangle with angles
        angle_triangle = sketch.preset.triangle(a=5, A=60, B=70)  # C will be 50°
        print(f"✓ Angle Triangle: {angle_triangle}")

        # Trapezoid - quadrilateral with parallel sides
        trapezoid = sketch.preset.trapezoid(
            width=5, height=3, left_side_angle=75, right_side_angle=105
        )
        print(f"✓ Trapezoid: {trapezoid}")

        # Symmetric trapezoid (right_side_angle = None)
        symmetric_trapezoid = sketch.preset.trapezoid(
            width=4, height=2, left_side_angle=80
        )
        print(f"✓ Symmetric Trapezoid: {symmetric_trapezoid}")

        return sketch

    except Exception as e:
        print(f"✗ 2D shape showcase failed: {e}")
        return None


def showcase_combined_usage():
    """Demonstrate combining multiple preset types in one sketch."""
    print("\n🎨 Combined Usage Showcase")
    print("=" * 40)

    try:
        from codetocad.adapters.build123d import Sketch

        sketch = Sketch("combined_showcase")

        # Create a complex sketch using multiple preset types
        print("Creating a complex mechanical part outline...")

        # Base rectangle
        base = sketch.preset.rectangle(20, 10)
        print(f"✓ Base rectangle: {base}")

        # Rounded corners for mounting holes area
        rounded_area = sketch.preset.rectangle_rounded(width=6, height=6, radius=1)
        print(f"✓ Rounded mounting area: {rounded_area}")

        # Circular features
        main_hole = sketch.preset.circle(2)
        small_hole_1 = sketch.preset.circle(0.5)
        small_hole_2 = sketch.preset.circle(0.5)
        print(f"✓ Circular features: {main_hole}, {small_hole_1}, {small_hole_2}")

        # Connecting arc
        connecting_arc = sketch.preset.center_arc(
            center=(0, 0, 0), radius=8, start_angle=30, arc_size=60
        )
        print(f"✓ Connecting arc: {connecting_arc}")

        # Spline for smooth transition
        transition_points = [(5, 0, 0), (7, 2, 0), (9, 3, 0), (12, 2, 0)]
        transition_spline = sketch.preset.spline(transition_points)
        print(f"✓ Transition spline: {transition_spline}")

        print(f"\n✓ Combined sketch created with {len(sketch.wires)} wire elements")
        return sketch

    except Exception as e:
        print(f"✗ Combined usage showcase failed: {e}")
        return None


def main():
    """Run the complete Wire presets showcase."""
    print("🚀 CodeToCAD Wire Presets Showcase")
    print("=" * 60)
    print("Demonstrating enhanced sketching capabilities with comprehensive")
    print("wire/edge creation methods matching build123d's 1D and 2D objects.")
    print()

    # Run all showcases
    showcases = [
        showcase_arc_presets,
        showcase_curve_presets,
        showcase_line_presets,
        showcase_2d_shape_presets,
        showcase_combined_usage,
    ]

    successful = 0
    for showcase in showcases:
        result = showcase()
        if result is not None:
            successful += 1

    print(f"\n🎉 Showcase Complete!")
    print(f"Successfully demonstrated {successful}/{len(showcases)} preset categories")

    print("\n📋 Summary of New Wire Preset Methods:")
    print("✅ Arc Methods: center_arc, three_point_arc, radius_arc, tangent_arc")
    print("✅ Curve Methods: spline, bezier")
    print("✅ Line Methods: polar_line, fillet_polyline")
    print(
        "✅ 2D Shape Methods: ellipse, polygon, rectangle_rounded, triangle, trapezoid"
    )
    print("\n🔧 All methods use modern Python type hints and integrate seamlessly")
    print("   with the existing Sketch class functionality!")


if __name__ == "__main__":
    main()
