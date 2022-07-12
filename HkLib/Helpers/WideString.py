def ReadWideString(file, char_amount, endian):
    string = ""
    for c in range(char_amount):
        integ = int.from_bytes(file.read(0x02), endian)
        if integ != 0: string += chr(integ)
    return string

def GetWideString(string, limit, endian):
    bytecode = b""

    bytecode += string.encode("utf-16")[2:]
    
    bytecode += bytes(limit-len(bytecode))

    if endian == "big": 
        bytecode = b"\x00" + bytecode[:-1]

    return bytecode