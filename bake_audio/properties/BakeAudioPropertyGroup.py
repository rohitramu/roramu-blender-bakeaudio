import bpy

from .BakeAudioPropertyGroup_Options import *
from .BakeAudioPropertyGroup_FrequencyData import *


class BakeAudioPropertyGroup(bpy.types.PropertyGroup):
    options: bpy.props.PointerProperty(
        name='Bake Audio Options',
        type=BakeAudioPropertyGroup_Options,
    )

    data: bpy.props.CollectionProperty(
        name='Bake Audio Data',
        type=BakeAudioPropertyGroup_FrequencyData,
    )


def register():
    bpy.utils.register_class(BakeAudioPropertyGroup)

    bpy.types.Scene.bakeaudio = bpy.props.PointerProperty(
        name="Bake Audio",
        type=BakeAudioPropertyGroup,
    )


def unregister():
    bpy.utils.unregister_class(BakeAudioPropertyGroup)

    del bpy.types.Scene.bakeaudio
