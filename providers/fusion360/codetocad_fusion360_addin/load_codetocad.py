from importlib import reload
import inspect
import sys
from pathlib import Path

from .lib import fusion360utils as futil


def register_fusion360_provider():
    from fusion360_provider.register import register

    register()


def reload_codetocad_modules():

    futil.log("Reloading CodeToCAD modules")
    import codetocad
    import fusion360_provider
    import fusion360_provider.fusion_actions

    all_providers_modules = inspect.getmembers(
        fusion360_provider.fusion_actions, predicate=inspect.ismodule
    )

    for module_name, module in all_providers_modules:
        reload(module)

    reload(fusion360_provider.fusion_actions)

    all_providers_modules = inspect.getmembers(
        fusion360_provider, predicate=inspect.ismodule
    )
    for module_name, module in all_providers_modules:
        reload(module)

    reload(fusion360_provider)

    all_providers_modules = inspect.getmembers(codetocad, predicate=inspect.ismodule)

    for module_name, module in all_providers_modules:
        reload(module)

    reload(codetocad)


def add_codetocad_to_path():
    codetocad_path = Path(__file__).parent.parent.parent.parent

    core_path = codetocad_path / "codetocad"
    fusion360_path = codetocad_path / "providers/fusion360"
    fusion360_provider_path = codetocad_path / "providers/fusion360/fusion360_provider"
    fusion360_provider_actions_path = (
        codetocad_path / "providers/fusion360/fusion360_provider/fusion_actions"
    )

    if not fusion360_provider_path.exists():
        raise Exception(
            f"Could not find fusion360_provider files at {fusion360_provider_path}. codetocad_path: {codetocad_path}"
        )

    futil.log("Adding {} to path".format(codetocad_path))

    sys.path.append(str(codetocad_path))

    futil.log("Adding {} to path".format(core_path))

    sys.path.append(str(core_path))

    futil.log("Adding {} to path".format(fusion360_path))

    sys.path.append(str(fusion360_path))

    futil.log("Adding {} to path".format(fusion360_provider_path))

    sys.path.append(str(fusion360_provider_path))

    futil.log("Adding {} to path".format(fusion360_provider_actions_path))

    sys.path.append(str(fusion360_provider_actions_path))
