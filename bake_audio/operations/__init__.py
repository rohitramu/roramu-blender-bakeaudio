from . import (
    TOOL_OT_bakeaudio_changedatavisibility,
    TOOL_OT_bakeaudio_cleardata,
    TOOL_OT_bakeaudio_cleardata_uiconfirm,
    TOOL_OT_bakeaudio_fileselect, TOOL_OT_bakeaudio,
)

__modules = [
    TOOL_OT_bakeaudio_changedatavisibility,
    TOOL_OT_bakeaudio_cleardata,
    TOOL_OT_bakeaudio_cleardata_uiconfirm,
    TOOL_OT_bakeaudio_fileselect,
    TOOL_OT_bakeaudio,
]


def register():
    for module in __modules:
        module.register()


def unregister():
    for module in reversed(__modules):
        module.unregister()
