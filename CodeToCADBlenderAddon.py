import bpy
import os
import sys
from pathlib import Path

import runpy

from bpy.types import Operator, AddonPreferences, OperatorFileListElement
from bpy.props import StringProperty, CollectionProperty

from bpy_extras.io_utils import ImportHelper, orientation_helper


bl_info = {
    "name": "CodeToCAD",
    "author": "CodeToCAD",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "description": "",
    "doc_url": "https://github.com/CodeToCad/CodeToCad-Blender",
    "category": "Scripting",
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

        # Add the directory to python execute path, so that imports work.
        # if there are submodules for the script being imported, the user will have to use:
        # from pathlib import Path
        # sys.path.append( Path(__file__).parent.absolute() )
        sys.path.append(self.directory)

        if not paths:
            paths.append(self.filepath)

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

            return addBlenderProviderToPath(context=context, returnBlenderOperationStatus=True)

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


def addBlenderProviderToPath(context=bpy.context, returnBlenderOperationStatus=False):
    print("addBlenderProviderToPath called")
    
    blenderProviderPath = CodeToCADAddonPreferences.getBlenderProviderFilePathFromPreferences(context)

    if not blenderProviderPath or not os.path.exists(blenderProviderPath) or not Path(blenderProviderPath+"/CodeToCADBlenderProvider.py").is_file():
        print("Could not add BlenderProvider to path. Please make sure you have installed and configured the CodeToCADBlenderAddon first.")
        return {'CANCELLED'} if returnBlenderOperationStatus else None

    print("Adding {} to path".format(blenderProviderPath))

    sys.path.append(blenderProviderPath)


    codeToCADPath = blenderProviderPath+"/CodeToCAD/"
    
    print("Adding {} to path".format(codeToCADPath))

    sys.path.append(codeToCADPath)


    return {'FINISHED'} if returnBlenderOperationStatus else None

# references https://blender.stackexchange.com/a/2751
from functools import wraps
from console_python import replace_help
import console_python

@wraps(replace_help)
def addCodeToCADConvenienceWordsToConsole(namspace):

    replace_help(namspace)
    
    from CodeToCADBlenderProvider import shape, curve, landmark, scene, analytics, joint

    namspace["shape"] = shape
    namspace["curve"] = curve
    namspace["landmark"] = landmark
    namspace["scene"] = scene
    namspace["analytics"] = analytics
    namspace["joint"] = joint

def register():
    print ("Registering ", __name__)
    bpy.utils.register_class(CodeToCADAddonPreferences)
    bpy.utils.register_class(CodeToCADAddonPreferences.AddBlenderProviderToPath)
    bpy.utils.register_class(ImportCodeToCAD)
    bpy.types.TOPBAR_MT_file_import.append(menu_import)
    
    bpy.app.timers.register(addBlenderProviderToPath)

    console_python.replace_help = addCodeToCADConvenienceWordsToConsole


def unregister():
    print ("Unregistering ", __name__)
    bpy.utils.unregister_class(CodeToCADAddonPreferences)
    bpy.utils.unregister_class(CodeToCADAddonPreferences.AddBlenderProviderToPath)
    bpy.utils.unregister_class(ImportCodeToCAD)
    bpy.types.TOPBAR_MT_file_import.remove(menu_import)

    console_python.replace_help = replace_help


if __name__ == "__main__":
    register()