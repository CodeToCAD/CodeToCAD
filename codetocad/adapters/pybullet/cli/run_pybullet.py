"""
PyBullet simulation CLI runner.

This module provides command-line interface for running PyBullet physics simulations
with CodeToCAD objects and files.
"""

import argparse
import sys
import os
import time
import json
from pathlib import Path
from typing import Dict, Any

from codetocad.adapters.pybullet.simulation.simulation import Simulation
from codetocad.core.dimensions.point import Point
from .config import get_pybullet_config, set_pybullet_config


def run_pybullet_simulation(
    input_file: str | None = None,
    output_dir: str | None = None,
    gui: bool = True,
    duration: float = 10.0,
    time_step: float = 1.0 / 240.0,
    gravity: tuple[float, float, float] = (0, 0, -9.81),
    config_file: str | None = None,
    verbose: bool = False,
    **kwargs,
) -> bool:
    """
    Run a PyBullet simulation with specified parameters.

    Args:
        input_file: Path to input file (URDF, STL, or Python script)
        output_dir: Directory to save simulation results
        gui: Whether to enable GUI visualization
        duration: Simulation duration in seconds
        time_step: Simulation time step in seconds
        gravity: Gravity vector (x, y, z)
        config_file: Path to configuration file
        verbose: Enable verbose logging
        **kwargs: Additional simulation parameters

    Returns:
        True if simulation completed successfully, False otherwise
    """
    try:
        # Load configuration if provided
        config = {}
        if config_file and os.path.exists(config_file):
            with open(config_file, "r") as f:
                config = json.load(f)
            if verbose:
                print(f"📄 Loaded configuration from {config_file}")

        # Merge config with parameters
        sim_params = {
            "gui": gui,
            "duration": duration,
            "time_step": time_step,
            "gravity": gravity,
            "verbose": verbose,
            **config,
            **kwargs,
        }

        if verbose:
            print("🚀 Starting PyBullet simulation...")
            print(f"   Input file: {input_file or 'None'}")
            print(f"   Output directory: {output_dir or 'None'}")
            print(f"   Duration: {sim_params['duration']}s")
            print(f"   Time step: {sim_params['time_step']}s")
            print(f"   GUI enabled: {sim_params['gui']}")

        # Create simulation
        sim_name = f"pybullet_cli_{int(time.time())}"
        sim = Simulation(sim_name)
        sim.initialize(gui=sim_params["gui"])

        # Set simulation parameters
        sim.set_gravity(Point(*sim_params["gravity"]))
        sim.set_time_step(sim_params["time_step"])

        # Add ground plane
        ground = sim.add_ground_plane()
        if verbose:
            print("✅ Added ground plane")

        # Load input file if provided
        bodies = []
        if input_file:
            input_path = Path(input_file)
            if not input_path.exists():
                print(f"❌ Input file not found: {input_file}")
                return False

            file_ext = input_path.suffix.lower()

            if file_ext == ".urdf":
                body = sim.load_urdf(str(input_path))
                bodies.append(body)
                if verbose:
                    print(f"✅ Loaded URDF: {input_file}")

            elif file_ext == ".stl":
                body = sim.load_stl(str(input_path), mass=sim_params.get("mass", 1.0))
                bodies.append(body)
                if verbose:
                    print(f"✅ Loaded STL: {input_file}")

            elif file_ext == ".py":
                # Execute Python script in simulation context
                exec_globals = {
                    "sim": sim,
                    "bodies": bodies,
                    "Point": Point,
                    "verbose": verbose,
                }
                with open(input_path, "r") as f:
                    script_content = f.read()
                exec(script_content, exec_globals)
                bodies = exec_globals.get("bodies", bodies)
                if verbose:
                    print(f"✅ Executed Python script: {input_file}")

            else:
                print(f"❌ Unsupported file format: {file_ext}")
                return False

        # Create output directory if specified
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            if verbose:
                print(f"📁 Created output directory: {output_dir}")

        # Run simulation
        if verbose:
            print(f"▶️  Running simulation for {sim_params['duration']} seconds...")

        sim.start()

        num_steps = int(sim_params["duration"] / sim_params["time_step"])
        results = []

        for step in range(num_steps):
            sim.step()

            # Log progress
            if verbose and step % (num_steps // 10) == 0:
                progress = (step / num_steps) * 100
                current_time = sim.get_current_time()
                print(f"   Progress: {progress:.1f}% (t={current_time:.2f}s)")

            # Record simulation state if output directory specified
            if output_dir and step % 10 == 0:  # Record every 10 steps
                state = {"time": sim.get_current_time(), "step": step, "bodies": []}

                for i, body in enumerate(bodies):
                    if hasattr(body, "get_position") and hasattr(
                        body, "get_linear_velocity"
                    ):
                        pos = body.get_position()
                        vel = body.get_linear_velocity()
                        state["bodies"].append(
                            {
                                "id": i,
                                "name": getattr(body, "name", f"body_{i}"),
                                "position": [pos.x, pos.y, pos.z],
                                "velocity": [vel.x, vel.y, vel.z],
                            }
                        )

                results.append(state)

            # Real-time simulation if GUI enabled
            if sim_params["gui"]:
                time.sleep(sim_params["time_step"])

        sim.stop()

        # Save results if output directory specified
        if output_dir and results:
            results_file = os.path.join(output_dir, f"{sim_name}_results.json")
            with open(results_file, "w") as f:
                json.dump(results, f, indent=2)
            if verbose:
                print(f"💾 Saved results to: {results_file}")

        # Save final state
        if output_dir:
            final_state = {
                "simulation_name": sim_name,
                "parameters": sim_params,
                "total_steps": num_steps,
                "final_time": sim.get_current_time(),
                "bodies_count": len(bodies),
            }

            state_file = os.path.join(output_dir, f"{sim_name}_final_state.json")
            with open(state_file, "w") as f:
                json.dump(final_state, f, indent=2)
            if verbose:
                print(f"💾 Saved final state to: {state_file}")

        if verbose:
            print("✅ Simulation completed successfully!")

        # Cleanup
        sim.disconnect()
        return True

    except Exception as e:
        print(f"❌ Simulation failed: {e}")
        if verbose:
            import traceback

            traceback.print_exc()
        return False


def main():
    """Main CLI entry point for PyBullet simulations."""
    parser = argparse.ArgumentParser(
        description="Run PyBullet physics simulations from command line",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run basic simulation with GUI
  python -m codetocad.adapters.pybullet.cli.run_pybullet --gui --duration 5

  # Load and simulate URDF file
  python -m codetocad.adapters.pybullet.cli.run_pybullet robot.urdf --duration 10 --output results/

  # Run with custom parameters
  python -m codetocad.adapters.pybullet.cli.run_pybullet --time-step 0.01 --gravity 0 0 -10

  # Use configuration file
  python -m codetocad.adapters.pybullet.cli.run_pybullet --config simulation.json
        """,
    )

    parser.add_argument(
        "input_file", nargs="?", help="Input file (URDF, STL, or Python script)"
    )
    parser.add_argument("--output", "-o", help="Output directory for results")
    parser.add_argument("--gui", action="store_true", help="Enable GUI visualization")
    parser.add_argument(
        "--no-gui", action="store_true", help="Disable GUI visualization"
    )
    parser.add_argument(
        "--duration",
        "-d",
        type=float,
        default=10.0,
        help="Simulation duration in seconds",
    )
    parser.add_argument(
        "--time-step",
        "-t",
        type=float,
        default=1.0 / 240.0,
        help="Simulation time step",
    )
    parser.add_argument(
        "--gravity",
        nargs=3,
        type=float,
        default=[0, 0, -9.81],
        help="Gravity vector (x y z)",
    )
    parser.add_argument(
        "--mass", type=float, default=1.0, help="Default mass for loaded objects"
    )
    parser.add_argument("--config", "-c", help="Configuration file (JSON)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--save-config", help="Save current parameters to config file")

    args = parser.parse_args()

    # Handle GUI flags
    gui = True  # Default
    if args.no_gui:
        gui = False
    elif args.gui:
        gui = True

    # Save configuration if requested
    if args.save_config:
        config = {
            "gui": gui,
            "duration": args.duration,
            "time_step": args.time_step,
            "gravity": args.gravity,
            "mass": args.mass,
        }
        with open(args.save_config, "w") as f:
            json.dump(config, f, indent=2)
        print(f"💾 Saved configuration to: {args.save_config}")
        return

    # Run simulation
    success = run_pybullet_simulation(
        input_file=args.input_file,
        output_dir=args.output,
        gui=gui,
        duration=args.duration,
        time_step=args.time_step,
        gravity=tuple(args.gravity),
        config_file=args.config,
        verbose=args.verbose,
        mass=args.mass,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
