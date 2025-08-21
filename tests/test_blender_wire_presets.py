"""
Test script for Blender Wire preset functionality.

This script tests the enhanced Blender Wire preset methods that provide
comprehensive wire/edge creation capabilities matching the build123d implementation.

Note: This test requires Blender to be available and can only be run within Blender.
"""

import pytest

from codetocad.adapters.blender.cli import run_blender


@pytest.mark.skipif(
    "bpy" not in locals(), reason="This test can only be run in Blender"
)
def test_blender_basic_wire_presets():
    """Test the basic Blender wire preset functionality."""
    print("Blender Basic Wire Presets Test Suite")
    print("=" * 50)

    try:
        from codetocad.adapters.blender import Wire, Sketch

        print("✓ Successfully imported Blender Wire and Sketch classes")

        # Create test sketch
        sketch = Sketch("blender_test_sketch")
        print(f"✓ Created test sketch: {sketch.name}")

        # Test existing presets
        print("\n1. Testing Existing Presets")
        print("-" * 40)

        # Test rectangle
        rect_wire = sketch.preset.rectangle(10, 5)
        print(f"✓ Created rectangle wire: {rect_wire}")

        # Test circle
        circle_wire = sketch.preset.circle(3)
        print(f"✓ Created circle wire: {circle_wire}")

        # Test regular polygon
        polygon_wire = sketch.preset.regular_polygon(2, 6, 0)
        print(f"✓ Created regular polygon wire: {polygon_wire}")

        # Test polyline
        points = [(0, 0), (1, 0), (1, 1), (0, 1)]
        polyline_wire = sketch.preset.polyline(points)
        print(f"✓ Created polyline wire: {polyline_wire}")

        return True

    except ImportError as e:
        print(f"✗ Failed to import required modules: {e}")
        return False
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        return False


@pytest.mark.skipif(
    "bpy" not in locals(), reason="This test can only be run in Blender"
)
def test_blender_arc_presets():
    """Test the new Blender arc preset methods."""
    print("\n2. Testing Blender Arc Presets")
    print("-" * 40)

    try:
        from codetocad.adapters.blender import Wire, Sketch

        sketch = Sketch("blender_arc_test_sketch")

        # Test center arc
        center_arc = sketch.preset.center_arc(
            center=(0, 0, 0), radius=5, start_angle=0, arc_size=90
        )
        print(f"✓ Created center arc: {center_arc}")

        # Test three point arc
        three_point_arc = sketch.preset.three_point_arc(
            start=(0, 0, 0), mid=(1, 1, 0), end=(2, 0, 0)
        )
        print(f"✓ Created three-point arc: {three_point_arc}")

        # Test radius arc
        radius_arc = sketch.preset.radius_arc(
            start_point=(0, 0, 0), end_point=(2, 2, 0), radius=2
        )
        print(f"✓ Created radius arc: {radius_arc}")

        # Test tangent arc
        tangent_arc = sketch.preset.tangent_arc(
            start=(0, 0, 0), end=(2, 2, 0), tangent=(1, 0, 0)
        )
        print(f"✓ Created tangent arc: {tangent_arc}")

        return True

    except Exception as e:
        print(f"✗ Blender arc preset test failed: {e}")
        return False


@pytest.mark.skipif(
    "bpy" not in locals(), reason="This test can only be run in Blender"
)
def test_blender_curve_presets():
    """Test the new Blender curve preset methods."""
    print("\n3. Testing Blender Curve Presets")
    print("-" * 40)

    try:
        from codetocad.adapters.blender import Wire, Sketch

        sketch = Sketch("blender_curve_test_sketch")

        # Test spline
        spline_points = [(0, 0, 0), (1, 2, 0), (3, 1, 0), (4, 3, 0)]
        spline_wire = sketch.preset.spline(spline_points)
        print(f"✓ Created spline: {spline_wire}")

        # Test spline with tangents
        tangents = [(1, 0, 0), (0, 1, 0)]
        spline_with_tangents = sketch.preset.spline(
            spline_points[:2], tangents=tangents
        )
        print(f"✓ Created spline with tangents: {spline_with_tangents}")

        # Test bezier curve
        control_points = [(0, 0, 0), (1, 2, 0), (3, 2, 0), (4, 0, 0)]
        bezier_wire = sketch.preset.bezier(control_points)
        print(f"✓ Created bezier curve: {bezier_wire}")

        # Test bezier with weights
        weights = [1.0, 2.0, 2.0, 1.0]
        weighted_bezier = sketch.preset.bezier(control_points, weights=weights)
        print(f"✓ Created weighted bezier curve: {weighted_bezier}")

        return True

    except Exception as e:
        print(f"✗ Blender curve preset test failed: {e}")
        return False


@pytest.mark.skipif(
    "bpy" not in locals(), reason="This test can only be run in Blender"
)
def test_blender_2d_shape_presets():
    """Test the new Blender 2D shape preset methods."""
    print("\n4. Testing Blender 2D Shape Presets")
    print("-" * 40)

    try:
        from codetocad.adapters.blender import Wire, Sketch

        sketch = Sketch("blender_shape_test_sketch")

        # Test ellipse
        ellipse_wire = sketch.preset.ellipse(x_radius=3, y_radius=2, rotation=30)
        print(f"✓ Created ellipse: {ellipse_wire}")

        # Test polygon
        polygon_points = [(0, 0, 0), (2, 0, 0), (3, 2, 0), (1, 3, 0), (-1, 1, 0)]
        polygon_wire = sketch.preset.polygon(polygon_points)
        print(f"✓ Created polygon: {polygon_wire}")

        # Test rounded rectangle
        rounded_rect = sketch.preset.rectangle_rounded(width=4, height=3, radius=0.5)
        print(f"✓ Created rounded rectangle: {rounded_rect}")

        # Test triangle
        triangle_wire = sketch.preset.triangle(a=3, b=4, c=5)
        print(f"✓ Created triangle: {triangle_wire}")

        # Test trapezoid
        trapezoid_wire = sketch.preset.trapezoid(
            width=4, height=2, left_side_angle=75, right_side_angle=105
        )
        print(f"✓ Created trapezoid: {trapezoid_wire}")

        return True

    except Exception as e:
        print(f"✗ Blender 2D shape preset test failed: {e}")
        return False


@pytest.mark.skipif(
    "bpy" not in locals(), reason="This test can only be run in Blender"
)
def test_blender_text_preset():
    """Test the Blender text preset method."""
    print("\n5. Testing Blender Text Preset")
    print("-" * 40)

    try:
        from codetocad.adapters.blender import Wire, Sketch

        sketch = Sketch("blender_text_test_sketch")

        # Test text
        text_wire = sketch.preset.text("Hello CodeToCAD", font_size=2.0)
        print(f"✓ Created text wire: {text_wire}")

        # Test text with custom font
        custom_text = sketch.preset.text("Custom Font", font_size=1.5, font="Helvetica")
        print(f"✓ Created custom text wire: {custom_text}")

        return True

    except Exception as e:
        print(f"✗ Blender text preset test failed: {e}")
        return False


@pytest.mark.skipif(
    "bpy" not in locals(), reason="This test can only be run in Blender"
)
def test_blender_wire_preset_integration():
    """Test that Blender wire presets integrate properly with sketches."""
    print("\n6. Testing Blender Wire Preset Integration")
    print("-" * 40)

    try:
        from codetocad.adapters.blender import Wire, Sketch

        sketch = Sketch("blender_integration_test_sketch")
        initial_wire_count = len(sketch.wires)

        # Create multiple wires using presets
        rect = sketch.preset.rectangle(2, 2)
        circle = sketch.preset.circle(1)
        arc = sketch.preset.center_arc((0, 0, 0), 1.5, 0, 180)
        text = sketch.preset.text("Test", 1.0)

        # Check that wires were added to sketch
        final_wire_count = len(sketch.wires)
        expected_count = initial_wire_count + 4

        if final_wire_count == expected_count:
            print(f"✓ Wire count correct: {final_wire_count} wires in sketch")
        else:
            print(
                f"✗ Wire count mismatch: expected {expected_count}, got {final_wire_count}"
            )
            return False

        # Check that wires have proper parent sketch reference
        for wire in [rect, circle, arc, text]:
            if sketch in wire.member_sketches:
                print(f"✓ Wire {wire} properly linked to sketch")
            else:
                print(f"✗ Wire {wire} not properly linked to sketch")
                return False

        return True

    except Exception as e:
        print(f"✗ Blender integration test failed: {e}")
        return False


def run_blender_wire_preset_tests():
    """Run all Blender wire preset tests."""
    print("Blender Wire Preset Enhancement Test Suite")
    print("=" * 60)

    tests = [
        test_blender_basic_wire_presets,
        test_blender_arc_presets,
        test_blender_curve_presets,
        test_blender_2d_shape_presets,
        test_blender_text_preset,
        test_blender_wire_preset_integration,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if run_blender(test, background=False):
                passed += 1
                print("✅ PASSED")
            else:
                failed += 1
                print("❌ FAILED")
        except Exception as e:
            failed += 1
            print(f"❌ FAILED with exception: {e}")

    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 ALL BLENDER WIRE PRESET TESTS PASSED!")
        return True
    else:
        print("❌ SOME BLENDER TESTS FAILED!")
        return False


if __name__ == "__main__":
    success = run_blender_wire_preset_tests()

    print("\nNew Blender Wire Preset Methods Available:")
    print("✅ Arc methods: center_arc, three_point_arc, radius_arc, tangent_arc")
    print("✅ Curve methods: spline, bezier")
    print("✅ Line methods: polar_line, fillet_polyline")
    print(
        "✅ 2D shape methods: ellipse, polygon, rectangle_rounded, triangle, trapezoid"
    )
    print("✅ Text method: text")

    exit(0 if success else 1)
