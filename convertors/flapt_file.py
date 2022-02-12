from tkinter import filedialog
from typing import BinaryIO
import utilities


class FlaptFile:
    
    def __init__(self, fp: BinaryIO):
        self.mFP = fp


    def Convert(self, import_entries_offset: int, import_entries_count: int) -> None:
        # check version
        self.mFP.seek(0x0)
        version = utilities.UnpackBytes(self.mFP, "B")
        assert version == 12, "Bad FlaptFile version."

        # header
        self.mFP.seek(0x4)
        utilities.SwapBytes(self.mFP, "<L")
        utilities.SwapBytes(self.mFP, "<L")
        movie_clips_count = utilities.SwapBytes(self.mFP, "<L")
        movie_clips_offset = utilities.SwapBytes(self.mFP, "<L")
        utilities.SwapBytes(self.mFP, "<L")
        utilities.SwapBytes(self.mFP, "<L")
        vertices_count = utilities.SwapBytes(self.mFP, "<L")
        vertices_offset = utilities.SwapBytes(self.mFP, "<L")
        fonts_count = utilities.SwapBytes(self.mFP, "<L")
        fonts_offset = utilities.SwapBytes(self.mFP, "<L")
        components_count = utilities.SwapBytes(self.mFP, "<L")
        component_names_offset = utilities.SwapBytes(self.mFP, "<L")
        utilities.SwapBytes(self.mFP, "<L")
        trigger_parameters_count = utilities.SwapBytes(self.mFP, "<L")
        trigger_parameters_offset = utilities.SwapBytes(self.mFP, "<L")
        strings_count = utilities.SwapBytes(self.mFP, "<L")
        strings_offsets = utilities.SwapBytes(self.mFP, "<L")
        special_textures_count = utilities.SwapBytes(self.mFP, "<L")
        special_textures_offsets = utilities.SwapBytes(self.mFP, "<L")
        debug_strings_count = utilities.SwapBytes(self.mFP, "<L")
        debug_strings_offsets = utilities.SwapBytes(self.mFP, "<L")

        # movie clips
        for i in range(movie_clips_count):
            self.ConvertMovieClip(movie_clips_offset + i * 0x44)
        
        # vertices
        self.mFP.seek(vertices_offset)
        for _ in range(vertices_count):
            self.ConvertVertex()

        # fonts
        self.mFP.seek(fonts_offset)
        for _ in range(fonts_count):
            self.ConvertFont()

        # components
        self.mFP.seek(component_names_offset)
        for _ in range(components_count):
            self.ConvertHashedString()

        # trigger parameters
        self.mFP.seek(trigger_parameters_offset)
        for _ in range(trigger_parameters_count):
            self.ConvertTriggerParameters()

        # strings
        self.mFP.seek(strings_offsets)
        for _ in range(strings_count):
            utilities.SwapBytes(self.mFP, "<L")

        # special textures
        self.mFP.seek(special_textures_offsets)
        for _ in range(special_textures_count):
            utilities.SwapBytes(self.mFP, "<L")

        # debug strings
        self.mFP.seek(debug_strings_offsets)
        for _ in range(debug_strings_count):
            utilities.SwapBytes(self.mFP, "<L")

        # import entries
        self.mFP.seek(import_entries_offset)
        for _ in range(import_entries_count):
            self.ConvertImportEntry()


    def ConvertMovieClip(self, movie_clip_offset: int) -> None:
        # movie clip
        self.mFP.seek(movie_clip_offset + 0x1)
        children_count = utilities.UnpackBytes(self.mFP, "B")
        meshes_count = utilities.UnpackBytes(self.mFP, "B")
        text_fields_count = utilities.UnpackBytes(self.mFP, "B")
        render_layers_count = utilities.UnpackBytes(self.mFP, "B")
        labelled_frames_count = utilities.UnpackBytes(self.mFP, "B")
        fscript_commands_count = utilities.UnpackBytes(self.mFP, "B")
        self.mFP.seek(0x1, 1)
        frames_in_timeline_count = utilities.SwapBytes(self.mFP, "<H")
        key_frames_count = utilities.SwapBytes(self.mFP, "<H")
        utilities.SwapBytes(self.mFP, "<L")
        frame_to_key_frames_map_offset = utilities.SwapBytes(self.mFP, "<L")
        utilities.SwapBytes(self.mFP, "<L")
        key_frames_offset = utilities.SwapBytes(self.mFP, "<L")
        key_frame_animations_offset = utilities.SwapBytes(self.mFP, "<L")
        fscript_commands_offset = utilities.SwapBytes(self.mFP, "<L")
        child_movie_clips_offset = utilities.SwapBytes(self.mFP, "<L")
        child_names_offset = utilities.SwapBytes(self.mFP, "<L")
        meshes_offset = utilities.SwapBytes(self.mFP, "<L")
        text_fields_offset = utilities.SwapBytes(self.mFP, "<L")
        text_field_names_offset = utilities.SwapBytes(self.mFP, "<L")
        frame_labels_offset = utilities.SwapBytes(self.mFP, "<L")
        labelled_frame_ids_offset = utilities.SwapBytes(self.mFP, "<L")
        utilities.SwapBytes(self.mFP, "<L")

        # frame to key frame map
        if frame_to_key_frames_map_offset != 0:
            self.mFP.seek(frame_to_key_frames_map_offset)
            for _ in range(frames_in_timeline_count):
                utilities.SwapBytes(self.mFP, "<H")

        # key frames
        self.mFP.seek(key_frames_offset)
        for _ in range(render_layers_count):
            self.ConvertKeyFrame()

        # key frame animations
        for i in range(key_frames_count):
            self.ConvertKeyFrameAnimations(key_frame_animations_offset + i * 0x20)

        # fscript commands
        if fscript_commands_offset != 0:
            self.mFP.seek(fscript_commands_offset)
            for _ in range(fscript_commands_count):
                self.ConvertFScriptCommand()

        # child movie clips
        self.mFP.seek(child_movie_clips_offset)
        for _ in range(children_count):
            utilities.SwapBytes(self.mFP, "<H")

        # child names
        self.mFP.seek(child_names_offset)
        for _ in range(children_count):
            self.ConvertHashedString()

        # meshes
        self.mFP.seek(meshes_offset)
        for _ in range(meshes_count):
            self.ConvertMesh()

        # text fields
        self.mFP.seek(text_fields_offset)
        for _ in range(text_fields_count):
            self.ConvertTextField()

        # text field names
        self.mFP.seek(text_field_names_offset)
        for _ in range(text_fields_count):
            self.ConvertHashedString()

        # frame labels
        self.mFP.seek(frame_labels_offset)
        for _ in range(labelled_frames_count):
            self.ConvertHashedString()

        # labelled frame ids
        self.mFP.seek(labelled_frame_ids_offset)
        for _ in range(labelled_frames_count):
            utilities.SwapBytes(self.mFP, "<H")


    def ConvertKeyFrameAnimations(self, key_frame_animation_offset: int) -> None:
        # key frame animation
        self.mFP.seek(key_frame_animation_offset)
        for _ in range(3):
            utilities.SwapBytes(self.mFP, "<L")
        self.mFP.seek(0x2, 1)
        transforms_count = utilities.UnpackBytes(self.mFP, "B")
        color_transforms_count = utilities.UnpackBytes(self.mFP, "B")
        utilities.SwapBytes(self.mFP, "<L")
        transforms_offset = utilities.SwapBytes(self.mFP, "<L")
        utilities.SwapBytes(self.mFP, "<L")
        color_transforms_offset = utilities.SwapBytes(self.mFP, "<L")

        # transforms
        self.mFP.seek(transforms_offset)
        for _ in range(transforms_count):
            self.ConvertTransform()

        # color transforms
        self.mFP.seek(color_transforms_offset)
        for _ in range(color_transforms_count):
            self.ConvertTransform()


    def ConvertHashedString(self) -> None:
        # hashed string
        utilities.SwapBytes(self.mFP, "<L")
        utilities.SwapBytes(self.mFP, "<L")


    def ConvertTransform(self) -> None:
        # transform
        for _ in range(8):
            utilities.SwapBytes(self.mFP, "<L")


    def ConvertKeyFrame(self) -> None:
        # key frame
        for _ in range(3):
            utilities.SwapBytes(self.mFP, "<L")


    def ConvertMesh(self) -> None:
        # mesh
        self.mFP.seek(0x2, 1)
        utilities.SwapBytes(self.mFP, "<H")

    
    def ConvertTextField(self) -> None:
        # text field
        self.ConvertHashedString()
        utilities.SwapBytes(self.mFP, "<H")
        self.mFP.seek(0x6, 1)
        for _ in range(4):
            utilities.SwapBytes(self.mFP, "<L")

    
    def ConvertFScriptCommand(self) -> None:
        # fscript command
        self.mFP.seek(0x2, 1)
        utilities.SwapBytes(self.mFP, "<H")


    def ConvertVertex(self) -> None:
        # vertex
        utilities.SwapBytes(self.mFP, "<L")
        utilities.SwapBytes(self.mFP, "<L")
        self.mFP.seek(0x4, 1)
        utilities.SwapBytes(self.mFP, "<L")
        utilities.SwapBytes(self.mFP, "<L")


    def ConvertFont(self) -> None:
        # font
        for _ in range(3):
            utilities.SwapBytes(self.mFP, "<L")

    
    def ConvertTriggerParameters(self) -> None:
        # trigger parameters
        for _ in range(4):
            utilities.SwapBytes(self.mFP, "<L")


    def ConvertImportEntry(self) -> None:
        # import entry
        utilities.SwapBytes(self.mFP, "<Q")
        utilities.SwapBytes(self.mFP, "<L")
        self.mFP.seek(0x4, 1)


def Main():
    flapt_file_path = filedialog.askopenfilename()
    import_entries_offset = int(input("import entries offset: "), 16)
    import_entries_count = int(input("import entries count: "))
    with open(flapt_file_path, "r+b") as fp:
        flapt_file = FlaptFile(fp)
        flapt_file.Convert(import_entries_offset, import_entries_count)


if __name__ == "__main__":
    Main()