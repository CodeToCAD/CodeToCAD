import os
import pkgutil
import runpy
import sys
import tempfile
import time
import traceback

try:
    import bpy
except ImportError:
    pass


import click
from codetocad.integrations.blender.adapter.console import write_to_console
from codetocad.integrations.blender.adapter.context import (
    get_context_view_3d,
    select_object,
    zoom_to_selected_objects,
)
from codetocad.cli.launcher_args import LauncherArgs


class ImportedFileWatcher:
    filepath: str
    lastTimestamp: float = 0
    _isWatching = True
    is_ask_before_reloading = False

    def __init__(self, path: str, is_ask_before_reloading: bool) -> None:
        self.filepath = path
        self.is_ask_before_reloading = is_ask_before_reloading

    def check_file_changed(self) -> bool:
        stamp: float = os.stat(self.filepath).st_mtime

        if stamp != self.lastTimestamp and self.lastTimestamp != 0:
            self.lastTimestamp = stamp
            return True
        self.lastTimestamp = stamp
        return False

    def reload_file(self, context):
        bpy.ops.wm.revert_mainfile()

        import_codetocad_file(file_path=self.filepath, blender_file_save_path=None)

    def stop_watching_file(self):
        self._isWatching = False
        try:
            bpy.app.timers.unregister(self.watch_file)
        except:
            pass

    def register_file_watcher(self):
        bpy.app.timers.register(self.watch_file, persistent=True)

    def watch_file(self) -> int | None:
        if not self._isWatching:
            print("Import auto-reload: stopping imported-file modify check timer.")
            return None
        if self.check_file_changed():
            print("Import auto-reload: file has changed.")
            if self.is_ask_before_reloading:
                click.confirm("File has changed, reload?")

            self.reload_file(bpy.context)
        # number of seconds before re-checking (courtesy of bpy.app.timers)
        return 5


imported_file_watcher: ImportedFileWatcher | None = None


def run_commandline_arguments():
    launcher_args = LauncherArgs.from_subprocess_args()

    if launcher_args.debug:
        from codetocad.integrations.blender.adapter.console import start_debugger

        start_debugger(wait_to_connect=True)


def import_codetocad_file(file_path: str, blender_file_save_path: str | None = None):

    if blender_file_save_path is None:
        blender_file_save_path = bpy.data.filepath or os.path.join(
            tempfile.gettempdir(), str(int(time.time())) + ".blend"
        )

    bpy.ops.wm.save_as_mainfile(filepath=blender_file_save_path)

    # Add the directory to python execute path, so that imports work.
    # if there are submodules for the script being imported, the user will have to use:
    from pathlib import Path

    script_directory = f"{Path(file_path).parent.absolute()}"
    sys.path.append(script_directory)

    print("Running script", file_path)

    with get_context_view_3d():
        global imported_file_watcher
        if not imported_file_watcher or imported_file_watcher.filepath != file_path:
            if imported_file_watcher:
                imported_file_watcher.stop_watching_file()
            imported_file_watcher = ImportedFileWatcher(
                file_path, is_ask_before_reloading=False
            )

        imported_file_watcher.watch_file()
        imported_file_watcher.register_file_watcher()

        try:
            runpy.run_path(file_path, run_name="__main__")
        except Exception as err:
            errorTrace = traceback.format_exc()
            print("Import failed: ", err, errorTrace)
            write_to_console(f"Import failed: {err}\n{errorTrace}", "ERROR")

            raise err
        finally:

            if len(bpy.data.objects) > 0:
                objectToZoomOn = bpy.data.objects[-1]
                objectToZoomOn = (
                    objectToZoomOn.parent
                    if objectToZoomOn.parent is not None
                    else objectToZoomOn
                )
                select_object(objectToZoomOn)
                zoom_to_selected_objects()

            # Cleanup:
            sys.path.remove(script_directory)
            for _, package_name, _ in pkgutil.iter_modules([script_directory]):
                if package_name in sys.modules:
                    del sys.modules[package_name]
