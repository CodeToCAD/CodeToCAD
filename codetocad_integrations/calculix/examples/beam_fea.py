"""FEA of a cantilever beam modeled with Build123D and solved with CalculiX.

A 200 x 20 x 10 mm steel beam is clamped at its left face and loaded with
100 N downward at its free end, then compared against the Euler-Bernoulli
analytic solution and rendered to beam_fea.png / beam_deflection.png.

Requires the calculix extra (pygccx) and the ccx solver (see the
integration README). Run:  python beam_fea.py
"""

from codetocad import steel_material
from codetocad_integrations.build123d import make_cube
from codetocad_integrations.calculix import analyze

LENGTH, WIDTH, HEIGHT = 0.2, 0.02, 0.01  # meters
FORCE = 100.0  # newtons, downward at the free end


def main() -> None:
    beam = make_cube(LENGTH, WIDTH, HEIGHT)
    beam.name = "beam"
    beam.set_material(steel_material())

    fea = analyze(beam, output_dir="beam_fea_output")
    fea.fix(beam.left_center)  # clamp the whole left face
    fea.add_force(beam.right_center, force=(0, 0, -FORCE))
    results = fea.solve()

    # Euler-Bernoulli cantilever: tip deflection F L^3 / 3 E I and root
    # bending stress M c / I.
    E = steel_material().youngs_modulus
    I = WIDTH * HEIGHT**3 / 12
    analytic_tip = FORCE * LENGTH**3 / (3 * E * I)
    analytic_stress = FORCE * LENGTH * (HEIGHT / 2) / I

    print(
        f"tip deflection: {results.max_displacement * 1000:.4f} mm "
        f"(analytic {analytic_tip * 1000:.4f} mm)"
    )
    print(
        f"max von Mises:  {results.max_von_mises / 1e6:.1f} MPa "
        f"(analytic root bending {analytic_stress / 1e6:.1f} MPa)"
    )

    results.visualize("beam_fea.png", field_name="von_mises")
    results.visualize("beam_deflection.png", field_name="displacement")
    print("wrote beam_fea.png and beam_deflection.png")


if __name__ == "__main__":
    main()
