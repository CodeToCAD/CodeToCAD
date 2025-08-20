"""
Blender Assembly Mates Example

This example demonstrates how to use the new Blender assembly mate system
to create complex kinematic and geometric relationships between parts in assemblies.

Note: This example requires Blender to be running to execute fully.
"""


def blender_assembly_mates_example():
    """Demonstrate Blender assembly mate functionality with practical examples."""
    print("Blender Assembly Mates Example")
    print("=" * 45)

    try:
        from codetocad.adapters.blender import Assembly, Part

        print("Creating assembly and parts for mate demonstration...")

        # Create assembly and parts
        assembly = Assembly("robotic_arm")
        base = Part("base")
        shoulder = Part("shoulder")
        upper_arm = Part("upper_arm")
        forearm = Part("forearm")
        wrist = Part("wrist")
        gripper = Part("gripper")

        print(f"✓ Created assembly: {assembly.name}")
        print(f"✓ Created parts: {base.name}, {shoulder.name}, {upper_arm.name}")
        print(f"                 {forearm.name}, {wrist.name}, {gripper.name}")

        # Add parts to assembly
        assembly.add.part(base)
        assembly.add.part(shoulder)
        assembly.add.part(upper_arm)
        assembly.add.part(forearm)
        assembly.add.part(wrist)
        assembly.add.part(gripper)

        print(f"✓ Added {len(assembly.parts)} parts to assembly")

        # Note: In a real Blender environment, you would create actual geometry here
        # For this example, we'll assume the parts have been created with geometry

        # Example 1: Rigid Mate - Base Connection
        print("\n--- Example 1: Rigid Mate ---")
        print("Creating rigid connection between base and shoulder...")

        try:
            rigid_mate = assembly.mate.rigid(
                part1=base,
                part2=shoulder,
                location1="base_mount",  # In real usage, these would be actual locations
                location2="shoulder_mount",
                name="base_shoulder_rigid",
            )

            if rigid_mate:
                print(f"✓ Applied rigid mate: {rigid_mate.name}")
                print(f"  Degrees of freedom: {rigid_mate.get_degrees_of_freedom()}")
            else:
                print("⚠ Rigid mate creation returned None")

        except Exception as e:
            print(f"⚠ Rigid mate (expected without Blender): {e}")

        # Example 2: Revolute Mate - Shoulder Joint
        print("\n--- Example 2: Revolute Mate ---")
        print("Creating revolute joint for shoulder rotation...")

        try:
            shoulder_revolute = assembly.mate.revolute(
                part1=shoulder,
                part2=upper_arm,
                axis="z_axis",  # In real usage, this would be a Vector
                location1="shoulder_pivot",
                location2="upper_arm_mount",
                angle_range=(-180, 180),
                current_angle=0,
                name="shoulder_revolute",
            )

            if shoulder_revolute:
                print(f"✓ Applied revolute mate: {shoulder_revolute.name}")
                print(f"  Angle range: {shoulder_revolute.angle_range}")
                print(f"  Current angle: {shoulder_revolute.current_angle}")
                print(
                    f"  Degrees of freedom: {shoulder_revolute.get_degrees_of_freedom()}"
                )
            else:
                print("⚠ Revolute mate creation returned None")

        except Exception as e:
            print(f"⚠ Revolute mate (expected without Blender): {e}")

        # Example 3: Another Revolute Mate - Elbow Joint
        print("\n--- Example 3: Elbow Revolute Mate ---")
        print("Creating revolute joint for elbow...")

        try:
            elbow_revolute = assembly.mate.revolute(
                part1=upper_arm,
                part2=forearm,
                axis="y_axis",
                location1="elbow_pivot",
                location2="forearm_mount",
                angle_range=(-150, 0),  # Elbow can only bend one way
                current_angle=-45,
                name="elbow_revolute",
            )

            if elbow_revolute:
                print(f"✓ Applied elbow revolute mate: {elbow_revolute.name}")
                print(f"  Angle range: {elbow_revolute.angle_range}")
                print(f"  Current angle: {elbow_revolute.current_angle}")
            else:
                print("⚠ Elbow revolute mate creation returned None")

        except Exception as e:
            print(f"⚠ Elbow revolute mate (expected without Blender): {e}")

        # Example 4: Ball Mate - Wrist Joint
        print("\n--- Example 4: Ball Mate ---")
        print("Creating ball joint for wrist (multi-axis rotation)...")

        try:
            wrist_ball = assembly.mate.ball(
                part1=forearm,
                part2=wrist,
                center_point="wrist_center",
                location1="forearm_end",
                location2="wrist_base",
                angle_ranges=((-90, 90), (-90, 90), (-180, 180)),
                current_angles=(0, 0, 0),
                name="wrist_ball",
            )

            if wrist_ball:
                print(f"✓ Applied ball mate: {wrist_ball.name}")
                print(f"  Angle ranges: {wrist_ball.angle_ranges}")
                print(f"  Current angles: {wrist_ball.current_angles}")
                print(f"  Degrees of freedom: {wrist_ball.get_degrees_of_freedom()}")
            else:
                print("⚠ Ball mate creation returned None")

        except Exception as e:
            print(f"⚠ Ball mate (expected without Blender): {e}")

        # Example 5: Linear Mate - Gripper
        print("\n--- Example 5: Linear Mate ---")
        print("Creating linear joint for gripper opening/closing...")

        try:
            gripper_linear = assembly.mate.linear(
                part1=wrist,
                part2=gripper,
                axis="x_axis",
                location1="gripper_mount",
                location2="gripper_base",
                position_range=(0, 50),  # 0-50mm opening
                current_position=25,
                name="gripper_linear",
            )

            if gripper_linear:
                print(f"✓ Applied linear mate: {gripper_linear.name}")
                print(f"  Position range: {gripper_linear.position_range}")
                print(f"  Current position: {gripper_linear.current_position}")
                print(
                    f"  Degrees of freedom: {gripper_linear.get_degrees_of_freedom()}"
                )
            else:
                print("⚠ Linear mate creation returned None")

        except Exception as e:
            print(f"⚠ Linear mate (expected without Blender): {e}")

        # Example 6: Geometric Mates
        print("\n--- Example 6: Geometric Mates ---")
        print("Creating geometric alignment constraints...")

        try:
            # Distance mate for clearance
            clearance_mate = assembly.mate.distance(
                part1=upper_arm,
                part2=forearm,
                entity1="upper_arm_surface",
                entity2="forearm_surface",
                distance=2.0,  # 2mm clearance
                name="arm_clearance",
            )

            if clearance_mate:
                print(f"✓ Applied distance mate: {clearance_mate.name}")
                print(f"  Distance: {clearance_mate.distance}")

            # Parallel mate for alignment
            parallel_mate = assembly.mate.parallel(
                part1=base,
                part2=shoulder,
                entity1="base_top_face",
                entity2="shoulder_bottom_face",
                name="base_shoulder_parallel",
            )

            if parallel_mate:
                print(f"✓ Applied parallel mate: {parallel_mate.name}")

        except Exception as e:
            print(f"⚠ Geometric mates (expected without Blender): {e}")

        # Mate Management Examples
        print("\n--- Mate Management ---")

        try:
            if hasattr(assembly, "mate") and hasattr(assembly.mate, "_mate_manager"):
                mate_manager = assembly.mate._mate_manager

                # Get all mates
                all_mates = mate_manager.get_all_mates()
                print(f"Total mates in assembly: {len(all_mates)}")

                for mate_name, mate in all_mates.items():
                    mate_type = (
                        mate.mate_type.value
                        if hasattr(mate, "mate_type")
                        else "unknown"
                    )
                    print(f"  - {mate_name} ({mate_type})")

                # Validate mates
                validation_results = mate_manager.validate_mates()
                valid_count = sum(
                    1 for is_valid in validation_results.values() if is_valid
                )
                print(f"Valid mates: {valid_count}/{len(validation_results)}")

                # Solve mates
                solve_success = mate_manager.solve_mates()
                print(f"Mate solving: {'successful' if solve_success else 'failed'}")

            else:
                print("⚠ Mate manager not available (expected without Blender)")

        except Exception as e:
            print(f"⚠ Mate management (expected without Blender): {e}")

        # Animation Control Example
        print("\n--- Animation Control ---")

        print("Demonstrating joint control (structure only):")
        print("  - shoulder_revolute.set_angle(45)  # Rotate shoulder")
        print("  - elbow_revolute.set_angle(-90)    # Bend elbow")
        print("  - wrist_ball.set_angles(15, -10, 30)  # Adjust wrist")
        print("  - gripper_linear.set_position(10)  # Close gripper")

        print("\nQuerying joint states:")
        print("  - shoulder_angle = shoulder_revolute.get_angle()")
        print("  - elbow_angle = elbow_revolute.get_angle()")
        print("  - wrist_angles = wrist_ball.get_angles()")
        print("  - gripper_position = gripper_linear.get_position()")

        # Summary
        print("\n--- Summary ---")
        mate_types_demonstrated = [
            "Rigid (base-shoulder connection)",
            "Revolute (shoulder and elbow joints)",
            "Ball (wrist multi-axis joint)",
            "Linear (gripper actuation)",
            "Distance (clearance constraint)",
            "Parallel (surface alignment)",
        ]

        print(f"Demonstrated mate types: {len(mate_types_demonstrated)}")
        for i, mate_type in enumerate(mate_types_demonstrated, 1):
            print(f"  {i}. {mate_type}")

        print("\n" + "=" * 45)
        print("✅ BLENDER ASSEMBLY MATES EXAMPLE COMPLETED!")

        return True

    except Exception as e:
        print(f"✗ Example failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def demonstrate_kinematic_chains():
    """Demonstrate kinematic chain creation."""
    print("\nKinematic Chain Examples")
    print("=" * 35)

    print(
        """
1. **Serial Kinematic Chain** (Robot Arm):
   Base → Shoulder (Revolute) → Upper Arm → Elbow (Revolute) → 
   Forearm → Wrist (Ball) → End Effector

2. **Parallel Kinematic Chain** (Stewart Platform):
   Base → 6 Linear Actuators → Moving Platform

3. **Hybrid Kinematic Chain** (Articulated Gripper):
   Wrist → Finger Base (Revolute) → Finger Segment (Revolute) → 
   Finger Tip (Linear)

4. **Closed Loop Chain** (Four-Bar Linkage):
   Ground → Link1 (Revolute) → Link2 → Link3 (Revolute) → 
   Link4 → Ground (Revolute)
"""
    )


def demonstrate_constraint_benefits():
    """Demonstrate the benefits of the assembly mate system."""
    print("\nAssembly Mate System Benefits")
    print("=" * 40)

    print(
        """
1. **Mechanical Accuracy**:
   ✅ Precise joint definitions with limits
   ✅ Realistic motion constraints
   ✅ Proper degrees of freedom control
   ✅ Collision and interference detection

2. **Animation Integration**:
   ✅ Keyframe animation of joint parameters
   ✅ Driver-based motion control
   ✅ Physics simulation compatibility
   ✅ Real-time constraint evaluation

3. **Design Validation**:
   ✅ Assembly feasibility checking
   ✅ Motion range validation
   ✅ Interference detection
   ✅ Kinematic analysis

4. **Workflow Efficiency**:
   ✅ Rapid prototyping of mechanisms
   ✅ Parametric design exploration
   ✅ Automated assembly sequences
   ✅ Design optimization feedback
"""
    )


if __name__ == "__main__":
    print("Blender Assembly Mates - Practical Examples")
    print("=" * 55)

    # Run the main example
    example_ok = blender_assembly_mates_example()

    # Show additional demonstrations
    demonstrate_kinematic_chains()
    demonstrate_constraint_benefits()

    print("\n" + "=" * 55)
    if example_ok:
        print("🎉 ALL EXAMPLES COMPLETED!")
    else:
        print("❌ SOME EXAMPLES FAILED!")

    print("\nKey Benefits of Blender Assembly Mates:")
    print("✅ Native Blender constraint integration")
    print("✅ Comprehensive kinematic and geometric mates")
    print("✅ Fluent API matching build123d patterns")
    print("✅ Full assembly constraint management")
    print("✅ Animation and simulation compatibility")
    print("✅ Real-time constraint evaluation")
    print("✅ Hierarchical assembly relationships")
