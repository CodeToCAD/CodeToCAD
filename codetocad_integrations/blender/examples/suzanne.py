"""A custom user part built with the bpy/bmesh API directly: Blender's
Suzanne monkey, smoothed with a CodeToCAD fillet (bevel) and exported to
glTF. CodeToCAD operations, queries and export work on top of any custom
build_native().

    codetocad suzanne.py
"""

from codetocad import Location
from codetocad_integrations.blender import Part3D, ensure_blender


class Suzanne(Part3D):
    def build_native(self):
        import bmesh
        import bpy

        bm = bmesh.new()
        bmesh.ops.create_monkey(bm)
        # Suzanne is ~2.7 units wide; scale her to ~15cm.
        for vertex in bm.verts:
            vertex.co *= 0.055
        mesh = bpy.data.meshes.new("suzanne")
        bm.to_mesh(mesh)
        bm.free()
        obj = bpy.data.objects.new("suzanne", mesh)
        bpy.context.collection.objects.link(obj)
        return obj


if __name__ == "__main__":
    ensure_blender()

    suzanne = Suzanne(name="suzanne")
    suzanne.fillet(amount="1mm")  # bevel every edge
    suzanne.transform(relative=Location(z="10cm").rotate(z_deg=30))

    suzanne.export("suzanne.glb")
    suzanne.export("suzanne.stl")
    bbox_min, bbox_max = suzanne.get_bounding_box()
    size = tuple(round((b - a) * 1000, 1) for a, b in zip(bbox_min.to_tuple(), bbox_max.to_tuple()))
    print(f"bounding box size: {size} mm")
