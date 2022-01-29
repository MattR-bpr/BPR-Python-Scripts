from zlib import crc32
from tkinter import filedialog
from typing import BinaryIO, Dict
import utilities


class LanguageResource:

    @staticmethod
    def GetHashFromStringId(string_id: str) -> int:
        hash = crc32(string_id.encode("ascii"))
        return ~hash & 0xFFFFFFFF


    def __init__(self):
        self.mEntries: Dict[int, str] = {}


    def LoadFromFile(self, fp: BinaryIO) -> None:
        # read file into memory
        fp.seek(0)
        buffer = fp.read()

        # header
        entries_count = utilities.ReadValue(buffer, 0x4, "<L")
        entries_offset = utilities.ReadValue(buffer, 0x8, "<L")

        # entries
        self.mEntries.clear()
        for i in range(entries_count):
            entry_offset = entries_offset + i * 0x8
            hash = utilities.ReadValue(buffer, entry_offset + 0x0, "<L")
            if not hash:
                continue

            string_offset = utilities.ReadValue(buffer, entry_offset + 0x4, "<L")
            string = utilities.ReadString(buffer, string_offset, "utf-8")
            self.mEntries[hash] = string


    def SaveToFile(self, fp: BinaryIO) -> None:
        # header
        header = b""
        header += utilities.GetBytes("<L", 7)
        header += utilities.GetBytes("<L", len(self.mEntries))
        header += utilities.GetBytes("<L", 0xC)

        # entries
        entries = b""
        strings = b""
        for hash, string in self.mEntries.items():
            string_offset = 0xC + len(self.mEntries) * 0x8 + len(strings)
            entries += utilities.GetBytes("<L", hash)
            entries += utilities.GetBytes("<L", string_offset)
            strings += string.encode("utf-8") + b"\x00"

        # write data into file
        fp.truncate(0)
        fp.write(header)
        fp.write(entries)
        fp.write(strings)


    def AddEntry(self, string_id: str, string: str) -> bool:
        hash = LanguageResource.GetHashFromStringId(string_id)
        if hash in self.mEntries:
            return False
        self.mEntries[hash] = string
        return True


    def EditEntry(self, string_id: str, string: str) -> bool:
        hash = LanguageResource.GetHashFromStringId(string_id)
        if hash not in self.mEntries:
            return False
        self.mEntries[hash] = string
        return True


    def DeleteEntry(self, string_id: str) -> bool:
        hash = LanguageResource.GetHashFromStringId(string_id)
        if hash not in self.mEntries:
            return False
        self.mEntries.pop(hash)
        return True


def Main():
    language_resource = LanguageResource()

    while True:
        try:
            option = input("Option [ (l)oad (s)ave (a)dd_entry (e)dit_entry (d)elete_entry ]: ")
            
            if option == "l":
                file_name = filedialog.askopenfilename()
                with open(file_name, "rb") as fp:
                    language_resource.LoadFromFile(fp)
                    print("File loaded.")
            
            elif option == "s":
                file_name = filedialog.askopenfilename()
                with open(file_name, "wb") as fp:
                    language_resource.SaveToFile(fp)
                    print("File saved.")
            
            elif option == "a":
                string_id = input("String ID: ")
                string = input("String: ")
                successful = language_resource.AddEntry(string_id, string)
                print("Entry added.") if successful else print("Failed to add entry!")
            
            elif option == "e":
                string_id = input("String ID: ")
                string = input("String: ")
                successful = language_resource.EditEntry(string_id, string)
                print("Entry edited.") if successful else print("Failed to edit entry!")
            
            elif option == "d":
                string_id = input("String ID: ")
                successful = language_resource.DeleteEntry(string_id)
                print("Entry deleted.") if successful else print("Failed to delete entry!")
            
            else:
                print("Invalid option!")
        
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    Main()