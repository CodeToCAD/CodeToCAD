import bpy
import providers.blender.blender_provider.blender_definitions as blender_definitions


def render_image(output_filepath: str, overwrite: bool):
    bpy.context.scene.render.use_overwrite = overwrite
    bpy.context.scene.render.filepath = output_filepath
    bpy.ops.render.render(write_still=True)


def render_animation(output_filepath: str, overwrite: bool):
    bpy.context.scene.render.use_overwrite = overwrite
    bpy.context.scene.render.filepath = output_filepath
    bpy.ops.render.render(animation=True)


def set_render_frame_rate(rate: int):
    bpy.context.scene.render.fps = rate


def set_render_quality(percentage: int):
    bpy.context.scene.render.image_settings.quality = percentage


def set_render_file_format(format: blender_definitions.FileFormat):
    bpy.context.scene.render.image_settings.file_format = format.name


def set_render_engine(engine: blender_definitions.RenderEngines):
    bpy.context.scene.render.engine = engine.name


def set_render_resolution(x: int, y: int):
    bpy.context.scene.render.resolution_x = x
    bpy.context.scene.render.resolution_y = y
