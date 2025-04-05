"""
Type-mapping, hand-crafted for templating purposes.
"""


def capabilities_type_to_python_type(type_name: str):
    return capabilities_parameter_types.get(type_name, type_name)


capabilities_parameter_types = {
    "string": "str",
    "array": "list",
    "object": "dict",
    "any": "Any",
    "number": "int",
    "float": "float",
    "boolean": "bool",
    "string,float": "str|float",
    "int,float": "int|float",
    "string,Part": "str|Part",
    "string,Entity": "str|Entity",
    "string,Sketch": "str|Sketch",
    "string,Wire": "str|Wire",
    "list[Entity]": "list[Entity]",
    "list[string,Entity]": "list[str|Entity]",
    "string,Landmark": "str|Landmark",
    "list[string,Landmark]": "list[str|Landmark]",
    "string,Material": "str|Material",
    "string,int,Axis": "str|int|Axis",
    "string,float,Dimension": "str|float|Dimension",
    "string,list[string],list[float],list[Dimension],Dimensions": "str|list[str]|list[float]|list[Dimension]|Dimensions",
    "string,float,Angle": "str|float|Angle",
    "string,Entity": "str|Entity",
    "string,list[string],list[float],list[Dimension],Point": "str|list[str]|list[float]|list[Dimension]|Point",
    "list[string,list[string],list[float],list[Dimension],Point]": "list[str|list[str]|list[float]|list[Dimension]|Point]",
    "string,list[string],list[float],list[Dimension],Point,Vertex": "str|list[str]|list[float]|list[Dimension]|Point|Vertex",
    "string,list[string],list[float],list[Dimension],Point,Vertex,Landmark,PresetLandmark": "str|list[str]|list[float]|list[Dimension]|Point|Vertex|Landmark|PresetLandmark",
    "list[string,list[string],list[float],list[Dimension],Point,Vertex]": "list[str|list[str]|list[float]|list[Dimension]|Point|Vertex]",
    "string,LengthUnit": "str|LengthUnit",
    "string,PresetLandmark": "str|PresetLandmark",
    "Camera": "Camera",
    "string,Camera": "Camera",
    "Exportable": "Exportable",
    "list[Exportable]": "list[Exportable]",
    "list[string,Exportable]": "list[str|Exportable]",
    "Booleanable": "Booleanable",
    "string,Booleanable": "Booleanable",
    "string,Landmarkable": "str|Landmarkable",
    "Wire,Sketch": "Wire|Sketch",
    "string,Wire,Sketch": "str|Wire|Sketch",
}
