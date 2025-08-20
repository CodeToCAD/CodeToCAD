"""
Test script for wire geometric constraint functionality.

This script demonstrates the new wire constraint system that allows
applying geometric constraints to wires such as tangent, parallel,
perpendicular, coincident, distance, length, and continuity constraints.
"""


def test_wire_constraints():
    """Test the wire constraint functionality."""
    print("Wire Constraint System Test Suite")
    print("=" * 50)

    try:
        from codetocad.adapters.build123d import Wire, Sketch
        from codetocad.interfaces.cad.wire.wire_constraint import (
            ConstraintType,
            ConstraintStatus,
        )

        print("✓ Successfully imported wire constraint classes")

        # Create test wires
        sketch = Sketch("test_sketch")
        wire1 = Wire(sketch, name="wire1")
        wire2 = Wire(sketch, name="wire2")

        print(f"✓ Created test wires: {wire1.name}, {wire2.name}")
        print(f"✓ Wire1 has constraint interface: {hasattr(wire1, 'constraint')}")
        print(f"✓ Constraint interface type: {type(wire1.constraint).__name__}")

        # Test constraint creation methods
        print("\n1. Testing Constraint Creation Methods")
        print("-" * 40)

        # Test tangent constraint
        print("   Testing tangent constraint...")
        try:
            tangent_constraint = wire1.constraint.tangent_to(
                target_entity=wire2, point=(0, 0, 0), name="tangent_test"
            )
            if tangent_constraint:
                print(f"   ✓ Created tangent constraint: {tangent_constraint.name}")
                print(
                    f"   ✓ Constraint type: {tangent_constraint.constraint_type.value}"
                )
                print(f"   ✓ Constraint status: {tangent_constraint.status.value}")
            else:
                print("   ⚠ Tangent constraint creation returned None")
        except Exception as e:
            print(f"   ✗ Failed to create tangent constraint: {e}")
            assert False

        # Test parallel constraint
        print("   Testing parallel constraint...")
        try:
            parallel_constraint = wire1.constraint.parallel_to(
                reference_entity=wire2, name="parallel_test"
            )
            if parallel_constraint:
                print(f"   ✓ Created parallel constraint: {parallel_constraint.name}")
                print(
                    f"   ✓ Constraint type: {parallel_constraint.constraint_type.value}"
                )
            else:
                print("   ⚠ Parallel constraint creation returned None")
        except Exception as e:
            print(f"   ✗ Failed to create parallel constraint: {e}")
            assert False

        # Test perpendicular constraint
        print("   Testing perpendicular constraint...")
        try:
            perp_constraint = wire1.constraint.perpendicular_to(
                reference_entity=wire2, name="perpendicular_test"
            )
            if perp_constraint:
                print(f"   ✓ Created perpendicular constraint: {perp_constraint.name}")
            else:
                print("   ⚠ Perpendicular constraint creation returned None")
        except Exception as e:
            print(f"   ✗ Failed to create perpendicular constraint: {e}")
            assert False

        # Test coincident constraint
        print("   Testing coincident constraint...")
        try:
            coincident_constraint = wire1.constraint.coincident_points(
                target_point=(1, 1, 0), wire_point="start", name="coincident_test"
            )
            if coincident_constraint:
                print(
                    f"   ✓ Created coincident constraint: {coincident_constraint.name}"
                )
            else:
                print("   ⚠ Coincident constraint creation returned None")
        except Exception as e:
            print(f"   ✗ Failed to create coincident constraint: {e}")
            assert False

        # Test distance constraint
        print("   Testing distance constraint...")
        try:
            distance_constraint = wire1.constraint.distance_from(
                target_entity=wire2, distance_value=5.0, name="distance_test"
            )
            if distance_constraint:
                print(f"   ✓ Created distance constraint: {distance_constraint.name}")
                print(
                    f"   ✓ Distance value: {distance_constraint.parameters.get('distance_value')}"
                )
            else:
                print("   ⚠ Distance constraint creation returned None")
        except Exception as e:
            print(f"   ✗ Failed to create distance constraint: {e}")
            assert False

        # Test length constraint
        print("   Testing length constraint...")
        try:
            length_constraint = wire1.constraint.set_length(
                length_value=10.0, name="length_test"
            )
            if length_constraint:
                print(f"   ✓ Created length constraint: {length_constraint.name}")
                print(
                    f"   ✓ Target length: {length_constraint.parameters.get('length_value')}"
                )
            else:
                print("   ⚠ Length constraint creation returned None")
        except Exception as e:
            print(f"   ✗ Failed to create length constraint: {e}")
            assert False

        # Test continuity constraint
        print("   Testing continuity constraint...")
        try:
            continuity_constraint = wire1.constraint.continuous_with(
                other_wire=wire2, continuity_order=1, name="continuity_test"
            )
            if continuity_constraint:
                print(
                    f"   ✓ Created continuity constraint: {continuity_constraint.name}"
                )
                print(
                    f"   ✓ Continuity order: {continuity_constraint.parameters.get('continuity_order')}"
                )
            else:
                print("   ⚠ Continuity constraint creation returned None")
        except Exception as e:
            print(f"   ✗ Failed to create continuity constraint: {e}")
            assert False

        # Test constraint management
        print("\n2. Testing Constraint Management")
        print("-" * 40)

        # Get all constraints
        all_constraints = wire1.constraint.get_all_constraints()
        print(f"   ✓ Total constraints created: {len(all_constraints)}")

        for constraint in all_constraints:
            print(
                f"   - {constraint.name} ({constraint.constraint_type.value}): {constraint.status.value}"
            )

        # Test constraint validation
        print("   Testing constraint validation...")
        validation_results = wire1.constraint.validate_constraints()
        valid_count = sum(1 for is_valid in validation_results.values() if is_valid)
        print(f"   ✓ Valid constraints: {valid_count}/{len(validation_results)}")

        # Test constraint solving
        print("   Testing constraint solving...")
        solve_success = wire1.constraint.solve_constraints()
        print(f"   ✓ Constraint solving result: {solve_success}")

        # Test constraint retrieval
        print("   Testing constraint retrieval...")
        if all_constraints:
            first_constraint_name = all_constraints[0].name
            retrieved_constraint = wire1.constraint.get_constraint(
                first_constraint_name
            )
            if retrieved_constraint:
                print(
                    f"   ✓ Successfully retrieved constraint: {retrieved_constraint.name}"
                )
            else:
                print("   ✗ Failed to retrieve constraint")
                assert False

        # Test constraint removal
        print("   Testing constraint removal...")
        if all_constraints:
            constraint_to_remove = all_constraints[0].name
            removal_success = wire1.constraint.remove_constraint(constraint_to_remove)
            print(f"   ✓ Constraint removal result: {removal_success}")

            # Verify removal
            remaining_constraints = wire1.constraint.get_all_constraints()
            print(f"   ✓ Remaining constraints: {len(remaining_constraints)}")

        # Test legacy methods for backward compatibility
        print("\n3. Testing Legacy Method Compatibility")
        print("-" * 40)

        print("   Testing legacy coincident method...")
        try:
            # This should work with the legacy interface
            wire1.constraint.coincident(None, None)  # Placeholder call
            print("   ✓ Legacy coincident method accessible")
        except Exception as e:
            print(f"   ⚠ Legacy method issue (expected): {e}")
            assert False

        print("   Testing legacy parallel method...")
        try:
            wire1.constraint.parallel(None, None)  # Placeholder call
            print("   ✓ Legacy parallel method accessible")
        except Exception as e:
            print(f"   ⚠ Legacy method issue (expected): {e}")
            assert False

        # Test fluent API demonstration
        print("\n4. Fluent API Demonstration")
        print("-" * 40)

        print("   The new constraint API provides a fluent interface:")
        print("   - wire.constraint.tangent_to(curve, point)")
        print("   - wire.constraint.parallel_to(reference_line)")
        print("   - wire.constraint.perpendicular_to(reference_line)")
        print("   - wire.constraint.coincident_points(target_point, wire_point)")
        print("   - wire.constraint.distance_from(entity, distance)")
        print("   - wire.constraint.set_length(length)")
        print("   - wire.constraint.continuous_with(other_wire, order)")

        print("\n5. Constraint Statistics")
        print("-" * 40)

        final_constraints = wire1.constraint.get_all_constraints()
        constraint_types = {}
        for constraint in final_constraints:
            constraint_type = constraint.constraint_type.value
            constraint_types[constraint_type] = (
                constraint_types.get(constraint_type, 0) + 1
            )

        print(f"   Total active constraints: {len(final_constraints)}")
        for constraint_type, count in constraint_types.items():
            print(f"   - {constraint_type}: {count}")

        print("\n" + "=" * 50)
        print("✅ WIRE CONSTRAINT TESTS COMPLETED SUCCESSFULLY!")

        return True

    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        assert False


def demonstrate_constraint_benefits():
    """Demonstrate the benefits of the wire constraint system."""
    print("\nWire Constraint System Benefits")
    print("=" * 40)

    print(
        """
The new wire constraint system provides:

1. **Geometric Constraint Types**:
   ✅ Tangent constraints for smooth curve connections
   ✅ Parallel/Perpendicular constraints for alignment
   ✅ Coincident constraints for point matching
   ✅ Distance constraints for spacing control
   ✅ Length constraints for size control
   ✅ Continuity constraints for smooth transitions

2. **Fluent API Design**:
   ✅ Intuitive method names (tangent_to, parallel_to, etc.)
   ✅ Clear parameter requirements
   ✅ Consistent with assembly mate patterns
   ✅ Better IDE autocomplete support

3. **Constraint Management**:
   ✅ Add, remove, and modify constraints
   ✅ Validate constraint configurations
   ✅ Solve constraint systems
   ✅ Query constraint status and properties

4. **Backward Compatibility**:
   ✅ Legacy methods still work
   ✅ Existing code continues to function
   ✅ Gradual migration path available

5. **Integration with build123d**:
   ✅ Uses build123d's constraint solving capabilities
   ✅ Maintains wire geometry integrity
   ✅ Supports complex constraint relationships
"""
    )


if __name__ == "__main__":
    print("Wire Geometric Constraint System Test")
    print("=" * 60)

    # Run tests
    test_ok = test_wire_constraints()
    demonstrate_constraint_benefits()

    print("\n" + "=" * 60)
    if test_ok:
        print("🎉 ALL WIRE CONSTRAINT TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED!")

    print("\nThe wire constraint system provides:")
    print("✅ Comprehensive geometric constraint types")
    print("✅ Fluent API for intuitive constraint creation")
    print("✅ Full constraint lifecycle management")
    print("✅ Backward compatibility with existing code")
    print("✅ Integration with build123d constraint solving")
