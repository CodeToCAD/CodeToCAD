from importlib import reload
import sys
from pathlib import Path


def reload_codetocad_modules():
    print("Reloading CodeToCAD modules")
    import codetocad
    import fusion360_provider

    reload(codetocad)
    reload(fusion360_provider)


def add_codetocad_to_path():
    codetocad_path = Path(__file__).parent.parent.parent.parent

    core_path = codetocad_path / "codetocad"
    fusion360_path = codetocad_path / "providers/fusion360"
    fusion360_provider_path = codetocad_path / "providers/fusion360/fusion360_provider"

    if not fusion360_provider_path.exists():
        raise Exception(
            f"Could not find fusion360_provider files at {fusion360_provider_path}. codetocad_path: {codetocad_path}"
        )

    print("Adding {} to path".format(codetocad_path))

    sys.path.append(str(codetocad_path))

    print("Adding {} to path".format(core_path))

    sys.path.append(str(core_path))

    print("Adding {} to path".format(fusion360_path))

    sys.path.append(str(fusion360_path))

    print("Adding {} to path".format(fusion360_provider_path))

    sys.path.append(str(fusion360_provider_path))
