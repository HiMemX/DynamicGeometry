import HkLib.Static.MAST as MAST
import HkLib.Helpers.WideString as WideString
import time
import datetime
import HkLib.Static.Asset as Asset
import HkLib.Helpers.MoreMath as MoreMath

class hkOArchive:
    def __init__(self, path):
        self.path = path
        self.Construct(open(path, "rb"))

    def Construct(self, file):
        file.seek(0x47)
        self.endian = ["little", "big"][int.from_bytes(file.read(0x01), "big")]
        endian = self.endian
        file.seek(0x00)

        self.magic = file.read(0x03).decode("ANSI")

        file.seek(0x10)
        self.timestamp = int.from_bytes(file.read(0x08), endian)
        self.date      = file.read(0x18).decode("ANSI")

        file.read(0x10)
        self.offset_to_mast = int.from_bytes(file.read(0x04), endian)
        self.unknown0 = int.from_bytes(file.read(0x04), endian)
        self.mast_sect_imp_length = int.from_bytes(file.read(0x04), endian)

        file.seek(0x3FC)
        self.platform = WideString.ReadWideString(file, 0x20, endian)
        self.username = WideString.ReadWideString(file, 0x20, endian)
        self.game     = WideString.ReadWideString(file, 0x20, endian)
        self.compiler = WideString.ReadWideString(file, 0x20, endian); file.read(0x100)
        self.hash     = WideString.ReadWideString(file, 0x20, endian)

        file.seek(self.offset_to_mast)
        self.mast = MAST.MAST(file, endian)

    def Update(self):
        self.mast.Update()

    def GetBytes(self):
        bytecode = b""
        bytecode += self.magic.encode("ANSI") + b"\x1A"
        bytecode += bytes(0x0C)
        bytecode += (int(time.time())).to_bytes(8, byteorder=self.endian)
        bytecode += (datetime.datetime.now().strftime('%c')).encode("ANSI")
        
        bytecode += bytes(0x10)
        bytecode += self.offset_to_mast.to_bytes(4, byteorder=self.endian)
        bytecode += self.unknown0.to_bytes(4, byteorder=self.endian)
        bytecode += self.mast_sect_imp_length.to_bytes(4, byteorder=self.endian)

        bytecode += bytes(0x3B4)

        bytecode += WideString.GetWideString(self.platform, 0x3C, self.endian)
        bytecode += WideString.GetWideString(self.username, 0x40, self.endian)
        bytecode += WideString.GetWideString(self.game, 0x40, self.endian)
        bytecode += WideString.GetWideString(self.compiler, 0x40, self.endian); bytecode += bytes(0x100)
        bytecode += WideString.GetWideString(self.hash, 0x40, self.endian)

        bytecode += bytes(0x1c4)

        return bytecode + self.mast.GetBytes()


    def SaveAs(self, wrapper):
        bytecode = self.GetBytes()

        wrapper.write(bytecode)

    def Save(self):
        bytecode = self.GetBytes()
        
        open(self.path, "wb").write(bytecode)

    def NewAsset(self, li, ti, id_in, type_in, name_in, data_in):
        length_padding = MoreMath.RoundUp(len(data_in), 0x40)
        length         = len(data_in)
        unknown0       = [4, 16, 32][ti]
        assetid        = id_in
        assettype      = type_in
        unknown1       = 1
        data           = data_in
        name           = name_in

        asset = Asset.Asset(None, self.endian, [length_padding, length, unknown0, assetid, assettype, unknown1, data, name])
        self.mast.sections[0].layers[li].sublayer.tables[ti].assets.append(asset)

        for layer in self.mast.sections[0].layers:
            if layer.sublayer_magic != "PSLD":
                continue
            
            layer.sublayer.floats.append(1)
            layer.sublayer.names[assetid] = name
            break
        


if __name__ == "__main__":
    start = time.time()
    test = hkOArchive(r"C:\Users\felix\Desktop\Research hoes\SHUB -do not edit.ho - Kopie (3).bak.bak", "big")
    created = time.time()
    test.Update()
    updated = time.time()
    test.Save()
    saved = time.time()
    print(f"Created: {created-start}")
    print(f"Updated: {updated-start}")
    print(f"Saved: {saved-start}")
    