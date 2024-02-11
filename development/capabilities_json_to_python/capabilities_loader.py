from copy import deepcopy
from development.capabilities_json_to_python.capabilities_imports_builder import (
    CapabilitiesImportsBuilder,
)
from development.capabilities_json_to_python.capabilities_parser import (
    CapabilitiesClass,
)
from development.capabilities_json_to_python.template_utils import get_capabilities


class CapabilitiesLoader:
    """
    Loads capabilities.json and parses it into useable metadata.

    Note: Before reading this code, please review the json schema/structure of capabilities.json first.
    """

    capabilities: dict[str, CapabilitiesClass] = {}
    _all_implementable_class_names = []
    _all_interface_only_class_names = []

    def __init__(self, capabilities_json_path: str | None = None) -> None:
        capabilities_json = get_capabilities(capabilities_json_path)

        for class_name, class_json in capabilities_json.items():
            self.capabilities[class_name] = CapabilitiesClass.from_json(
                class_name, class_json
            )

            # cache interface-only class names for better performance:
            if self.capabilities[class_name].is_interface_only:
                self._all_interface_only_class_names.append(class_name)
            else:
                self._all_implementable_class_names.append(class_name)

    def append_interface_suffix_if_interface_only_class(
        self, class_name, surround_in_quotes: bool = True, union_none_type: bool = False
    ):
        """
        This fills a templating need, and could likely be moved out of CapabiliesLoader.
        Adds Interface as a suffix to a class_name, and has options to add | None and surround the resulting type in quotes.
        """
        output_name = class_name
        if class_name in self._all_interface_only_class_names:
            output_name += "Interface"

        if union_none_type:
            output_name += "| None"

        return output_name if not surround_in_quotes else f'"{output_name}"'

    @property
    def all_implementable_class_names(self):
        return deepcopy(self._all_implementable_class_names)

    @property
    def all_interface_only_class_names(self):
        return deepcopy(self._all_interface_only_class_names)

    @property
    def all_class_names(self):
        return self.all_implementable_class_names + self.all_interface_only_class_names

    def generate_imports(self, class_name: str, exclude_class_names: list[str] | None):
        """
        Recursively grab CodeToCAD class names from parameters and returnType fields.

        TODO: memoization to save some cpu cycles
        """
        imports_builder = CapabilitiesImportsBuilder(
            capabilities_loader=self, exclude_class_names=exclude_class_names
        )

        capabilities_class = self.capabilities[class_name]

        methods = deepcopy(capabilities_class.methods)
        if capabilities_class.constructor:
            methods.append(capabilities_class.constructor)

        for method in methods:
            return_type = method.return_type

            if return_type:
                imports_builder.add_class_name(return_type)

            for parameter in method.parameters:
                imports_builder.add_class_name(parameter.type)

        for implemented_class in capabilities_class.implements:
            # Recursively build imports from implemented classes.
            imports_builder.copy_from(
                self.generate_imports(implemented_class, exclude_class_names)
            )

        return imports_builder
