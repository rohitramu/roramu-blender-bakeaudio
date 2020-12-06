import bpy


class TOOL_OT_bakeaudio_changedatavisibility(bpy.types.Operator):
    '''
    Shows, hides or toggles the selected group's data in the UI.
    '''
    bl_idname = 'roramu.operator_bakeaudio_changedatavisibility'
    bl_label = 'Show/Hide Data'
    bl_category = 'Tool'
    bl_options = {'REGISTER'}

    group_name: bpy.props.StringProperty(
        name="Group name",
        description="The name of the frequency band group to show/hide/toggle, or empty string to show/hide/toggle the visibility of all groups' data.",
        default='',
    )

    operation: bpy.props.EnumProperty(
        name="Visibility Operation",
        description="Describes how to change the visibility of groups' data.",
        default=0,
        items=[
            ("HIDE", "Hide", "Hides groups' data.", 0),
            ("SHOW", "Show", "Shows groups' data.", 1),
            ("TOGGLE", "Toggle", "Toggles the visibility groups' data.", 2),
        ]
    )

    def execute(self, context):
        data = context.scene.bakeaudio.data

        if not self.operation:
            self.report({'ERROR'}, 'Visibility option not provided')
            return {'CANCELLED'}

        if self.group_name:
            # A group was specified, so change its visibility
            self.__single_group(data[self.group_name])
        else:
            # Group name was not provided, so change visibility of all groups
            self.__all_groups(data)

        return {'FINISHED'}

    def __all_groups(self, data):
        # Enumerate all groups
        for group in data.values():
            self.__single_group(group)

    def __single_group(self, group):
        def show(g): g.show_in_ui = True
        def hide(g): g.show_in_ui = False
        def toggle(g): g.show_in_ui = not g.show_in_ui
        switcher = {
            "SHOW": show,
            "HIDE": hide,
            "TOGGLE": toggle,
        }
        switcher[self.operation](group)


def register():
    bpy.utils.register_class(TOOL_OT_bakeaudio_changedatavisibility)


def unregister():
    bpy.utils.unregister_class(TOOL_OT_bakeaudio_changedatavisibility)
