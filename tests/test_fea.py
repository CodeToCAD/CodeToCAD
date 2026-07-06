import numpy as np
import pytest

from codetocad import FEA, Location, cube, steel_material, white_material


def test_fea_requires_elastic_material():
    part = cube(0.2, 0.02, 0.01)
    with pytest.raises(ValueError, match="youngs_modulus"):
        FEA(part, white_material())
    fea = FEA(part)  # defaults to steel
    assert fea.material.youngs_modulus == pytest.approx(210e9)


def test_fix_and_load_recorded_with_resolved_locations():
    part = cube(0.2, 0.02, 0.01)
    fea = FEA(part, steel_material())
    fea.fix(part.left_center)
    fea.add_force(part.right_center, force=(0, 0, -100))
    assert fea.fixed_supports[0].location.to_tuple() == pytest.approx((-0.1, 0, 0))
    assert fea.loads[0].force == (0, 0, -100)


def test_node_selection_plane_vs_sphere():
    part = cube(0.2, 0.02, 0.01)
    fea = FEA(part, steel_material())
    coords = np.array(
        [(-0.1, 0, 0), (-0.1, 0.01, 0.005), (0, 0, 0), (0.1, 0, 0)]
    )
    # left_center lies on the bbox x-min plane: selects the whole face.
    face = fea.select_node_indices(coords, part.left_center, tolerance=1e-4)
    assert list(face) == [0, 1]
    # An interior point selects only nearby nodes.
    near = fea.select_node_indices(coords, Location(0, 0, 0), tolerance=1e-3)
    assert list(near) == [2]


def test_base_solve_not_implemented():
    fea = FEA(cube(1, 1, 1), steel_material())
    with pytest.raises(NotImplementedError):
        fea.solve()


# -- end-to-end with CalculiX (skipped when pygccx/ccx are unavailable) --

pygccx = pytest.importorskip("pygccx")


def _ccx_available():
    try:
        from codetocad_integrations.calculix import find_ccx

        find_ccx()
        return True
    except FileNotFoundError:
        return False


@pytest.mark.skipif(not _ccx_available(), reason="ccx solver not installed")
def test_cantilever_beam_matches_analytic(tmp_path):
    build123d = pytest.importorskip("build123d")  # noqa: F841
    from codetocad_integrations.build123d import make_cube
    from codetocad_integrations.calculix import analyze

    length, width, height = 0.2, 0.02, 0.01
    force = 100.0
    beam = make_cube(length, width, height)
    beam.name = "beam"
    beam.set_material(steel_material())

    fea = analyze(beam, output_dir=tmp_path)
    fea.fix(beam.left_center)
    fea.add_force(beam.right_center, force=(0, 0, -force))
    results = fea.solve()

    E = steel_material().youngs_modulus
    inertia = width * height**3 / 12
    analytic_tip = force * length**3 / (3 * E * inertia)
    analytic_stress = force * length * (height / 2) / inertia

    assert results.max_displacement == pytest.approx(analytic_tip, rel=0.10)
    assert results.max_von_mises == pytest.approx(analytic_stress, rel=0.25)
    # Displacement grows from the clamped face to the tip.
    x = results.nodes[:, 0]
    tip_disp = results.displacement_magnitudes[x > x.max() - 1e-6].mean()
    root_disp = results.displacement_magnitudes[x < x.min() + 1e-6].max()
    assert root_disp < 1e-9
    assert tip_disp == pytest.approx(results.max_displacement, rel=0.05)

    image = tmp_path / "beam.png"
    results.visualize(str(image))
    assert image.exists() and image.stat().st_size > 10_000
