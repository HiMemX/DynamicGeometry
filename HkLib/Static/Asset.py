import HkLib.Helpers.MoreMath as MoreMath

class Asset:
    def __init__(self, file, endian, args):
        self.endian = endian
        if args == []:
            self.Construct(file, endian)
        else:
            self.length_padding = args[0]
            self.offset         = 0
            self.length         = args[1]
            self.unknown0       = args[2]
            self.assetid        = args[3]
            self.assettype      = args[4]
            self.unknown1       = args[5]
            self.data           = args[6]
            self.name           = args[7]

    def Construct(self, file, endian):
        self.length_padding = int.from_bytes(file.read(0x04), endian)
        self.offset = int.from_bytes(file.read(0x04), endian)
        self.length = int.from_bytes(file.read(0x04), endian)
        self.unknown0 = int.from_bytes(file.read(0x04), endian)
        self.assetid = file.read(0x08)
        self.assettype = file.read(0x04)
        file.read(0x02)
        self.unknown1 = int.from_bytes(file.read(0x02), endian)

        self.data = []
        self.name = ""

    def GetBytes0(self):
        bytecode = b""
        bytecode += self.length_padding.to_bytes(4, byteorder=self.endian)
        bytecode += self.offset.to_bytes(4, byteorder=self.endian)
        bytecode += self.length.to_bytes(4, byteorder=self.endian)
        bytecode += self.unknown0.to_bytes(4, byteorder=self.endian)
        bytecode += self.assetid
        bytecode += self.assettype
        bytecode += bytes(0x02)
        bytecode += self.unknown1.to_bytes(2, byteorder=self.endian)

        return bytecode

    def Update(self):
        self.length = len(self.data)
        self.length_padding = MoreMath.RoundUp(self.length, 0x40)