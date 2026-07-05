from pathlib import Path

import pytest

from codetocad.cli import InteractiveSession, init_project, main


def run_session(tmp_path: Path, inputs: list[str], name: str = "cup"):
    project_dir = init_project(name, parent_dir=tmp_path)
    feed = iter(inputs)
    output: list[str] = []
    session = InteractiveSession(
        project_dir,
        name,
        input_fn=lambda prompt="": next(feed),
        output_fn=lambda *args: output.append(" ".join(str(a) for a in args)),
    )
    session.run()
    return project_dir, output, session


def test_init_creates_project_file(tmp_path):
    project_dir = init_project("cup", parent_dir=tmp_path)
    assert (project_dir / "cup.py").exists()


def test_spec_flow_create_cylinder_and_shell(tmp_path):
    inputs = [
        "1",  # Part
        "1",  # Create a part
        "cup_cylinder",  # name
        "4",  # Cylinder
        "2cm, 5cm",  # radius, height
        "1",  # Part
        "5",  # Shell selected part
        "5mm",  # thickness
        "q",  # quit
    ]
    project_dir, output, session = run_session(tmp_path, inputs)
    part_file = (project_dir / "cup_cylinder.py").read_text()
    assert "codetocad.cylinder(radius='2cm', height='5cm')" in part_file
    assert "cup_cylinder.shell(thickness='5mm')" in part_file
    assert session.selected == "cup_cylinder"
    assert any("You've started the project cup!" in line for line in output)
    project_file = (project_dir / "cup.py").read_text()
    assert "from cup_cylinder import cup_cylinder" in project_file


def test_greyed_out_options_require_selection(tmp_path):
    inputs = [
        "1",  # Part
        "5",  # Shell (greyed out, nothing selected yet)
        "q",
    ]
    _, output, _ = run_session(tmp_path, inputs)
    assert any("Please select geometry first." in line for line in output)
    assert any("greyed out since no selected geometry" in line for line in output)


def test_export_writes_stl(tmp_path):
    inputs = [
        "1", "1", "box", "3", "1cm, 1cm, 1cm",  # create a cube part
        "4",  # Export selected geometry
        "",  # default file name
        "q",
    ]
    project_dir, _, _ = run_session(tmp_path, inputs)
    stl = project_dir / "box.stl"
    assert stl.exists()
    assert stl.read_text().startswith("solid")


def test_sketch_and_extrude_flow(tmp_path):
    inputs = [
        "2",  # Sketch
        "1",  # Create a sketch
        "profile",
        "2",  # Circle
        "2cm",
        "q",
    ]
    project_dir, _, session = run_session(tmp_path, inputs)
    part_file = (project_dir / "profile.py").read_text()
    assert "codetocad.circle(radius='2cm')" in part_file
    assert session.parts["profile"]["dim"] == "2d"


def test_boolean_between_parts(tmp_path):
    inputs = [
        "1", "1", "body", "3", "10cm, 10cm, 10cm",
        "1", "1", "cutter", "4", "2cm, 20cm",
        "3",  # Select geometry
        "1",  # body
        "1",  # Part
        "4",  # Boolean selected part
        "1",  # Subtract
        "1",  # cutter
        "q",
    ]
    project_dir, _, _ = run_session(tmp_path, inputs)
    body_file = (project_dir / "body.py").read_text()
    assert "from cutter import cutter" in body_file
    assert "body.subtract(codetocad.Location(), cutter, codetocad.Location())" in body_file


def test_main_usage_and_run(tmp_path, capsys):
    assert main([]) == 0
    assert "codetocad init" in capsys.readouterr().out

    script = tmp_path / "myscript.py"
    script.write_text("import codetocad\npart = codetocad.cube(1, 1, 1)\n")
    assert main([str(script)]) == 0

    with pytest.raises(SystemExit):
        main([str(tmp_path / "missing.py")])
