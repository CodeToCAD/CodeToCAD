from dataclasses import dataclass
from codetocad.core.cad.native import NativeObject


@dataclass(kw_only=True)
class Sketch(NativeObject):
    """A vertex is a point in 3D space."""

    is_hidden: bool = False


def get_sketch(sketch_name: str) -> "Sketch":
    """Get a sketch by name."""
    raise NotImplementedError("Method not implemented.")
