# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from codetocad.interfaces import SubdividableInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


class Subdividable(SubdividableInterface):
    def remesh(self, strategy: str, amount: float):
        return self

    def subdivide(self, amount: float):
        return self

    def decimate(self, amount: float):
        return self
