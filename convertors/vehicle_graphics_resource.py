from tkinter import filedialog
from typing import BinaryIO
import utilities


class VehicleGraphicsResource:

    def __init__(self, fp: BinaryIO):
        self.mFP = fp


    def Convert(self, import_entries_offset: int, import_entries_count: int) -> None:
        # check version
        self.mFP.seek(0x0)
        version = utilities.SwapBytes(self.mFP, "<L")
        assert version == 3, "Bad VehicleGraphicsResource version."

        # header
        parts_count = utilities.SwapBytes(self.mFP, "<L")
        utilities.SwapBytes(self.mFP, "<L")
        shattered_glass_parts_count = utilities.SwapBytes(self.mFP, "<L")
        shattered_glass_parts_offset = utilities.SwapBytes(self.mFP, "<L")
        part_locators_offset = utilities.SwapBytes(self.mFP, "<L")
        utilities.SwapBytes(self.mFP, "<L")
        rigid_body_counts_offset = utilities.SwapBytes(self.mFP, "<L")
        rigid_bodies_offsets = utilities.SwapBytes(self.mFP, "<L")
        
        # shattered glass parts
        self.mFP.seek(shattered_glass_parts_offset)
        for _ in range(shattered_glass_parts_count):
            self.ConvertShatteredGlassPart()

        # part locators
        self.mFP.seek(part_locators_offset)
        for _ in range(parts_count):
            self.ConvertMatrix4x4()

        # rigid bodies
        if rigid_body_counts_offset != 0:
            for i in range(parts_count):
                self.mFP.seek(rigid_body_counts_offset + i)
                rigid_bodies_count = utilities.UnpackBytes(self.mFP, "B")
                self.mFP.seek(rigid_bodies_offsets + i * 0x4)
                rigid_bodies_offset = utilities.SwapBytes(self.mFP, "<L")
                self.ConvertRigidBodies(rigid_bodies_offset, rigid_bodies_count)

        # import entries
        self.mFP.seek(import_entries_offset)
        for _ in range(import_entries_count):
            self.ConvertImportEntry()


    def ConvertMatrix4x4(self) -> None:
        # matrix 4x4
        for _ in range(16):
            utilities.SwapBytes(self.mFP, "<L")


    def ConvertShatteredGlassPart(self) -> None:
        # shattered glass part
        for _ in range(3):
            utilities.SwapBytes(self.mFP, "<L")


    def ConvertRigidBodies(self, rigid_bodies_offset: int, rigid_bodies_count: int) -> None:
        # rigid bodies
        self.mFP.seek(rigid_bodies_offset)
        for _ in range(rigid_bodies_count):
            self.ConvertMatrix4x4()


    def ConvertImportEntry(self) -> None:
        # import entry
        utilities.SwapBytes(self.mFP, "<Q")
        utilities.SwapBytes(self.mFP, "<L")
        self.mFP.seek(0x4, 1)


def Main():
    vehicle_graphics_resource_path = filedialog.askopenfilename()
    import_entries_offset = int(input("import entries offset: "), 16)
    import_entries_count = int(input("import entries count: "))
    with open(vehicle_graphics_resource_path, "r+b") as fp:
        vehicle_graphics_resource = VehicleGraphicsResource(fp)
        vehicle_graphics_resource.Convert(import_entries_offset, import_entries_count)


if __name__ == "__main__":
    Main()