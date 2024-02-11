from dataclasses import dataclass, field, fields


@dataclass
class CapabilitiesParameter:
    name: str
    information: str
    type: str
    default_value: str | None
    required: bool

    @staticmethod
    def from_json(name: str, parameter_json: dict) -> "CapabilitiesParameter":
        return CapabilitiesParameter(
            name=name,
            information=parameter_json.get("information", ""),
            type=parameter_json["type"],
            default_value=parameter_json.get("default_value"),
            required=parameter_json.get("required", True),
        )


@dataclass
class CapabilitiesMethod:
    name: str
    information: str
    action: str
    return_type: str | None
    static_method: bool
    parameters: list[CapabilitiesParameter] = field(default_factory=list)

    @staticmethod
    def from_json(name: str, method_json: dict) -> "CapabilitiesMethod":
        return CapabilitiesMethod(
            name=name,
            information=method_json.get("information", ""),
            action=method_json["action"],
            return_type=method_json.get("return_type")
            if method_json["action"] != "get"
            else method_json["return_type"],
            static_method=method_json.get("is_static_method", False),
            parameters=[
                CapabilitiesParameter.from_json(parameter_name, parameter_json)
                for parameter_name, parameter_json in method_json.get(
                    "parameters", {}
                ).items()
            ],
        )


@dataclass
class CapabilitiesClass:
    name: str
    information: str
    is_interface_only: bool
    constructor: CapabilitiesMethod | None
    extends: list[str] = field(default_factory=list)
    implements: list[str] = field(default_factory=list)
    methods: list[CapabilitiesMethod] = field(default_factory=list)

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
