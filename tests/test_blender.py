import os
import shutil
import subprocess
from pathlib import Path

import pytest

BLENDER = os.environ.get("CODETOCAD_BLENDER") or shutil.which("blender")


@pytest.mark.skipif(BLENDER is None, reason="blender is not on the PATH")
def test_blender_smoke(tmp_path):
    from codetocad_integrations.blender import blender_command

    script = Path(__file__).parent / "blender_smoke_script.py"
    command, env = blender_command(script)
    result = subprocess.run(
        command,
        env=env,
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=600,
    )
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert "BLENDER_SMOKE_OK" in result.stdout
    assert (tmp_path / "smoke_cube.stl").exists()
    assert (tmp_path / "smoke_scene.blend").exists()


@pytest.mark.skipif(BLENDER is None, reason="blender is not on the PATH")
def test_blender_simulation(tmp_path):
    from codetocad_integrations.blender import blender_command

    script = Path(__file__).parent / "blender_sim_smoke_script.py"
    command, env = blender_command(script)
    result = subprocess.run(
        command,
        env=env,
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=600,
    )
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert "BLENDER_SIM_SMOKE_OK" in result.stdout


def test_stubs_outside_blender():
    from codetocad_integrations import blender

    if blender.INSIDE_BLENDER:
        pytest.skip("running inside Blender")
    # Importable and subclassable outside Blender...
    make_cube = blender.make_cube
    part3d = blender.Part3D

    class MyPart(part3d):
        pass

    # ...but using them requires bpy.
    with pytest.raises(RuntimeError, match="ensure_blender"):
        make_cube("1cm", "1cm", "1cm")
    with pytest.raises(RuntimeError, match="ensure_blender"):
        MyPart()
