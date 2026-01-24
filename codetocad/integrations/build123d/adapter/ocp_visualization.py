"""
OCP Visualization utilities for build123d joints and assemblies.

This module provides helper functions for visualizing build123d objects
with joints using the ocp-vscode extension.

Requirements:
    pip install ocp-vscode

Usage:
    from codetocad.integrations.build123d.adapter.ocp_visualization import (
        show_with_joints,
        show_assembly,
        setup_ocp_viewer,
    )
"""

from typing import Any
import build123d as bd


def check_ocp_available() -> bool:
    """Check if ocp_vscode is available."""
    try:
        import ocp_vscode

        return True
    except ImportError:
        return False


def setup_ocp_viewer(**kwargs) -> None:
    """Setup OCP viewer with default settings for joint visualization.

    Args:
        **kwargs: Additional settings to pass to ocp_vscode.set_defaults()
    """
    try:
        from ocp_vscode import set_defaults

        defaults = {
            "render_joints": True,
            "reset_camera": True,
            "helper_scale": 1.0,
            "default_opacity": 0.8,
        }
        defaults.update(kwargs)
        set_defaults(**defaults)
    except ImportError:
        print("ocp_vscode not available. Install with: pip install ocp-vscode")


def show_with_joints(
    *parts: "bd.Part | bd.Solid | bd.Compound",
    render_joints: bool = True,
    reset_camera: bool = True,
    **kwargs,
) -> None:
    """Show parts with joint visualization enabled.

    Args:
        *parts: Build123d parts to display
        render_joints: Whether to render joint symbols
        reset_camera: Whether to reset camera view
        **kwargs: Additional arguments for ocp_vscode.show()
    """
    try:
        from ocp_vscode import show

        show(*parts, render_joints=render_joints, reset_camera=reset_camera, **kwargs)
    except ImportError:
        print("ocp_vscode not available. Install with: pip install ocp-vscode")
        print(f"Would display {len(parts)} parts")


def show_assembly(
    assembly_name: str,
    parts: list["bd.Part | bd.Solid | bd.Compound"],
    render_joints: bool = True,
    show_axes: bool = True,
    **kwargs,
) -> None:
    """Show an assembly with parts and joints.

    Args:
        assembly_name: Name for the assembly in the viewer
        parts: List of parts in the assembly
        render_joints: Whether to render joint symbols
        show_axes: Whether to show coordinate axes
        **kwargs: Additional arguments for ocp_vscode.show()
    """
    try:
        from ocp_vscode import show, set_defaults

        set_defaults(render_joints=render_joints)
        show(*parts, reset_camera=True, **kwargs)
        print(f"Showing assembly '{assembly_name}' with {len(parts)} parts")
    except ImportError:
        print("ocp_vscode not available. Install with: pip install ocp-vscode")


def export_assembly_screenshot(
    parts: list["bd.Part | bd.Solid | bd.Compound"],
    filename: str,
    width: int = 1920,
    height: int = 1080,
) -> None:
    """Export assembly screenshot (if supported by ocp-vscode).

    Args:
        parts: Parts to capture
        filename: Output filename (PNG)
        width: Image width
        height: Image height
    """
    try:
        from ocp_vscode import show

        # Note: Screenshot functionality may vary by ocp-vscode version
        show(*parts, render_joints=True)
        print(f"Screenshot export not directly supported. Use OCP viewer UI.")
    except ImportError:
        print("ocp_vscode not available")


def get_joint_info(part: "bd.Part | bd.Solid | bd.Compound") -> list[dict[str, Any]]:
    """Get information about joints attached to a part.

    Args:
        part: The part to inspect

    Returns:
        List of dictionaries with joint information
    """
    joints_info = []

    if hasattr(part, "joints"):
        for label, joint in part.joints.items():
            info = {
                "label": label,
                "type": type(joint).__name__,
                "location": str(joint.location) if hasattr(joint, "location") else None,
            }

            # Add type-specific info
            if hasattr(joint, "angular_range"):
                info["angular_range"] = joint.angular_range
            if hasattr(joint, "linear_range"):
                info["linear_range"] = joint.linear_range
            if hasattr(joint, "axis"):
                info["axis"] = str(joint.axis) if hasattr(joint.axis, "__str__") else None

            joints_info.append(info)

    return joints_info


def print_joint_summary(parts: list["bd.Part | bd.Solid | bd.Compound"]) -> None:
    """Print a summary of all joints in the given parts."""
    print("\n=== Joint Summary ===")
    for i, part in enumerate(parts):
        joints = get_joint_info(part)
        if joints:
            print(f"\nPart {i}:")
            for joint in joints:
                print(f"  - {joint['label']} ({joint['type']})")
                if joint.get("angular_range"):
                    print(f"    Angular range: {joint['angular_range']}")
                if joint.get("linear_range"):
                    print(f"    Linear range: {joint['linear_range']}")

