import bpy
import os
import sys
from pathlib import Path

import runpy

from bpy.types import Operator, AddonPreferences, OperatorFileListElement
from bpy.props import StringProperty, IntProperty, BoolProperty, CollectionProperty

from bpy_extras.io_utils import ImportHelper, orientation_helper

bl_info = {
    "name": "CodeToCAD",
    "author": "CodeToCAD",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "description": "",
    "doc_url": "https://github.com/CodeToCad/CodeToCad-Blender",
    "category": "Testing",
}

@orientation_helper(axis_forward='Y', axis_up='Z')
class ImportCodeToCAD(Operator, ImportHelper):
    bl_idname = "code_to_cad.import_codetocad"
    bl_label = "Import CodeToCAD"
    bl_description = "Load a CodeToCAD file"
    bl_options = {'UNDO'}

    filter_glob: StringProperty(
        default="*.codetocad;*.py",
        options={'HIDDEN'},
    )
    files: CollectionProperty(
        name="File Path",
        type=OperatorFileListElement,
    )
    directory: StringProperty(
        subtype='DIR_PATH',
    )

    def execute(self, context):

        paths = [os.path.join(self.directory, name.name) for name in self.files]

        if not paths:
            paths.append(self.filepath)

        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode='OBJECT')

        if bpy.ops.object.select_all.poll():
            bpy.ops.object.select_all(action='DESELECT')

        for path in paths:
            print("Running script", path)
            runpy.run_path(path)

        return {'FINISHED'}

    def draw(self, context):
        pass
    

def menu_import(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator(ImportCodeToCAD.bl_idname, text="CodeToCAD (.codetocad)")

# References https://docs.blender.org/api/current/bpy.types.AddonPreferences.html
class CodeToCADAddonPreferences(AddonPreferences):
    bl_idname = __name__

    blenderProviderFilePath: StringProperty(
        name="BlenderProvider Folder",
        subtype='FILE_PATH',
    )
    
    class AddBlenderProviderToPath(Operator):
        """Print object name in Console"""
        bl_idname = "code_to_cad.add_blender_provider_to_path"
        bl_label = "Add Blender Provider To Path"
        bl_options = {'REGISTER'}

        def execute(self, context):
            blenderProviderPath = CodeToCADAddonPreferences.getBlenderProviderFilePathFromPreferences(context=context)

            if not blenderProviderPath or not os.path.exists(blenderProviderPath) or not Path(blenderProviderPath+"/CodeToCADBlenderProvider.py").is_file():
                print("AddBlenderProviderToPath error: Invalid path. Please make sure the addon is configured correctly.")
                return {'CANCELLED'}

            print("Adding {} to path".format(blenderProviderPath))

            sys.path.append(blenderProviderPath)

            return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Configure CodeToCAD.")
        layout.label(text="For setup instructions, please see https://github.com/CodeToCad/CodeToCad-Blender", icon="QUESTION")
        layout.prop(self, "blenderProviderFilePath")
        
        layout.operator(CodeToCADAddonPreferences.AddBlenderProviderToPath.bl_idname, text="Refresh BlenderProvider", icon="CONSOLE")

    @staticmethod
    def getBlenderProviderFilePathFromPreferences(context):
        preferenceKey = "blenderProviderFilePath"
        preferences = context.preferences.addons[__name__].preferences
        return preferences[preferenceKey] if preferenceKey in preferences else None


def register():
    print ("Registering ", __name__)
    bpy.utils.register_class(CodeToCADAddonPreferences)
    bpy.utils.register_class(CodeToCADAddonPreferences.AddBlenderProviderToPath)
    bpy.utils.register_class(ImportCodeToCAD)
    bpy.types.TOPBAR_MT_file_import.append(menu_import)

    # Add BlenderProvider to path if the addon is already configured.
    if CodeToCADAddonPreferences.getBlenderProviderFilePathFromPreferences(bpy.context):
        bpy.ops.code_to_cad.add_blender_provider_to_path()
        bpy.ops.console.insert(text="from CodeToCADBlenderProvider import shape, curve, landmark, scene, analytics, joint")

def unregister():
    print ("Unregistering ", __name__)
    bpy.utils.unregister_class(CodeToCADAddonPreferences)
    bpy.utils.unregister_class(CodeToCADAddonPreferences.AddBlenderProviderToPath)
    bpy.utils.unregister_class(ImportCodeToCAD)
    bpy.types.TOPBAR_MT_file_import.remove(menu_import)

if __name__ == "__main__":
    register()