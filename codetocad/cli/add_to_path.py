def pip_install_codetocad():
    """Installs CodeToCAD as an editable package using pip in the python environment of the consuming application. WARNING: This affects the python environment of the consuming application. TODO: use Virtual Environments."""
    import sys
    import os
    import subprocess
    from pathlib import Path

    codetocad_path = Path(__file__).parent.parent.parent

    if not codetocad_path.exists():
        raise Exception(f"Could not find CodeToCAD files at {codetocad_path}.")

    python = os.path.abspath(sys.executable)

    subprocess.call([python, "-m", "pip", "install", "-e", str(codetocad_path)])


def add_codetocad_to_path():
    import sys
    from pathlib import Path

    codetocad_path = Path(__file__).parent.parent.parent

    if not codetocad_path.exists():
        raise Exception(f"Could not find CodeToCAD files at {codetocad_path}.")

    print(f"Adding {codetocad_path} to path")

    sys.path.append(str(codetocad_path))


def add_codetocad_to_path_as_string():
    from pathlib import Path

    return f"""
from pathlib import Path
import sys
import os
import subprocess
codetocad_path = Path("{Path(__file__).parent.parent.parent.absolute()}")

if not codetocad_path.exists():
    raise Exception(
        f"Could not find CodeToCAD files at {{codetocad_path}}."
    )

# print(f"Adding {{codetocad_path}} to path")

# sys.path.append(str(codetocad_path))

"""
