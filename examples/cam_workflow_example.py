"""
CAM Workflow Example for CodeToCAD.

This example demonstrates a complete CAM workflow including:
1. Tool library setup with presets
2. Toolpath generation for different operations
3. Work coordinate system setup
4. Job management and organization
5. G-code post-processing simulation
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from codetocad.core.cam.tool import Tool
from codetocad.core.cam.toolpath import Toolpath
from codetocad.core.cam.tool_library import ToolLibrary
from codetocad.core.cam.work_coordinate_system import WorkCoordinateSystem

from codetocad.interfaces.cam.toolpath_interface import (
    ToolpathStrategy,
    ToolpathOperation,
    CuttingParameters,
)
from codetocad.interfaces.cam.work_coordinate_system_interface import (
    WCSOrigin,
    WorkpieceSetup,
)


def create_sample_tool_library():
    """Create a sample tool library with various tools."""
    print("🔧 Creating Tool Library...")

    library = ToolLibrary()
    library.set_name("Sample CNC Tool Library")
    library.set_description("A collection of common CNC tools for aluminum machining")

    # Add roughing tools
    roughing_6mm = Tool.preset.end_mill.roughing_carbide_6mm(tool_number=1)
    roughing_10mm = Tool.preset.end_mill.roughing_carbide_10mm(tool_number=2)

    # Add finishing tools
    finishing_3mm = Tool.preset.end_mill.finishing_carbide_3mm(tool_number=3)
    finishing_6mm = Tool.preset.end_mill.finishing_carbide_6mm(tool_number=4)

    # Add drilling tools
    center_drill = Tool.preset.drill.center_drill_60_degree(tool_number=5)
    twist_drill_5mm = Tool.preset.drill.twist_drill_carbide_5mm(tool_number=6)
    twist_drill_8mm = Tool.preset.drill.twist_drill_carbide_8mm(tool_number=7)

    # Add specialty tools
    ball_mill_3mm = Tool.preset.ball_mill.ball_mill_carbide_3mm(tool_number=8)
    v_bit_90deg = Tool.preset.v_bit.engraving_90_degree(tool_number=9)
    chamfer_45deg = Tool.preset.v_bit.chamfer_45_degree(tool_number=10)

    # Add all tools to library
    tools = [
        roughing_6mm,
        roughing_10mm,
        finishing_3mm,
        finishing_6mm,
        center_drill,
        twist_drill_5mm,
        twist_drill_8mm,
        ball_mill_3mm,
        v_bit_90deg,
        chamfer_45deg,
    ]

    for tool in tools:
        library.add_tool(tool)
        print(f"  ✓ Added: {tool.name} (T{tool.tool_number})")

    # Print library statistics
    stats = library.get_library_statistics()
    print(f"\n📊 Library Statistics:")
    print(f"  Total tools: {stats['total_tools']}")
    print(f"  Tool types: {', '.join(stats['tool_types'].keys())}")
    print(
        f"  Diameter range: {stats['diameter_range']['min']:.1f} - {stats['diameter_range']['max']:.1f} mm"
    )
    print(
        f"  Manufacturers: {', '.join(stats['manufacturers']) if stats['manufacturers'] else 'Generic'}"
    )

    return library


def setup_work_coordinate_system():
    """Setup work coordinate system for the job."""
    print("\n📐 Setting up Work Coordinate System...")

    wcs = WorkCoordinateSystem()
    wcs.set_name("Main WCS")
    wcs.set_description("Primary work coordinate system for aluminum part")

    # Define workpiece
    workpiece = WorkpieceSetup(
        length=100.0,  # X dimension
        width=50.0,  # Y dimension
        height=20.0,  # Z dimension
        stock_to_leave=0.5,  # 0.5mm stock allowance
        fixture_height=5.0,  # 5mm vise height
    )
    wcs.set_workpiece_setup(workpiece)

    # Set origin at bottom-left-front corner
    wcs.set_origin_from_preset(WCSOrigin.BOTTOM_LEFT_FRONT)

    print(
        f"  ✓ Workpiece: {workpiece.length} × {workpiece.width} × {workpiece.height} mm"
    )
    print(f"  ✓ Origin: {WCSOrigin.BOTTOM_LEFT_FRONT.value}")
    print(f"  ✓ Stock allowance: {workpiece.stock_to_leave} mm")

    return wcs


def create_roughing_toolpath(library: ToolLibrary):
    """Create roughing toolpath operation."""
    print("\n🏗️  Creating Roughing Toolpath...")

    # Get roughing tool
    roughing_tool = library.get_tool(2)  # 10mm roughing end mill

    # Create toolpath
    toolpath = Toolpath()
    toolpath.set_name("Roughing Operation")
    toolpath.set_operation(ToolpathOperation.ROUGHING)
    toolpath.set_strategy(ToolpathStrategy.ADAPTIVE_CLEARING)
    toolpath.set_tool(roughing_tool)
    toolpath.set_description("Adaptive roughing to remove bulk material")

    # Set aggressive cutting parameters for roughing
    cutting_params = CuttingParameters(
        depth_of_cut=15.0,  # Cut 15mm deep
        step_down=3.0,  # 3mm per pass
        step_over=0.6,  # 60% stepover for roughing
        feed_rate=2400,  # Fast feed rate
        spindle_speed=12000,
        plunge_rate=600,
        safe_height=5.0,
        clearance_height=2.0,
    )
    toolpath.set_cutting_parameters(cutting_params)

    print(f"  ✓ Tool: {roughing_tool.name}")
    print(f"  ✓ Strategy: {toolpath.strategy.value}")
    print(f"  ✓ Depth of cut: {cutting_params.depth_of_cut} mm")
    print(f"  ✓ Feed rate: {cutting_params.feed_rate} mm/min")

    return toolpath


def create_finishing_toolpath(library: ToolLibrary):
    """Create finishing toolpath operation."""
    print("\n✨ Creating Finishing Toolpath...")

    # Get finishing tool
    finishing_tool = library.get_tool(4)  # 6mm finishing end mill

    # Create toolpath
    toolpath = Toolpath()
    toolpath.set_name("Finishing Operation")
    toolpath.set_operation(ToolpathOperation.FINISHING)
    toolpath.set_strategy(ToolpathStrategy.PROFILE)
    toolpath.set_tool(finishing_tool)
    toolpath.set_description("Profile finishing for final dimensions")

    # Set precise cutting parameters for finishing
    cutting_params = CuttingParameters(
        depth_of_cut=0.5,  # Light finishing pass
        step_down=0.5,  # Single pass
        step_over=0.3,  # 30% stepover for good finish
        feed_rate=1800,  # Moderate feed rate
        spindle_speed=18000,
        plunge_rate=450,
        safe_height=5.0,
        clearance_height=2.0,
        finish_passes=1,  # One spring pass
    )
    toolpath.set_cutting_parameters(cutting_params)

    print(f"  ✓ Tool: {finishing_tool.name}")
    print(f"  ✓ Strategy: {toolpath.strategy.value}")
    print(f"  ✓ Depth of cut: {cutting_params.depth_of_cut} mm")
    print(f"  ✓ Feed rate: {cutting_params.feed_rate} mm/min")

    return toolpath


def create_drilling_toolpath(library: ToolLibrary):
    """Create drilling toolpath operation."""
    print("\n🕳️  Creating Drilling Toolpath...")

    # Get drilling tools
    center_drill = library.get_tool(5)  # Center drill
    twist_drill = library.get_tool(6)  # 5mm twist drill

    # Create center drilling toolpath
    center_toolpath = Toolpath()
    center_toolpath.set_name("Center Drilling")
    center_toolpath.set_operation(ToolpathOperation.DRILLING)
    center_toolpath.set_strategy(ToolpathStrategy.DRILLING)
    center_toolpath.set_tool(center_drill)

    # Center drilling parameters
    center_params = CuttingParameters(
        depth_of_cut=2.0,  # Light center drill depth
        step_down=1.0,
        step_over=1.0,  # Not applicable for drilling
        feed_rate=100,  # Slow for center drilling
        spindle_speed=4000,
        plunge_rate=100,
        safe_height=5.0,
        clearance_height=2.0,
    )
    center_toolpath.set_cutting_parameters(center_params)

    # Generate drilling pattern
    drill_points = [
        (20, 15),  # First hole
        (80, 15),  # Second hole
        (20, 35),  # Third hole
        (80, 35),  # Fourth hole
    ]
    center_toolpath.generate_drilling_pattern(drill_points, 2.0)

    # Create main drilling toolpath
    drill_toolpath = Toolpath()
    drill_toolpath.set_name("Through Drilling")
    drill_toolpath.set_operation(ToolpathOperation.DRILLING)
    drill_toolpath.set_strategy(ToolpathStrategy.DRILLING)
    drill_toolpath.set_tool(twist_drill)

    # Main drilling parameters
    drill_params = CuttingParameters(
        depth_of_cut=22.0,  # Through hole + extra
        step_down=3.0,  # Peck drilling
        step_over=1.0,
        feed_rate=200,
        spindle_speed=3000,
        plunge_rate=200,
        safe_height=5.0,
        clearance_height=2.0,
    )
    drill_toolpath.set_cutting_parameters(drill_params)
    drill_toolpath.generate_drilling_pattern(drill_points, 22.0)

    print(f"  ✓ Center drill: {center_drill.name}")
    print(f"  ✓ Twist drill: {twist_drill.name}")
    print(f"  ✓ Hole pattern: {len(drill_points)} holes")
    print(f"  ✓ Center drilling points: {len(center_toolpath.points)}")
    print(f"  ✓ Main drilling points: {len(drill_toolpath.points)}")

    return [center_toolpath, drill_toolpath]


def create_chamfer_toolpath(library: ToolLibrary):
    """Create chamfering toolpath operation."""
    print("\n🔷 Creating Chamfer Toolpath...")

    # Get chamfer tool
    chamfer_tool = library.get_tool(10)  # 45° chamfer mill

    # Create toolpath
    toolpath = Toolpath()
    toolpath.set_name("Edge Chamfering")
    toolpath.set_operation(ToolpathOperation.CHAMFERING)
    toolpath.set_strategy(ToolpathStrategy.PROFILE)
    toolpath.set_tool(chamfer_tool)
    toolpath.set_description("Chamfer all edges for deburring")

    # Chamfering parameters
    cutting_params = CuttingParameters(
        depth_of_cut=1.0,  # 1mm chamfer
        step_down=1.0,  # Single pass
        step_over=0.8,
        feed_rate=800,  # Moderate feed
        spindle_speed=15000,
        plunge_rate=200,
        safe_height=5.0,
        clearance_height=2.0,
    )
    toolpath.set_cutting_parameters(cutting_params)

    print(f"  ✓ Tool: {chamfer_tool.name}")
    print(f"  ✓ Chamfer size: {cutting_params.depth_of_cut} mm")
    print(f"  ✓ Feed rate: {cutting_params.feed_rate} mm/min")

    return toolpath


def analyze_machining_job(toolpaths: list):
    """Analyze the complete machining job."""
    print("\n📊 Job Analysis:")

    total_time = 0
    total_length = 0
    tools_used = set()

    for i, toolpath in enumerate(toolpaths, 1):
        if isinstance(toolpath, list):
            # Handle drilling operations (list of toolpaths)
            for j, tp in enumerate(toolpath):
                time_est = tp.get_machining_time_estimate()
                length = tp.get_total_length()
                total_time += time_est
                total_length += length
                tools_used.add(tp.tool.tool_number)
                print(
                    f"  {i}.{j+1} {tp.name}: {length:.1f}mm, {time_est:.1f}min, T{tp.tool.tool_number}"
                )
        else:
            time_est = toolpath.get_machining_time_estimate()
            length = toolpath.get_total_length()
            total_time += time_est
            total_length += length
            tools_used.add(toolpath.tool.tool_number)
            print(
                f"  {i}. {toolpath.name}: {length:.1f}mm, {time_est:.1f}min, T{toolpath.tool.tool_number}"
            )

    print(f"\n📈 Summary:")
    print(f"  Total toolpath length: {total_length:.1f} mm")
    print(
        f"  Estimated machining time: {total_time:.1f} minutes ({total_time/60:.1f} hours)"
    )
    print(f"  Tools required: {len(tools_used)} ({sorted(tools_used)})")
    print(f"  Tool changes: {len(tools_used) - 1}")


def save_tool_library_example(library: ToolLibrary):
    """Save tool library to file as example."""
    print("\n💾 Saving Tool Library...")

    # Save to JSON format
    json_path = project_root / "examples" / "sample_tool_library.json"
    library.save_to_file(json_path)
    print(f"  ✓ Saved JSON: {json_path}")

    # Export to CSV format
    csv_path = project_root / "examples" / "sample_tool_library.csv"
    library.export_to_format(csv_path, "csv")
    print(f"  ✓ Exported CSV: {csv_path}")


def main():
    """Main CAM workflow example."""
    print("🏭 CodeToCAD CAM Workflow Example")
    print("=" * 50)

    try:
        # Step 1: Create tool library
        library = create_sample_tool_library()

        # Step 2: Setup work coordinate system
        wcs = setup_work_coordinate_system()

        # Step 3: Create toolpaths for different operations
        roughing_tp = create_roughing_toolpath(library)
        finishing_tp = create_finishing_toolpath(library)
        drilling_tps = create_drilling_toolpath(library)
        chamfer_tp = create_chamfer_toolpath(library)

        # Step 4: Analyze complete job
        all_toolpaths = [roughing_tp, finishing_tp, drilling_tps, chamfer_tp]
        analyze_machining_job(all_toolpaths)

        # Step 5: Save examples
        save_tool_library_example(library)

        print("\n✅ CAM workflow example completed successfully!")
        print("\nThis example demonstrated:")
        print("  • Tool library creation with presets")
        print("  • Work coordinate system setup")
        print(
            "  • Multiple toolpath operations (roughing, finishing, drilling, chamfering)"
        )
        print("  • Job analysis and time estimation")
        print("  • Tool library export formats")

        print(f"\nNext steps:")
        print(
            "  • Integrate with FreeCAD Path Workbench for actual toolpath generation"
        )
        print("  • Add G-code post-processing")
        print("  • Implement simulation and verification")
        print("  • Connect to actual CAD geometry")

    except Exception as e:
        print(f"❌ Error in CAM workflow: {e}")
        import traceback

        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
