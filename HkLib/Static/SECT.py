import HkLib.Helpers.String as String
import HkLib.Helpers.MoreMath as MoreMath
import HkLib.Helpers.MoreHex as MoreHex
import HkLib.Static.Layer as Layer

class SECT:
    def __init__(self, file, endian):
        self.endian = endian
        self.Construct(file, endian)
    
    def Construct(self, file, endian):
        # -- Metadata -- #
        self.magic = String.ReadString(file, 0x04, endian)
        self.flag = int.from_bytes(file.read(0x04), "big")
        file.read(0x04)
        self.unknown0 = int.from_bytes(file.read(0x04), endian)
        self.definition_length = int.from_bytes(file.read(0x04), endian)
        file.read(0x04)
        self.unknown1 = int.from_bytes(file.read(0x04), endian)
        self.data_offset = int.from_bytes(file.read(0x04), endian)*0x800
        self.data_length = int.from_bytes(file.read(0x04), endian)
        file.read(0x04)
        self.unknown2 = int.from_bytes(file.read(0x04), endian)
        file.read(0x04)
        self.unknown3 = int.from_bytes(file.read(0x04), endian)
        file.read(0x04)
        self.unknown4 = int.from_bytes(file.read(0x04), endian)
        file.read(0x04)

        self.imports = []
        while file.tell() < self.definition_length+0x800:
            file.read(0x0C)
            self.imports.append(String.ReadUntil(file, b"\x00"))
            file.seek(MoreMath.RoundUp(file.tell(), 0x4))
        
        self.path = String.ReadUntil(file, b"\x00")

        file.seek(self.data_offset)

        file.read(0x04)
        self.layer_amount = int.from_bytes(file.read(0x04), endian)
        file.read(0x04)
        self.layers_definition_length = int.from_bytes(file.read(0x04), endian)
        self.unknown5 = int.from_bytes(file.read(0x04), endian)
        self.layers_definition_length_path = int.from_bytes(file.read(0x04), endian)
        self.layers_data_length = int.from_bytes(file.read(0x04), endian)
        file.read(0x04)

        self.layers = [Layer.Layer(file, endian, self.data_offset) for layer in range(self.layer_amount)]

        names = {}

        for layer in self.layers:
            if layer.sublayer_magic == "PSLD":
                names.update(layer.sublayer.names)

        for layer in self.layers:
            if layer.sublayer_magic == "PSLD":
                continue

            for table in layer.sublayer.tables:
                for asset in table.assets:
                    asset.name = names[asset.assetid]

    def GetData(self):
        bytecode = b""
        bytecode += String.ToString(self.magic, self.endian)
        bytecode += self.flag.to_bytes(4, byteorder=self.endian)
        bytecode += bytes(0x04)
        bytecode += self.unknown0.to_bytes(4, byteorder=self.endian)
        bytecode += self.definition_length.to_bytes(4, byteorder=self.endian)
        bytecode += bytes(0x04)
        bytecode += self.unknown1.to_bytes(4, byteorder=self.endian)
        bytecode += int(self.data_offset/0x800).to_bytes(4, byteorder=self.endian)
        bytecode += self.data_length.to_bytes(4, byteorder=self.endian)
        bytecode += self.data_length.to_bytes(4, byteorder=self.endian)
        bytecode += self.unknown2.to_bytes(4, byteorder=self.endian)
        bytecode += bytes(0x04)
        bytecode += self.unknown3.to_bytes(4, byteorder=self.endian)
        bytecode += bytes(0x04)
        bytecode += self.unknown4.to_bytes(4, byteorder=self.endian)
        bytecode += bytes(0x04)

        for imp in self.imports:
            bytecode += b"\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE"
            bytecode += imp.encode("ANSI") + b"\x00"
            bytecode += MoreHex.GenerateBytes(b"\x33", MoreMath.RoundUp(len(bytecode), 0x04)-len(bytecode))

        bytecode += self.path.encode("ANSI") + b"\x00"
        
        bytecode += MoreHex.GenerateBytes(b"\x33", MoreMath.RoundUp(len(bytecode)+0x20, 0x800)-(len(bytecode)+0x20))

        bytecode += self.magic.encode("ANSI")
        bytecode += self.layer_amount.to_bytes(4, byteorder=self.endian)
        bytecode += bytes(0x04)
        bytecode += self.layers_definition_length.to_bytes(4, byteorder=self.endian)
        bytecode += self.unknown5.to_bytes(4, byteorder=self.endian)
        bytecode += self.layers_definition_length_path.to_bytes(4, byteorder=self.endian)
        bytecode += self.layers_data_length.to_bytes(4, byteorder=self.endian)
        bytecode += bytes(0x04)

        for layer in self.layers:
            bytecode += layer.GetBytes0()

        bytecode += self.path.encode("ANSI") + b"\x00"
        bytecode += MoreHex.GenerateBytes(b"\x33", MoreMath.RoundUp(len(bytecode), 0x20)-len(bytecode))

        for layer in self.layers:
            bytecode += layer.GetBytes1()
        
        bytecode += MoreHex.GenerateBytes(b"\x33", MoreMath.RoundUp(len(bytecode)+0x20, 0x800)-len(bytecode)-0x20)

        for layer in self.layers:
            bytecode += layer.GetBytes2()

        return bytecode

    def Update(self):
        for layer in self.layers:
            layer.Update()
        for layer in range(1, len(self.layers)):
            self.layers[layer].data_offset = int(MoreMath.RoundUp(self.layers[layer-1].data_length + self.layers[layer-1].data_offset, 0x800))

