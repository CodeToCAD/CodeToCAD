
import os
import pkgutil
import runpy
import sys
from functools import wraps
from importlib import reload
from pathlib import Path

import bpy
import console_python
from bpy.props import CollectionProperty, StringProperty
from bpy.types import AddonPreferences, Operator, OperatorFileListElement
from bpy_extras.io_utils import ImportHelper, orientation_helper
from console_python import replace_help

bl_info = {
    "name": "CodeToCAD",
    "author": "CodeToCAD",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "description": "",
    "doc_url": "https://github.com/CodeToCad/CodeToCad-Blender",
    "category": "Scripting",
}


class DisplayMessage(Operator):
    bl_idname = "code_to_cad.display_message"
    bl_label = "Display CodeToCAD Message"
    bl_options = {'REGISTER'}

    message: StringProperty()
    log_type: StringProperty()  # e.g. INFO, WARNING, ERROR

    def execute(self, context):

        # https://docs.blender.org/api/current/bpy.types.Operator.html#bpy.types.Operator.report
        self.report(
            {self.log_type},
            self.message
        )

        return {'FINISHED'}


def reloadCodeToCADModules():
    print("Reloading CodeToCAD modules")
    import BlenderActions
    import BlenderDefinitions
    import BlenderProvider
    import CodeToCADInterface
    import utilities
    import CodeToCAD

    reload(utilities)
    reload(CodeToCADInterface)
    reload(BlenderProvider)
    reload(BlenderDefinitions)
    reload(BlenderActions)
    reload(CodeToCAD)

    from BlenderProvider import injectBlenderProvider
    injectBlenderProvider()


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

        paths: list[str] = [os.path.join(self.directory, name.name)
                            for name in self.files]

        reloadCodeToCADModules()

        # Add the directory to python execute path, so that imports work.
        # if there are submodules for the script being imported, the user will have to use:
        # from pathlib import Path
        # sys.path.append( Path(__file__).parent.absolute() )
        sys.path.append(self.directory)

        for path in paths:
            print("Running script", path)
            runpy.run_path(path, run_name="__main__")

        from BlenderActions import zoomToSelectedObjects
        zoomToSelectedObjects()

        # Cleanup:
        sys.path.remove(self.directory)
        for _, package_name, _ in pkgutil.iter_modules([self.directory]):
            if package_name in sys.modules:
                del sys.modules[package_name]

        return {'FINISHED'}

    def draw(self, context):
        pass


def menu_import(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator(ImportCodeToCAD.bl_idname,
                         text="CodeToCAD (.codetocad)")


class CodeToCADAddonPreferences(AddonPreferences):
    # References https://docs.blender.org/api/current/bpy.types.AddonPreferences.html
    bl_idname = __name__

    codeToCadFilePath: StringProperty(
        name="CodeToCAD Folder",
        subtype='FILE_PATH',
    )

    class addCodeToCADToPath(Operator):
        """Print object name in Console"""
        bl_idname = "code_to_cad.add_blender_provider_to_path"
        bl_label = "Add CodeToCAD To Path"
        bl_options = {'REGISTER'}

        def execute(self, context):

            return addCodeToCADToPath(context=context, returnBlenderOperationStatus=True)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Configure CodeToCAD.")
        layout.label(
            text="For setup instructions, please see https://github.com/CodeToCad/CodeToCad-Blender", icon="QUESTION")
        layout.prop(self, "codeToCadFilePath")

        layout.operator(CodeToCADAddonPreferences.addCodeToCADToPath.bl_idname,
                        text="Refresh BlenderProvider", icon="CONSOLE")

    @staticmethod
    def getCodeToCadFilePathFromPreferences(context):
        preferenceKey = "codeToCadFilePath"
        preferences = context.preferences.addons[__name__].preferences
        return preferences[preferenceKey] if preferenceKey in preferences else None


def addCodeToCADToPath(context=bpy.context, returnBlenderOperationStatus=False):
    print("addCodeToCADToPath called")

    codeToCADPath = CodeToCADAddonPreferences.getCodeToCadFilePathFromPreferences(
        context)

    if not codeToCADPath or not os.path.exists(codeToCADPath):
        print("Could not add BlenderProvider to path. Please make sure you have installed and configured the CodeToCADBlenderAddon first.")
        return {'CANCELLED'} if returnBlenderOperationStatus else None

    corePath = codeToCADPath+"/core"
    codeToCadProviderPath = codeToCADPath+"/providers"
    blenderProviderPath = codeToCADPath+"/providers/blender"

    if not Path(blenderProviderPath+"/BlenderProvider.py").is_file():
        print(
            "Could not find BlenderProvider files. Please reconfigure CodeToCADBlenderAddon")
        return {'CANCELLED'} if returnBlenderOperationStatus else None

    print("Adding {} to path".format(corePath))

    sys.path.append(corePath)

    print("Adding {} to path".format(codeToCadProviderPath))

    sys.path.append(codeToCadProviderPath)

    print("Adding {} to path".format(blenderProviderPath))

    sys.path.append(blenderProviderPath)

    print("Adding {} to path".format(codeToCADPath))

    sys.path.append(codeToCADPath)

    from BlenderProvider import injectBlenderProvider
    injectBlenderProvider()

    return {'FINISHED'} if returnBlenderOperationStatus else None


@wraps(replace_help)
def addCodeToCADConvenienceWordsToConsole(namspace):
    # references https://blender.stackexchange.com/a/2751

    replace_help(namspace)

    from CodeToCAD import (Analytics, Angle, Animation, Curve, Dimension,
                           Dimensions, Joint, Landmark, Material, Part, Scene,
                           Shape, Sketch, center, max, min)
    from core.utilities import Angle, Dimension, Dimensions, center, max, min

    namspace["Part"] = Part
    namspace["Shape"] = Part
    namspace["Sketch"] = Sketch
    namspace["Curve"] = Sketch
    namspace["Landmark"] = Landmark
    namspace["Scene"] = Scene
    namspace["Analytics"] = Analytics
    namspace["Joint"] = Joint
    namspace["Material"] = Material
    namspace["Animation"] = Animation
    namspace["min"] = min
    namspace["max"] = max
    namspace["center"] = center
    namspace["Dimension"] = Dimension
    namspace["Dimensions"] = Dimensions
    namspace["Angle"] = Angle


def register():
    print("Registering ", __name__)
    bpy.utils.register_class(CodeToCADAddonPreferences)
    bpy.utils.register_class(CodeToCADAddonPreferences.addCodeToCADToPath)
    bpy.utils.register_class(DisplayMessage)
    bpy.utils.register_class(ImportCodeToCAD)
    bpy.types.TOPBAR_MT_file_import.append(menu_import)

    bpy.app.timers.register(addCodeToCADToPath)

    console_python.replace_help = addCodeToCADConvenienceWordsToConsole


def unregister():
    print("Unregistering ", __name__)
    bpy.utils.unregister_class(CodeToCADAddonPreferences)
    bpy.utils.unregister_class(CodeToCADAddonPreferences.addCodeToCADToPath)
    bpy.utils.unregister_class(DisplayMessage)
    bpy.utils.unregister_class(ImportCodeToCAD)
    bpy.types.TOPBAR_MT_file_import.remove(menu_import)

    console_python.replace_help = replace_help


if __name__ == "__main__":
    register()
