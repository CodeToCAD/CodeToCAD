import os

bl_info = {
    "name": "TextToBlender",
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
    from bpy.props import StringProperty, BoolProperty
    from bpy_extras.io_utils import ImportHelper
    from bpy.types import Operator,Panel

    class TextToBlender_PT_main_panel(Panel):
        bl_label = "TextToBlender"
        bl_idname = "TEXTTOBLENDER_PT_main_panel"
        bl_space_type = "VIEW_3D"
        bl_region_type = "UI"
        bl_category = "TextToBlender"
        bl_context = "objectmode"

        def draw(self, context):
            layout = self.layout

            row = layout.row()
            row.label(text="Import TextToBlender file", icon="FILE_NEW")
            row = layout.row()
            row.operator(TextToBlender_OT_file_browser.bl_idname, text="Choose file")

    class TextToBlender_OT_file_browser(Operator, ImportHelper):

        bl_idname = "texttoblender.file_browser"
        bl_label = "Open the file browser"
        
        filter_glob: StringProperty(
            default='*.py;*.txt;*.texttoblender',
            options={'HIDDEN'}
        )
        
        stopOnErrorFlag: BoolProperty(
            name='Stop on error',
            description='Stop running after encountering an error',
            default=True,
        )

        def execute(self, context):

            filename, extension = os.path.splitext(self.filepath)
            
            print('Selected file:', self.filepath)
            print('File name:', filename)
            print('File extension:', extension)
            print('Some Boolean:', self.stopOnErrorFlag)

            # exec(open(self.filepath).read())
            file = bpy.data.texts.load(self.filepath)
            ctx = bpy.context.copy()
            ctx['edit_text'] = file
            bpy.ops.text.run_script(ctx)
            
            return {'FINISHED'}


    def register():
        print ("Registering ", __name__)
        bpy.utils.register_class(TextToBlender_PT_main_panel)
        bpy.utils.register_class(TextToBlender_OT_file_browser)

    def unregister():
        print ("Unregistering ", __name__)
        bpy.utils.unregister_class(TextToBlender_PT_main_panel)
        bpy.utils.unregister_class(TextToBlender_OT_file_browser)

    if __name__ == "__main__":
        register()
except:
    print("Not running inside blender.")