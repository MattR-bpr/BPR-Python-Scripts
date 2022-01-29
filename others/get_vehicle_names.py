import struct
from tkinter import filedialog
from typing import BinaryIO, Dict
from cgsid import GetUncompressedCgsID


gVehicleNames: Dict[int, str] = {}


def ReadVehicleIDs(fp: BinaryIO) -> None:
    global gVehicleNames

    # read the header
    vehicles_count, vehicle_entries_offset = struct.unpack("<LL", fp.read(2 * 4))

    # read vehicle entries
    fp.seek(vehicle_entries_offset)
    for _ in range(vehicles_count):
        vehicle_id = struct.unpack("<Q", fp.read(8))[0]
        vehicle_name = GetUncompressedCgsID(vehicle_id)
        gVehicleNames[vehicle_id] = vehicle_name
        fp.seek(0x100, 1)


def Main():
    global gVehicleNames

    # read the vehicle IDs
    vehicle_list = filedialog.askopenfilename()
    with open(vehicle_list, "rb") as fp:
        ReadVehicleIDs(fp)

    # save vehicle names
    with open("rsc/vehicle_names.py", "w") as fp:
        fp.write("VEHICLE_NAMES = {\n")
        for vehicle_id in sorted(gVehicleNames.keys()):
            vehicle_name = gVehicleNames.get(vehicle_id)
            fp.write(f"    0x{vehicle_id :016X}: '{vehicle_name}',\n")
        fp.write("}")


if __name__ == "__main__":
    Main()