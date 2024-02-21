import bpy

from providers.blender.blender_provider.blender_actions.objects import get_object


def get_material(
    material_name: str,
) -> bpy.types.Material:
    blenderMaterial = bpy.data.materials.get(material_name)

    assert blenderMaterial is not None, f"Material {material_name} does not exist."

    return blenderMaterial


def get_materials(obj_name: str) -> list[bpy.types.Material]:
    obj = bpy.data.objects[obj_name]
    return [material_slot.material for material_slot in obj.material_slots]


def create_material(
    new_material_name: str,
):
    material = bpy.data.materials.get(new_material_name)

    assert material is None, f"Material with name {material} already exists."

    material = bpy.data.materials.new(name=new_material_name)

    return material


def set_material_color(material_name: str, r_value, g_value, b_value, a_value=1.0):
    if isinstance(r_value, int):
        r_value /= 255.0

    if isinstance(g_value, int):
        g_value /= 255.0

    if isinstance(b_value, int):
        b_value /= 255.0

    if isinstance(a_value, int):
        a_value /= 255.0

    material = get_material(material_name)

    material.diffuse_color = (r_value, g_value, b_value, a_value)

    return material


def set_material_metallicness(material_name: str, value: float):
    material = get_material(material_name)
    material.metallic = value


def set_material_roughness(material_name: str, value: float):
    material = get_material(material_name)
    material.roughness = value


def set_material_specularness(material_name: str, value: float):
    material = get_material(material_name)
    material.specular_intensity = value


def set_material_to_object(material_name: str, object_name: str, is_union=False):
    material = get_material(material_name)

    object = get_object(object_name)

    mesh: bpy.types.Mesh = object.data

    objectMaterial = mesh.materials

    if is_union or len(objectMaterial) == 0:
        objectMaterial.append(material)
    else:
        objectMaterial[0] = material

    return material


# def getTexture(textureName):
# 	blenderTexture = bpy.data.textures.get(textureName)

# 	assert \
# 		blenderTexture is not None, \
# 			f"Texture {textureName} does not exist."

# 	return blenderTexture


# def createImageTexture(textureName, image_file_path, repeatMode:blender_definitions.RepeatMode):
#   image = bpy.data.images.load(image_file_path)
#   blenderTexture = bpy.data.textures.new(name=textureName, type="IMAGE")
#   blenderTexture.image = image
#   blenderTexture.extension = repeatMode.getBlenderName

# ref https://blender.stackexchange.com/questions/118646/add-a-texture-to-an-object-using-python-and-blender-2-8/129014#129014


def add_texture_to_material(
    material_name: str,
    image_file_path: str,
):
    material = get_material(material_name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes["Principled BSDF"]
    texImage: bpy.types.ShaderNodeTexImage = material.node_tree.nodes.new(
        "ShaderNodeTexImage"
    )
    image = bpy.data.images.load(image_file_path)
    texImage.image = image
    material.node_tree.links.new(bsdf.inputs["Base Color"], texImage.outputs["Color"])
