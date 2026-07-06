"""PyBullet integration: simulate CodeToCAD assemblies.

``simulate(part)`` walks the assembly constraints (fixed/revolute/prismatic)
recorded on a root Part3D, exports every part's mesh as STL, generates a
URDF and loads it into PyBullet. Model in Build123D or Blender and import
into simulation right away::

    from codetocad_integrations.build123d import make_cylinder
    from codetocad_integrations.pybullet import simulate

    base = make_cylinder("5cm", "4cm")
    arm = make_cylinder("2cm", "15cm", start_location=Location(z="12cm"))
    base.revolute(Location(z="4cm", name="shoulder"), arm, Location(z="4cm"))

    sim = simulate(base, gui=True)
    sim.set_joint_target("shoulder", 1.0)
    sim.run(2.0, realtime=True)
"""

from codetocad_integrations.pybullet.simulation import PyBulletSimulation, build_urdf, simulate

__all__ = ["simulate", "PyBulletSimulation", "build_urdf"]
