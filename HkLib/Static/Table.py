import HkLib.Helpers.MoreHex as MoreHex
import HkLib.Static.Asset as Asset
import HkLib.Helpers.MoreMath as MoreMath

class Table:
    def __init__(self, file, endian, dir, data):
        self.endian = endian
        self.Construct(file, endian, dir, data)

    def Construct(self, file, endian, dir, data):
        self.dir_rel_offset = 0
        self.dir_offset = dir[0]
        self.dir_length = dir[1]
        self.data_offset = data[0]
        self.data_length = data[1]

        file.seek(self.dir_offset)
        self.asset_amount = int.from_bytes(file.read(0x04), endian)
        file.read(0x1C)
        self.assets = [Asset.Asset(file, endian, []) for asset in range(self.asset_amount)]
        
        file.seek(self.data_offset)
        for asset in self.assets:
            asset.data = file.read(asset.length)
            file.read(asset.length_padding - asset.length)

    def GetBytes0(self): # Returns Table Definition Data // DIRECTORY
        bytecode = b""
        bytecode += bytes(0x04)
        bytecode += self.dir_rel_offset.to_bytes(4, byteorder=self.endian) # This line isn't important actually
        bytecode += self.dir_length.to_bytes(4, byteorder=self.endian)
        bytecode += bytes(0x04)

        return bytecode

    def GetBytes1(self): # Returns Table Definition Data // DATA
        bytecode = b""
        bytecode += 0x02.to_bytes(4, byteorder=self.endian)
        bytecode += bytes(0x0C)

        bytecode += 0x01.to_bytes(4, byteorder=self.endian)
        bytecode += self.data_offset.to_bytes(4, byteorder=self.endian) # This line isn't important actually
        bytecode += self.data_length.to_bytes(4, byteorder=self.endian)
        bytecode += bytes(0x04)

        return bytecode

    def GetBytes2(self):
        bytecode = b""
        bytecode += self.asset_amount.to_bytes(4, byteorder=self.endian)
        bytecode += MoreHex.GenerateBytes(b"\xFF", 0x04)
        bytecode += MoreHex.GenerateBytes(b"\x74", 0x18)

        for asset in self.assets:
            bytecode += asset.GetBytes0()
        
        bytecode += MoreHex.GenerateBytes(b"\x33", MoreMath.RoundUp(len(bytecode), 0x40) - len(bytecode))

        return bytecode

    def GetBytes3(self):
        bytecode = b""
        for asset in self.assets:
            bytecode += asset.data
            bytecode += MoreHex.GenerateBytes(b"\x33", asset.length_padding-asset.length)
        
        return bytecode


    def Update(self):
        [asset.Update() for asset in self.assets]

        self.data_length = sum([asset.length_padding for asset in self.assets])
        self.dir_length = MoreMath.RoundUp(len(self.assets)*0x20 + 0x20, 0x40)
        self.asset_amount = len(self.assets)