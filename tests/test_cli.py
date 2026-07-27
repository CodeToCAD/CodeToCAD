import importlib.util
import io
from pathlib import Path

import pytest

from codetocad.cli import STATE_FILE_NAME, InteractiveSession, init_project, main


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


def resume_session(project_dir: Path, inputs: list[str]):
    """A fresh session over an existing project folder, like codetocad load."""
    feed = iter(inputs)
    output: list[str] = []
    session = InteractiveSession(
        project_dir,
        project_dir.name,
        input_fn=lambda prompt="": next(feed),
        output_fn=lambda *args: output.append(" ".join(str(a) for a in args)),
    )
    session.restore()
    session.run()
    return output, session


def test_init_creates_project_file(tmp_path):
    project_dir = init_project("cup", parent_dir=tmp_path)
    assert (project_dir / "cup.py").exists()


def test_spec_flow_create_cylinder_and_shell(tmp_path):
    inputs = [
        "1",  # Part
        "1",  # Create a part
        "1",  # backend: no integration
        "cup_cylinder",  # name
        "4",  # Cylinder
        "2cm, 5cm",  # radius, height
        "1",  # Part
        "5",  # Shell selected part
        "5mm",  # thickness
        "",  # shell opening location (blank = fully closed)
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


def test_shell_with_opening_location(tmp_path):
    inputs = [
        "1",  # Part
        "1",  # Create a part
        "1",  # backend: no integration
        "cup_cylinder",  # name
        "4",  # Cylinder
        "2cm, 5cm",  # radius, height
        "1",  # Part
        "5",  # Shell selected part
        "5mm",  # thickness
        "0, 0, 2.5cm",  # opening location (top face)
        "q",  # quit
    ]
    project_dir, _, _ = run_session(tmp_path, inputs)
    part_file = (project_dir / "cup_cylinder.py").read_text()
    assert (
        "cup_cylinder.shell(thickness='5mm', start_at_location="
        "codetocad.Location(x='0', y='0', z='2.5cm'))"
    ) in part_file


def test_disabled_options_cannot_be_chosen(tmp_path):
    inputs = [
        "1",  # Part
        "5",  # Shell (disabled, nothing selected yet)
        "q",
    ]
    _, output, _ = run_session(tmp_path, inputs)
    assert any("That option is unavailable" in line for line in output)
    # The old literal "(greyed out ...)" suffix must not be printed.
    assert not any("greyed out" in line for line in output)


def test_export_writes_stl(tmp_path):
    inputs = [
        "1", "1", "1", "box", "3", "1cm, 1cm, 1cm",  # create a cube part
        "9",  # Export selected geometry
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
        "1",  # backend: no integration
        "profile",
        "2",  # Circle
        "2cm",
        "2",  # Sketch
        "2",  # Extrude selected sketch
        "1cm",  # height
        "",  # default part name
        "q",
    ]
    project_dir, _, session = run_session(tmp_path, inputs)
    part_file = (project_dir / "profile.py").read_text()
    assert "codetocad.circle(radius='2cm')" in part_file
    assert "profile_solid = profile.extrude('1cm')" in part_file
    assert session.parts["profile"]["kind"] == "sketch"
    assert session.parts["profile_solid"]["kind"] == "part"
    assert session.selected == "profile_solid"


def test_sketch_and_revolve_flow(tmp_path):
    inputs = [
        "2",  # Sketch
        "1",  # Create a sketch
        "1",  # backend: no integration
        "profile",
        "2",  # Circle
        "2cm",
        "2",  # Sketch
        "3",  # Revolve selected sketch
        "1",  # axis: Y
        "90",  # angle in degrees
        "",  # default part name
        "q",
    ]
    project_dir, _, session = run_session(tmp_path, inputs)
    part_file = (project_dir / "profile.py").read_text()
    # Angle is emitted as a numeric literal (degrees), not a string (radians).
    assert "profile_solid = profile.revolve(90.0, axis='y')" in part_file
    assert session.parts["profile_solid"]["kind"] == "part"
    assert session.selected == "profile_solid"


def test_boolean_between_parts(tmp_path):
    inputs = [
        "1", "1", "1", "body", "3", "10cm, 10cm, 10cm",
        "1", "1", "cutter", "4", "2cm, 20cm",
        "7",  # Select geometry
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


def test_material_and_hole(tmp_path):
    inputs = [
        "1", "1", "1", "plate", "3", "10cm, 10cm, 1cm",
        "1",  # Part
        "2",  # Set material
        "3",  # Custom
        "frame",  # material name
        "0.82",  # mass
        "0.15, 0.35, 0.75, 1.0",  # color
        "1",  # Part
        "6",  # Cut a hole
        "0, 0, 0",  # position
        "2mm",  # radius
        "1cm",  # depth
        "q",
    ]
    project_dir, _, _ = run_session(tmp_path, inputs)
    part_file = (project_dir / "plate.py").read_text()
    assert (
        "plate.set_material(codetocad.MaterialBase('frame', mass=0.82, "
        "color_rgba=codetocad.Vec4(0.15, 0.35, 0.75, 1.0)))"
    ) in part_file
    assert (
        "plate.hole(codetocad.Location(x='0', y='0', z='0'), "
        "radius_or_shape='2mm', amount='1cm')"
    ) in part_file


def test_revolute_joint_flow(tmp_path):
    inputs = [
        "1", "1", "1", "chassis", "4", "0.069, 0.14",
        "1", "1", "wheel", "4", "0.033, 0.027",
        "7", "1",  # select chassis
        "3",  # Assemble
        "2",  # Revolute
        "1",  # wheel
        "axle",  # joint name
        "0.03, 0.08, 0.033",  # position
        "-90",  # axis tilt: x_deg=-90 points the hinge along Y
        "q",
    ]
    project_dir, _, session = run_session(tmp_path, inputs)
    chassis_file = (project_dir / "chassis.py").read_text()
    assert "from wheel import wheel" in chassis_file
    assert (
        "axle = codetocad.Location.from_euler(x='0.03', y='0.08', z='0.033', "
        "x_deg=-90, name='axle')"
    ) in chassis_file
    assert "chassis.revolute(axle, wheel, axle)" in chassis_file
    assert session.joints["axle"] == {
        "parent": "chassis",
        "child": "wheel",
        "type": "revolute",
    }


def test_turtlebot_style_robot_flow(tmp_path):
    """Model a one-wheel diff-drive robot the way the turtlebot example is
    written by hand: part + motorized wheel, a named axle joint, an ESP32
    with pin bindings, an encoder, a MuJoCo simulation with the firmware
    emulated in-process, and a control web app."""
    inputs = [
        "1", "1", "1", "chassis", "4", "0.069, 0.14",
        "1", "1", "wheel", "4", "0.033, 0.027",
        "4", "2", "1", "",  # Electronics > motorize wheel > DC > default specs
        "7", "1",  # select chassis
        "3", "2", "1", "axle", "0.03, 0.08, 0.033", "-90",  # revolute joint
        "4", "1", "", "1",  # Electronics > add mcu (default name) > ESP32
        "4", "4", "", "", "1",  # add encoder (defaults), measuring axle
        "4", "5", "1", "",  # connect wheel to mcu, default pins
        "4", "5", "2", "",  # connect encoder to mcu, default pins
        "5", "1", "1", "", "n",  # Simulate > create > MuJoCo > mobile > no terrain
        "5", "2",  # emulate the microcontroller inside the simulation
        "5", "3",  # make the simulation runnable
        "6", "1", "",  # App > create web app (default title)
        "6", "2",  # motor slider (single app/motor picked automatically)
        "6", "4", "1", "1",  # gauge > encoder > count
        "6", "5",  # rpm plot
        "6", "7", "",  # make the app runnable, default port
        "q",
    ]
    project_dir, output, session = run_session(tmp_path, inputs, name="robot")

    wheel_file = (project_dir / "wheel.py").read_text()
    assert "class WheelDCMotor(type(wheel), codetocad.DCMotorMixin):" in wheel_file
    assert "no_load_speed_rpm = 57.0" in wheel_file
    assert "wheel.__class__ = WheelDCMotor" in wheel_file

    mcu_file = (project_dir / "mcu.py").read_text()
    assert "codetocad.Microcontroller('mcu', board=codetocad.MicrocontrollerBoard.ESP32)" in mcu_file
    assert "mcu.bind_actuator(wheel, name='wheel', pwm_pin=4, dir_pin=16)" in mcu_file
    assert "mcu.bind_sensor(encoder, name='encoder', a=34, b=35)" in mcu_file
    assert "from wheel import wheel" in mcu_file

    encoder_file = (project_dir / "encoder.py").read_text()
    assert "class EncoderEncoder(codetocad.EncoderMixin):" in encoder_file
    assert "counts_per_revolution = 4096" in encoder_file

    sim_file = (project_dir / "sim.py").read_text()
    assert "from codetocad_integrations.mujoco import simulate" in sim_file
    assert "from chassis import chassis" in sim_file
    assert "fixed_base=False" in sim_file
    assert "ground_plane=True" in sim_file
    assert "actuator_types={'axle': 'velocity'}" in sim_file
    assert "actuator_forcerange={'axle': 1.4}" in sim_file
    assert "emulator = codetocad.EmulatedMicrocontroller(mcu)" in sim_file
    assert "emulator.on_command('wheel', _motor_handler('axle', 57.0))" in sim_file
    assert "emulator.set_sensor('encoder', _encoder_reader('axle', 4096))" in sim_file
    assert "emulator.add_telemetry('pose', _read_pose, sample_rate_hz=10.0)" in sim_file
    assert "sim.launch_viewer(on_step=lambda: emulator.step(sim.data.time))" in sim_file

    app_file = (project_dir / "app.py").read_text()
    assert ".set_communication(emulator.communication)" in app_file
    assert "from sim import emulator" in app_file
    assert (
        "app.add_slider('wheel (rpm)', target=wheel, command='velocity_rpm', "
        "minimum=-57.0, maximum=57.0)"
    ) in app_file
    assert "app.add_gauge('encoder count', source=encoder, key='count', units='ticks')" in app_file
    assert "app.add_plot('encoder (rpm)', source=encoder, key='rpm')" in app_file
    assert "_physics_loop" in app_file
    assert "app.run(port=8080)" in app_file

    # The project file only imports/builds geometry, not devices.
    project_file = (project_dir / "robot.py").read_text()
    assert "from chassis import chassis" in project_file
    assert "mcu" not in project_file
    assert any("http://localhost:8080" in line for line in output)


def test_camera_flow(tmp_path):
    inputs = [
        "1", "1", "1", "cam", "3", "0.025, 0.025, 0.025",
        "4", "3", "",  # Electronics > make selected part a camera > defaults
        "q",
    ]
    project_dir, _, session = run_session(tmp_path, inputs)
    cam_file = (project_dir / "cam.py").read_text()
    assert "class CamCamera(type(cam), codetocad.CameraMixin):" in cam_file
    assert "resolution = (320, 240)" in cam_file
    assert session.parts["cam"]["camera"] == {"resolution": (320, 240)}


def test_pybullet_simulation_codegen(tmp_path):
    inputs = [
        "1", "1", "1", "base", "4", "5cm, 4cm",
        "5", "1",  # Simulate > create
        "2",  # PyBullet
        "n",  # fixed base
        "5", "3",  # make it runnable
        "q",
    ]
    project_dir, _, _ = run_session(tmp_path, inputs)
    sim_file = (project_dir / "sim.py").read_text()
    assert "from codetocad_integrations.pybullet import simulate" in sim_file
    assert "simulate(base, gui=__name__ == '__main__', fixed_base=True, ground_plane=False)" in sim_file
    assert "while sim.is_connected():" in sim_file


def test_load_restores_state_and_continues(tmp_path):
    inputs = ["1", "1", "1", "cup_cylinder", "4", "2cm, 5cm", "q"]
    project_dir, _, _ = run_session(tmp_path, inputs)
    assert (project_dir / STATE_FILE_NAME).exists()

    # A brand-new session over the same folder picks up where we left off.
    output, session = resume_session(project_dir, ["1", "5", "5mm", "", "q"])
    assert session.parts["cup_cylinder"]["kind"] == "part"
    assert session.selected == "cup_cylinder"
    assert any("You've loaded the project cup" in line for line in output)
    part_file = (project_dir / "cup_cylinder.py").read_text()
    assert "cup_cylinder.shell(thickness='5mm')" in part_file


def test_load_restores_robot_state_for_codegen(tmp_path):
    """Reloaded state must keep driving codegen: motor specs, joints and
    bindings from the first session shape the simulation created in the
    second one."""
    inputs = [
        "1", "1", "1", "chassis", "4", "0.069, 0.14",
        "1", "1", "wheel", "4", "0.033, 0.027",
        "4", "2", "1", "",  # motorize wheel
        "7", "1",  # select chassis
        "3", "2", "1", "axle", "0.03, 0.08, 0.033", "-90",  # revolute joint
        "4", "1", "", "1",  # add mcu
        "4", "5", "1", "",  # connect wheel
        "q",
    ]
    project_dir, _, first = run_session(tmp_path, inputs, name="robot")

    output, session = resume_session(
        project_dir,
        ["5", "1", "1", "", "n", "q"],  # create a MuJoCo sim of chassis
    )
    assert session.joints == first.joints
    assert session.selected == "chassis"
    assert session.parts["wheel"]["motor"]["no_load_rpm"] == 57.0
    assert session.parts["mcu"]["bindings"] == [
        {"var": "wheel", "name": "wheel", "kind": "motor"}
    ]
    sim_file = (project_dir / "sim.py").read_text()
    assert "actuator_types={'axle': 'velocity'}" in sim_file
    assert "actuator_forcerange={'axle': 1.4}" in sim_file


def test_scan_fallback_without_manifest(tmp_path):
    """Without a manifest (hand-assembled or pre-manifest project), load
    recovers the state by reading the generated files."""
    inputs = [
        "1", "1", "1", "chassis", "4", "0.069, 0.14",
        "1", "1", "wheel", "4", "0.033, 0.027",
        "4", "2", "1", "",
        "7", "1",
        "3", "2", "1", "axle", "0.03, 0.08, 0.033", "-90",
        "4", "1", "", "1",
        "4", "4", "", "", "1",  # encoder measuring axle
        "4", "5", "1", "",
        "4", "5", "2", "",
        "5", "1", "1", "", "n",
        "5", "2",  # emulate
        "6", "1", "",  # web app
        "q",
    ]
    project_dir, _, first = run_session(tmp_path, inputs, name="robot")
    (project_dir / STATE_FILE_NAME).unlink()

    session = InteractiveSession(
        project_dir, "robot", input_fn=lambda p="": "q", output_fn=lambda *a: None
    )
    assert session.restore()
    assert session.parts["chassis"]["kind"] == "part"
    assert session.parts["wheel"]["motor"]["no_load_rpm"] == 57.0
    assert session.joints["axle"] == {
        "parent": "chassis",
        "child": "wheel",
        "type": "revolute",
    }
    assert session.parts["mcu"]["kind"] == "mcu"
    assert session.parts["mcu"]["bindings"] == first.parts["mcu"]["bindings"]
    assert session.parts["encoder"]["cpr"] == 4096
    assert session.parts["encoder"]["joint"] == "axle"
    assert session.parts["sim"]["engine"] == "mujoco"
    assert session.parts["sim"]["root"] == "chassis"
    assert session.parts["sim"]["emulated"] is True
    assert session.parts["emulator"]["kind"] == "emulator"
    assert session.parts["app"]["kind"] == "app"
    assert session.selected == "wheel"  # the last geometry


def test_build123d_backend_codegen(tmp_path):
    inputs = [
        "1", "1",
        "2",  # backend: Build123D
        "body", "3", "6in, 0.5in, 2in",
        "1", "1", "bracket", "3", "2in, 10mm, 2in",  # backend already chosen
        "1", "4", "2", "1",  # Part > Boolean > Union > body
        "q",
    ]
    project_dir, _, session = run_session(tmp_path, inputs, name="shelf")
    assert session.backend == "build123d"
    body_file = (project_dir / "body.py").read_text()
    assert "from codetocad_integrations.build123d import adapt" in body_file
    assert "body = adapt(codetocad.cube(length='6in', width='0.5in', height='2in'))" in body_file
    bracket_file = (project_dir / "bracket.py").read_text()
    assert "bracket = adapt(codetocad.cube(" in bracket_file
    assert "bracket.union(" in bracket_file
    # The backend choice survives a reload.
    output, resumed = resume_session(project_dir, ["q"])
    assert resumed.backend == "build123d"


def test_backend_switch_retrofits_existing_files(tmp_path):
    inputs = [
        "1", "1", "1", "body", "3", "6in, 0.5in, 2in",  # no integration
        "1",  # Part
        "11",  # Set modeling backend
        "2",  # Build123D
        "y",  # rewrite existing files
        "q",
    ]
    project_dir, output, session = run_session(tmp_path, inputs)
    assert session.backend == "build123d"
    body_file = (project_dir / "body.py").read_text()
    assert "from codetocad_integrations.build123d import adapt" in body_file
    assert "body = adapt(codetocad.cube(length='6in', width='0.5in', height='2in'))" in body_file
    assert any("Rewrote body.py" in line for line in output)


def test_boolean_without_backend_warns_once(tmp_path):
    inputs = [
        "1", "1", "1", "body", "3", "10cm, 10cm, 10cm",
        "1", "1", "cutter", "4", "2cm, 20cm",
        "1", "4", "1", "1",  # Boolean > Subtract > body
        "q",
    ]
    _, output, _ = run_session(tmp_path, inputs)
    assert any("without a modeling backend" in line for line in output)


def test_preview_exports_meshes_for_viewer(tmp_path, monkeypatch):
    pytest.importorskip("open3d")
    from codetocad.cli import LivePreview

    launched = []
    monkeypatch.setattr(LivePreview, "_ensure_viewer", lambda self: launched.append(True))
    inputs = [
        "1", "1", "1", "box", "3", "1cm, 1cm, 1cm",
        "8",  # Preview
        "1",  # Open/refresh the preview window
        "q",
    ]
    _, output, session = run_session(tmp_path, inputs)
    directory = session.preview.directory
    assert (directory / "box.stl").exists()
    assert (directory / "version.txt").exists()
    assert (directory / "colors.json").exists()
    assert launched  # the viewer process would have been (re)started


def _offscreen_gl_available() -> bool:
    if importlib.util.find_spec("open3d") is None:
        return False
    import open3d as o3d

    try:
        vis = o3d.visualization.Visualizer()
        created = vis.create_window(width=1, height=1, visible=False)
        vis.destroy_window()
    except Exception:
        return False
    return bool(created)


@pytest.mark.skipif(
    not _offscreen_gl_available(),
    reason="offscreen OpenGL context unavailable (headless CI)",
)
def test_highlight_geometry_renders_png(tmp_path):
    destination = tmp_path / "face.png"
    inputs = [
        "1", "1", "1", "block", "3", "6cm, 4cm, 3cm",  # create a cube
        "1",  # Part
        "10",  # Highlight a face/edge/vertex
        "1",  # Face
        "TOP_CENTER",  # cube location
        str(destination),  # PNG path
        "q",
    ]
    _, output, _ = run_session(tmp_path, inputs)
    assert destination.exists()
    assert any("with the face highlighted" in line for line in output)


def test_backend_unavailable_falls_back_after_warning(tmp_path, monkeypatch):
    monkeypatch.setattr(
        InteractiveSession, "_backend_available", lambda self, backend: False
    )
    inputs = [
        "1", "1",
        "2",  # backend: Build123D (not installed)
        "n",  # do not use it anyway
        "box", "3", "1cm, 1cm, 1cm",
        "q",
    ]
    project_dir, output, session = run_session(tmp_path, inputs)
    assert session.backend == "none"
    assert any("build123d is not installed" in line for line in output)
    # Codegen fell back to plain codetocad, so the file still runs.
    assert "box = codetocad.cube(" in (project_dir / "box.py").read_text()


def test_export_failure_is_reported_honestly(tmp_path):
    project_dir, _, _ = run_session(
        tmp_path, ["1", "1", "1", "box", "3", "1cm, 1cm, 1cm", "q"]
    )
    # Simulate a broken environment: the part file no longer imports.
    box_file = project_dir / "box.py"
    box_file.write_text(
        "import module_that_does_not_exist\n" + box_file.read_text()
    )
    output, _ = resume_session(project_dir, ["9", "", "q"])
    assert not (project_dir / "box.stl").exists()
    assert any("could not execute box.py" in line for line in output)
    assert any("The export did not complete" in line for line in output)
    assert not any(line.startswith("Exported box") for line in output)


def test_load_with_relative_path_exports(tmp_path, monkeypatch):
    """codetocad load <relative/path>: file paths must survive the chdir
    into the project during execution (export/preview used to double the
    path and fail)."""
    project_dir, _, _ = run_session(
        tmp_path, ["1", "1", "1", "box", "3", "1cm, 1cm, 1cm", "q"]
    )
    monkeypatch.chdir(tmp_path)
    output, _ = resume_session(Path("cup"), ["9", "", "q"])
    assert (project_dir / "box.stl").exists()
    assert any(line.startswith("Exported box") for line in output)
    assert not any("could not execute" in line for line in output)


def test_main_load_command(tmp_path, monkeypatch):
    project_dir, _, _ = run_session(tmp_path, ["1", "1", "1", "box", "3", "1cm, 1cm, 1cm", "q"])
    monkeypatch.setattr("sys.stdin", io.StringIO("q\n"))
    assert main(["load", str(project_dir)]) == 0

    with pytest.raises(SystemExit):
        main(["load", str(tmp_path / "missing")])


def test_main_usage_and_run(tmp_path, capsys):
    assert main([]) == 0
    assert "codetocad init" in capsys.readouterr().out

    script = tmp_path / "myscript.py"
    script.write_text("import codetocad\npart = codetocad.cube(1, 1, 1)\n")
    assert main([str(script)]) == 0

    with pytest.raises(SystemExit):
        main([str(tmp_path / "missing.py")])


def test_bootstrap_project_builds_manifest_from_files(tmp_path):
    """A hand-assembled project (an entry point plus part files, no manifest)
    is traversed into an editable project with a .codetocad.json."""
    from codetocad.cli import bootstrap_project

    project_dir = tmp_path / "gadget"
    project_dir.mkdir()
    (project_dir / "gadget.py").write_text(
        '"""CodeToCAD project gadget."""\n'
        "from widget import widget\n\n"
        'if __name__ == "__main__":\n'
        "    for _part in [widget]:\n"
        "        _part.build()\n"
    )
    (project_dir / "widget.py").write_text(
        "import codetocad\n"
        "widget = codetocad.cube(length='1cm', width='1cm', height='1cm')\n"
        "widget.name = 'widget'\n"
    )
    assert not (project_dir / STATE_FILE_NAME).exists()

    returned_dir, name = bootstrap_project(project_dir / "gadget.py")
    assert returned_dir == project_dir.resolve()
    assert name == "gadget"

    import json

    data = json.loads((project_dir / STATE_FILE_NAME).read_text())
    assert data["project"] == "gadget"
    assert "widget" in data["parts"]
    assert data["parts"]["widget"]["kind"] == "part"

    # Idempotent: re-running keeps the recovered manifest.
    bootstrap_project(project_dir)
    data = json.loads((project_dir / STATE_FILE_NAME).read_text())
    assert "widget" in data["parts"]


def test_discovery_executes_entry_for_function_built_parts(tmp_path):
    """A hand-written project builds its parts inside build() and returns them
    (no top-level assignments to scan). bootstrap_project falls back to running
    the entry point and recovers the parts and joints from the live objects."""
    import json

    from codetocad.cli import bootstrap_project

    project_dir = tmp_path / "arm"
    project_dir.mkdir()
    (project_dir / "arm.py").write_text(
        "import codetocad\n"
        "from codetocad.location import Location\n"
        "\n"
        "def build():\n"
        "    base = codetocad.cube(length='2cm', width='2cm', height='1cm')\n"
        "    base.name = 'base'\n"
        "    link = codetocad.cube(length='1cm', width='1cm', height='3cm')\n"
        "    link.name = 'link'\n"
        "    base.revolute(Location.from_euler(name='elbow'), link, Location(),\n"
        "                  min_limits=0, max_limits=1)\n"
        "    return base, link\n"
        "\n"
        "if __name__ == '__main__':\n"
        "    raise SystemExit('the __main__ block must not run during discovery')\n"
    )
    bootstrap_project(project_dir / "arm.py")

    data = json.loads((project_dir / STATE_FILE_NAME).read_text())
    assert set(data["parts"]) == {"base", "link"}
    assert data["parts"]["base"]["kind"] == "part"
    assert data["parts"]["base"]["file"] == "arm.py"
    assert data["parts"]["base"]["source_name"] == "base"
    assert data["entry"] == "arm.py"
    assert data["joints"]["elbow"] == {
        "parent": "base",
        "child": "link",
        "type": "revolute",
    }


def test_discovered_project_rebuilds_live_parts_after_reload(tmp_path):
    """A reloaded execution-discovered project rebuilds its live 3D objects by
    re-running the entry point (they are not top-level part-file variables), so
    the preview has geometry to mesh."""
    project_dir = tmp_path / "arm"
    project_dir.mkdir()
    (project_dir / "arm.py").write_text(
        "import codetocad\n"
        "\n"
        "def build():\n"
        "    base = codetocad.cube(length='2cm', width='2cm', height='1cm')\n"
        "    base.name = 'base'\n"
        "    tip = codetocad.cube(length='1cm', width='1cm', height='3cm')\n"
        "    tip.name = 'tip'\n"
        "    return base, tip\n"
    )
    from codetocad.cli import bootstrap_project

    bootstrap_project(project_dir / "arm.py")

    # A fresh session, like `codetocad load` / the studio reopening the project.
    session = InteractiveSession(
        project_dir, "arm", input_fn=lambda p="": "q", output_fn=lambda *a: None
    )
    session.restore()
    assert session.entry is not None and session.entry.name == "arm.py"

    live = session._load_solid_parts()
    assert set(live) == {"base", "tip"}
    assert all(getattr(part, "name", None) for part in live.values())


def test_main_entry_point_without_manifest_inits_then_runs(tmp_path):
    """codetocad <entry.py> with no manifest sets the folder up as a project
    (writes .codetocad.json) and then runs the script."""
    project_dir = tmp_path / "gadget"
    project_dir.mkdir()
    (project_dir / "gadget.py").write_text(
        '"""CodeToCAD project gadget."""\nfrom widget import widget\n'
    )
    (project_dir / "widget.py").write_text(
        "import codetocad\nwidget = codetocad.cube(length='1cm', width='1cm', height='1cm')\n"
        "widget.name = 'widget'\n"
    )
    assert main([str(project_dir / "gadget.py")]) == 0
    assert (project_dir / STATE_FILE_NAME).exists()


def test_main_inits_when_entry_name_differs_from_folder(tmp_path):
    """The entry file need not match its folder name: pointing at
    medel_charger/charger_holder.py still initializes the project, naming it
    after the entry file (charger_holder)."""
    import json

    project_dir = tmp_path / "medel_charger"
    project_dir.mkdir()
    (project_dir / "charger_holder.py").write_text(
        "import codetocad\nfrom holder import holder\n"
    )
    (project_dir / "holder.py").write_text(
        "import codetocad\nholder = codetocad.cube(length='2cm', width='2cm', height='1cm')\n"
        "holder.name = 'holder'\n"
    )
    assert not (project_dir / STATE_FILE_NAME).exists()
    assert main([str(project_dir / "charger_holder.py")]) == 0

    data = json.loads((project_dir / STATE_FILE_NAME).read_text())
    assert data["project"] == "charger_holder"
    # The entry file is treated as the project file, not scanned as a part;
    # the sibling part is recovered.
    assert "holder" in data["parts"]
    assert "charger_holder" not in data["parts"]


def test_mujoco_script_reexecs_under_mjpython_on_macos(tmp_path, monkeypatch):
    """A script that opens the MuJoCo viewer is relaunched under mjpython on
    macOS (plain python cannot host the Cocoa main-thread viewer)."""
    import os

    from codetocad.cli import _reexec_under_mjpython_if_needed

    script = tmp_path / "robot_sim.py"
    script.write_text("import codetocad\nsim.launch_viewer()\n")
    fake_mjpython = tmp_path / "mjpython"
    fake_mjpython.write_text("#!/bin/sh\n")

    monkeypatch.setattr("sys.platform", "darwin")
    monkeypatch.delenv("MJPYTHON_BIN", raising=False)
    monkeypatch.delenv("CODETOCAD_MJPYTHON", raising=False)
    monkeypatch.setattr("codetocad.cli._find_mjpython", lambda: fake_mjpython)

    execs: list[tuple] = []

    def fake_execve(program, argv, env):
        execs.append((program, argv, env))

    monkeypatch.setattr(os, "execve", fake_execve)
    _reexec_under_mjpython_if_needed(script)

    assert len(execs) == 1
    program, argv, env = execs[0]
    assert program == str(fake_mjpython)
    assert argv == [str(fake_mjpython), str(script)]
    assert env["CODETOCAD_MJPYTHON"] == "1"


def test_mjpython_reexec_skipped_when_not_needed(tmp_path, monkeypatch):
    """Off macOS, when already under mjpython, or for a non-viewer script, the
    process is not re-exec'd."""
    import os

    from codetocad.cli import _reexec_under_mjpython_if_needed

    execs: list = []
    monkeypatch.setattr(os, "execve", lambda *a: execs.append(a))
    monkeypatch.setattr("codetocad.cli._find_mjpython", lambda: tmp_path / "mjpython")

    viewer = tmp_path / "sim.py"
    viewer.write_text("sim.launch_viewer()\n")
    plain = tmp_path / "cube.py"
    plain.write_text("import codetocad\npart = codetocad.cube(1, 1, 1)\n")

    # Not macOS: never re-exec.
    monkeypatch.setattr("sys.platform", "linux")
    _reexec_under_mjpython_if_needed(viewer)
    assert not execs

    # macOS but no viewer marker: never re-exec.
    monkeypatch.setattr("sys.platform", "darwin")
    monkeypatch.delenv("MJPYTHON_BIN", raising=False)
    monkeypatch.delenv("CODETOCAD_MJPYTHON", raising=False)
    _reexec_under_mjpython_if_needed(plain)
    assert not execs

    # Already running under mjpython: never re-exec.
    monkeypatch.setenv("MJPYTHON_BIN", "/some/mjpython")
    _reexec_under_mjpython_if_needed(viewer)
    assert not execs


def test_run_subcommand_runs_without_bootstrap(tmp_path):
    """`codetocad run <script>` is a pure run: it does not write a manifest,
    unlike the bare `codetocad <script>` which initializes the project."""
    script = tmp_path / "notes.py"
    script.write_text("import codetocad\npart = codetocad.cube(1, 1, 1)\n")

    assert main(["run", str(script)]) == 0
    assert not (tmp_path / STATE_FILE_NAME).exists()

    # The bare form initializes the project (writes the manifest) then runs.
    assert main([str(script)]) == 0
    assert (tmp_path / STATE_FILE_NAME).exists()


def test_duplicate_part_flow(tmp_path):
    inputs = [
        "1", "1", "1", "wheel", "4", "2cm, 1cm",  # cylinder part
        "1",  # Part
        "7",  # Duplicate selected part
        "",  # default name (wheel_copy)
        "0, 0, 5cm",  # offset for the copy
        "q",
    ]
    project_dir, _, session = run_session(tmp_path, inputs)
    part_file = (project_dir / "wheel.py").read_text()
    assert "wheel_copy = wheel.duplicate(name='wheel_copy')" in part_file
    assert (
        "wheel_copy.transform(relative=codetocad.Location(x='0', y='0', z='5cm'))"
        in part_file
    )
    assert session.parts["wheel_copy"]["kind"] == "part"
    assert session.selected == "wheel_copy"
    # The duplicated var survives a reload even without the manifest.
    (project_dir / STATE_FILE_NAME).unlink()
    _, resumed = resume_session(project_dir, ["q"])
    assert resumed.parts["wheel_copy"]["kind"] == "part"


def test_pattern_part_flow(tmp_path):
    inputs = [
        "1", "1", "1", "post", "4", "1cm, 10cm",  # cylinder part
        "1", "8",  # Part > Pattern selected part
        "1",  # Linear
        "4",  # instances
        "5cm, 0, 0",  # offset
        "1", "8",  # Part > Pattern selected part
        "2",  # Circular
        "",  # instances (default 3)
        "",  # angle (default 120)
        "",  # axis (default z)
        "",  # center (default origin)
        "q",
    ]
    project_dir, _, _ = run_session(tmp_path, inputs)
    part_file = (project_dir / "post.py").read_text()
    assert (
        "post.linear_pattern(4, codetocad.Location(x='5cm', y='0', z='0'))"
        in part_file
    )
    assert "post.circular_pattern(3, 120, axis='z')" in part_file
    # The generated file runs with the recorded operations.
    import runpy

    namespace = runpy.run_path(str(project_dir / "post.py"))
    assert len(namespace["post"].operations) == 2


# A 1x1 pixel PNG for reference-image tests.
_PNG_1PX = bytes.fromhex(
    "89504e470d0a1a0a0000000d4948445200000001000000010806000000"
    "1f15c4890000000d49444154789c63f8cfc0f01f0005050202b9cdb1b2"
    "0000000049454e44ae426082"
)


def test_reference_image_flow_and_persistence(tmp_path):
    image = tmp_path / "blueprint.png"
    image.write_bytes(_PNG_1PX)
    inputs = [
        "8",  # Preview
        "3",  # Add a reference image
        str(image),
        "1",  # Front view (xz)
        "0.5",  # width in meters
        "",  # center (default origin)
        "q",
    ]
    project_dir, output, session = run_session(tmp_path, inputs)
    references = session.preview.references
    assert references == [
        {
            "path": str(image.resolve()),
            "plane": "xz",
            "width": 0.5,
            "center": [0.0, 0.0, 0.0],
        }
    ]
    assert any("Added the reference image" in line for line in output)
    # Persisted in the manifest and restored on load.
    _, resumed = resume_session(project_dir, ["q"])
    assert resumed.preview.references == references
    # A missing image file is dropped on restore instead of breaking the viewer.
    image.unlink()
    _, resumed = resume_session(project_dir, ["q"])
    assert resumed.preview.references == []


def test_reference_image_rejects_missing_file(tmp_path):
    inputs = [
        "8", "3", str(tmp_path / "nope.png"),
        "q",
    ]
    _, output, session = run_session(tmp_path, inputs)
    assert any("No such image" in line for line in output)
    assert session.preview.references == []


def test_preview_publishes_references_json(tmp_path, monkeypatch):
    pytest.importorskip("open3d")
    import json

    from codetocad.cli import LivePreview

    monkeypatch.setattr(LivePreview, "_ensure_viewer", lambda self: None)
    image = tmp_path / "sketch.png"
    image.write_bytes(_PNG_1PX)
    inputs = [
        "8", "3", str(image), "3", "", "",  # add a floor reference image
        "8", "1",  # Preview > Open/refresh (references only, no parts yet)
        "q",
    ]
    _, _, session = run_session(tmp_path, inputs)
    directory = session.preview.directory
    references = json.loads((directory / "references.json").read_text())
    assert references[0]["plane"] == "xy"
    assert (directory / "version.txt").exists()


def test_viewer_source_compiles():
    from codetocad.cli import _VIEWER_SOURCE

    compile(_VIEWER_SOURCE, "viewer", "exec")
    assert "create_coordinate_frame" in _VIEWER_SOURCE
    assert "references.json" in _VIEWER_SOURCE


def test_wrong_number_of_dimensions_asks_again(tmp_path):
    """A wrong number of parameters is reported and the question is asked
    again, instead of dropping back to the menu."""
    inputs = [
        "1", "1", "1", "box", "3",
        "1cm, 1cm",  # only two of the three dimensions
        "1cm, 1cm, 1cm",  # asked again, answered correctly
        "q",
    ]
    project_dir, output, _ = run_session(tmp_path, inputs)
    assert any(
        "Expected 3 comma-separated value(s), got 2." in line for line in output
    )
    assert "codetocad.cube(length='1cm', width='1cm', height='1cm')" in (
        project_dir / "box.py"
    ).read_text()


def test_unreadable_length_asks_again(tmp_path):
    inputs = [
        "1", "1", "1", "box", "3",
        "1cm, wide, 1cm",  # 'wide' is not a length
        "1cm, 2cm, 1cm",
        "q",
    ]
    project_dir, output, _ = run_session(tmp_path, inputs)
    assert any("'wide' is not a length" in line for line in output)
    assert "width='2cm'" in (project_dir / "box.py").read_text()


def test_invalid_number_asks_again(tmp_path):
    """_ask_numbers used to keep the default silently; it now asks again."""
    inputs = [
        "1", "1", "1", "wheel", "4", "3cm, 1cm",
        "4",  # Electronics
        "2",  # Make selected part a motor
        "1",  # DC motor
        "fast, 1.4, 11.1",  # 'fast' is not a number
        "57, 1.4, 11.1",
        "q",
    ]
    project_dir, output, _ = run_session(tmp_path, inputs)
    assert any("'fast' is not a number." in line for line in output)
    assert "no_load_speed_rpm = 57.0" in (project_dir / "wheel.py").read_text()


def test_invalid_axis_asks_again(tmp_path):
    inputs = [
        "1", "1", "1", "post", "4", "1cm, 10cm",
        "1", "8", "2",  # Part > Pattern > Circular
        "", "",  # instances, angle
        "w",  # not an axis
        "y",
        "",  # center
        "q",
    ]
    project_dir, output, _ = run_session(tmp_path, inputs)
    assert any("'w' is not one of x, y, z." in line for line in output)
    assert "axis='y'" in (project_dir / "post.py").read_text()


def test_back_leaves_a_rejected_prompt(tmp_path):
    """'b' escapes a question the user cannot answer, without writing code."""
    inputs = [
        "1", "1", "1", "box", "3",
        "nope",  # invalid dimensions
        "b",  # back out of the question
        "q",
    ]
    project_dir, output, session = run_session(tmp_path, inputs)
    assert any("Expected 3 comma-separated value(s), got 1." in line for line in output)
    assert not (project_dir / "box.py").exists()
    assert session.parts == {}


def test_main_init_reports_wrong_number_of_parameters(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(SystemExit):
        main(["init", "cup", "extra"])
    assert "Expected 1 argument, got 2" in capsys.readouterr().out


def test_main_unknown_command_shows_usage(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(SystemExit) as error:
        main(["frobnicate"])
    assert "No such script: frobnicate" in str(error.value)
    assert "codetocad init" in str(error.value)
