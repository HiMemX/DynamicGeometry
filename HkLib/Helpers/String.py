def ReadString(file, char_amount, endian):
    bytes = bytearray(file.read(char_amount))
    if endian == "little":
        bytes.reverse()
    return bytes.decode("ANSI")

def ToString(string, endian):
    output = string.encode("ANSI")
    if endian == "little":
        output = output.reverse()

    return output

def ReadUntil(file, terminator):
    string = ""
    while True:
        char = file.read(0x01)
        if char == terminator:
            break
        string += char.decode("ANSI")

    return string