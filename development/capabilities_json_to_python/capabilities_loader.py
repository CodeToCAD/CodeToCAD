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
    _all_implementable_class_names: list[str] = []
    _all_interface_only_class_names: list[str] = []

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

    def append_interface_suffix(
        self,
        class_name: str,
        surround_in_quotes: bool = True,
        union_none_type: bool = False,
    ):
        """
        This fills a templating need, and could likely be moved out of CapabiliesLoader.
        Adds Interface as a suffix to a class_name, and has options to add | None and surround the resulting type in quotes.
        """
        output_name = self.type_to_type_interface(class_name)
        # if class_name in self.all_class_names:
        #     output_name += "Interface"

        if union_none_type:
            output_name += "| None"

        return output_name if not surround_in_quotes else f'"{output_name}"'

    def type_to_type_interface(self, type: str):
        """
        For templating, turns any known CodeToCAD class names and appends Interface to them.
        e.g. list[str|Entity] -> list[str|EntityInterface]
        """
        if type.startswith("list"):
            return "list[" + self.type_to_type_interface(type[5:-1]) + "]"

        return "|".join(
            [
                (
                    (
                        type_pipe + "Interface"
                        if type_pipe in self.all_class_names
                        else type_pipe
                    )
                    if not type_pipe.startswith("list")
                    else self.type_to_type_interface(type_pipe)
                )
                for type_pipe in type.split("|")
            ]
        )

    def get_constructor_parameters_for_class(self, class_name: str):
        """
        Grabs the constructor parameters for the given class, and any class it extends.
        """

        classes = self.capabilities[class_name].extends + [class_name]

        parameters = []  # Order of params matters here

        # Parameters that don't have a default value
        # need to be placed first in the parameter list
        last_non_default_value_index = 0

        for some_class in classes:
            capabilities_class = self.capabilities[some_class]

            if capabilities_class.constructor:
                for parameter in capabilities_class.constructor.parameters:
                    if parameter in parameters:
                        continue

                    if parameter.default_value is None and parameter.required:
                        parameters.insert(last_non_default_value_index, parameter)
                        last_non_default_value_index += 1
                        continue

                    parameters.append(parameter)

        return parameters

    def get_implementable_method_names_for_class(self, class_name: str):
        """
        Grabs all the method names that should be generated for a class.
        """

        classes = self.capabilities[class_name].implements + [class_name]

        method_names = []  # needs to be ordered

        for some_class in classes:
            capabilities_class = self.capabilities[some_class]

            method_names += capabilities_class.methods_names

        return method_names

    @property
    def all_implementable_class_names(self) -> list[str]:
        return deepcopy(self._all_implementable_class_names)

    @property
    def all_interface_only_class_names(self) -> list[str]:
        return deepcopy(self._all_interface_only_class_names)

    @property
    def all_class_names(self):
        return self.all_implementable_class_names + self.all_interface_only_class_names

    def generate_imports(self, class_name: str, exclude_class_names: list[str] = []):
        """
        Recursively grab CodeToCAD class names from parameters and returnType fields.

        TODO: memoization to save some cpu cycles
        """

        capabilities_class = self.capabilities[class_name]

        exclude_class_names += capabilities_class.extends

        imports_builder = CapabilitiesImportsBuilder(
            capabilities_loader=self, exclude_class_names=exclude_class_names
        )

        # for capabilities_class_name in capabilities_class.get_extends_class_names(
        #     ""
        # ) + capabilities_class.get_implements_class_names(""):
        for capabilities_class_name in capabilities_class.get_implements_class_names(
            ""
        ):
            imports_builder.add_class_name(capabilities_class_name)

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
                self.generate_imports(
                    implemented_class, exclude_class_names + capabilities_class.extends
                )
            )

        return imports_builder
