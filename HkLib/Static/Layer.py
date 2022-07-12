import HkLib.Helpers.String as String
import HkLib.Helpers.MoreMath as MoreMath
import HkLib.Static.PSL as PSL
import HkLib.Static.PSLD as PSLD

class Layer:
    def __init__(self, file, endian, rel_offset):
        self.endian = endian
        self.Construct(file, endian, rel_offset)

    def Construct(self, file, endian, rel_offset):
        self.type = String.ReadString(file, 0x04, endian)
        self.flag = int.from_bytes(file.read(0x04), "big")
        file.read(0x04)
        self.unknown0 = int.from_bytes(file.read(0x04), endian)
        self.layers_definition_length = int.from_bytes(file.read(0x04), endian)
        self.unknown5 = int.from_bytes(file.read(0x04), endian)
        self.unknown1 = int.from_bytes(file.read(0x04), endian)
        self.data_offset = int.from_bytes(file.read(0x04), endian)*0x800
        self.data_length = int.from_bytes(file.read(0x04), endian)
        file.read(0x04)
        self.unknown2 = int.from_bytes(file.read(0x04), endian)
        file.read(0x04)
        self.unknown4 = int.from_bytes(file.read(0x04), endian)
        self.unknown3 = int.from_bytes(file.read(0x04), endian)
        self.data_description_offset = int.from_bytes(file.read(0x04), endian)
        file.read(0x04)

        return_addr = file.tell()
        file.seek(rel_offset+self.data_description_offset)
        self.sublayer_magic = file.read(0x04).decode("ANSI")

        if self.sublayer_magic != "PSLD":
            self.sublayer = PSL.PSL(file, endian, self.data_offset)

        elif self.sublayer_magic == "PSLD":
            self.sublayer = PSLD.PSLD(file, endian)
            file.seek(self.data_offset)
            self.sublayer.GetData(file, endian)

        file.seek(return_addr)

    def GetBytes0(self):
        bytecode = b""
        bytecode += String.ToString(self.type, self.endian)
        bytecode += self.flag.to_bytes(4, byteorder=self.endian)
        bytecode += bytes(0x04)
        bytecode += self.unknown0.to_bytes(4, byteorder=self.endian)
        bytecode += self.layers_definition_length.to_bytes(4, byteorder=self.endian)
        bytecode += self.unknown5.to_bytes(4, byteorder=self.endian)
        bytecode += self.unknown1.to_bytes(4, byteorder=self.endian)
        bytecode += int(self.data_offset/0x800).to_bytes(4, byteorder=self.endian)
        bytecode += self.data_length.to_bytes(4, byteorder=self.endian)
        bytecode += self.data_length.to_bytes(4, byteorder=self.endian)
        bytecode += self.unknown2.to_bytes(4, byteorder=self.endian)
        bytecode += bytes(0x04)
        bytecode += self.unknown4.to_bytes(4, byteorder=self.endian)
        bytecode += self.unknown3.to_bytes(4, byteorder=self.endian)
        bytecode += self.data_description_offset.to_bytes(4, byteorder=self.endian)
        bytecode += bytes(0x04)

        return bytecode

    def GetBytes1(self):
        bytecode = b""
        bytecode += self.sublayer_magic.encode("ANSI")
        bytecode += self.sublayer.length.to_bytes(4, byteorder=self.endian)
        bytecode += self.sublayer.entry_amount.to_bytes(4, byteorder=self.endian)

        bytecode += self.sublayer.GetBytes0()
        #if self.sublayer_magic == "PSLD":

        #else:
            # CONTINUE HERE
            # Hey tomorrow Felix! :) How did the english homework go?   # Tomorrow Felix here, it went quite well!
        return bytecode

    def GetBytes2(self):
        return self.sublayer.GetBytes1()

    def Update(self):
        self.sublayer.Update()

        if self.sublayer_magic == "PSLD":
            self.sublayer.entry_amount = len(self.sublayer.names)
            return
        total_offset = 0
        if self.sublayer.identifier == 0:
            for table in self.sublayer.tables:
                table.dir_rel_offset = total_offset
                total_offset += table.dir_length
                
        else:
            for table in self.sublayer.tables:
                total_offset += table.data_length

            total_offset = MoreMath.RoundUp(total_offset, 0x800)
            
            for table in self.sublayer.tables:
                table.dir_rel_offset = total_offset
                total_offset += table.dir_length

        total_offset = 0
        for table in self.sublayer.tables:
            for asset in table.assets:
                asset.offset = total_offset
                total_offset += asset.length_padding

        if self.sublayer.tables[0].dir_offset < self.sublayer.tables[0].data_offset:
            self.data_length = MoreMath.RoundUp(sum([table.dir_length for table in self.sublayer.tables]), 0x800) + sum([table.data_length for table in self.sublayer.tables])

        elif self.sublayer.tables[0].dir_offset > self.sublayer.tables[0].data_offset:
            self.data_length = MoreMath.RoundUp(sum([table.data_length for table in self.sublayer.tables]), 0x800) + sum([table.dir_length for table in self.sublayer.tables])
