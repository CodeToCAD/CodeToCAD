from codetocad.utilities import *
from codetocad.codetocad_types import *
from codetocad.interfaces import *

from importlib.util import find_spec

if find_spec("blender_provider"):
    # this will only be available when the Blender Addon is packaged:
    from providers.blender.blender_provider import *
elif find_spec("fusion360_provider"):
    # this will only be available when the Fusion360 Addon is packaged:
    from providers.fusion360.fusion360_provider import *
else:
    # When this python library is bundled, use the sample if non of the other known providers are available.
    print(
        "Warning: you are dry-running using the sample provider. All outputs are sample text explaining which methods will be executed. Please run this script in a supported software for a real output. See the README for more information."
    )
    from providers.sample import *
