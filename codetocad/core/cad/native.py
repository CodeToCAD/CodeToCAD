from dataclasses import dataclass, field


@dataclass
class NativeObject:
    """A native object is a reference to an object in the CAD software.

    The native_refs dictionary stores multiple native object references by key.
    Common keys include:
    - "default": The primary native object reference
    - "face": The original face when an Edge represents a face boundary
    - "parent": A parent/containing native object reference

    Use get_native() and set_native() helper methods for convenient access.
    """

    native_refs: "dict[str, object | None]" = field(default_factory=dict)
    description: str | None = None

    def get_native(self, key: str = "default") -> object | None:
        """Retrieve a native object reference by key.

        Args:
            key: The key identifying the native object (default: "default")

        Returns:
            The native object reference, or None if not found
        """
        return self.native_refs.get(key)

    def set_native(self, obj: object, key: str = "default") -> None:
        """Set a native object reference with a key.

        Args:
            obj: The native object to store
            key: The key to store it under (default: "default")
        """
        self.native_refs[key] = obj
