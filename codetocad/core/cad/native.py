
from dataclasses import dataclass


@dataclass
class NativeObject:
    """A native object is a reference to an object in the CAD software."""
    native: object|None = None
    description: str|None = None