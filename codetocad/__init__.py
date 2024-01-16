from codetocad.utilities import *
from codetocad.codetocad_types import *
from codetocad.interfaces import *

from importlib.util import find_spec

if find_spec("blender_provider"):
    # this will only be available when the Blender Addon is packaged:
    from blender_provider import *
elif find_spec("fusion360_provider"):
    # this will only be available when the Fusion360 Addon is packaged:
    from fusion360_provider import *
else:
    # When this python library is bundled, use the providers_sample if the "providers" directory is not copied.
    print("Warning: CodeToCAD is using the providers_sample")
    from codetocad.providers_sample import *
