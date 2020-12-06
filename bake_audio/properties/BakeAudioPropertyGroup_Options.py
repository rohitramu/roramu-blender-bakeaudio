import bpy


class BakeAudioPropertyGroup_Options(bpy.types.PropertyGroup):
    filepath: bpy.props.StringProperty(
        name="Audio filepath",
        description="The path to the audio file which should be analyzed.",
    )

    num_frequency_bands: bpy.props.IntProperty(
        name="Number of frequency bands",
        description="The number of frequency bands in the resulting data set.",
        default=10,
        min=1,
        max=100,
    )

    min_frequency: bpy.props.FloatProperty(
        name="Minimum frequency (Hz)",
        description="The minimum frequency to analyze when generating a data set.",
        default=20,
        min=0,
    )

    max_frequency: bpy.props.FloatProperty(
        name="Maximum frequency (Hz)",
        description="The maximum frequency to analyze when generating a data set.",
        default=22000,
        min=1,
    )

    attack_time: bpy.props.FloatProperty(
        name="Attack response time (ms)",
        default=0.01,
        min=0.0,
        max=2,
    )

    release_time: bpy.props.FloatProperty(
        name="Release response time (ms)",
        default=0.2,
        min=0,
        max=5,
    )

    threshold: bpy.props.FloatProperty(
        name="Minimum value threshold",
        description="The minimum value which generates a change in the data.",
        default=0,
        min=0,
        max=1,
    )

    fcurve_group_name: bpy.props.StringProperty(
        name="F-Curve group name",
        description="A user-friendly display name for the resulting data set.",
        default="Audio",
    )

    frame_start: bpy.props.IntProperty(
        name="Start frame",
        description="The first frame which will hold audio data.  The end frame will depend on the duration of the audio file.",
        default=0,
        min=0,
    )

    update_preview_range: bpy.props.BoolProperty(
        name="Update preview range",
        description="If set to True, the 'Bake Audio' operation will update the scene's preview range to match the start and end frame of the generated audio data.",
        default=True,
    )

    insert_audio_strip: bpy.props.BoolProperty(
        name="Insert audio strip",
        description="If set to True, the 'Bake Audio' operation will import the audio file into the Video Sequencer as an audio strip.",
        default=True,
    )


def register():
    bpy.utils.register_class(BakeAudioPropertyGroup_Options)


def unregister():
    bpy.utils.unregister_class(BakeAudioPropertyGroup_Options)
