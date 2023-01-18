
import functools
import os
import pkgutil
import runpy
import sys
from functools import wraps
from importlib import reload
from pathlib import Path
import tempfile
import time
from typing import Optional

import bpy
import console_python
from bpy.props import CollectionProperty, StringProperty
from bpy.types import AddonPreferences, Operator, OperatorFileListElement, PropertyGroup
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

    message: StringProperty()  # type: ignore
    log_type: StringProperty()   # type: ignore # e.g. INFO, WARNING, ERROR

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


class ImportedFileWatcher():
    filepath: str
    directory: str
    lastTimestamp: float = 0
    isWatching = True

    def __init__(self, path: str, directory: str) -> None:
        self.filepath = path
        self.directory = directory

    def checkFileChanged(self) -> bool:
        stamp: float = os.stat(self.filepath).st_mtime
        print("Watchdog, last modified", stamp)
        if stamp != self.lastTimestamp and self.lastTimestamp != 0:
            self.lastTimestamp = stamp
            return True
        self.lastTimestamp = stamp
        return False

    def reloadFile(self, context):
        bpy.ops.wm.revert_mainfile()

        bpy.app.timers.register(functools.partial(
            importCodeToCADFile, self.filepath, self.directory, False))

    def watchFile(self) -> Optional[int]:
        # if self.isShowingDialog:
        #     return
        if not self.isWatching:
            return None
        if self.checkFileChanged():
            bpy.ops.code_to_cad.confirm_imported_file_reload('INVOKE_DEFAULT')
            return None
        return 5


importedFileWatcher: Optional[ImportedFileWatcher] = None


def importCodeToCADFile(filePath, directory, saveFile):

    if saveFile:
        blendFilepath = bpy.data.filepath or os.path.join(
            tempfile.gettempdir(), str(int(time.time())) + ".blend")
        bpy.ops.wm.save_as_mainfile(filepath=blendFilepath)

    reloadCodeToCADModules()

    # Add the directory to python execute path, so that imports work.
    # if there are submodules for the script being imported, the user will have to use:
    # from pathlib import Path
    # sys.path.append( Path(__file__).parent.absolute() )
    sys.path.append(directory)

    print("Running script", filePath)
    runpy.run_path(filePath, run_name="__main__")

    from BlenderActions import zoomToSelectedObjects, selectObject
    selectObject(bpy.data.objects[-1])
    zoomToSelectedObjects()

    # Cleanup:
    sys.path.remove(directory)
    for _, package_name, _ in pkgutil.iter_modules([directory]):
        if package_name in sys.modules:
            del sys.modules[package_name]

    global importedFileWatcher
    if not importedFileWatcher or importedFileWatcher.filepath != filePath:
        if importedFileWatcher:
            importedFileWatcher.isWatching = False
            bpy.app.timers.unregister(importedFileWatcher.watchFile)
        importedFileWatcher = ImportedFileWatcher(filePath, directory)
    importedFileWatcher.watchFile()
    bpy.app.timers.register(importedFileWatcher.watchFile, persistent=True)


@ orientation_helper(axis_forward='Y', axis_up='Z')  # type: ignore
class ImportCodeToCAD(Operator, ImportHelper):
    bl_idname = "code_to_cad.import_codetocad"
    bl_label = "Import CodeToCAD"
    bl_description = "Load a CodeToCAD file"
    bl_options = {'UNDO'}

    filter_glob: StringProperty(
        default="*.codetocad;*.py",
        options={'HIDDEN'},
    )  # type: ignore
    files: CollectionProperty(
        name="File Path",
        type=OperatorFileListElement,
    )  # type: ignore
    directory: StringProperty(
        subtype='DIR_PATH',
    )  # type: ignore

    def execute(self, context):

        paths: list[str] = [os.path.join(self.directory, name.name)
                            for name in self.files]

        importCodeToCADFile(paths[0], self.directory, True)

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
    )  # type: ignore

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
        layout.prop(self, "codeToCadFilePath")  # type: ignore

        layout.operator(CodeToCADAddonPreferences.addCodeToCADToPath.bl_idname,
                        text="Refresh BlenderProvider", icon="CONSOLE")

    @ staticmethod
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


@ wraps(replace_help)
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


class ConfirmImportedFileReload(bpy.types.Operator):
    bl_idname = "code_to_cad.confirm_imported_file_reload"
    bl_label = "Imported file has changed. Reload?"
    bl_options = {'REGISTER'}

    reload: bpy.props.BoolProperty(name="reload", default=True)
    stopWatching: bpy.props.BoolProperty(name="stopWatching")

    @ classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        self.report({'INFO'}, "Reload imported file? {self.reload}")
        print(context.area, context.window)
        global importedFileWatcher
        if importedFileWatcher and self.reload:
            importedFileWatcher.reloadFile(context=context)

        if importedFileWatcher:
            importedFileWatcher.isWatching = not self.stopWatching

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        row = self.layout
        row.prop(self, "reload", text="Reload")
        row.prop(self, "stopWatching", text="Stop watching file changes.")


def register():
    print("Registering ", __name__)
    bpy.utils.register_class(CodeToCADAddonPreferences)
    bpy.utils.register_class(CodeToCADAddonPreferences.addCodeToCADToPath)
    bpy.utils.register_class(DisplayMessage)
    bpy.utils.register_class(ImportCodeToCAD)
    bpy.types.TOPBAR_MT_file_import.append(menu_import)
    bpy.utils.register_class(ConfirmImportedFileReload)

    # bpy.types.Scene.importedFileWatcher = bpy.props.PointerProperty(
    #     type=ImportedFileWatcher)

    bpy.app.timers.register(addCodeToCADToPath)

    console_python.replace_help = addCodeToCADConvenienceWordsToConsole


def unregister():
    print("Unregistering ", __name__)
    bpy.utils.unregister_class(CodeToCADAddonPreferences)
    bpy.utils.unregister_class(CodeToCADAddonPreferences.addCodeToCADToPath)
    bpy.utils.unregister_class(DisplayMessage)
    bpy.utils.unregister_class(ImportCodeToCAD)
    bpy.types.TOPBAR_MT_file_import.remove(menu_import)
    bpy.utils.unregister_class(ConfirmImportedFileReload)
    # del bpy.types.Scene.importedFileWatcher

    console_python.replace_help = replace_help


if __name__ == "__main__":
    register()
