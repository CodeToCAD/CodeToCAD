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

namespace = "code_to_cad"

operatorIds = {
    "ReloadLastImport": namespace + ".reload_last_import",
    "StopAutoReload": namespace + ".stop_auth_reload_last_import",
    "ImportCodeToCAD": namespace + ".import_codetocad",
    "ConfirmImportedFileReload": namespace + ".confirm_imported_file_reload",
    "AddCodeToCADToPath": namespace + ".add_blender_provider_to_path",
    "OpenPreferences": namespace + ".open_preferences",
    "LogMessage": namespace + ".log_message",
}


class ReloadLastImport(Operator):
    bl_idname = operatorIds["ReloadLastImport"]
    bl_label = "Reload last import"
    bl_options = {'REGISTER'}

    def execute(self, context):

        # https://docs.blender.org/api/current/bpy.types.Operator.html#bpy.types.Operator.report

        global importedFileWatcher
        if not importedFileWatcher:
            self.report({'ERROR'}, "No CodeToCAD file imported")
            return {'CANCELLED'}

        importedFileWatcher.reloadFile(context)

        return {'FINISHED'}


class LogMessage(Operator):
    bl_idname = operatorIds["LogMessage"]
    bl_label = "Log Message"
    bl_options = {'REGISTER'}
    message: bpy.props.StringProperty(
        name="Message", default="Reporting : Base message")

    def execute(self, context):

        # https://blender.stackexchange.com/questions/50098/force-logs-to-appear-in-info-view-when-chaining-operator-calls

        log = {"INFO"}
        self.report(log, self.message)

        return {'FINISHED'}


class StopAutoReload(Operator):
    bl_idname = operatorIds["StopAutoReload"]
    bl_label = "Stop auto-reloading last import"
    bl_options = {'REGISTER'}

    def execute(self, context):

        # https://docs.blender.org/api/current/bpy.types.Operator.html#bpy.types.Operator.report

        global importedFileWatcher
        if not importedFileWatcher:
            self.report({'ERROR'}, "No CodeToCAD file imported")
            return {'CANCELLED'}

        importedFileWatcher.stopWatchingFile()

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
    _isWatching = True
    isAskBeforeReloading = False

    def __init__(self, path: str, directory: str, context) -> None:
        self.filepath = path
        self.directory = directory
        self.isAskBeforeReloading = CodeToCADAddonPreferences.getIsAskBeforeReloadingFromPreferences(
            context)

    def checkFileChanged(self) -> bool:
        stamp: float = os.stat(self.filepath).st_mtime
        print("Import auto-reload: last modified", stamp)
        if stamp != self.lastTimestamp and self.lastTimestamp != 0:
            self.lastTimestamp = stamp
            return True
        self.lastTimestamp = stamp
        return False

    def reloadFile(self, context):
        bpy.ops.wm.revert_mainfile()

        bpy.app.timers.register(functools.partial(
            importCodeToCADFile, context, self.filepath, self.directory, False))

    def stopWatchingFile(self):
        self._isWatching = False
        try:
            bpy.app.timers.unregister(self.watchFile)
        except:
            pass

    def registerFileWatcher(self):
        bpy.app.timers.register(self.watchFile, persistent=True)

    def watchFile(self) -> Optional[int]:
        if not self._isWatching:
            print("Import auto-reload: stopping imported-file modify check timer.")
            return None
        if self.checkFileChanged():
            print("Import auto-reload: file has changed.")
            if self.isAskBeforeReloading:
                bpy.ops.code_to_cad.confirm_imported_file_reload(  # type: ignore
                    'INVOKE_DEFAULT')
            else:
                self.reloadFile(bpy.context)
        # number of seconds before re-checking (courtesy of bpy.app.timers)
        return 5


importedFileWatcher: Optional[ImportedFileWatcher] = None


def importCodeToCADFile(context, filePath, directory, saveFile):

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

    if not CodeToCADAddonPreferences.getisAutoReloadImportsFromPreferences(context):
        return

    global importedFileWatcher
    if not importedFileWatcher or importedFileWatcher.filepath != filePath:
        if importedFileWatcher:
            importedFileWatcher.stopWatchingFile()
        importedFileWatcher = ImportedFileWatcher(filePath, directory, context)
    importedFileWatcher.watchFile()
    importedFileWatcher.registerFileWatcher()


@ orientation_helper(axis_forward='Y', axis_up='Z')  # type: ignore
class ImportCodeToCAD(Operator, ImportHelper):
    bl_idname = operatorIds["ImportCodeToCAD"]
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

        importCodeToCADFile(context, paths[0], self.directory, True)

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
    isAutoReloadImports: bpy.props.BoolProperty(
        name="Auto Reload", default=False)  # type: ignore
    isAskBeforeReloading: bpy.props.BoolProperty(
        name="Ask before auto-reload", default=False)  # type: ignore

    class AddCodeToCADToPath(Operator):
        """Print object name in Console"""
        bl_idname = operatorIds["AddCodeToCADToPath"]
        bl_label = "Add CodeToCAD To Path"
        bl_options = {'REGISTER'}

        def execute(self, context):

            return addCodeToCADToPath(context=context, returnBlenderOperationStatus=True)

    def draw(self, context):
        layout = self.layout

        layout.label(text="Configure CodeToCAD.")
        layout.separator()
        box = layout.box()
        box.label(text="Path to CodeToCAD folder:")
        box.label(
            text="For setup instructions, please see https://github.com/CodeToCad/CodeToCad-Blender", icon="QUESTION")
        box.prop(self, "codeToCadFilePath")  # type: ignore

        box.operator(CodeToCADAddonPreferences.AddCodeToCADToPath.bl_idname,
                     text="Refresh BlenderProvider", icon="CONSOLE")

        layout.separator()
        box = layout.box()
        box.label(text="Importing:")
        box.prop(self, "isAutoReloadImports")  # type: ignore
        box.prop(self, "isAskBeforeReloading")  # type: ignore

    @staticmethod
    def getPreferenceKey(preferenceKey, context):
        preferences = context.preferences.addons[__name__].preferences
        return preferences[preferenceKey] if preferenceKey in preferences else None

    @staticmethod
    def getisAutoReloadImportsFromPreferences(context):
        return CodeToCADAddonPreferences.getPreferenceKey("isAutoReloadImports", context) or False

    @staticmethod
    def getIsAskBeforeReloadingFromPreferences(context):
        return CodeToCADAddonPreferences.getPreferenceKey("isAskBeforeReloading", context) or False

    @staticmethod
    def getCodeToCadFilePathFromPreferences(context):
        return CodeToCADAddonPreferences.getPreferenceKey("codeToCadFilePath", context)


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
    bl_idname = operatorIds["ConfirmImportedFileReload"]
    bl_label = "Imported file has changed. Reload?"
    bl_options = {'REGISTER'}

    reload: bpy.props.BoolProperty(name="Reload", default=True)  # type: ignore
    stopWatching: bpy.props.BoolProperty(name="Stop Watching")  # type: ignore

    @ classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        self.report({'INFO'}, "Reload imported file? {self.reload}")
        print(context.area, context.window)
        global importedFileWatcher
        if importedFileWatcher and self.reload:
            importedFileWatcher.reloadFile(context=context)

        if importedFileWatcher and self.stopWatching:
            importedFileWatcher.stopWatchingFile()

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        row = self.layout
        row.prop(self, "reload", text="Reload")  # type: ignore
        row.prop(self, "stopWatching",  # type: ignore
                 text="Stop watching file changes.")


class OpenPreferences(bpy.types.Operator):
    bl_idname = operatorIds["OpenPreferences"]
    bl_label = "Open Preferences"
    bl_options = {'REGISTER'}

    @staticmethod
    def openPreferences():
        bpy.ops.screen.userpref_show()
        bpy.context.preferences.active_section = 'ADDONS'
        bpy.data.window_managers["WinMan"].addon_search = bl_info["name"]

    def execute(self, context):
        OpenPreferences.openPreferences()
        return {"FINISHED"}


class CodeToCADPanel(bpy.types.Panel):
    bl_idname = "code_to_cad.main_panel"
    bl_label = "CodeToCAD"
    bl_space_type = "VIEW_3D"
    bl_category = "CodeToCAD"
    bl_region_type = "UI"

    def draw(self, context):
        self.layout.operator(ImportCodeToCAD.bl_idname,
                             icon='IMPORT', text="Import CodeToCAD")
        self.layout.operator(ReloadLastImport.bl_idname,
                             icon='FILE_REFRESH', text="Reload imported file")
        self.layout.operator(StopAutoReload.bl_idname,
                             icon='REMOVE', text="Stop auto-reload")
        self.layout.operator(OpenPreferences.bl_idname,
                             icon='PREFERENCES', text="Open Preferences")


def register():
    print("Registering ", __name__)
    bpy.utils.register_class(CodeToCADAddonPreferences)
    bpy.utils.register_class(CodeToCADAddonPreferences.AddCodeToCADToPath)
    bpy.utils.register_class(ReloadLastImport)
    bpy.utils.register_class(StopAutoReload)
    bpy.utils.register_class(ImportCodeToCAD)
    bpy.types.TOPBAR_MT_file_import.append(menu_import)
    bpy.utils.register_class(ConfirmImportedFileReload)
    bpy.utils.register_class(CodeToCADPanel)
    bpy.utils.register_class(OpenPreferences)
    bpy.utils.register_class(LogMessage)

    bpy.app.timers.register(addCodeToCADToPath)

    console_python.replace_help = addCodeToCADConvenienceWordsToConsole


def unregister():
    print("Unregistering ", __name__)
    bpy.utils.unregister_class(CodeToCADAddonPreferences)
    bpy.utils.unregister_class(CodeToCADAddonPreferences.AddCodeToCADToPath)
    bpy.utils.unregister_class(ReloadLastImport)
    bpy.utils.unregister_class(StopAutoReload)
    bpy.utils.unregister_class(ImportCodeToCAD)
    bpy.types.TOPBAR_MT_file_import.remove(menu_import)
    bpy.utils.unregister_class(ConfirmImportedFileReload)
    bpy.utils.unregister_class(CodeToCADPanel)
    bpy.utils.unregister_class(OpenPreferences)
    bpy.utils.unregister_class(LogMessage)

    console_python.replace_help = replace_help


if __name__ == "__main__":
    register()