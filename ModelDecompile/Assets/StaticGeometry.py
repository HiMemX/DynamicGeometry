
def getids(data):
    ids = []

    ids.append(data[0x28:0x30])

    idoffset = int.from_bytes(data[0x44:0x48], "big")
    idnum = int.from_bytes(data[0x39:0x3A], "big")+1

    for i in range(idnum):
        ids.append(data[idoffset:idoffset+0x08])
        idoffset += 0x10
    
    return ids

def checkskin(data):
    idoffset = int.from_bytes(data[0x44:0x48], "big")+0x08
    
    if data[idoffset:idoffset+0x01] == b"\x10": return True
    return False

def getreferenceamount(data):
    return int.from_bytes(data[0x39:0x3A], "big")

def getanimamount(data):
    return int.from_bytes(data[0x33:0x34], "big")