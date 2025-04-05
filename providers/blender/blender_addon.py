import os
import pkgutil
import runpy
import sys
from pathlib import Path
import tempfile
import time
import traceback
from typing import Optional

import bpy
import console_python
from bpy.props import CollectionProperty, StringProperty
from bpy.types import AddonPreferences, Operator, OperatorFileListElement
from bpy_extras.io_utils import ImportHelper, orientation_helper
from console_python import replace_help

git_epoch = 0
try:
    with open("version.txt") as f:
        git_epoch = int(f.read())
except Exception as e:
    print("No version file found.", e)

version = (1, 0, git_epoch)
print("CodeToCAD Addon Version: ", version)

bl_info = {
    "name": "CodeToCAD",
    "author": "CodeToCAD",
    "blender": (3, 1, 0),
    "description": "CodeToCAD is a modeling automation. Visit https://github.com/CodeToCAD/CodeToCAD#Blender for more information",
    "doc_url": "https://github.com/CodeToCAD/CodeToCAD",
    "category": "Scripting",
}

namespace = "codetocad"

operatorIds = {
    "ReloadLastImport": namespace + ".reload_last_import",
    "StopAutoReload": namespace + ".stop_auth_reload_last_import",
    "ImportCodeToCAD": namespace + ".import_codetocad",
    "ConfirmImportedFileReload": namespace + ".confirm_imported_file_reload",
    "AddCodeToCADToPath": namespace + ".add_blender_provider_to_path",
    "OpenPreferences": namespace + ".open_preferences",
    "LogMessage": namespace + ".log_message",
    "ReloadCodeToCADModules": namespace + ".reload_codetocad_modules",
    "StartDebugger": namespace + ".start_debugger",
}


class StartDebugger(Operator):
    bl_idname = operatorIds["StartDebugger"]
    bl_label = "Start a debugpy server"
    bl_options = {"REGISTER"}
    bl_description = "Start a debugpy server. Warning: If debugpy is not installed, this will try to automatically pip install debugpy."

    def execute(self, context):
        from providers.blender.blender_provider.blender_actions.console import (
            start_debugger,
        )

        start_debugger()

        return {"FINISHED"}


class ReloadCodeToCADModules(Operator):
    bl_idname = operatorIds["ReloadCodeToCADModules"]
    bl_label = "Reload CodeToCAD Modules"
    bl_options = {"REGISTER"}

    def execute(self, context):
        from providers.blender.blender_provider.blender_actions.console import (
            reload_codetocad_modules,
        )

        reload_codetocad_modules()

        return {"FINISHED"}


class ReloadLastImport(Operator):
    bl_idname = operatorIds["ReloadLastImport"]
    bl_label = "Reload last import"
    bl_options = {"REGISTER"}

    def execute(self, context):
        global imported_file_watcher
        if not imported_file_watcher:
            self.report({"ERROR"}, "No CodeToCAD file imported")
            return {"CANCELLED"}

        imported_file_watcher.reload_file(context)

        return {"FINISHED"}


class LogMessage(Operator):
    bl_idname = operatorIds["LogMessage"]
    bl_label = "Log Message"
    bl_options = {"REGISTER"}
    message: bpy.props.StringProperty(
        name="Message", default="Reporting : Base message"
    )  # type: ignore
    isError: bpy.props.BoolProperty(name="isError", default=False)  # type: ignore

    def execute(self, context):
        # https://blender.stackexchange.com/questions/50098/force-logs-to-appear-in-info-view-when-chaining-operator-calls

        logType = {"ERROR"} if self.isError else {"INFO"}
        self.report(logType, self.message)

        return {"FINISHED"}


class StopAutoReload(Operator):
    bl_idname = operatorIds["StopAutoReload"]
    bl_label = "Stop auto-reloading last import"
    bl_options = {"REGISTER"}

    def execute(self, context):
        # https://docs.blender.org/api/current/bpy.types.Operator.html#bpy.types.Operator.report

        global imported_file_watcher
        if not imported_file_watcher:
            self.report({"ERROR"}, "No CodeToCAD file imported")
            return {"CANCELLED"}

        imported_file_watcher.stop_watching_file()

        return {"FINISHED"}


class ImportedFileWatcher:
    filepath: str
    directory: str
    lastTimestamp: float = 0
    _isWatching = True
    is_ask_before_reloading = False

    def __init__(self, path: str, directory: str, context) -> None:
        self.filepath = path
        self.directory = directory
        self.is_ask_before_reloading = (
            CodeToCADAddonPreferences.get_is_ask_before_reloading_from_preferences(
                context
            )
        )

    def check_file_changed(self) -> bool:
        stamp: float = os.stat(self.filepath).st_mtime

        if stamp != self.lastTimestamp and self.lastTimestamp != 0:
            self.lastTimestamp = stamp
            return True
        self.lastTimestamp = stamp
        return False

    def reload_file(self, context):
        bpy.ops.wm.revert_mainfile()

        import_codetocad_file(self.filepath, self.directory, False)

    def stop_watching_file(self):
        self._isWatching = False
        try:
            bpy.app.timers.unregister(self.watch_file)
        except:
            pass

    def register_file_watcher(self):
        bpy.app.timers.register(self.watch_file, persistent=True)

    def watch_file(self) -> Optional[int]:
        if not self._isWatching:
            print("Import auto-reload: stopping imported-file modify check timer.")
            return None
        if self.check_file_changed():
            print("Import auto-reload: file has changed.")
            if self.is_ask_before_reloading:
                codetocad_ops = getattr(bpy.ops, namespace)
                codetocad_ops.confirm_imported_file_reload("INVOKE_DEFAULT")
            else:
                self.reload_file(bpy.context)
        # number of seconds before re-checking (courtesy of bpy.app.timers)
        return 5


imported_file_watcher: Optional[ImportedFileWatcher] = None


def import_codetocad_file(filePath, directory, saveFile):
    from providers.blender.blender_provider.blender_actions.console import (
        reload_codetocad_modules,
    )

    reload_codetocad_modules()

    if saveFile:
        blendFilepath = bpy.data.filepath or os.path.join(
            tempfile.gettempdir(), str(int(time.time())) + ".blend"
        )
        bpy.ops.wm.save_as_mainfile(filepath=blendFilepath)

    # Add the directory to python execute path, so that imports work.
    # if there are submodules for the script being imported, the user will have to use:
    # from pathlib import Path
    # sys.path.append( Path(__file__).parent.absolute() )
    sys.path.append(directory)

    print("Running script", filePath)

    from providers.blender.blender_provider.blender_actions.context import (
        get_context_view_3d,
    )

    with get_context_view_3d():
        global imported_file_watcher
        if not imported_file_watcher or imported_file_watcher.filepath != filePath:
            if imported_file_watcher:
                imported_file_watcher.stop_watching_file()
            imported_file_watcher = ImportedFileWatcher(
                filePath, directory, bpy.context
            )

        if CodeToCADAddonPreferences.get_is_auto_reload_imports_from_preferences(
            bpy.context
        ):
            imported_file_watcher.watch_file()
            imported_file_watcher.register_file_watcher()

        try:
            runpy.run_path(filePath, run_name="__main__")
        except Exception as err:
            errorTrace = traceback.format_exc()
            print("Import failed: ", err, errorTrace)
            codetocad_ops = getattr(bpy.ops, namespace)
            codetocad_ops.log_message(
                # type: ignore
                "INVOKE_DEFAULT",
                message=f"{errorTrace}",
                isError=True,
            )

            raise err
        finally:
            from providers.blender.blender_provider.blender_actions.context import (
                zoom_to_selected_objects,
                select_object,
            )

            if len(bpy.data.objects) > 0:
                objectToZoomOn = bpy.data.objects[-1]
                objectToZoomOn = (
                    objectToZoomOn.parent
                    if objectToZoomOn.parent is not None
                    else objectToZoomOn
                )
                select_object(objectToZoomOn.name)
                zoom_to_selected_objects()

            # Cleanup:
            sys.path.remove(directory)
            for _, package_name, _ in pkgutil.iter_modules([directory]):
                if package_name in sys.modules:
                    del sys.modules[package_name]


@orientation_helper(axis_forward="Y", axis_up="Z")  # type: ignore
class ImportCodeToCAD(Operator, ImportHelper):
    bl_idname = operatorIds["ImportCodeToCAD"]
    bl_label = "Import CodeToCAD"
    bl_description = "Load a CodeToCAD file"
    bl_options = {"UNDO"}

    filter_glob: StringProperty(
        default="*.codetocad;*.py",
        options={"HIDDEN"},
    )  # type: ignore
    files: CollectionProperty(
        name="File Path",
        type=OperatorFileListElement,
    )  # type: ignore
    directory: StringProperty(
        subtype="DIR_PATH",
    )  # type: ignore

    def execute(self, context):
        paths: list[str] = [
            os.path.join(self.directory, name.name) for name in self.files
        ]

        try:
            import_codetocad_file(paths[0], self.directory, True)
        except Exception as err:
            self.report({"ERROR"}, f"Import failed: {err}")
            return {"CANCELLED"}

        return {"FINISHED"}

    def draw(self, context):
        pass


def menu_import(self, context):
    self.layout.operator_context = "INVOKE_DEFAULT"
    self.layout.operator(ImportCodeToCAD.bl_idname, text="CodeToCAD (.codetocad)")


class CodeToCADAddonPreferences(AddonPreferences):
    # References https://docs.blender.org/api/current/bpy.types.AddonPreferences.html
    bl_idname = __name__

    codetocad_file_path: StringProperty(
        name="CodeToCAD Folder",
        subtype="FILE_PATH",
        default=str(Path(__file__).parent.absolute()),
    )  # type: ignore
    is_auto_reload_imports: bpy.props.BoolProperty(
        name="Auto Reload", default=True  # type: ignore
    )
    is_ask_before_reloading: bpy.props.BoolProperty(
        name="Ask before auto-reload", default=False  # type: ignore
    )

    class AddCodeToCADToPath(Operator):
        """Print object name in Console"""

        bl_idname = operatorIds["AddCodeToCADToPath"]
        bl_label = "Add CodeToCAD To Path"
        bl_options = {"REGISTER"}

        def execute(self, context):
            return add_codetocad_to_path(
                context=context, return_blender_operation_status=True
            )

    def draw(self, context):
        layout = self.layout

        layout.label(text="Configure CodeToCAD.")
        layout.separator()
        box = layout.box()
        box.label(text="Path to CodeToCAD folder:")
        box.label(
            text="https://github.com/CodeToCAD/CodeToCAD#Blender",
            icon="QUESTION",
        )
        box.prop(self, "codetocad_file_path")  # type: ignore

        box.operator(
            CodeToCADAddonPreferences.AddCodeToCADToPath.bl_idname,
            text="Refresh blender_provider",
            icon="CONSOLE",
        )

        layout.separator()
        box = layout.box()
        box.label(text="Importing:")
        box.prop(self, "is_auto_reload_imports")  # type: ignore
        box.prop(self, "is_ask_before_reloading")  # type: ignore

    @staticmethod
    def get_preference_key(preferenceKey, context):
        preferences = context.preferences.addons[__name__].preferences
        return preferences[preferenceKey] if preferenceKey in preferences else None

    @staticmethod
    def get_is_auto_reload_imports_from_preferences(context):
        return (
            CodeToCADAddonPreferences.get_preference_key(
                "is_auto_reload_imports", context
            )
            or True
        )

    @staticmethod
    def get_is_ask_before_reloading_from_preferences(context):
        return (
            CodeToCADAddonPreferences.get_preference_key(
                "is_ask_before_reloading", context
            )
            or False
        )

    @staticmethod
    def get_codetocad_file_path_from_preferences(context) -> str:
        value: str = CodeToCADAddonPreferences.get_preference_key(
            "codetocad_file_path", context
        )  # type: ignore
        return value


def add_codetocad_to_path(context=bpy.context, return_blender_operation_status=False):
    print("Going to add CodeToCAD files to path.")

    root_path = CodeToCADAddonPreferences.get_codetocad_file_path_from_preferences(
        context
    ) or str(Path(__file__).parent.absolute())

    if not root_path or not os.path.exists(root_path):
        print("The CodeToCAD base module path that you provided does not exist.")
        return {"CANCELLED"} if return_blender_operation_status else None

    root_path = Path(root_path)

    blender_path = root_path / "providers/blender"
    blender_provider_path = blender_path / "blender_provider"

    if not Path(blender_provider_path).is_dir():
        print(
            "Could not find blender_provider files. Please reconfigure the CodeToCAD Blender Addon.",
            "Searching in: ",
            blender_provider_path,
        )
        return {"CANCELLED"} if return_blender_operation_status else None

    print("Adding {} to path".format(root_path))

    sys.path.append(str(root_path))

    return {"FINISHED"} if return_blender_operation_status else None


class ConfirmImportedFileReload(bpy.types.Operator):
    bl_idname = operatorIds["ConfirmImportedFileReload"]
    bl_label = "Imported file has changed. Reload?"
    bl_options = {"REGISTER"}

    reload: bpy.props.BoolProperty(name="Reload", default=True)  # type: ignore
    stopWatching: bpy.props.BoolProperty(name="Stop Watching")  # type: ignore

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        self.report({"INFO"}, "Reload imported file? {self.reload}")
        print(context.area, context.window)
        global imported_file_watcher
        if imported_file_watcher and self.reload:
            imported_file_watcher.reload_file(context=context)

        if imported_file_watcher and self.stopWatching:
            imported_file_watcher.stop_watching_file()

        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        row = self.layout
        row.prop(self, "reload", text="Reload")  # type: ignore
        row.prop(
            self, "stopWatching", text="Stop watching file changes."  # type: ignore
        )


class OpenPreferences(bpy.types.Operator):
    bl_idname = operatorIds["OpenPreferences"]
    bl_label = "Open Preferences"
    bl_options = {"REGISTER"}

    @staticmethod
    def open_preferences():
        bpy.ops.screen.userpref_show()
        bpy.context.preferences.active_section = "ADDONS"
        bpy.data.window_managers["WinMan"].addon_search = bl_info["name"]

    def execute(self, context):
        OpenPreferences.open_preferences()
        return {"FINISHED"}


class CodeToCADPanel(bpy.types.Panel):
    bl_idname = "CODETOCAD_PT_main_panel"
    bl_label = "CodeToCAD"
    bl_space_type = "VIEW_3D"
    bl_category = "CodeToCAD"
    bl_region_type = "UI"

    def draw(self, context):
        self.layout.operator(
            ImportCodeToCAD.bl_idname, icon="IMPORT", text="Import CodeToCAD"
        )
        self.layout.operator(
            ReloadLastImport.bl_idname, icon="FILE_REFRESH", text="Reload imported file"
        )
        self.layout.operator(
            StopAutoReload.bl_idname, icon="REMOVE", text="Stop auto-reload"
        )
        self.layout.separator()
        self.layout.operator(
            StartDebugger.bl_idname, icon="LINKED", text="Start Debugger"
        )
        self.layout.separator()
        self.layout.operator(
            ReloadCodeToCADModules.bl_idname,
            icon="FILE_REFRESH",
            text="Reload CodeToCAD Modules",
        )
        self.layout.operator(
            OpenPreferences.bl_idname, icon="PREFERENCES", text="Open Preferences"
        )


@bpy.app.handlers.persistent  # type: ignore
def add_codetocad_to_blender_console(*args):
    from providers.blender.blender_provider.blender_actions.console import (
        add_codetocad_convenience_words_to_console,
    )

    if len(args) != 0:
        # If add_codetocad_to_blender_console is called via the app handler, wait a bit before printing the CodeToCAD banner, otherwise it somehow replaces the default banner..
        bpy.app.timers.register(print_codetocad_banner, first_interval=1)

    console_python.replace_help = add_codetocad_convenience_words_to_console


def print_codetocad_banner():
    from providers.blender.blender_provider.blender_actions.console import (
        write_to_console,
    )

    try:
        write_to_console(
            """
------------------------------
CodeToCAD has been added to your console.

You can access the CodeToCAD menu in the sidebar. (Press 'n' on the keyboard)
                    
Try `my_cube = Part.create_cube("100cm", "1m", "1m")`
------------------------------
    """,
            "INFO",
        )
    except:  # noqa
        ...


@bpy.app.handlers.persistent  # type: ignore
def run_from_commandline_arguments(*args):
    # if --CodeToCAD path/to/file.py is passed in, we should automatically run it
    for index in range(1, len(sys.argv)):
        if sys.argv[index].lower() == "--codetocad":
            from codetocad.utilities import get_absolute_filepath

            filepath = sys.argv[index + 1]
            filepath = get_absolute_filepath(filepath)

            if not Path(filepath).exists():
                raise Exception(
                    f"Could not find file {filepath}. If you're using a relative path via command line, consider using `$(pwd)/filename.py`."
                )

            directory = str(Path(filepath).parent)

            print("Waiting for debugger to attach")
            start_debugger(host="localhost", port=5678, wait_to_connect=True)

            import_codetocad_file(filepath, directory, directory)

            break


blenderLoadPostHandler: list = bpy.app.handlers.load_post  # type: ignore


def check_version():
    from providers.blender.blender_provider.blender_actions.context import (
        get_blender_version,
    )

    from providers.blender.blender_provider.blender_definitions import BlenderVersions

    if (
        get_blender_version()
        and get_blender_version() < BlenderVersions.TWO_DOT_EIGHTY.value
    ):
        print(
            f"WARNING: CodeToCAD only supports Blender versions {BlenderVersions.THREE_DOT_ONE.version} and above. You are running version {'.'.join(get_blender_version())}"
        )


@bpy.app.handlers.persistent  # type: ignore
def register_blender_provider(*args):
    from providers.blender.blender_provider.register import register

    print("Registering BlenderAddon as codetocad.factory provider.")
    register()


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
    bpy.utils.register_class(ReloadCodeToCADModules)
    bpy.utils.register_class(StartDebugger)

    add_codetocad_to_path()

    blenderLoadPostHandler.append(register_blender_provider)

    blenderLoadPostHandler.append(add_codetocad_to_blender_console)

    blenderLoadPostHandler.append(run_from_commandline_arguments)


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
    bpy.utils.unregister_class(ReloadCodeToCADModules)
    bpy.utils.unregister_class(StartDebugger)

    console_python.replace_help = replace_help

    blenderLoadPostHandler.remove(run_from_commandline_arguments)


if __name__ == "__main__":
    register()
