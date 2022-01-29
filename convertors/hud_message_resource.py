from tkinter import filedialog
from typing import BinaryIO
import utilities


class HudMessageResource:

    def __init__(self, fp: BinaryIO):
        self.mFP = fp


    def Convert(self) -> None:
        # header
        self.mFP.seek(0x0)
        hud_messages_offsets = utilities.SwapBytes(self.mFP, "<L")
        utilities.SwapBytes(self.mFP, "<L")
        hud_messages_count = utilities.SwapBytes(self.mFP, "<L")

        # hud messages
        for i in range(hud_messages_count):
            self.mFP.seek(hud_messages_offsets + i * 0x4)
            hud_messsage_offset = utilities.SwapBytes(self.mFP, "<L")
            self.ConvertHudMessage(hud_messsage_offset)
        

    def ConvertHudMessage(self, hud_message_offset: int) -> None:
        # hud message
        self.mFP.seek(hud_message_offset + 0x110)
        utilities.SwapBytes(self.mFP, "<Q")
        for _ in range(21):
            utilities.SwapBytes(self.mFP, "<L")


def Main():
    hud_message_resource_path = filedialog.askopenfilename()
    with open(hud_message_resource_path, "r+b") as fp:
        hud_message_resource = HudMessageResource(fp)
        hud_message_resource.Convert()


if __name__ == "__main__":
    Main()