"""Shared headless screenshot helper for the PyBullet example renders."""
import numpy as np
import pybullet as p
import pybullet_data
from PIL import Image


def _matrices(sim, eye, target, fov, width, height):
    view_matrix = p.computeViewMatrix(
        cameraEyePosition=eye,
        cameraTargetPosition=target,
        cameraUpVector=[0, 0, 1],
        physicsClientId=sim.client,
    )
    proj_matrix = p.computeProjectionMatrixFOV(
        fov=fov, aspect=width / height, nearVal=0.01, farVal=5.0
    )
    return view_matrix, proj_matrix


def _frame(sim, view_matrix, proj_matrix, width, height):
    img = p.getCameraImage(
        width,
        height,
        view_matrix,
        proj_matrix,
        lightDirection=[1.0, 1.0, 2.0],
        shadow=1,
        renderer=p.ER_TINY_RENDERER,
        physicsClientId=sim.client,
    )
    rgba = np.array(img[2], dtype=np.uint8).reshape(height, width, 4)
    return Image.fromarray(rgba[:, :, :3], "RGB")


def capture(sim, out_png, eye, target, fov=48, width=1000, height=850):
    """Add a ground plane and save a DIRECT-mode render of ``sim`` to
    ``out_png``, looking from ``eye`` towards ``target``."""
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.loadURDF("plane.urdf", physicsClientId=sim.client)

    view_matrix, proj_matrix = _matrices(sim, eye, target, fov, width, height)
    _frame(sim, view_matrix, proj_matrix, width, height).save(out_png)
    print("saved", out_png)


def record_gif(
    sim, out_gif, *, duration_seconds, fps, eye, target, fov=48, width=480, height=360
):
    """Add a ground plane, step ``sim``, and record a DIRECT-mode render
    every ``1/fps`` seconds into an animated GIF."""
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.loadURDF("plane.urdf", physicsClientId=sim.client)

    view_matrix, proj_matrix = _matrices(sim, eye, target, fov, width, height)
    steps_per_frame = max(1, round((1.0 / fps) / sim.time_step))
    frame_count = round(duration_seconds * fps)

    frames = []
    for i in range(frame_count):
        # Render before stepping, so frame 0 is the resting pose: PID/motor
        # convergence is often faster than one frame interval, and stepping
        # first would skip straight past the visible motion.
        frame = _frame(sim, view_matrix, proj_matrix, width, height)
        frames.append(frame.convert("P", palette=Image.ADAPTIVE))
        if i < frame_count - 1:
            sim.step(steps_per_frame)

    frames[0].save(
        out_gif,
        save_all=True,
        append_images=frames[1:],
        duration=round(1000 / fps),
        loop=0,
        optimize=True,
    )
    print("saved", out_gif, f"({len(frames)} frames)")
