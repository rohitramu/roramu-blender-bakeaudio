import bpy

from . import prop_utils
from .BakeAudioPropertyGroup_FrequencyData_Band import *


class BakeAudioPropertyGroup_FrequencyData(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(
        name="Name",
        get=prop_utils.property_getter('name'),
        set=prop_utils.property_setter_fake(),
    )

    show_in_ui: bpy.props.BoolProperty(
        name="Show data",
        default=True,
    )

    filepath: bpy.props.StringProperty(
        name="Audio filepath",
        get=prop_utils.property_getter('filepath'),
        set=prop_utils.property_setter_fake(),
    )

    generated_timestamp: bpy.props.FloatProperty(
        name="Generated Time",
        description="The date and time when this data group was generated.",
        get=prop_utils.property_getter('generated_timestamp'),
        set=prop_utils.property_setter_fake(),
    )

    num_bands: bpy.props.IntProperty(
        name="Number of frequency bands",
        min=1,
        get=prop_utils.property_getter('num_bands'),
        set=prop_utils.property_setter_fake(),
    )

    min_frequency: bpy.props.FloatProperty(
        name="Minimum frequency (Hz)",
        min=0,
        get=prop_utils.property_getter('min_frequency'),
        set=prop_utils.property_setter_fake(),
    )

    max_frequency: bpy.props.FloatProperty(
        name="Maximum frequency (Hz)",
        min=0,
        get=prop_utils.property_getter('max_frequency'),
        set=prop_utils.property_setter_fake(),
    )

    attack_time: bpy.props.FloatProperty(
        name="Attack response time (ms)",
        default=0.01,
        min=0,
        max=2,
        get=prop_utils.property_getter('attack_time'),
        set=prop_utils.property_setter_fake(),
    )

    release_time: bpy.props.FloatProperty(
        name="Release response time (ms)",
        default=0.2,
        min=0,
        max=5,
        get=prop_utils.property_getter('release_time'),
        set=prop_utils.property_setter_fake(),
    )

    threshold: bpy.props.FloatProperty(
        name="Minimum value threshold",
        default=0,
        min=0,
        max=1,
        get=prop_utils.property_getter('threshold'),
        set=prop_utils.property_setter_fake(),
    )

    frame_start: bpy.props.IntProperty(
        name="Start frame",
        description="The first frame which holds audio data.",
        default=-1,
        min=0,
        get=prop_utils.property_getter('frame_start'),
        set=prop_utils.property_setter_fake(),
    )

    frame_end: bpy.props.IntProperty(
        name="End frame",
        description="The last frame which holds audio data.",
        default=-1,
        min=0,
        get=prop_utils.property_getter('frame_end'),
        set=prop_utils.property_setter_fake(),
    )

    bands: bpy.props.CollectionProperty(
        name="Frequency data",
        type=BakeAudioPropertyGroup_FrequencyData_Band,
    )


def register():
    bpy.utils.register_class(BakeAudioPropertyGroup_FrequencyData)


def unregister():
    bpy.utils.unregister_class(BakeAudioPropertyGroup_FrequencyData)
