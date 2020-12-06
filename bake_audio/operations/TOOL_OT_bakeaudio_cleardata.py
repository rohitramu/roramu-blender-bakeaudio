import bpy


class TOOL_OT_bakeaudio_cleardata(bpy.types.Operator):
    '''
    Deletes generated audio data for the active object.
    '''
    bl_idname = 'roramu.operator_bakeaudio_cleardata'
    bl_label = 'Delete Data'
    bl_category = 'Tool'
    bl_options = {'REGISTER'}

    group_name: bpy.props.StringProperty(
        name="Group name",
        description="The name of the frequency band group to delete, or empty string to delete all groups.",
        default='',
    )

    clear_all_confirm: bpy.props.BoolProperty(
        name="Confirm delete all data",
        description='If true, confirms that it is ok to delete all audio data on this object.  Otherwise, cancels the operation if no group name was provided.',

    )

    def execute(self, context):
        scene = context.scene
        data = scene.bakeaudio.data

        if self.group_name:
            # A group was specified, so delete it
            self.__delete_group(scene, data, self.group_name)
            return {'FINISHED'}
        else:
            # Before deleting all groups, check if confirmation was provided
            if not self.clear_all_confirm:
                self.report(
                    {'ERROR'},
                    f'Confirmation was not provided to delete all audio data.  Please set the "{self.clear_all_confirm.__name__}" parameter to True when calling this operation to confirm deletion of all audio data.',
                )
                return {'CANCELLED'}

            # Group name was not provided, so delete all groups
            self.report(
                {'WARNING'},
                f'Group name was not provided - deleting all audio data.',
            )

            self.__delete_all_groups(scene, data)

            return {'FINISHED'}

    def __delete_all_groups(self, scene, data):
        # Enumerate all groups
        for group_name in data.keys():
            self.__delete_group(scene, data, group_name)

    def __delete_group(self, scene, data, group_name):
        self.report({'WARNING'}, f'Deleting data for group: {group_name}')

        # Find any existing fcurves in the specified group so they can be deleted
        if hasattr(scene, "animation_data") and hasattr(scene.animation_data, "action") and hasattr(scene.animation_data.action, "fcurves"):
            fcurves = list(filter(
                lambda x: x.group.name == group_name,
                scene.animation_data.action.fcurves
            ))

            # Remove the fcurves
            for fcurve in fcurves:
                scene.animation_data.action.fcurves.remove(fcurve)

        # Remove any pre-existing data for the specified group
        to_delete_index = data.find(group_name)
        while to_delete_index >= 0:
            data.remove(to_delete_index)
            to_delete_index = data.find(group_name)


def register():
    bpy.utils.register_class(TOOL_OT_bakeaudio_cleardata)


def unregister():
    bpy.utils.unregister_class(TOOL_OT_bakeaudio_cleardata)
