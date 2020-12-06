import bpy


class TOOL_OT_bakeaudio_cleardata_uiconfirm(bpy.types.Operator):
    '''
    Deletes all generated audio data for the active object, asking for a confirmation first from the user.
    '''
    bl_idname = 'roramu.operator_bakeaudio_cleardata_uiconfirm'
    bl_label = 'Delete All Audio Data'
    bl_category = 'Tool'
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return bpy.ops.roramu.operator_bakeaudio_cleardata.poll()

    def execute(self, context):
        return bpy.ops.roramu.operator_bakeaudio_cleardata(clear_all_confirm=True)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


def register():
    bpy.utils.register_class(TOOL_OT_bakeaudio_cleardata_uiconfirm)


def unregister():
    bpy.utils.unregister_class(TOOL_OT_bakeaudio_cleardata_uiconfirm)
