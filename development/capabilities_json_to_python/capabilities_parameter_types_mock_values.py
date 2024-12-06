"""
Example and mock values, hand-crafted for templating purposes.
"""


def capabilities_type_to_python_mock_value(type_name: str | None):
    if type_name is None:
        return None
    return capabilities_parameter_types_mock_values[type_name]


dummy_point = "Point.from_list_of_float_or_string([0,0,0])"
dummy_vertex = f"Vertex('a vertex', {dummy_point})"
dummy_edge = f"Edge(v1={dummy_vertex}, v2={dummy_vertex}, name='an edge')"
importable_codetocad = '__import__("codetocad").'
capabilities_parameter_types_mock_values = {
    "str": "'String'",
    "list": [],
    "dict": {},
    "object": "'instance'",
    "int": 0,
    "float": 0.0,
    "list[float]": "[0.0]",
    "bool": True,
    "str|float": 0.0,
    "int|float": 0,
    "Part": "Part('a part')",
    "str|Part": "Part('a part')",
    "Entity": f"{importable_codetocad}Part('an entity')",
    "str|Entity": f"{importable_codetocad}Part('an entity')",
    "Sketch": "Sketch('a sketch')",
    "str|Sketch": "Sketch('a sketch')",
    "list[Entity]": [f"{importable_codetocad}Part('an entity')"],
    "list[str|Entity]": [f"{importable_codetocad}Part('an entity')"],
    "Landmark": "Landmark('name', 'parent')",
    "str|Landmark": "Landmark('name', 'parent')",
    "list[str|Landmark]": ["Landmark('name', 'parent')"],
    "Material": "Material('mat')",
    "str|Material": "Material('mat')",
    "PresetMaterial": "PresetMaterial.red",
    "Axis": "Axis.x",
    "str|int|Axis": "'x'",
    "Dimension": "Dimension(0,'mm')",
    "str|float|Dimension": "Dimension(0,'mm')",
    "str|list[str]|list[float]|list[Dimension]|Dimensions": "Dimensions(Dimension(0,'mm'),Dimension(0,'mm'),Dimension(0,'mm'))",
    "Angle": "Angle(90)",
    "str|float|Angle": "Angle(90)",
    "list[Angle]": "[Angle(90)]",
    "Point": dummy_point,
    "list[Point]": [dummy_point],
    "str|list[str]|list[float]|list[Dimension]|Point": dummy_point,
    "list[str|list[str]|list[float]|list[Dimension]|Point]": [dummy_point],
    "str|list[str]|list[float]|list[Dimension]|Point|Vertex": dummy_point,
    "list[str|list[str]|list[float]|list[Dimension]|Point|Vertex]": [dummy_point],
    "str|list[str]|list[float]|list[Dimension]|Point|Vertex|Landmark|PresetLandmark": [
        dummy_point
    ],
    "str|LengthUnit": "'mm'",
    "PresetLandmark": "PresetLandmark.leftTop",
    "str|PresetLandmark": "PresetLandmark.leftTop",
    "Camera": "Camera('a camera')",
    "str|Camera": "Camera('a camera')",
    "str|Exportable": f"{importable_codetocad}Part('an exportable part')",
    "list[str|Exportable]": f"[{importable_codetocad}Part('an exportable part')]",
    "Exportable": f"{importable_codetocad}Part('an exportable part')",
    "list[Exportable]": f"[{importable_codetocad}Part('an exportable part')]",
    "Projectable": f"{importable_codetocad}Sketch('a projected sketch')",
    "BoundaryBox": "BoundaryBox(BoundaryAxis(0,0),BoundaryAxis(0,0),BoundaryAxis(0,0))",
    "Dimensions": "Dimensions.from_point(Point.from_list_of_float_or_string([0,0,0]))",
    "Vertex": dummy_vertex,
    "Edge": dummy_edge,
    "list[Edge]": f"[{dummy_edge}]",
    "Wire": f"Wire('a wire',[])",
    "list[Wire]": f"[Wire('a wire',[])]",
    "str|Wire": f"Wire('a wire',[])",
    "list[Vertex]": "[" + dummy_vertex + "]",
    "Animation": "Animation()",
    "Scene": "Scene()",
    "Booleanable": f"{importable_codetocad}Part('a booleanable part')",
    "str|Landmarkable": f"{importable_codetocad}Part('a landmarkable part')",
    "CurveTypes": "CurveTypes.NURBS",
    "PartOptions": "PartOptions()",
    "SketchOptions": "SketchOptions()",
    "Wire|Sketch": f"Wire('a wire',[])",
    "str|Wire|Sketch": f"Wire('a wire',[])",
}
