from dataclasses import dataclass


@dataclass
class NativeObject:
    """A native object is a reference to an object in the CAD software."""

    native_ref: object | None = None
    native_parent_ref: object | None = None
    description: str | None = None
