from codetocad import *

blue_material = Material("blue").set_color(0, 0.1, 1.0)
red_material = Material("red").set_color(1.0, 0.1, 0)

Part("fillet_all_edges").create_cube(1, 1, 1).fillet_all_edges("10cm").set_material(
    blue_material
)
Part("chamfer_all_edges").create_cube(1, 1, 1).translate_xyz(1.5, 0, 0).set_material(
    red_material
).chamfer_all_edges("10cm")

Part("fillet_all_edgesCylinder").create_cylinder(1 / 2, 2).translate_xyz(
    1.5 * 2, 0, 0
).fillet_all_edges("10cm").set_material(blue_material)
Part("chamfer_all_edgesCylinder").create_cylinder(1 / 2, 2).translate_xyz(
    1.5 * 3, 0, 0
).chamfer_all_edges("10cm").set_material(red_material)

fillet_two_edges = Part("filletTwoEdges").create_cube(1, 1, 1)
fillet_two_edges_edge1 = fillet_two_edges.create_landmark("edge1", max, 0, max)
fillet_two_edges_edge2 = fillet_two_edges.create_landmark("edge2", min, 0, min)
fillet_two_edges.fillet_edges(
    "10cm", [fillet_two_edges_edge1, fillet_two_edges_edge2]
).translate_xyz(0, 1.5, 0).set_material(blue_material)

chamfer_two_edges = Part("chamferTwoEdges").create_cube(1, 1, 1)
chamfer_two_edges_edge1 = chamfer_two_edges.create_landmark("edge1", max, 0, max)
chamfer_two_edges_edge2 = chamfer_two_edges.create_landmark("edge2", min, 0, min)
chamfer_two_edges.chamfer_edges(
    "10cm", [chamfer_two_edges_edge1, chamfer_two_edges_edge2]
).translate_xyz(1.5, 1.5, 0).set_material(red_material)

fillet_two_faces = Part("filletTwoFaces").create_cube(1, 1, 1)
fillet_two_faces_face1 = fillet_two_faces.create_landmark("face1", 0, 0, max)
fillet_two_faces_face2 = fillet_two_faces.create_landmark("face2", min, 0, 0)
fillet_two_faces.fillet_faces(
    "10cm", [fillet_two_faces_face1, fillet_two_faces_face2]
).translate_xyz(1.5 * 2, 1.5, 0).set_material(blue_material)

chamge_two_faces = Part("chamferTwoFaces").create_cube(1, 1, 1)
chamge_two_faces_face1 = chamge_two_faces.create_landmark("face1", 0, 0, max)
chamge_two_faces_face2 = chamge_two_faces.create_landmark("face2", min, 0, 0)
chamge_two_faces.chamfer_faces(
    "10cm", [chamge_two_faces_face1, chamge_two_faces_face2]
).translate_xyz(1.5 * 3, 1.5, 0).set_material(red_material)
