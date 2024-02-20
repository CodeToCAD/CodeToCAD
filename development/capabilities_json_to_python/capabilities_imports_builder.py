from functools import cache
import re
from typing import TYPE_CHECKING
import weakref

from development.capabilities_to_snake_case import to_snake_case

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

    def get_interface_class_names(self, suffix: str = ""):
        return [
            class_name + suffix
            for class_name in list(self._codetocad_interface_class_names)
        ]

    @staticmethod
    def format_import_statement(class_name: str, parent_path: str):
        """
        Given a class_name, e.g. PartInterface and a parent_path, e.g. codetocad.interfaces
        returns "from codetocad.interfaces.part_interface import PartInterface
        """
        snake_class_name = to_snake_case(class_name)
        return f"from {parent_path}{snake_class_name} import {class_name}"

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
    def loader_implementable_class_names(self) -> list[str]:
        capabilities_loader = self.capabilities_loader_ref()

        if not capabilities_loader:
            raise RuntimeError("CapabilitiesLoader reference is null")

        return capabilities_loader.all_implementable_class_names

    @property
    def loader_interface_class_names(self) -> list[str]:
        capabilities_loader = self.capabilities_loader_ref()

        if not capabilities_loader:
            raise RuntimeError("CapabilitiesLoader reference is null")

        return capabilities_loader.all_interface_only_class_names

    def _check_class_in_list(
        self, class_name: str, list_of_names: list[str]
    ) -> str | None:
        """
        Check if class_name is in a list of other names.
        If class_name contains non-letter characters, such as , or [] - then the comparison logic is complex, so we'll loop through the known names and check if the known name is in the class_name instead.
        The latter check may yield false positives if the known name is a substring of the class_name, e.g. known name: Part, class_name: Particle -> would yield a false positive.
        """
        if re.match("^[A-Za-z]+$", class_name):
            if class_name in list_of_names:
                return class_name
            else:
                return None

        for capabilities_class in list_of_names:
            if capabilities_class in class_name:
                return capabilities_class
        return None

    @cache
    def _check_class_in_implementable_class_names(self, class_name: str) -> str | None:
        return self._check_class_in_list(
            class_name, self.loader_implementable_class_names
        )

    @cache
    def _check_class_in_interface_class_names(self, class_name: str) -> str | None:
        return self._check_class_in_list(class_name, self.loader_interface_class_names)

    def add_class_name(self, class_name: str):
        """
        The checks are using a forloop because sometimes class_name is a composite, like list[Part] or str,Part.
        """
        for capabilities_class in self.exclude_class_names:
            if class_name in capabilities_class:
                return

        capabilities_class = self._check_class_in_implementable_class_names(class_name)
        if capabilities_class and capabilities_class not in self.exclude_class_names:
            self._codetocad_implementable_class_names.add(capabilities_class)
            return

        capabilities_class = self._check_class_in_interface_class_names(class_name)
        if capabilities_class and capabilities_class not in self.exclude_class_names:
            self._codetocad_interface_class_names.add(capabilities_class)
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
