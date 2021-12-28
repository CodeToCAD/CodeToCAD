import bpy
from pathlib import Path
import zipfile

addonName = "TextToBlender"

path = Path(__file__).parent.absolute()
zipfileName = addonName + ".zip"

with zipfile.ZipFile(zipfileName, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for entry in path.rglob("*"):
            if not entry.match(zipfileName):
                zip_file.write(entry, addonName + "/"+entry.name )

            
zipfilePath = str(path / zipfileName).replace('\\', '/')
            
bpy.ops.preferences.addon_install(filepath=zipfilePath)
bpy.ops.preferences.addon_enable(module='TextToBlender')
bpy.ops.wm.save_userpref()