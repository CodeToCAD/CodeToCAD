def capabilities_type_to_python_mock_value(type_name: str | None):
    if type_name is None:
        return None
    return capabilities_parameter_types_mock_values[type_name]


dummy_point = "Point.from_list_of_float_or_string([0,0,0])"
dummy_vertex = "Vertex(" + dummy_point + ", 'a vertex')"
capabilities_parameter_types_mock_values = {
    "str": "'String'",
    "list": [],
    "dict": {},
    "object": "'instance'",
    "int": 0,
    "float": 0.0,
    "list[float]": "[0.0]",
    "bool": True,
    "FloatOrItsStringValue": 0.0,
    "IntOrFloat": 0,
    "Part": "Part('a part')",
    "PartOrItsName": "Part('a part')",
    "Entity": "Part('an entity')",
    "EntityOrItsName": "Part('an entity')",
    "Sketch": "Sketch('a sketch')",
    "SketchOrItsName": "Sketch('a sketch')",
    "list[EntityOrItsName]": ["Part('an entity')"],
    "Landmark": "Landmark('name', 'parent')",
    "LandmarkOrItsName": "Landmark('name', 'parent')",
    "list[LandmarkOrItsName]": ["Landmark('name', 'parent')"],
    "Material": "Material('mat')",
    "MaterialOrItsName": "Material('mat')",
    "PresetMaterial": "PresetMaterial.red",
    "Axis": "Axis.x",
    "AxisOrItsIndexOrItsName": "x",
    "Dimension": "Dimension(0,'mm')",
    "DimensionOrItsFloatOrStringValue": "Dimension(0,'mm')",
    "DimensionsOrItsListOfFloatOrString": "Dimensions(Dimension(0,'mm'),Dimension(0,'mm'),Dimension(0,'mm'))",
    "Angle": "Angle('90')",
    "AngleOrItsFloatOrStringValue": "Angle('90')",
    "list[Angle]": "[Angle('90')]",
    "Point": dummy_point,
    "PointOrListOfFloatOrItsStringValue": dummy_point,
    "list[PointOrListOfFloatOrItsStringValue]": [dummy_point],
    "PointOrListOfFloatOrItsStringValueOrVertex": dummy_point,
    "list[PointOrListOfFloatOrItsStringValueOrVertex]": [dummy_point],
    "LengthUnitOrItsName": "mm",
    "PresetLandmark": "PresetLandmark.topLeft",
    "PresetLandmarkOrItsName": "PresetLandmark.topLeft",
    "Camera": "Camera()",
    "CameraOrItsName": "Camera()",
    "ExportableOrItsName": "Part('an exportable part')",
    "list[ExportableOrItsName]": "[Part('an exportable part')]",
    "Exportable": "Part('an exportable part')",
    "Projectable": "Sketch('a projected sketch')",
    "BoundaryBox": "BoundaryBox(BoundaryAxis(0,0),BoundaryAxis(0,0),BoundaryAxis(0,0))",
    "Dimensions": "Dimensions.from_point(Point.from_list_of_float_or_string([0,0,0]))",
    "Vertex": dummy_vertex,
    "Edge": "Edge(v1=" + dummy_vertex + ", v2=" + dummy_vertex + ", name='an edge')",
    "list[Edge]": "["
    + "Edge(v1="
    + dummy_vertex
    + ", v2="
    + dummy_vertex
    + ", name='an edge')"
    + "]",
    "Wire": "Wire([], 'a wire')",
    "list[Vertex]": "[" + dummy_vertex + "]",
    "Animation": "Animation()",
    "Scene": "Scene()",
    "BooleanableOrItsName": "Part('a booleanable part')",
    "LandmarkableOrItsName": "Part('a landmarkable part')",
    "CurveTypes": "CurveTypes.NURBS",
}
