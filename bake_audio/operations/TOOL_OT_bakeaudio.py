import bpy
import time
import math

from .. import properties


class TOOL_OT_bakeaudio(bpy.types.Operator):
    '''
    Bakes an audio file into f-curves.
    '''
    bl_idname = 'roramu.operator_bakeaudio'
    bl_label = 'Bake Audio'
    bl_category = 'Tool'
    bl_options = {'REGISTER'}

    __log_base = math.e
    __action_name = 'Bake Audio'

    filepath: str
    num_frequency_bands: int
    min_frequency: float
    max_frequency: float
    attack_time: float
    release_time: float
    threshold: float
    fcurve_group_name: str
    frame_start: int
    update_preview_range: bool
    insert_audio_strip: bool

    def execute(self, context):
        scene = context.scene
        options = scene.bakeaudio.options

        if not options.filepath:
            self.report({'ERROR'}, 'Filepath was not specified')
            return {'CANCELLED'}

        self.filepath = options.filepath
        self.num_frequency_bands = options.num_frequency_bands
        self.min_frequency = options.min_frequency
        self.max_frequency = options.max_frequency
        self.attack_time = options.attack_time
        self.release_time = options.release_time
        self.threshold = options.threshold
        self.fcurve_group_name = options.fcurve_group_name
        self.frame_start = options.frame_start
        self.update_preview_range = options.update_preview_range
        self.insert_audio_strip = options.insert_audio_strip

        # We will need to temporarily change some context properties - remember them so we can revert back later
        old_area_type = context.area.type
        old_frame = context.scene.frame_current
        old_frame_start = context.scene.frame_start
        old_frame_end = context.scene.frame_end

        try:
            context.area.type = 'GRAPH_EDITOR'

            # Sanitize values
            self.min_frequency = max(0, self.min_frequency)
            self.max_frequency = max(1, self.max_frequency)
            if self.min_frequency >= self.max_frequency:
                self.report(
                    {'ERROR'},
                    f'The provided minimum frequency ({self.min_frequency}) should be less than the provided maximum frequency ({self.max_frequency})',
                )
                return {'CANCELLED'}

            # Bake each frequency range into an F-Curve
            self.__generate_audio_data(context)
        except Exception as e:
            context.scene.frame_start = old_frame_start
            context.scene.frame_end = old_frame_end

            self.report({'ERROR'}, f'Unexpected error: {e}')
            return {'CANCELLED'}
        finally:
            context.area.type = old_area_type
            context.scene.frame_set(old_frame)

        return {'FINISHED'}

    def __generate_audio_data(self, context):
        scene = context.scene

        frequency_ranges = self.__get_frequency_ranges()

        # Create the action that will be used to store the data
        if not hasattr(scene.animation_data, 'action'):
            scene.animation_data_create()

        if not hasattr(scene.animation_data.action, 'fcurves'):
            scene.animation_data.action = bpy.data.actions.new(
                self.__action_name)

        # Delete the old groups with the same name, and their associated f-curve data
        bpy.ops.roramu.operator_bakeaudio_cleardata(
            group_name=self.fcurve_group_name
        )

        # Create a group to hold the new data
        data_group = self.__create_data_group(scene, frequency_ranges)

        # Generate audio data
        self.__bake_audio_data_to_fcurves(
            scene,
            data_group,
            frequency_ranges
        )

        # Do any necessary post processing on the fcurves
        self.__post_process_fcurves(scene, data_group)

        # Insert the file as an audio strip into the video sequencer
        if self.insert_audio_strip:
            if not scene.sequence_editor:
                scene.sequence_editor_create()

            sequences = scene.sequence_editor.sequences

            if len(sequences) >= 32:
                self.report(
                    {'WARNING'},
                    f'Failed to add audio file to sequencer because the maximum number of channels (32) are being used: {data_group.filepath}',
                )
            else:
                sequences.new_sound(
                    name=data_group.name,
                    filepath=data_group.filepath,
                    channel=len(sequences) + 1,  # add to the end
                    frame_start=data_group.frame_start,
                )

    def __get_frequency_ranges(self):
        # Get the minimum log value
        min_log = 0
        if (self.min_frequency > 1):
            min_log = math.log(
                self.min_frequency,
                TOOL_OT_bakeaudio.__log_base
            )

        # Get the maximum log value
        max_log = math.log(self.max_frequency, TOOL_OT_bakeaudio.__log_base)

        # Evenly divide the range of frequencies
        log_step_size = (max_log - min_log)/self.num_frequency_bands
        frequency_ranges = [
            (
                # Divide the log range evenly, and then convert back to frequencies
                math.pow(
                    TOOL_OT_bakeaudio.__log_base,
                    min_log + i * log_step_size
                ),
                math.pow(
                    TOOL_OT_bakeaudio.__log_base,
                    min_log + (i + 1) * log_step_size
                ),
            )
            for i in range(self.num_frequency_bands)
        ]

        # Add the full frequency range as a band as well
        if len(frequency_ranges) > 1:
            frequency_ranges.insert(
                0,
                (self.min_frequency, self.max_frequency)
            )

        return frequency_ranges

    def __create_data_group(self, scene, frequency_ranges):
        data_group = scene.bakeaudio.data.add()
        data_group.show_in_ui = True
        properties.prop_utils.property_setter(data_group, 'name')(
            self.fcurve_group_name
        )
        properties.prop_utils.property_setter(data_group, 'filepath')(
            self.filepath
        )
        properties.prop_utils.property_setter(data_group, 'generated_timestamp')(
            time.time()
        )
        properties.prop_utils.property_setter(data_group, 'num_bands')(
            self.num_frequency_bands
        )
        properties.prop_utils.property_setter(data_group, 'min_frequency')(
            frequency_ranges[0][0]
        )
        properties.prop_utils.property_setter(data_group, 'max_frequency')(
            frequency_ranges[0][1]
        )
        properties.prop_utils.property_setter(data_group, 'attack_time')(
            self.attack_time
        )
        properties.prop_utils.property_setter(data_group, 'release_time')(
            self.release_time
        )
        properties.prop_utils.property_setter(data_group, 'threshold')(
            self.threshold
        )

        return data_group

    def __bake_audio_data_to_fcurves(self, scene, data_group, frequency_ranges):
        i_str_width = len(str(len(frequency_ranges)))
        for (i, (range_min_frequency, range_max_frequency)) in enumerate(frequency_ranges, start=0):
            # Clear F-Curve selection so data doesn't get overwritten
            if scene.animation_data:
                for fcurve in scene.animation_data.action.fcurves:
                    fcurve.select = False

            # Create the object which will hold the data
            frequency_band_data = data_group.bands.add()
            properties.prop_utils.property_setter(frequency_band_data, 'name')(
                f'[{str(i).rjust(i_str_width, "0")}] {int(range_min_frequency)}Hz to {int(range_max_frequency)}Hz'
            )
            properties.prop_utils.property_setter(frequency_band_data, 'index')(
                i
            )
            properties.prop_utils.property_setter(frequency_band_data, 'frequency_band_min')(
                range_min_frequency
            )
            properties.prop_utils.property_setter(frequency_band_data, 'frequency_band_max')(
                range_max_frequency
            )
            properties.prop_utils.property_setter(frequency_band_data, 'value')(
                0.0
            )

            # Insert a keyframe to generate an F-Curve for the property
            scene.frame_set(self.frame_start)
            frequency_band_data.keyframe_insert(
                f'["value"]',
                frame=self.frame_start,
                group=self.fcurve_group_name)

            # Bake the sound into the new property
            # If this fails due to sound_bake.poll() failing, see the poll() source code here: https://github.com/blender/blender/blob/2d1cce8331f3ecdfb8cb0c651e111ffac5dc7153/source/blender/editors/space_graph/graph_utils.c#L292
            # The sound_bake operation source code is here: https://github.com/blender/blender/blob/600a627f6e326f4542a876e6e82f771cd3da218f/source/blender/editors/space_graph/graph_edit.c#L1845
            bpy.ops.graph.sound_bake(
                filepath=self.filepath,
                low=range_min_frequency,
                high=range_max_frequency,
                attack=data_group.attack_time,
                release=data_group.release_time,
                threshold=data_group.threshold,
            )

    def __post_process_fcurves(self, scene, data_group):
        frame_start_current = self.frame_start
        frame_end_current = 0

        for fcurve in scene.animation_data.action.fcurves:
            if fcurve.group.name == data_group.name:
                # Get the keyframe range for this fcurve
                (frame_start, frame_end) = fcurve.range()

                # Convert all sampled points to keyframes
                fcurve.convert_to_keyframes(
                    frame_start,
                    frame_end)

                # Deselect the fcurve so that it doesn't get overwritten by the next run
                fcurve.select = False

                # Calculate the overall start and end frames for the whole data group (i.e. across all fcurves)
                start = min(frame_start, frame_start_current)
                end = max(frame_end, frame_end_current)

                # Set the start and end frame properties for the data group
                properties.prop_utils.property_setter(data_group, 'frame_start')(
                    start
                )
                properties.prop_utils.property_setter(data_group, 'frame_end')(
                    end
                )

                # Update the scene's start and end frames
                if self.update_preview_range:
                    scene.frame_start = start
                    # scene.frame_preview_start = start

                    scene.frame_end = end
                    # scene.frame_preview_end = end


def register():
    bpy.utils.register_class(TOOL_OT_bakeaudio)


def unregister():
    bpy.utils.unregister_class(TOOL_OT_bakeaudio)
