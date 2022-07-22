
def readobj(file):
    verts = []
    uvs = []
    tempuvs = []
    normals = []
    faces = []
    mtllib = ""
    usemtl = []
    valid = True

    for li, line in enumerate(file.readlines()):
        if line[:2] == "v ":
            vert = [float(axis) for axis in line[2:-1].split(" ")]
            vert[0] = -vert[0]
            verts.append(vert)
        
        elif line[:2] == "vt":
            uv = [float(axis) for axis in line[3:-1].split(" ")]
            if uv[0] > 1 or uv[0] < 0 or uv[1] > 1 or uv[1] < 0:
                valid = False
            #uvs.append([float(axis) for axis in line[3:-1].split(" ")])
            tempuvs.append(uv)
        
        elif line[:2] == "vn":
            normals.append([float(axis) for axis in line[3:-1].split(" ")])
           
        elif line[:1] == "f":
            face = []
            for index in line[2:-1].split(" "):
                face.append([int(i)-1 for i in index.split("/")][:(2+(len(normals)>0))])
            faces.append(face)

        elif line[:6] == "usemtl":
            usemtl.append(line[7:-1])
            uvs.append(tempuvs) # This Temp UV stuff is so we can properly transform them later for the Atlas
            tempuvs = []
            
        elif line[:6] == "mtllib":
            mtllib = line[7:-1]

    return verts, uvs, normals, faces, mtllib, usemtl, valid

def saveobj(file, name, verts, normals, uvs, faces):
    file.write(f"mtllib {name}.mtl\n")
    file.write(f"o {name}\n")

    for vert in verts:
        file.write(f"v {-vert[0]} {vert[1]} {vert[2]}\n")

    for uv in uvs:
        file.write(f"vt {uv[0]} {uv[1]}\n")
        
    for normal in normals:
        file.write(f"vn {normal[0]} {normal[1]} {normal[2]}\n")

    file.write("usemtl shader\n") 
    
    for fi, face in enumerate(faces):
        #file.write(f"f {face[0][0]+1} {face[1][0]+1} {face[2][0]+1}\n")
        file.write(f"f {face[0][0]+1}/{face[0][1]+1}/{face[0][2]+1} {face[1][0]+1}/{face[1][1]+1}/{face[1][2]+1} {face[2][0]+1}/{face[2][1]+1}/{face[2][2]+1}\n")