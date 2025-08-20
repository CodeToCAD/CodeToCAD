"""
Wire Geometric Constraints Example

This example demonstrates how to use the new wire constraint system
to create complex geometric relationships between wires and other entities.
"""


def wire_constraints_example():
    """Demonstrate wire constraint functionality with practical examples."""
    print("Wire Geometric Constraints Example")
    print("=" * 50)

    try:
        from codetocad.adapters.build123d import Wire, Sketch

        print("Creating wires for constraint demonstration...")

        # Create a sketch and multiple wires
        sketch = Sketch("constraint_demo")

        # Create base wires
        main_wire = Wire(sketch, name="main_wire")
        reference_wire = Wire(sketch, name="reference_wire")
        connecting_wire = Wire(sketch, name="connecting_wire")

        print(
            f"✓ Created wires: {main_wire.name}, {reference_wire.name}, {connecting_wire.name}"
        )

        # Example 1: Parallel Constraint
        print("\n--- Example 1: Parallel Constraint ---")
        print("Making main_wire parallel to reference_wire...")

        parallel_constraint = main_wire.constraint.parallel_to(
            reference_entity=reference_wire, name="main_parallel_to_ref"
        )

        if parallel_constraint:
            print(f"✓ Applied parallel constraint: {parallel_constraint.name}")
            print(f"  Status: {parallel_constraint.status.value}")

        # Example 2: Distance Constraint
        print("\n--- Example 2: Distance Constraint ---")
        print("Maintaining 5.0 units distance between wires...")

        distance_constraint = main_wire.constraint.distance_from(
            target_entity=reference_wire, distance_value=5.0, name="maintain_distance"
        )

        if distance_constraint:
            print(f"✓ Applied distance constraint: {distance_constraint.name}")
            print(
                f"  Distance: {distance_constraint.parameters['distance_value']} units"
            )

        # Example 3: Length Constraint
        print("\n--- Example 3: Length Constraint ---")
        print("Setting connecting_wire to exactly 15.0 units long...")

        length_constraint = connecting_wire.constraint.set_length(
            length_value=15.0, name="fixed_length"
        )

        if length_constraint:
            print(f"✓ Applied length constraint: {length_constraint.name}")
            print(
                f"  Target length: {length_constraint.parameters['length_value']} units"
            )

        # Example 4: Tangent Constraint
        print("\n--- Example 4: Tangent Constraint ---")
        print("Making connecting_wire tangent to main_wire at connection point...")

        connection_point = (2.5, 0, 0)  # Example connection point
        tangent_constraint = connecting_wire.constraint.tangent_to(
            target_entity=main_wire, point=connection_point, name="smooth_connection"
        )

        if tangent_constraint:
            print(f"✓ Applied tangent constraint: {tangent_constraint.name}")
            print(f"  Connection point: {tangent_constraint.parameters['point']}")

        # Example 5: Coincident Points
        print("\n--- Example 5: Coincident Points ---")
        print("Making wire endpoints coincident...")

        endpoint = (5.0, 2.5, 0)  # Target endpoint
        coincident_constraint = connecting_wire.constraint.coincident_points(
            target_point=endpoint, wire_point="end", name="endpoint_match"
        )

        if coincident_constraint:
            print(f"✓ Applied coincident constraint: {coincident_constraint.name}")
            print(f"  Target point: {coincident_constraint.parameters['target_point']}")

        # Example 6: Continuity Between Wires
        print("\n--- Example 6: Wire Continuity ---")
        print("Ensuring smooth continuity between main_wire and connecting_wire...")

        continuity_constraint = main_wire.constraint.continuous_with(
            other_wire=connecting_wire,
            continuity_order=1,  # Tangent continuity
            name="smooth_transition",
        )

        if continuity_constraint:
            print(f"✓ Applied continuity constraint: {continuity_constraint.name}")
            print(
                f"  Continuity order: {continuity_constraint.parameters['continuity_order']} (tangent)"
            )

        # Example 7: Perpendicular Constraint
        print("\n--- Example 7: Perpendicular Constraint ---")
        print("Making connecting_wire perpendicular to reference_wire...")

        perp_constraint = connecting_wire.constraint.perpendicular_to(
            reference_entity=reference_wire, name="perpendicular_connection"
        )

        if perp_constraint:
            print(f"✓ Applied perpendicular constraint: {perp_constraint.name}")

        # Constraint Management Examples
        print("\n--- Constraint Management ---")

        # Get all constraints for main_wire
        main_constraints = main_wire.constraint.get_all_constraints()
        print(f"Main wire has {len(main_constraints)} constraints:")
        for constraint in main_constraints:
            print(f"  - {constraint.name} ({constraint.constraint_type.value})")

        # Get all constraints for connecting_wire
        connecting_constraints = connecting_wire.constraint.get_all_constraints()
        print(f"Connecting wire has {len(connecting_constraints)} constraints:")
        for constraint in connecting_constraints:
            print(f"  - {constraint.name} ({constraint.constraint_type.value})")

        # Validate all constraints
        print("\nValidating constraints...")
        for wire in [main_wire, reference_wire, connecting_wire]:
            validation_results = wire.constraint.validate_constraints()
            if validation_results:
                valid_count = sum(
                    1 for is_valid in validation_results.values() if is_valid
                )
                print(
                    f"  {wire.name}: {valid_count}/{len(validation_results)} constraints valid"
                )

        # Solve all constraints
        print("\nSolving constraint systems...")
        for wire in [main_wire, reference_wire, connecting_wire]:
            constraints = wire.constraint.get_all_constraints()
            if constraints:
                solve_result = wire.constraint.solve_constraints()
                print(
                    f"  {wire.name}: Constraint solving {'succeeded' if solve_result else 'failed'}"
                )

        # Demonstrate constraint modification
        print("\n--- Constraint Modification ---")
        if distance_constraint:
            print("Updating distance constraint from 5.0 to 7.5 units...")
            update_success = distance_constraint.update_parameters(distance_value=7.5)
            if update_success:
                print(
                    f"✓ Updated distance to {distance_constraint.parameters['distance_value']} units"
                )

        # Demonstrate constraint suppression
        print("\nSuppressing and unsuppressing constraints...")
        if parallel_constraint:
            suppress_result = parallel_constraint.suppress()
            print(f"  Parallel constraint suppressed: {suppress_result}")
            print(f"  Status: {parallel_constraint.status.value}")

            unsuppress_result = parallel_constraint.unsuppress()
            print(f"  Parallel constraint unsuppressed: {unsuppress_result}")
            print(f"  Status: {parallel_constraint.status.value}")

        # Summary
        print("\n--- Summary ---")
        total_constraints = 0
        for wire in [main_wire, reference_wire, connecting_wire]:
            wire_constraints = len(wire.constraint.get_all_constraints())
            total_constraints += wire_constraints
            print(f"  {wire.name}: {wire_constraints} constraints")

        print(f"Total constraints in system: {total_constraints}")

        print("\n" + "=" * 50)
        print("✅ WIRE CONSTRAINTS EXAMPLE COMPLETED!")

        return True

    except Exception as e:
        print(f"✗ Example failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def demonstrate_constraint_types():
    """Demonstrate different types of constraints and their use cases."""
    print("\nConstraint Types and Use Cases")
    print("=" * 40)

    print(
        """
1. **Tangent Constraints**
   Use case: Creating smooth curves and transitions
   Example: Connecting a straight line to a circle smoothly
   API: wire.constraint.tangent_to(target_curve, connection_point)

2. **Parallel Constraints**
   Use case: Maintaining parallel relationships
   Example: Creating parallel rails or guides
   API: wire.constraint.parallel_to(reference_line)

3. **Perpendicular Constraints**
   Use case: Creating right-angle relationships
   Example: Connecting perpendicular supports or brackets
   API: wire.constraint.perpendicular_to(reference_line)

4. **Coincident Constraints**
   Use case: Ensuring points meet exactly
   Example: Connecting wire endpoints precisely
   API: wire.constraint.coincident_points(target_point, wire_point)

5. **Distance Constraints**
   Use case: Maintaining specific spacing
   Example: Creating offset curves or maintaining clearances
   API: wire.constraint.distance_from(target_entity, distance)

6. **Length Constraints**
   Use case: Controlling wire dimensions
   Example: Creating wires of exact length for manufacturing
   API: wire.constraint.set_length(target_length)

7. **Continuity Constraints**
   Use case: Creating smooth multi-segment curves
   Example: Spline curves with smooth transitions
   API: wire.constraint.continuous_with(other_wire, continuity_order)
"""
    )


if __name__ == "__main__":
    print("Wire Geometric Constraints - Practical Examples")
    print("=" * 60)

    # Run the main example
    example_ok = wire_constraints_example()

    # Show constraint types
    demonstrate_constraint_types()

    print("\n" + "=" * 60)
    if example_ok:
        print("🎉 ALL EXAMPLES COMPLETED SUCCESSFULLY!")
    else:
        print("❌ SOME EXAMPLES FAILED!")

    print("\nKey Benefits of Wire Constraints:")
    print("✅ Precise geometric control")
    print("✅ Automated constraint solving")
    print("✅ Flexible constraint management")
    print("✅ Integration with CAD workflows")
    print("✅ Support for complex geometric relationships")
