import HkLib.Helpers.MoreHex as MoreHex
import HkLib.Helpers.String as String
import HkLib.Helpers.MoreMath as MoreMath

class PSLD:
    def __init__(self, file, endian):
        self.endian = endian
        self.Construct(file, endian)

    def Construct(self, file, endian):
        self.length = int.from_bytes(file.read(0x04), endian)
        self.entry_amount = int.from_bytes(file.read(0x04), endian)
        self.name_offset = int.from_bytes(file.read(0x04), endian)
        
        self.unknown0 = int.from_bytes(file.read(0x04), endian)
        self.unknown1 = int.from_bytes(file.read(0x04), endian)
        self.unknown2 = int.from_bytes(file.read(0x04), endian)
        self.unknown3 = int.from_bytes(file.read(0x04), endian)

        self.names = {}
        self.floats = []

    def GetData(self, file, endian):
        return_addr = file.tell()

        for asset in range(self.entry_amount):
            self.floats.append(MoreHex.BytesToFloat(file.read(0x04), self.endian))

        file.seek(return_addr+self.name_offset)

        for asset in range(self.entry_amount):
            id = file.read(0x08)
            file.read(0x18)
            name = String.ReadUntil(file, b"\x00")
            self.names[id] = name
            file.seek(MoreMath.RoundUp(file.tell(), 0x40))

    def GetBytes0(self): # Returns SubLayer Data
        bytecode = b""
        bytecode += self.name_offset.to_bytes(4, byteorder=self.endian)
            
        bytecode += self.unknown0.to_bytes(4, byteorder=self.endian)
        bytecode += self.unknown1.to_bytes(4, byteorder=self.endian)
        bytecode += self.unknown2.to_bytes(4, byteorder=self.endian)
        bytecode += self.unknown3.to_bytes(4, byteorder=self.endian)

        return bytecode

    def GetBytes1(self): # Returns Data
        bytecode = b""
        for float in self.floats:
            bytecode += MoreHex.FloatToBytes(float, self.endian)
        bytecode += MoreHex.GenerateBytes(b"\x33", self.name_offset - len(bytecode))

        for name in self.names:
            bytecode += name
            bytecode += bytes(0x18)
            bytecode += String.ToString(self.names[name], "big") + b"\x00"
            bytecode += MoreHex.GenerateBytes(b"\x33", MoreMath.RoundUp(len(bytecode), 0x40) - len(bytecode))
        
        bytecode += MoreHex.GenerateBytes(b"\x33", MoreMath.RoundUp(len(bytecode), 0x800) - len(bytecode))
        


        return bytecode

    def Update(self):
        self.name_offset = MoreMath.RoundUp(len(self.floats)*0x4, 0x40)
