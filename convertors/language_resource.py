from tkinter import filedialog
from typing import BinaryIO
import utilities


class LanguageResource:

    def __init__(self, fp: BinaryIO):
        self.mFP = fp


    def Convert(self) -> None:
        # header
        self.mFP.seek(0x0)
        utilities.SwapBytes(self.mFP, "<L")
        entries_count = utilities.SwapBytes(self.mFP, "<L")
        entries_offset = utilities.SwapBytes(self.mFP, "<L")

        # entries
        self.mFP.seek(entries_offset)
        for _ in range(entries_count):
            utilities.SwapBytes(self.mFP, "<L")
            utilities.SwapBytes(self.mFP, "<L")


def Main():
    language_resource_path = filedialog.askopenfilename()
    with open(language_resource_path, "r+b") as fp:
        lanuage_resource = LanguageResource(fp)
        lanuage_resource.Convert()


if __name__ == "__main__":
    Main()