
def readmtl(file):
    textures = {}
    for line in file.readlines():
        if line[:6] == "newmtl":
            currmtl = line[7:-1]

        elif line[:6] == "map_Kd":
            textures[currmtl] = line[7:-1]

    return textures

def savemtl(file, name):
    file.write(f"newmtl shader\n")
    file.write("Ns 0\n")
    file.write("Ka 1.0 1.0 1.0\n")
    file.write("Kd 1 1 1\n")
    file.write("Ks 0 0 0\n")
    file.write(f"map_Kd {name}.png\n")
    file.write("illum 0\n")