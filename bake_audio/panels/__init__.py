from . import (
    TOOL_PT_bakeaudio,
    TOOL_PT_bakeaudio_groups,
)

__modules = [
    TOOL_PT_bakeaudio,
    TOOL_PT_bakeaudio_groups,
]


def register():
    for module in __modules:
        module.register()


def unregister():
    for module in reversed(__modules):
        module.unregister()
