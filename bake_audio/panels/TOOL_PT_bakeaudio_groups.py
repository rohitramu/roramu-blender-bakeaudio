import bpy
import time

from .TOOL_PT_bakeaudio import *

from ..operations.TOOL_OT_bakeaudio_cleardata import *
from ..operations.TOOL_OT_bakeaudio_cleardata_uiconfirm import *
from ..operations.TOOL_OT_bakeaudio_changedatavisibility import *


class TOOL_PT_bakeaudio_groups(bpy.types.Panel):
    '''
    Displays the properties of the fcurve groups which were generated from audio files.
    '''
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    # bl_context_mode = 'OBJECT'
    # bl_context = 'scene'
    bl_label = "Audio Data (Read-Only)"
    bl_parent_id = TOOL_PT_bakeaudio.__name__

    def draw(self, context):
        data = context.scene.bakeaudio.data

        if not data:
            row = self.layout.box().row()
            row.separator()
            row.alignment = 'CENTER'
            row.label(text='No audio data.')
            return

        col = self.layout.column()

        del_box = col.box()
        del_box.operator(
            TOOL_OT_bakeaudio_cleardata_uiconfirm.bl_idname,
            icon="TRASH",
        )

        col.separator()

        ops_row = col.row(align=True)
        op = ops_row.operator(
            TOOL_OT_bakeaudio_changedatavisibility.bl_idname,
            text='Show all data'
        )
        op.operation = "SHOW"
        op = ops_row.operator(
            TOOL_OT_bakeaudio_changedatavisibility.bl_idname,
            text='Hide all data'
        )
        op.operation = "HIDE"
        op = ops_row.operator(
            TOOL_OT_bakeaudio_changedatavisibility.bl_idname,
            text='Toggle visibility of data'
        )
        op.operation = "TOGGLE"

        for (_, group) in data.items():
            self.draw_group_info(context, self.layout, group)

    def draw_group_info(self, context, layout, group):
        top_col = layout.column(align=True)
        top_col.use_property_split = True
        top_col.use_property_decorate = False

        # Header for the group
        header_row = top_col.box().row()
        header_row.label(
            text=f'{group.name}'
        )
        header_row.label(
            text=f'{time.ctime(group.generated_timestamp)}'
        )
        cell = header_row.column()
        cell.alignment = "RIGHT"
        op = cell.operator(
            TOOL_OT_bakeaudio_cleardata.bl_idname,
            text='',
            icon='TRASH',
        )
        op.group_name = group.name

        # Group info
        group_info_col = top_col.box().column()
        group_info_col.use_property_split = True
        group_info_col.use_property_decorate = False
        group_info_col.prop(group, 'name')
        group_info_col.prop(group, 'filepath')
        group_info_col.prop(group, 'num_bands')

        row = group_info_col.row(align=True)
        row.prop(group, 'min_frequency', text='Frequency range')
        row.prop(group, 'max_frequency', text='')

        group_info_col.prop(group, 'attack_time')
        group_info_col.prop(group, 'release_time')
        group_info_col.prop(group, 'threshold')

        row = group_info_col.row(align=True)
        row.prop(group, 'frame_start', text='Start/end frames')
        row.prop(group, 'frame_end', text='')

        row = group_info_col.row()
        row.use_property_split = False
        row.use_property_decorate = False
        row.alignment = "LEFT"
        row.prop(
            group,
            'show_in_ui',
            text='',
            icon='DISCLOSURE_TRI_DOWN' if group.show_in_ui else 'DISCLOSURE_TRI_RIGHT',
            toggle=1,
        )

        # Inner layout for each data point
        if not group.show_in_ui:
            return

        if not group.bands:
            box = top_col.box()
            box.alignment = 'CENTER'
            box.label(text='No frequency data for this group.')
            return

        self.draw_group_data1(context, top_col.box(), group)

    def draw_group_data1(self, context, layout, group):
        layout = layout.column(align=True)

        data_table = layout.row(align=True)

        index_col = data_table.column(align=True)
        frequency_col = data_table.column(align=True)
        value_col = data_table.column(align=True)

        cell = index_col.box().column()
        cell.alignment = 'CENTER'
        row = cell.row(align=True)
        row.alignment = 'CENTER'
        row.label(text='Band #')

        cell = frequency_col.box().column()
        cell.alignment = 'CENTER'
        row = cell.row(align=True)
        row.alignment = 'CENTER'
        row.label(text='Frequency range (Hz)')

        cell = value_col.box().column()
        cell.alignment = 'CENTER'
        row = cell.row(align=True)
        row.alignment = 'CENTER'
        row.label(text=f'Value')
        row.label(text='@ frame')
        row.prop(context.scene, 'frame_current', text='')

        index_col.separator(factor=0.2)
        frequency_col.separator(factor=0.2)
        value_col.separator(factor=0.2)

        for frequency_band in group.bands:
            cell = index_col.box()
            row = cell.row(align=True)
            row.alignment = 'CENTER'
            row.emboss = 'NONE'
            row.prop(frequency_band, 'index', text='')

            cell = frequency_col.box().row()
            cell.alignment = 'CENTER'
            row = cell.row(align=True)
            row.alignment = 'CENTER'
            row.emboss = 'NONE'
            row.prop(frequency_band, 'frequency_band_min', text='')
            row.prop(frequency_band, 'frequency_band_max', text='')

            cell = value_col.box()
            row = cell.row(align=True)
            row.alignment = 'EXPAND'
            # row.emboss = 'NONE'
            row.prop(frequency_band, 'value', text='')

    def draw_group_data2(self, context, layout, group):
        layout = layout.column(align=True)

        # Header row for the table
        header_row = layout.row(align=True)
        cell = header_row.box()
        row = cell.row()
        row.alignment = 'CENTER'
        row.label(text='Band #')
        cell.label(text='')

        cell = header_row.box()
        row = cell.row()
        row.alignment = 'CENTER'
        row.label(text='Frequency range (Hz)')
        row = cell.row(align=True)
        row.label(text='')
        row.label(text='')

        cell = header_row.box()
        row = cell.row()
        row.alignment = 'CENTER'
        row.label(text=f'Value @ frame {context.scene.frame_current}')
        cell.label(text='')

        data_table = layout.column(align=True)

        for frequency_band in group.bands:
            row = data_table.row(align=True)

            cell = row.box().row(align=True)
            cell.emboss = 'NONE'
            cell.prop(frequency_band, 'index', text='')

            cell = row.box().row(align=True)
            cell.emboss = 'NONE'
            cell.prop(frequency_band, 'frequency_band_min', text='')
            cell.prop(frequency_band, 'frequency_band_max', text='')

            cell = row.box().row(align=True)
            # cell.emboss = 'NONE'
            cell.prop(frequency_band, 'value', text='')


def register():
    bpy.utils.register_class(TOOL_PT_bakeaudio_groups)


def unregister():
    bpy.utils.unregister_class(TOOL_PT_bakeaudio_groups)
