"""CalculiX (pygccx) integration: FEA of CodeToCAD parts.

``analyze(part)`` exports the part's geometry, meshes it with gmsh
(second-order tetrahedra), applies fixtures and loads described with
CodeToCAD Locations, solves a static analysis with CalculiX and returns
``FEAResults`` with displacement and von Mises stress fields::

    from codetocad import steel_material
    from codetocad_integrations.build123d import make_cube
    from codetocad_integrations.calculix import analyze

    beam = make_cube("200mm", "20mm", "10mm")
    beam.set_material(steel_material())

    fea = analyze(beam)
    fea.fix(beam.left_center)
    fea.add_force(beam.right_center, force=(0, 0, -100))
    results = fea.solve()
    results.visualize("beam_fea.png")

The CalculiX solver (``ccx``) must be installed: set ``CODETOCAD_CCX`` to
its path, have it on the PATH, or install it to ``~/.codetocad/ccx`` (e.g.
``micromamba create -p ~/.codetocad/ccx -c conda-forge calculix``).
"""

from codetocad_integrations.calculix.fea import CalculixFEA, analyze, find_ccx

__all__ = ["analyze", "CalculixFEA", "find_ccx"]
