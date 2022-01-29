from tkinter import filedialog
from typing import BinaryIO
import utilities


class PopupResource:

    def __init__(self, fp: BinaryIO):
        self.mFP = fp


    def Convert(self) -> None:
        # header
        self.mFP.seek(0x0)
        popups_offsets = utilities.SwapBytes(self.mFP, "<L")
        popups_count = utilities.SwapBytes(self.mFP, "<H")
        utilities.SwapBytes(self.mFP, "<H")

        # popups
        for i in range(popups_count):
            self.mFP.seek(popups_offsets + i * 0x4)
            popup_offset = utilities.SwapBytes(self.mFP, "<L")
            self.ConvertPopup(popup_offset)


    def ConvertPopup(self, popup_offset: int) -> None:
        # popup
        self.mFP.seek(popup_offset)
        utilities.SwapBytes(self.mFP, "<Q")
        self.mFP.seek(0x10, 1)
        utilities.SwapBytes(self.mFP, "<L")
        utilities.SwapBytes(self.mFP, "<L")
        self.mFP.seek(0x40, 1)
        for _ in range(3):
            utilities.SwapBytes(self.mFP, "<L")
        self.mFP.seek(0x20, 1)
        utilities.SwapBytes(self.mFP, "<L")
        self.mFP.seek(0x24, 1)
        utilities.SwapBytes(self.mFP, "<L")


def Main():
    popup_resource_path = filedialog.askopenfilename()
    with open(popup_resource_path, "r+b") as fp:
        popup_resource = PopupResource(fp)
        popup_resource.Convert()


if __name__ == "__main__":
    Main()