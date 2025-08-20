"""
Example demonstrating assembly mate functionality with build123d adapter.

This example shows how to create parts, assemble them, and apply various
types of mates to constrain their relationships.
"""


def example_assembly_mates():
    """Example of creating an assembly with various mate types."""
    try:
        from codetocad.adapters.build123d import Part, Assembly, MateType

        print("Creating parts for assembly mate example...")

        # Create some basic parts
        base_part = Part.preset.cube(10, 10, 2)
        base_part.set_name("base")

        moving_part = Part.preset.cylinder(2, 5)
        moving_part.set_name("cylinder")

        lid_part = Part.preset.cube(8, 8, 1)
        lid_part.set_name("lid")

        print(f"Created parts: {base_part.name}, {moving_part.name}, {lid_part.name}")

        # Create assembly
        assembly = Assembly("mate_example_assembly")
        assembly.add_part(base_part)
        assembly.add_part(moving_part)
        assembly.add_part(lid_part)

        print(f"Created assembly with {len(assembly)} parts")

        # Example 1: Rigid mate - fix the cylinder to the base (NEW FLUENT API)
        print("\n--- Creating Rigid Mate (Fluent API) ---")
        rigid_mate = assembly.mate.rigid(
            base_part,
            moving_part,
            location1=None,  # Location on base part
            location2=None,  # Location on cylinder part
            name="cylinder_to_base",
        )

        if rigid_mate:
            print(f"Successfully created rigid mate: {rigid_mate.name}")
            print(f"Mate status: {rigid_mate.status.value}")
        else:
            print("Failed to create rigid mate")

        # Example 2: Distance mate - keep lid at specific distance from base (NEW FLUENT API)
        print("\n--- Creating Distance Mate (Fluent API) ---")
        distance_mate = assembly.mate.distance(
            base_part,
            lid_part,
            entity1=None,  # Would be specific face in real implementation
            entity2=None,  # Would be specific face in real implementation
            distance=5.0,
            name="lid_distance",
        )

        if distance_mate:
            print(f"Successfully created distance mate: {distance_mate.name}")
            print(f"Distance: {distance_mate.distance}")
        else:
            print("Failed to create distance mate")

        # Example 3: Revolute mate - allow rotation (NEW FLUENT API)
        print("\n--- Creating Revolute Mate (Fluent API) ---")
        try:
            import build123d as bd

            axis = bd.Axis((0, 0, 0), (0, 0, 1))  # Z-axis
            location1 = bd.Location((0, 0, 1))  # Location on base part
            location2 = bd.Location((0, 0, 0))  # Location on cylinder part

            revolute_mate = assembly.mate.revolute(
                base_part,
                moving_part,
                axis=axis,
                location1=location1,
                location2=location2,
                angle_range=(0, 180),
                current_angle=45,
                name="cylinder_rotation",
            )

            if revolute_mate:
                print(f"Successfully created revolute mate: {revolute_mate.name}")
                print(f"Current angle: {revolute_mate.current_angle}°")
                print(f"Angle range: {revolute_mate.angle_range}")

                # Test changing the angle
                if revolute_mate.set_angle(90):
                    print(f"Changed angle to: {revolute_mate.current_angle}°")
                else:
                    print("Failed to change angle")
            else:
                print("Failed to create revolute mate")

        except ImportError:
            print("build123d not available for revolute mate example")

        # Display assembly statistics
        print("\n--- Assembly Statistics ---")
        stats = assembly.get_mate_statistics()
        print(f"Total mates: {stats['total']}")
        print(f"Active mates: {stats['active']}")
        print(f"Failed mates: {stats['failed']}")

        # List all mates
        print("\n--- All Mates ---")
        all_mates = assembly.get_all_mates()
        for mate in all_mates:
            print(f"  {mate}")

        # Validate all mates
        print("\n--- Mate Validation ---")
        validation_results = assembly.validate_mates()
        for mate_name, is_valid in validation_results.items():
            status = "✓ Valid" if is_valid else "✗ Invalid"
            print(f"  {mate_name}: {status}")

        # Solve mates
        print("\n--- Solving Mates ---")
        if assembly.solve_mates():
            print("All mates solved successfully")
        else:
            print("Some mates failed to solve")

        return assembly

    except ImportError as e:
        print(f"build123d is not installed: {e}")
        print("Install build123d with: pip install build123d")
        return None
    except Exception as e:
        print(f"Error in assembly mates example: {e}")
        return None


def example_kinematic_mates():
    """Example focusing on kinematic mates that allow motion."""
    try:
        from codetocad.adapters.build123d import Part, Assembly, MateType
        import build123d as bd

        print("\n" + "=" * 50)
        print("KINEMATIC MATES EXAMPLE")
        print("=" * 50)

        # Create parts for kinematic assembly
        base = Part.preset.cube(20, 20, 5)
        base.set_name("kinematic_base")

        slider = Part.preset.cube(5, 5, 10)
        slider.set_name("slider")

        rotor = Part.preset.cylinder(3, 8)
        rotor.set_name("rotor")

        # Create assembly
        assembly = Assembly("kinematic_assembly")
        assembly.add_part(base)
        assembly.add_part(slider)
        assembly.add_part(rotor)

        print(f"Created kinematic assembly with {len(assembly)} parts")

        # Linear mate - slider can move along X axis (NEW FLUENT API)
        print("\n--- Linear Mate Example (Fluent API) ---")
        linear_axis = bd.Axis((0, 0, 0), (1, 0, 0))  # X-axis
        location1 = bd.Location((10, 0, 0))  # Location on base
        location2 = bd.Location((0, 0, 0))  # Location on slider

        linear_mate = assembly.mate.linear(
            base,
            slider,
            axis=linear_axis,
            location1=location1,
            location2=location2,
            position_range=(-10, 10),
            current_position=0,
            name="slider_motion",
        )

        if linear_mate:
            print(f"Created linear mate: {linear_mate.name}")
            print(f"Position range: {linear_mate.position_range}")

            # Test moving the slider
            positions = [-5, 0, 5, 8]
            for pos in positions:
                if linear_mate.set_position_value(pos):
                    print(f"  Moved slider to position: {pos}")
                else:
                    print(f"  Failed to move slider to position: {pos}")

        # Cylindrical mate - rotor can rotate and translate (NEW FLUENT API)
        print("\n--- Cylindrical Mate Example (Fluent API) ---")
        cylindrical_axis = bd.Axis((0, 0, 0), (0, 0, 1))  # Z-axis
        location1 = bd.Location((0, 0, 2.5))  # Location on base
        location2 = bd.Location((0, 0, 0))  # Location on rotor

        cylindrical_mate = assembly.mate.cylindrical(
            base,
            rotor,
            axis=cylindrical_axis,
            location1=location1,
            location2=location2,
            position_range=(0, 15),
            angle_range=(0, 360),
            current_position=5,
            current_angle=0,
            name="rotor_motion",
        )

        if cylindrical_mate:
            print(f"Created cylindrical mate: {cylindrical_mate.name}")
            print(f"Degrees of freedom: {cylindrical_mate.get_degrees_of_freedom()}")

            # Test combined motion
            test_moves = [
                (3, 45),  # position=3, angle=45°
                (8, 90),  # position=8, angle=90°
                (12, 180),  # position=12, angle=180°
            ]

            for pos, angle in test_moves:
                if cylindrical_mate.set_position_and_angle(pos, angle):
                    current = cylindrical_mate.get_position()
                    print(
                        f"  Moved rotor to position={current['position']}, angle={current['angle']}°"
                    )
                else:
                    print(f"  Failed to move rotor to position={pos}, angle={angle}°")

        # Display final statistics
        print("\n--- Final Assembly State ---")
        stats = assembly.get_mate_statistics()
        for key, value in stats.items():
            if key != "total" and value > 0:
                print(f"  {key.replace('_', ' ').title()}: {value}")

        return assembly

    except ImportError as e:
        print(f"build123d is not installed: {e}")
        return None
    except Exception as e:
        print(f"Error in kinematic mates example: {e}")
        return None


def example_geometric_mates():
    """Example focusing on geometric constraint mates."""
    try:
        from codetocad.adapters.build123d import Part, Assembly, MateType

        print("\n" + "=" * 50)
        print("GEOMETRIC MATES EXAMPLE")
        print("=" * 50)

        # Create parts for geometric constraints
        part1 = Part.preset.cube(10, 10, 5)
        part1.set_name("block1")

        part2 = Part.preset.cube(8, 8, 3)
        part2.set_name("block2")

        part3 = Part.preset.cylinder(2, 6)
        part3.set_name("pin")

        # Create assembly
        assembly = Assembly("geometric_assembly")
        assembly.add_part(part1)
        assembly.add_part(part2)
        assembly.add_part(part3)

        print(f"Created geometric assembly with {len(assembly)} parts")

        # Coincident mate - align faces (NEW FLUENT API)
        print("\n--- Coincident Mate Example (Fluent API) ---")
        coincident_mate = assembly.mate.coincident(
            part1,
            part2,
            entity1=None,  # Would be specific face in real implementation
            entity2=None,  # Would be specific face in real implementation
            flip_alignment=False,
            name="align_faces",
        )

        if coincident_mate:
            print(f"Created coincident mate: {coincident_mate.name}")
            print(f"Flip alignment: {coincident_mate.flip_alignment}")

        # Parallel mate - keep faces parallel (NEW FLUENT API)
        print("\n--- Parallel Mate Example (Fluent API) ---")
        parallel_mate = assembly.mate.parallel(
            part1,
            part2,
            entity1=None,  # Would be specific face
            entity2=None,  # Would be specific face
            name="parallel_faces",
        )

        if parallel_mate:
            print(f"Created parallel mate: {parallel_mate.name}")

        # Angle mate - maintain specific angle (NEW FLUENT API)
        print("\n--- Angle Mate Example (Fluent API) ---")
        angle_mate = assembly.mate.angle(
            part1,
            part2,
            entity1=None,  # Would be specific face
            entity2=None,  # Would be specific face
            angle=45.0,
            name="angled_faces",
        )

        if angle_mate:
            print(f"Created angle mate: {angle_mate.name}")
            print(f"Angle: {angle_mate.angle}°")

        # Concentric mate - align cylindrical features (NEW FLUENT API)
        print("\n--- Concentric Mate Example (Fluent API) ---")
        concentric_mate = assembly.mate.concentric(
            part1,
            part3,
            entity1=None,  # Would be cylindrical face/edge
            entity2=None,  # Would be cylindrical face/edge
            name="align_cylinders",
        )

        if concentric_mate:
            print(f"Created concentric mate: {concentric_mate.name}")

        # Show all geometric constraints
        print("\n--- Geometric Constraints Summary ---")
        geometric_mates = assembly.mate_manager.get_mates_by_type(MateType.COINCIDENT)
        geometric_mates.extend(
            assembly.mate_manager.get_mates_by_type(MateType.PARALLEL)
        )
        geometric_mates.extend(assembly.mate_manager.get_mates_by_type(MateType.ANGLE))
        geometric_mates.extend(
            assembly.mate_manager.get_mates_by_type(MateType.CONCENTRIC)
        )

        for mate in geometric_mates:
            print(f"  {mate.mate_type.value.title()}: {mate.name}")

        return assembly

    except Exception as e:
        print(f"Error in geometric mates example: {e}")
        return None


if __name__ == "__main__":
    print("Assembly Mates Examples")
    print("=" * 50)

    # Run all examples
    basic_assembly = example_assembly_mates()
    kinematic_assembly = example_kinematic_mates()
    geometric_assembly = example_geometric_mates()

    print("\n" + "=" * 50)
    print("Examples completed!")

    if basic_assembly:
        print(f"Basic assembly: {len(basic_assembly.get_all_mates())} mates")
    if kinematic_assembly:
        print(f"Kinematic assembly: {len(kinematic_assembly.get_all_mates())} mates")
    if geometric_assembly:
        print(f"Geometric assembly: {len(geometric_assembly.get_all_mates())} mates")
