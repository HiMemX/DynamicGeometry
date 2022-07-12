import HkLib.Static.SECT as SECT
import HkLib.Helpers.MoreMath as MoreMath

class MAST:
    def __init__(self, file, endian):
        self.endian = endian
        self.Construct(file, endian)

    def Construct(self, file, endian):
        self.magic = file.read(0x04).decode("ANSI")
        self.amount = int.from_bytes(file.read(0x04), endian)
        file.read(0x04)
        self.definition_length = int.from_bytes(file.read(0x04), endian)
        self.import_length = int.from_bytes(file.read(0x04), endian)
        self.unknown0 = int.from_bytes(file.read(0x04), endian)
        file.read(0x08)

        self.sections = [SECT.SECT(file, endian) for sect in range(self.amount)]

    def Update(self):
        self.amount = len(self.sections)
        self.definition_length = 0x20 + 0x40*self.amount
        self.import_length = sum([sum([MoreMath.RoundUp(0x0D + len(curr_import), 0x04) for curr_import in section.imports]) for section in self.sections]) + len(self.sections[0].path) + 0x01 # I particullarly like this line

        [section.Update() for section in self.sections]

    def GetBytes(self):
        bytecode = b""
        bytecode += self.magic.encode("ANSI")
        bytecode += self.amount.to_bytes(4, byteorder=self.endian)
        bytecode += bytes(0x04)
        bytecode += self.definition_length.to_bytes(4, byteorder=self.endian)
        bytecode += self.import_length.to_bytes(4, byteorder=self.endian)
        bytecode += self.unknown0.to_bytes(4, byteorder=self.endian)
        bytecode += bytes(0x08)

        for section in self.sections:
            bytecode += section.GetData()

        return bytecode

