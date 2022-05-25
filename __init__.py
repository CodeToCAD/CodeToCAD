import os

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

try:
    import bpy

    def register():
        print ("Registering ", __name__)

    def unregister():
        print ("Unregistering ", __name__)

    if __name__ == "__main__":
        register()
except:
    print("Not running inside blender.")