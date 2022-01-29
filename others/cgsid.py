def GetCompressedCgsId(string: str) -> int:
    result = 0
    for c in string.ljust(12, " "):
        c = ord(c)
        result *= 40
        if c == 95:
            result += 39
        elif c >= 65:
            result += c - 52
        elif c >= 48:
            result += c - 45
        elif c >= 47:
            result += 2
        elif c >= 45:
            result += 1
    return result


def GetUncompressedCgsID(cgsid: int) -> str:
    result = ""
    for _ in range(12):
        mod = cgsid % 40
        cgsid //= 40
        if mod == 39:
            result += "_"
        elif mod >= 13:
            result += chr(mod + 52)
        elif mod >= 3:
            result += chr(mod + 45)
        elif mod >= 2:
            result += "/"
        elif mod == 1:
            result += "-"
        else:
            result += " "
    return result[::-1].rstrip(" ")


def Main():
    while True:
        try:
            option = input("Option [ (c)ompress (u)ncompress ]: ")

            if option == "c":
                string = input("String: ")
                cgsid = GetCompressedCgsId(string)
                print(f"{cgsid :016X}")

            elif option == "u":
                cgsid = int(input("CgsID: "), 16)
                string = GetUncompressedCgsID(cgsid)
                print(string)

            else:
                print("Invalid option!")
        
        except KeyboardInterrupt:
            break
    

if __name__ == "__main__":
    Main()