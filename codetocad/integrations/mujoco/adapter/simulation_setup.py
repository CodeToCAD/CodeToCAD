"""
MuJoCo simulation setup and management functions.
"""

from typing import Tuple, Any
import mujoco as mj
import numpy as np
from codetocad.core.dimensions.point import Point


def initialize_mujoco_model(
    xml_string: str | None = None, xml_path: str | None = None
) -> mj.MjModel:
    """Initialize MuJoCo model from XML."""
    if xml_string:
        model = mj.MjModel.from_xml_string(xml_string)
    elif xml_path:
        model = mj.MjModel.from_xml_path(xml_path)
    else:
        # Create minimal default model
        default_xml = """
        <mujoco>
            <worldbody>
                <geom name="ground" type="plane" size="10 10 0.1" rgba="0.8 0.8 0.8 1"/>
            </worldbody>
        </mujoco>
        """
        model = mj.MjModel.from_xml_string(default_xml)

    return model


def create_mujoco_data(model: mj.MjModel) -> mj.MjData:
    """Create MuJoCo data structure."""
    return mj.MjData(model)


def step_mujoco_simulation(
    model: mj.MjModel, data: mj.MjData, num_steps: int = 1
) -> None:
    """Step the MuJoCo simulation forward."""
    for _ in range(num_steps):
        mj.mj_step(model, data)


def reset_mujoco_simulation(model: mj.MjModel, data: mj.MjData) -> None:
    """Reset the MuJoCo simulation."""
    mj.mj_resetData(model, data)


def set_mujoco_gravity(
    model: mj.MjModel, gravity: Point | tuple[float, float, float]
) -> None:
    """Set gravity in MuJoCo model."""
    if isinstance(gravity, Point):
        gravity_vec = np.array([gravity.x, gravity.y, gravity.z])
    else:
        gravity_vec = np.array(gravity)

    model.opt.gravity[:] = gravity_vec


def set_mujoco_timestep(model: mj.MjModel, timestep: float) -> None:
    """Set simulation timestep."""
    model.opt.timestep = timestep


def get_simulation_time(data: mj.MjData) -> float:
    """Get current simulation time."""
    return data.time


def set_solver_parameters(
    model: mj.MjModel, iterations: int = 100, tolerance: float = 1e-6
) -> None:
    """Set solver parameters."""
    model.opt.iterations = iterations
    model.opt.tolerance = tolerance


def enable_contact_detection(model: mj.MjModel, enable: bool = True) -> None:
    """Enable or disable contact detection."""
    if enable:
        model.opt.disableflags &= ~mj.mjtDisableBit.mjDSBL_CONTACT
    else:
        model.opt.disableflags |= mj.mjtDisableBit.mjDSBL_CONTACT


def set_integrator(model: mj.MjModel, integrator: str = "euler") -> None:
    """Set the integrator type."""
    integrator_map = {
        "euler": mj.mjtIntegrator.mjINT_EULER,
        "rk4": mj.mjtIntegrator.mjINT_RK4,
        "implicit": mj.mjtIntegrator.mjINT_IMPLICIT,
    }

    if integrator in integrator_map:
        model.opt.integrator = integrator_map[integrator]


def configure_visualization_options(model: mj.MjModel) -> None:
    """Configure visualization options."""
    # Enable visualization flags
    model.vis.global_.fovy = 45
    model.vis.quality.shadowsize = 4096
    model.vis.quality.offsamples = 4


def save_model_xml(model: mj.MjModel, filename: str) -> None:
    """Save model to XML file."""
    xml_string = mj.mj_saveXML(model, None, None, 0)
    with open(filename, "w") as f:
        f.write(xml_string)


def get_model_info(model: mj.MjModel) -> dict[str, Any]:
    """Get model information."""
    return {
        "nbody": model.nbody,
        "njnt": model.njnt,
        "ngeom": model.ngeom,
        "nsite": model.nsite,
        "nsensor": model.nsensor,
        "nactuator": model.nactuator,
        "nq": model.nq,
        "nv": model.nv,
        "timestep": model.opt.timestep,
        "gravity": model.opt.gravity.copy(),
    }


def compile_model(xml_string: str) -> mj.MjModel:
    """Compile XML string to MuJoCo model."""
    try:
        model = mj.MjModel.from_xml_string(xml_string)
        return model
    except Exception as e:
        raise RuntimeError(f"Failed to compile MuJoCo model: {e}")


def validate_model(model: mj.MjModel) -> bool:
    """Validate MuJoCo model."""
    try:
        # Try to create data - this will fail if model is invalid
        data = mj.MjData(model)
        return True
    except Exception:
        return False
