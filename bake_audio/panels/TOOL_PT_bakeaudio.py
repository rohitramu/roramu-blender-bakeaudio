import bpy

from ..operations.TOOL_OT_bakeaudio_fileselect import *
from ..operations.TOOL_OT_bakeaudio import *


class TOOL_PT_bakeaudio(bpy.types.Panel):
    '''
    Bakes an audio file into f-curves.
    '''
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context_mode = 'OBJECT'
    bl_context = 'scene'
    bl_label = "Bake Audio"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        scene = context.scene
        options = scene.bakeaudio.options

        col = self.layout.column()
        row = col.row(align=True)
        row.use_property_split = True
        row.use_property_decorate = False
        row.prop(options, 'filepath')
        row.operator(
            TOOL_OT_bakeaudio_fileselect.bl_idname,
            text="",
            icon="FILEBROWSER"
        )

        col = self.layout.column()
        col.use_property_split = True
        col.use_property_decorate = False
        col.prop(options, 'num_frequency_bands')

        row = col.row(align=True)
        row.use_property_split = True
        row.use_property_decorate = False
        row.prop(options, 'min_frequency', text="Frequency Range (Hz)")
        row.prop(options, 'max_frequency', text="")

        col.prop(options, 'attack_time')
        col.prop(options, 'release_time')
        col.prop(options, 'threshold')
        col.prop(options, 'fcurve_group_name')
        col.prop(options, 'frame_start')
        col.prop(options, 'update_preview_range')
        col.prop(options, 'insert_audio_strip')

        col.separator()

        row = col.row().box()
        row.operator(
            TOOL_OT_bakeaudio.bl_idname,
            text="Bake audio data",
            icon="SOUND",
        )


def register():
    bpy.utils.register_class(TOOL_PT_bakeaudio)


def unregister():
    bpy.utils.unregister_class(TOOL_PT_bakeaudio)
