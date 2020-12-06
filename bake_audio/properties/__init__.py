from . import (
    BakeAudioPropertyGroup_FrequencyData_Band,
    BakeAudioPropertyGroup_FrequencyData,
    BakeAudioPropertyGroup_Options,
    BakeAudioPropertyGroup,
    prop_utils,
)

__modules = [
    BakeAudioPropertyGroup_FrequencyData_Band,
    BakeAudioPropertyGroup_FrequencyData,
    BakeAudioPropertyGroup_Options,
    BakeAudioPropertyGroup,
]


def register():
    for module in __modules:
        module.register()


def unregister():
    for module in reversed(__modules):
        module.unregister()
