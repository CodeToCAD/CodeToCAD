from typing import TYPE_CHECKING
import weakref

if TYPE_CHECKING:
    from development.capabilities_json_to_python.capabilities_loader import (
        CapabilitiesLoader,
    )


class CapabilitiesImportsBuilder:
    """
    Holds references to CodeToCAD class names to help categorize imports by type for templating purposes.
    """

    def get_implementable_class_names(self, suffix: str = ""):
        return [
            class_name + suffix
            for class_name in list(self._codetocad_implementable_class_names)
        ]

    def get_interface_class_names(self, suffix: str = "Interface"):
        return [
            class_name + suffix
            for class_name in list(self._codetocad_interface_class_names)
        ]

    def __init__(
        self,
        capabilities_loader: "CapabilitiesLoader",
        exclude_class_names: list[str] | None = None,
    ) -> None:
        self.exclude_class_names = exclude_class_names or []
        self.capabilities_loader_ref = weakref.ref(capabilities_loader)

        self._codetocad_implementable_class_names = set()
        self._codetocad_interface_class_names = set()

    @property
    def loader_implementable_class_names(self):
        capabilities_loader = self.capabilities_loader_ref()

        if not capabilities_loader:
            raise RuntimeError("CapabilitiesLoader reference is null")

        return capabilities_loader.all_implementable_class_names

    @property
    def loader_interface_class_names(self):
        capabilities_loader = self.capabilities_loader_ref()

        if not capabilities_loader:
            raise RuntimeError("CapabilitiesLoader reference is null")

        return capabilities_loader.all_interface_only_class_names

    def _check_class_in_implementable_class_names(self, class_name: str):
        return class_name in self.loader_implementable_class_names

    def _check_class_in_interface_class_names(self, class_name: str):
        return class_name in self.loader_interface_class_names

    def add_class_name(self, class_name: str):
        if class_name in self.exclude_class_names:
            return

        if self._check_class_in_implementable_class_names(class_name):
            self._codetocad_implementable_class_names.add(class_name)
            return

        if self._check_class_in_interface_class_names(class_name):
            self._codetocad_interface_class_names.add(class_name)
            return

    def copy_from(self, other: "CapabilitiesImportsBuilder"):
        """
        In-place copies class names from another ImportsBuilder
        """
        self._codetocad_implementable_class_names = (
            self._codetocad_implementable_class_names.union(
                other._codetocad_implementable_class_names
            )
        )

        self._codetocad_interface_class_names = (
            self._codetocad_interface_class_names.union(
                other._codetocad_interface_class_names
            )
        )

        return self
