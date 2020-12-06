import bpy


class TOOL_OT_bakeaudio_fileselect(bpy.types.Operator):
    '''
    Selects a file and puts it in the bakeaudio_options attribute on the currently active object.
    '''
    bl_idname = 'roramu.operator_bakeaudio_fileselect'
    bl_label = 'Select Audio File'
    bl_category = 'Tool'
    bl_options = {'INTERNAL'}

    filepath: bpy.props.StringProperty(
        name="Audio filepath",
        subtype='FILE_PATH',
    )

    filename: bpy.props.StringProperty(
        name="Audio filename",
        subtype="FILE_NAME",
    )

    # filter_glob: bpy.props.StringProperty(default="*", options={'HIDDEN'})
    filter_blender: bpy.props.BoolProperty(
        default=False, options={'HIDDEN'})
    filter_backup: bpy.props.BoolProperty(
        default=False, options={'HIDDEN'})
    filter_image: bpy.props.BoolProperty(default=False, options={'HIDDEN'})
    filter_movie: bpy.props.BoolProperty(default=True, options={'HIDDEN'})
    filter_python: bpy.props.BoolProperty(
        default=False, options={'HIDDEN'})
    filter_font: bpy.props.BoolProperty(default=False, options={'HIDDEN'})
    filter_sound: bpy.props.BoolProperty(default=True, options={'HIDDEN'})
    filter_text: bpy.props.BoolProperty(default=False, options={'HIDDEN'})
    filter_archive: bpy.props.BoolProperty(
        default=False, options={'HIDDEN'})
    filter_btx: bpy.props.BoolProperty(default=False, options={'HIDDEN'})
    filter_collada: bpy.props.BoolProperty(
        default=False, options={'HIDDEN'})
    filter_alembic: bpy.props.BoolProperty(
        default=False, options={'HIDDEN'})
    filter_usd: bpy.props.BoolProperty(default=False, options={'HIDDEN'})
    filter_volume: bpy.props.BoolProperty(
        default=False, options={'HIDDEN'})
    filter_folder: bpy.props.BoolProperty(default=True, options={'HIDDEN'})
    filter_blenlib: bpy.props.BoolProperty(
        default=False, options={'HIDDEN'})
    filemode: bpy.props.IntProperty(default=9, options={'HIDDEN'})
    show_multiview: bpy.props.BoolProperty(
        default=False, options={'HIDDEN'})
    use_multiview: bpy.props.BoolProperty(
        default=False, options={'HIDDEN'})
    display_type: bpy.props.StringProperty(
        default='DEFAULT', options={'HIDDEN'})
    # sort_method: bpy.props.StringProperty(default='FILE_SORT_ALPHA')

    def execute(self, context):
        scene = context.scene
        options = scene.bakeaudio.options

        options.filepath = self.filepath  # bpy.path.abspath(self.filepath)
        options.fcurve_group_name = self.filename

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)

        return {'RUNNING_MODAL'}


def register():
    bpy.utils.register_class(TOOL_OT_bakeaudio_fileselect)


def unregister():
    bpy.utils.unregister_class(TOOL_OT_bakeaudio_fileselect)
