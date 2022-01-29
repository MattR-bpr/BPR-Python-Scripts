import os
import struct
from xml.etree import ElementTree
from tkinter import filedialog
from typing import BinaryIO, Dict, Set


gResources: Dict[int, str] = {}
gResourceTypes: Dict[int, Set[str]] = {}


def UpdateResources(fp: BinaryIO) -> None:
    global gResources
    global gResourceTypes

    # check whether the file is a valid BundleV2
    fp.seek(0)
    if fp.read(4) != b"bnd2":
        return
    
    # read the header
    fp.seek(0xC)
    debug_data_offset, resource_entries_count, resource_entries_offset = struct.unpack("<LLL", fp.read(3 * 4))
    
    # read the debug data
    fp.seek(debug_data_offset)
    debug_data = fp.read(resource_entries_offset - debug_data_offset)
    debug_data = debug_data.rstrip(b"\x00").decode("utf-8")
    if len(debug_data) == 0:
        return

    # parse the data
    resources = ElementTree.fromstring(debug_data).findall("Resource")
    fp.seek(resource_entries_offset)
    for _ in range(resource_entries_count):
        # read the resource data
        resource_id = struct.unpack("<L", fp.read(4))[0]
        fp.seek(0x34, 1)
        resource_type_id = struct.unpack("<L", fp.read(4))[0]
        fp.seek(0x4, 1)

        # find and parse the debug data
        resource_name = None
        resource_type = None
        for resource in resources:
            if int(resource.attrib["id"], 16) == resource_id:
                resource_name = resource.attrib["name"]
                resource_type = resource.attrib["type"]
                break

        # update resources
        gResources[resource_id] = resource_name
        
        # update resource types
        if resource_type_id not in gResourceTypes:
            gResourceTypes[resource_type_id] = set()
        gResourceTypes[resource_type_id].add(resource_type)


def Main():
    global gResources
    global gResourceTypes

    # extract resource data
    bpr_dir = filedialog.askdirectory()
    for root, _, files in os.walk(bpr_dir):
        for file in files:
            with open(f"{root}/{file}", "rb") as fp:
                UpdateResources(fp)

    # save resources
    with open("rsc/resources.py", "w") as fp:
        fp.write("RESOURCES = {\n")
        for resource_id in sorted(gResources.keys()):
            resource_name = gResources.get(resource_id).replace("\\", "\\\\")
            fp.write(f"    0x{resource_id :08X}: '{resource_name}',\n")
        fp.write("}")

    # save resource types
    with open("rsc/resource_types.py", "w") as fp:
        fp.write("RESOURCE_TYPES = {\n")
        for resource_type_id in sorted(gResourceTypes.keys()):
            resource_type = sorted(gResourceTypes.get(resource_type_id))
            fp.write(f"    0x{resource_type_id :08X}: {resource_type},\n")
        fp.write("}")
        

if __name__ == "__main__":
    Main()