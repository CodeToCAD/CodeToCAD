"""
Capabilities.json is the core of CodeToCAD. This parser understands the ins-and-outs of the json file's structure and relationships.
"""

from dataclasses import dataclass, field, fields


from .capabilities_parameter_types import capabilities_type_to_python_type
from .capabilities_parameter_types_mock_values import (
    capabilities_type_to_python_mock_value,
)


@dataclass(frozen=True)
class CapabilitiesParameter:
    name: str
    information: str
    type: str
    default_value: str | None
    required: bool

    @property
    def type_parsed(self):
        if self.type == "any":
            return "Any"
        return capabilities_type_to_python_type(self.type)

    @property
    def type_mock_value(self):
        return capabilities_type_to_python_mock_value(self.type_parsed)

    @staticmethod
    def from_json(name: str, parameter_json: dict) -> "CapabilitiesParameter":
        return CapabilitiesParameter(
            name=name,
            information=parameter_json.get("information", ""),
            type=parameter_json["type"],
            default_value=parameter_json.get("default_value"),
            required=parameter_json.get("required", True),
        )


@dataclass(frozen=True)
class CapabilitiesMethod:
    name: str
    information: str
    action: str
    return_type: str | None
    is_static_method: bool
    parameters: list[CapabilitiesParameter] = field(default_factory=list)

    @property
    def parameters_names(self):
        return [parameter.name for parameter in self.parameters]

    @property
    def return_type_parsed(self):
        if self.return_type:
            return capabilities_type_to_python_type(self.return_type)

        if self.is_static_method:
            return None

        return "Self"

    @property
    def return_type_mock_value(self):
        if self.return_type:
            return capabilities_type_to_python_mock_value(self.return_type_parsed)

        if self.is_static_method:
            return None

        return "self"

    @staticmethod
    def from_json(name: str, method_json: dict) -> "CapabilitiesMethod":
        return CapabilitiesMethod(
            name=name,
            information=method_json.get("information", ""),
            action=method_json["action"],
            return_type=(
                method_json.get("return_type")
                if method_json["action"] != "get"
                else method_json["return_type"]
            ),
            is_static_method=method_json.get("is_static_method", False),
            parameters=[
                CapabilitiesParameter.from_json(parameter_name, parameter_json)
                for parameter_name, parameter_json in method_json.get(
                    "parameters", {}
                ).items()
            ],
        )


@dataclass(frozen=True)
class CapabilitiesClass:
    name: str
    information: str
    is_interface_only: bool
    constructor: CapabilitiesMethod | None
    extends: list[str] = field(default_factory=list)
    implements: list[str] = field(default_factory=list)

    methods: list[CapabilitiesMethod] = field(default_factory=list)

    @property
    def methods_names(self):
        return [method.name for method in self.methods]

    @property
    def static_methods(self):
        return [method for method in self.methods if method.is_static_method]

    def get_extends_class_names(self, suffix: str = "Interface"):
        return [class_name + suffix for class_name in self.extends]

    def get_implements_class_names(self, suffix: str = "Interface"):
        return [class_name + suffix for class_name in self.implements]

    @staticmethod
    def get_custom_keys_from_json(class_json: dict) -> list[str]:
        """
        In a json containing keys such as information, constructor, is_interface_only, etc.. there will be custom keys. We want to grab those.
        """

        field_names_to_ignore = [field.name for field in fields(CapabilitiesClass)]
        field_names_to_ignore.remove("methods")

        custom_keys = list(
            filter(lambda key: key not in field_names_to_ignore, class_json.keys())
        )

        return custom_keys

    @staticmethod
    def from_json(name: str, class_json: dict) -> "CapabilitiesClass":
        information = class_json.get("information", "")
        is_interface_only = class_json.get("is_interface_only", False)

        constructor = class_json.get("constructor")
        if constructor:
            constructor["action"] = "create"
            constructor = CapabilitiesMethod.from_json("constructor", constructor)

        extends = class_json.get("extends", [])
        if extends:
            extends = extends.split(",")

        implements = class_json.get("implements", [])
        if implements:
            implements = implements.split(",")

        methods = []

        for key in CapabilitiesClass.get_custom_keys_from_json(class_json):
            methods.append(CapabilitiesMethod.from_json(key, class_json[key]))

        return CapabilitiesClass(
            name=name,
            information=information,
            is_interface_only=is_interface_only,
            constructor=constructor,
            extends=extends,
            implements=implements,
            methods=methods,
        )
