from tkinter import filedialog
from typing import BinaryIO
import utilities


class TriggerData:

    def __init__(self, fp: BinaryIO):
        self.mFP = fp


    def Convert(self) -> None:
        # check version
        self.mFP.seek(0x0)
        version = utilities.SwapBytes(self.mFP, "<L")
        assert version >= 34 and version <= 42, "Bad TriggerData version."

        # header
        utilities.SwapBytes(self.mFP, "<L")
        self.mFP.seek(0x10)
        for _ in range(8):
            utilities.SwapBytes(self.mFP, "<L")
        landmarks_offset = utilities.SwapBytes(self.mFP, "<L")
        landmarks_count = utilities.SwapBytes(self.mFP, "<L")
        utilities.SwapBytes(self.mFP, "<L")
        signature_stunts_offset = utilities.SwapBytes(self.mFP, "<L")
        signature_stunts_count = utilities.SwapBytes(self.mFP, "<L")
        generic_regions_offset = utilities.SwapBytes(self.mFP, "<L")
        generic_regions_count = utilities.SwapBytes(self.mFP, "<L")
        killzones_offset = utilities.SwapBytes(self.mFP, "<L")
        killzones_count = utilities.SwapBytes(self.mFP, "<L")
        blackspots_offset = utilities.SwapBytes(self.mFP, "<L")
        blackspots_count = utilities.SwapBytes(self.mFP, "<L")
        vfx_box_regions_offset = utilities.SwapBytes(self.mFP, "<L")
        vfx_box_regions_count = utilities.SwapBytes(self.mFP, "<L")
        roaming_locations_offset = utilities.SwapBytes(self.mFP, "<L")
        roaming_locations_count = utilities.SwapBytes(self.mFP, "<L")
        spawn_locations_offset = utilities.SwapBytes(self.mFP, "<L")
        spawn_locations_count = utilities.SwapBytes(self.mFP, "<L")
        regions_offsets = utilities.SwapBytes(self.mFP, "<L")
        regions_count = utilities.SwapBytes(self.mFP, "<L")

        # landmarks
        for i in range(landmarks_count):
            self.ConvertLandmark(landmarks_offset + i * 0x34)

        # signature stunts
        for i in range(signature_stunts_count):
            self.ConvertSignatureStunt(signature_stunts_offset + i * 0x18)

        # generic regions
        self.mFP.seek(generic_regions_offset)
        for _ in range(generic_regions_count):
            self.ConvertGenericRegion()

        # killzones
        for i in range(killzones_count):
            self.ConvertKillzone(killzones_offset + i * 0x10)

        # blackspots
        self.mFP.seek(blackspots_offset)
        for _ in range(blackspots_count):
            self.ConvertBlackspot()

        # vfx box regions
        self.mFP.seek(vfx_box_regions_offset)
        for _ in range(vfx_box_regions_count):
            self.ConvertTriggerRegion()

        # roaming locations
        self.mFP.seek(roaming_locations_offset)
        for _ in range(roaming_locations_count):
            self.ConvertRoamingLocation()

        # spawn locations
        self.mFP.seek(spawn_locations_offset)
        for _ in range(spawn_locations_count):
            self.ConvertSpawnLocation()

        # regions
        self.mFP.seek(regions_offsets)
        for _ in range(regions_count):
            utilities.SwapBytes(self.mFP, "<L")


    def ConvertTriggerRegion(self) -> None:
        # trigger region
        for _ in range(10):
            utilities.SwapBytes(self.mFP, "<L")
        utilities.SwapBytes(self.mFP, "<H")
        self.mFP.seek(0x2, 1)

    
    def ConvertGenericRegion(self) -> None:
        # trigger region
        self.ConvertTriggerRegion()

        # generic region
        utilities.SwapBytes(self.mFP, "<L")
        utilities.SwapBytes(self.mFP, "<H")
        utilities.SwapBytes(self.mFP, "<H")
        self.mFP.seek(0x4, 1)


    def ConvertStartingGrid(self) -> None:
        # starting grid
        for _ in range(64):
            utilities.SwapBytes(self.mFP, "<L")


    def ConvertLandmark(self, landmark_offset: int) -> None:
        # trigger region
        self.mFP.seek(landmark_offset)
        self.ConvertTriggerRegion()

        # landmark
        starting_grids_offset = utilities.SwapBytes(self.mFP, "<L")
        starting_grids_count = utilities.UnpackBytes(self.mFP, "B")
        
        # starting grids
        self.mFP.seek(starting_grids_offset)
        for _ in range(starting_grids_count):
            self.ConvertStartingGrid()


    def ConvertSignatureStunt(self, signature_stunt_offset: int) -> None:
        # signature stunt
        self.mFP.seek(signature_stunt_offset)
        utilities.SwapBytes(self.mFP, "<Q")
        utilities.SwapBytes(self.mFP, "<Q")
        stunt_elements_offset = utilities.SwapBytes(self.mFP, "<L")
        stunt_elements_count = utilities.SwapBytes(self.mFP, "<L")

        # stunt elements
        self.mFP.seek(stunt_elements_offset)
        for _ in range(stunt_elements_count):
            utilities.SwapBytes(self.mFP, "<L")


    def ConvertKillzone(self, killzone_offset: int) -> None:
        # killzone
        self.mFP.seek(killzone_offset)
        triggers_offsets = utilities.SwapBytes(self.mFP, "<L")
        triggers_count = utilities.SwapBytes(self.mFP, "<L")
        region_ids_offset = utilities.SwapBytes(self.mFP, "<L")
        region_ids_count = utilities.SwapBytes(self.mFP, "<L")

        # triggers
        self.mFP.seek(triggers_offsets)
        for _ in range(triggers_count):
            utilities.SwapBytes(self.mFP, "<L")

        # region ids
        self.mFP.seek(region_ids_offset)
        for _ in range(region_ids_count):
            utilities.SwapBytes(self.mFP, "<Q")


    def ConvertBlackspot(self) -> None:
        # blackspot
        self.ConvertTriggerRegion()
        self.mFP.seek(0x4, 1)
        utilities.SwapBytes(self.mFP, "<L")


    def ConvertRoamingLocation(self) -> None:
        # roaming location
        for _ in range(4):
            utilities.SwapBytes(self.mFP, "<L")
        self.mFP.seek(0x10, 1)


    def ConvertSpawnLocation(self) -> None:
        # spawn location
        for _ in range(8):
            utilities.SwapBytes(self.mFP, "<L")
        utilities.SwapBytes(self.mFP, "<Q")
        self.mFP.seek(0x8, 1)
        

def Main():
    trigger_data_path = filedialog.askopenfilename()
    with open(trigger_data_path, "r+b") as fp:
        trigger_data = TriggerData(fp)
        trigger_data.Convert()


if __name__ == "__main__":
    Main()