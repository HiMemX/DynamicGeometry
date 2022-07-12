import HkLib.Static.Table as Table
import HkLib.Helpers.MoreHex as MoreHex
import HkLib.Helpers.MoreMath as MoreMath

class PSL:
    def __init__(self, file, endian, offset):
        self.endian = endian
        self.Construct(file, endian, offset)

    def Construct(self, file, endian, offset):
        self.length = int.from_bytes(file.read(0x04), endian)
        self.entry_amount = int.from_bytes(file.read(0x04), endian)
        return_addr = file.tell()

        dirs = []
        datas = []
        total_offset = offset

        file.read(0x04)
        self.identifier = int.from_bytes(file.read(0x04), endian) # Just to check if the data layer comes first or not
        file.seek(return_addr)
        if self.identifier == 0: # It doesn't come first
            for table in range(int((self.entry_amount-1)/3)):
                file.read(0x0C)
                length = int.from_bytes(file.read(0x04), endian)
                dirs.append([total_offset, length])
                total_offset += length
            
            file.read(0x0C)
            total_offset += int.from_bytes(file.read(0x04), endian)

            for table in range(int((self.entry_amount-1)/3)):
                file.read(0x1C)
                length = int.from_bytes(file.read(0x04), endian)
                datas.append([total_offset, length])
                total_offset += length

        else: # It does
            for table in range(int((self.entry_amount-1)/3)):
                file.read(0x1C)
                length = int.from_bytes(file.read(0x04), endian)
                datas.append([total_offset, length])
                total_offset += length
                
            file.read(0x0C)
            total_offset += int.from_bytes(file.read(0x04), endian)
            
            for table in range(int((self.entry_amount-1)/3)):
                file.read(0x0C)
                length = int.from_bytes(file.read(0x04), endian)
                dirs.append([total_offset, length])
                total_offset += length
        self.tables = [Table.Table(file, endian, dirs[table], datas[table]) for table in range(int((self.entry_amount-1)/3))]

    def GetBytes0(self):
        bytecode = b""
        bytecode += bytes(0x04)

        padding_length = 0

        if self.identifier == 0:
            for table in self.tables:
                bytecode += table.GetBytes0()
                padding_length += table.dir_length

            bytecode += 0x02.to_bytes(4, byteorder=self.endian)
            bytecode += bytes(0x04)
            bytecode += (MoreMath.RoundUp(padding_length, 0x800) - padding_length).to_bytes(4, byteorder=self.endian)
            bytecode += bytes(0x04)

            for table in self.tables:
                bytecode += table.GetBytes1()

        else:
            for table in self.tables:
                bytecode += table.GetBytes1()
                padding_length += table.data_length

            bytecode += 0x02.to_bytes(4, byteorder=self.endian)
            bytecode += bytes(0x04)
            bytecode += (MoreMath.RoundUp(padding_length, 0x800) - padding_length).to_bytes(4, byteorder=self.endian)
            bytecode += bytes(0x04)

            for table in self.tables:
                bytecode += table.GetBytes0()

        return bytecode

    def GetBytes1(self):
        bytecode = b""

        if self.identifier == 0:
            for table in self.tables:
                bytecode += table.GetBytes2()
            
            bytecode += MoreHex.GenerateBytes(b"\x33", MoreMath.RoundUp(len(bytecode), 0x800) - len(bytecode))

            for table in self.tables:
                bytecode += table.GetBytes3()

        else:
            for table in self.tables:
                bytecode += table.GetBytes3()
            
            bytecode += MoreHex.GenerateBytes(b"\x33", MoreMath.RoundUp(len(bytecode), 0x800) - len(bytecode))

            for table in self.tables:
                bytecode += table.GetBytes2()

        bytecode += MoreHex.GenerateBytes(b"\x33", MoreMath.RoundUp(len(bytecode), 0x800) - len(bytecode))

        return bytecode

    def Update(self):
        [table.Update() for table in self.tables]

