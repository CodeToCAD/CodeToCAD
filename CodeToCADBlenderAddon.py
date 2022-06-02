import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty

bl_info = {
    "name": "CodeToCAD",
    "author": "",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "None",
    "description": "",
    "warning": "",
    "doc_url": "",
    "category": "Testing",
}

# References https://docs.blender.org/api/current/bpy.types.AddonPreferences.html
class CodeToCADAddonPreferences(AddonPreferences):
    bl_idname = __name__

    blenderProviderFilePath: StringProperty(
        name="BlenderProvider Folder",
        subtype='FILE_PATH',
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Configure CodeToCAD.")
        layout.label(text="For setup instructions, see https://github.com/CodeToCad/CodeToCad-Blender", icon="QUESTION")
        layout.prop(self, "blenderProviderFilePath")

    @staticmethod
    def getBlenderProviderFilePathFromPreferences(context):
        return context.preferences.addons[__name__].preferences["blenderProviderFilePath"]


def register():
    print ("Registering ", __name__)
    bpy.utils.register_class(CodeToCADAddonPreferences)

def unregister():
    print ("Unregistering ", __name__)
    bpy.utils.unregister_class(CodeToCADAddonPreferences)

if __name__ == "__main__":
    register()