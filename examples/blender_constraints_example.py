"""
Blender Constraints Example

This example demonstrates how to use the new Blender constraint system
to create complex kinematic and geometric relationships between objects.

Note: This example requires Blender to be running to execute fully.
"""


def blender_constraints_example():
    """Demonstrate Blender constraint functionality with practical examples."""
    print("Blender Constraints Example")
    print("=" * 40)

    try:
        from codetocad.adapters.blender import Part

        print("Creating parts for constraint demonstration...")

        # Create parts for the example
        base_part = Part("base")
        moving_part = Part("moving_part")
        target_part = Part("target")
        camera_part = Part("camera")
        path_follower = Part("follower")

        print(
            f"✓ Created parts: {base_part.name}, {moving_part.name}, {target_part.name}"
        )
        print(f"                 {camera_part.name}, {path_follower.name}")

        # Note: In a real Blender environment, you would create actual geometry here
        # For this example, we'll assume the parts have been created with geometry

        # Example 1: Copy Location Constraint
        print("\n--- Example 1: Copy Location Constraint ---")
        print("Making moving_part follow target_part's position...")

        try:
            copy_location_constraint = moving_part.constraints.copy_location(
                target_object=target_part.get_blender_object(),
                use_x=True,
                use_y=True,
                use_z=False,  # Don't copy Z position
                use_offset=False,
                influence=0.8,  # 80% influence
                name="follow_target",
            )

            if copy_location_constraint:
                print(
                    f"✓ Applied copy location constraint: {copy_location_constraint.name}"
                )
                print(
                    f"  Influence: {copy_location_constraint.parameters.get('influence', 1.0)}"
                )
                print(f"  Status: {copy_location_constraint.status.value}")
            else:
                print("⚠ Copy location constraint creation returned None")

        except Exception as e:
            print(f"⚠ Copy location constraint (expected without Blender): {e}")

        # Example 2: Limit Location Constraint
        print("\n--- Example 2: Limit Location Constraint ---")
        print("Restricting moving_part to a specific area...")

        try:
            limit_constraint = moving_part.constraints.limit_location(
                min_x=-5.0,
                max_x=5.0,
                min_y=-3.0,
                max_y=3.0,
                min_z=0.0,
                max_z=2.0,
                name="movement_bounds",
            )

            if limit_constraint:
                print(f"✓ Applied limit location constraint: {limit_constraint.name}")
                print(
                    f"  X bounds: {limit_constraint.parameters.get('min_x')} to {limit_constraint.parameters.get('max_x')}"
                )
                print(
                    f"  Y bounds: {limit_constraint.parameters.get('min_y')} to {limit_constraint.parameters.get('max_y')}"
                )
                print(
                    f"  Z bounds: {limit_constraint.parameters.get('min_z')} to {limit_constraint.parameters.get('max_z')}"
                )
            else:
                print("⚠ Limit location constraint creation returned None")

        except Exception as e:
            print(f"⚠ Limit location constraint (expected without Blender): {e}")

        # Example 3: Track To Constraint
        print("\n--- Example 3: Track To Constraint ---")
        print("Making camera look at target...")

        try:
            track_constraint = camera_part.constraints.track_to(
                target_object=target_part.get_blender_object(),
                track_axis="TRACK_NEGATIVE_Z",
                up_axis="UP_Y",
                influence=1.0,
                name="camera_tracking",
            )

            if track_constraint:
                print(f"✓ Applied track to constraint: {track_constraint.name}")
                print(f"  Track axis: {track_constraint.parameters.get('track_axis')}")
                print(f"  Up axis: {track_constraint.parameters.get('up_axis')}")
            else:
                print("⚠ Track to constraint creation returned None")

        except Exception as e:
            print(f"⚠ Track to constraint (expected without Blender): {e}")

        # Example 4: Copy Rotation Constraint
        print("\n--- Example 4: Copy Rotation Constraint ---")
        print("Making moving_part match target's rotation...")

        try:
            copy_rotation_constraint = moving_part.constraints.copy_rotation(
                target_object=target_part.get_blender_object(),
                use_x=True,
                use_y=True,
                use_z=False,  # Don't copy Z rotation
                use_offset=True,  # Add to existing rotation
                influence=0.6,
                name="match_rotation",
            )

            if copy_rotation_constraint:
                print(
                    f"✓ Applied copy rotation constraint: {copy_rotation_constraint.name}"
                )
                print(
                    f"  Use offset: {copy_rotation_constraint.parameters.get('use_offset')}"
                )
                print(
                    f"  Influence: {copy_rotation_constraint.parameters.get('influence')}"
                )
            else:
                print("⚠ Copy rotation constraint creation returned None")

        except Exception as e:
            print(f"⚠ Copy rotation constraint (expected without Blender): {e}")

        # Example 5: Child Of Constraint
        print("\n--- Example 5: Child Of Constraint ---")
        print("Creating parent-child relationship...")

        try:
            child_constraint = moving_part.constraints.child_of(
                parent_object=base_part.get_blender_object(),
                influence=1.0,
                name="parent_relationship",
            )

            if child_constraint:
                print(f"✓ Applied child of constraint: {child_constraint.name}")
                print(f"  Parent: {base_part.name}")
                print(f"  Child: {moving_part.name}")
            else:
                print("⚠ Child of constraint creation returned None")

        except Exception as e:
            print(f"⚠ Child of constraint (expected without Blender): {e}")

        # Example 6: Maintain Distance Constraint
        print("\n--- Example 6: Maintain Distance Constraint ---")
        print("Keeping follower at specific distance from target...")

        try:
            distance_constraint = path_follower.constraints.maintain_distance(
                target_object=target_part.get_blender_object(),
                distance=3.0,
                name="keep_distance",
            )

            if distance_constraint:
                print(
                    f"✓ Applied maintain distance constraint: {distance_constraint.name}"
                )
                print(
                    f"  Distance: {distance_constraint.parameters.get('distance')} units"
                )
            else:
                print("⚠ Maintain distance constraint creation returned None")

        except Exception as e:
            print(f"⚠ Maintain distance constraint (expected without Blender): {e}")

        # Constraint Management Examples
        print("\n--- Constraint Management ---")

        # Get all constraints for moving_part
        try:
            if moving_part.constraints:
                all_constraints = moving_part.constraints.get_all_constraints()
                print(f"Moving part has {len(all_constraints)} constraints:")
                for constraint in all_constraints:
                    print(
                        f"  - {constraint.name} ({constraint.constraint_type.value}): {constraint.status.value}"
                    )
            else:
                print(
                    "⚠ Moving part constraints not initialized (expected without Blender)"
                )
        except Exception as e:
            print(f"⚠ Constraint management (expected without Blender): {e}")

        # Demonstrate constraint modification
        print("\n--- Constraint Modification ---")

        try:
            if moving_part.constraints:
                # Get a specific constraint
                follow_constraint = moving_part.constraints.get_constraint(
                    "follow_target"
                )
                if follow_constraint:
                    print("Modifying constraint properties...")

                    # Change influence
                    influence_result = follow_constraint.set_influence(0.5)
                    print(f"  Set influence to 0.5: {influence_result}")

                    # Mute constraint
                    mute_result = follow_constraint.mute()
                    print(f"  Muted constraint: {mute_result}")
                    print(f"  Status after muting: {follow_constraint.status.value}")

                    # Unmute constraint
                    unmute_result = follow_constraint.unmute()
                    print(f"  Unmuted constraint: {unmute_result}")
                    print(f"  Status after unmuting: {follow_constraint.status.value}")
                else:
                    print("⚠ Could not find 'follow_target' constraint")
            else:
                print("⚠ Constraint modification (expected without Blender)")
        except Exception as e:
            print(f"⚠ Constraint modification (expected without Blender): {e}")

        # Summary
        print("\n--- Summary ---")
        constraint_types_demonstrated = [
            "Copy Location",
            "Limit Location",
            "Track To",
            "Copy Rotation",
            "Child Of",
            "Maintain Distance",
        ]

        print(f"Demonstrated constraint types: {len(constraint_types_demonstrated)}")
        for i, ctype in enumerate(constraint_types_demonstrated, 1):
            print(f"  {i}. {ctype}")

        print("\n" + "=" * 40)
        print("✅ BLENDER CONSTRAINTS EXAMPLE COMPLETED!")

        return True

    except Exception as e:
        print(f"✗ Example failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def demonstrate_use_cases():
    """Demonstrate practical use cases for Blender constraints."""
    print("\nPractical Use Cases")
    print("=" * 30)

    print(
        """
1. **Mechanical Assemblies**:
   - Copy location/rotation for linked parts
   - Limit location for sliding mechanisms
   - Track to for rotating components
   - Child of for hierarchical assemblies

2. **Animation Rigs**:
   - Track to for look-at behaviors
   - Copy rotation for synchronized movement
   - Limit constraints for joint restrictions
   - Child of for bone hierarchies

3. **Architectural Visualization**:
   - Floor constraints for object placement
   - Maintain distance for spacing requirements
   - Copy transformations for repeated elements
   - Limit location for design boundaries

4. **Product Design**:
   - Copy scale for proportional sizing
   - Track to for component alignment
   - Distance constraints for clearances
   - Child of for assembly relationships

5. **Camera Systems**:
   - Track to for automatic camera targeting
   - Follow path for camera movement
   - Copy location for camera following
   - Limit location for camera bounds
"""
    )


def show_constraint_workflow():
    """Show a typical constraint workflow."""
    print("\nTypical Constraint Workflow")
    print("=" * 35)

    print(
        """
1. **Create Objects**:
   ```python
   part1 = Part("object1")
   part2 = Part("target")
   # Create geometry for parts
   ```

2. **Apply Constraints**:
   ```python
   constraint = part1.constraints.copy_location(
       target_object=part2.get_blender_object(),
       name="follow_target"
   )
   ```

3. **Manage Constraints**:
   ```python
   # Modify properties
   constraint.set_influence(0.5)
   
   # Temporarily disable
   constraint.mute()
   
   # Re-enable
   constraint.unmute()
   ```

4. **Query Constraints**:
   ```python
   all_constraints = part1.constraints.get_all_constraints()
   specific_constraint = part1.constraints.get_constraint("follow_target")
   ```

5. **Remove Constraints**:
   ```python
   part1.constraints.remove_constraint("follow_target")
   # or remove all
   part1.constraints.clear_all_constraints()
   ```
"""
    )


if __name__ == "__main__":
    print("Blender Constraints - Practical Examples")
    print("=" * 50)

    # Run the main example
    example_ok = blender_constraints_example()

    # Show use cases and workflow
    demonstrate_use_cases()
    show_constraint_workflow()

    print("\n" + "=" * 50)
    if example_ok:
        print("🎉 ALL EXAMPLES COMPLETED!")
    else:
        print("❌ SOME EXAMPLES FAILED!")

    print("\nKey Benefits of Blender Constraints:")
    print("✅ Native Blender integration")
    print("✅ Comprehensive constraint types")
    print("✅ Fluent API design")
    print("✅ Full constraint lifecycle management")
    print("✅ Animation system compatibility")
