import bpy

from . import prop_utils


class BakeAudioPropertyGroup_FrequencyData_Band(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(
        name="Name",
        get=prop_utils.property_getter('name'),
        set=prop_utils.property_setter_fake(),
    )

    index: bpy.props.IntProperty(
        name="Band index",
        get=prop_utils.property_getter('index'),
        set=prop_utils.property_setter_fake(),
    )

    frequency_band_min: bpy.props.FloatProperty(
        name="Minimum frequency",
        get=prop_utils.property_getter('frequency_band_min'),
        set=prop_utils.property_setter_fake(),
    )

    frequency_band_max: bpy.props.FloatProperty(
        name="Maximum frequency",
        get=prop_utils.property_getter('frequency_band_max'),
        set=prop_utils.property_setter_fake(),
    )

    value: bpy.props.FloatProperty(
        name="Value",
        get=prop_utils.property_getter('value'),
        set=prop_utils.property_setter_fake(),
    )


def register():
    bpy.utils.register_class(BakeAudioPropertyGroup_FrequencyData_Band)


def unregister():
    bpy.utils.unregister_class(BakeAudioPropertyGroup_FrequencyData_Band)
