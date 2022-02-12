from tkinter import filedialog
from typing import BinaryIO
import utilities


class ModelResource:

    def __init__(self, fp: BinaryIO):
        self.mFP = fp


    def Convert(self, import_entries_offset: int, import_entries_count: int) -> None:
        # check version
        self.mFP.seek(0x13)
        version = utilities.UnpackBytes(self.mFP, "B")
        assert version == 2, "Bad ModelResource version."

        # header
        self.mFP.seek(0x0)
        utilities.SwapBytes(self.mFP, "<L")
        utilities.SwapBytes(self.mFP, "<L")
        lod_distances_offset = utilities.SwapBytes(self.mFP, "<L")
        utilities.SwapBytes(self.mFP, "<L")
        renderables_count = utilities.UnpackBytes(self.mFP, "B")
        
        # lod distances
        self.mFP.seek(lod_distances_offset)
        for _ in range(renderables_count):
            utilities.SwapBytes(self.mFP, "<L")

        # import entries
        self.mFP.seek(import_entries_offset)
        for _ in range(import_entries_count):
            self.ConvertImportEntry()


    def ConvertImportEntry(self) -> None:
        # import entry
        utilities.SwapBytes(self.mFP, "<Q")
        utilities.SwapBytes(self.mFP, "<L")
        self.mFP.seek(0x4, 1)


def Main():
    model_resource_path = filedialog.askopenfilename()
    import_entries_offset = int(input("import entries offset: "), 16)
    import_entries_count = int(input("import entries count: "))
    with open(model_resource_path, "r+b") as fp:
        model_resource = ModelResource(fp)
        model_resource.Convert(import_entries_offset, import_entries_count)


if __name__ == "__main__":
    Main()