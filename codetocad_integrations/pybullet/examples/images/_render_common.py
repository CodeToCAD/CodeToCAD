"""Shared headless screenshot helper for the PyBullet example renders."""
import numpy as np
import pybullet as p
import pybullet_data
from PIL import Image


def capture(sim, out_png, eye, target, fov=48, width=1000, height=850):
    """Add a ground plane and save a DIRECT-mode render of ``sim`` to
    ``out_png``, looking from ``eye`` towards ``target``."""
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.loadURDF("plane.urdf", physicsClientId=sim.client)

    view_matrix = p.computeViewMatrix(
        cameraEyePosition=eye,
        cameraTargetPosition=target,
        cameraUpVector=[0, 0, 1],
        physicsClientId=sim.client,
    )
    proj_matrix = p.computeProjectionMatrixFOV(
        fov=fov, aspect=width / height, nearVal=0.01, farVal=5.0
    )
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
    Image.fromarray(rgba[:, :, :3], "RGB").save(out_png)
    print("saved", out_png)
