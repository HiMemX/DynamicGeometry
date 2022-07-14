from PIL import Image
import numpy as np

def mesh(verts, normals, uvs, faces, texture):
    newverts = []
    newuvs = []
    newnormals = []

    for tri in faces:
        for index in tri:
            newverts.append(verts[index[0]])
            #print("index")
            newuvs.append(uvs[index[1]])
            #print("UV APPENDED")
            newnormals.append(normals[index[2]])
            #print("NORMAL APPENDED")

    #print("Geometry Generated")

    newtexture = Image.fromarray(np.array([np.array([[x[0], x[1], x[2], 255] for x in i], np.uint8) for i in texture[0]], np.uint8), "RGBA")
    
    if len(texture) > 1: 
        rgbaarray = np.array([np.array([x for x in i], np.uint8) for i in texture[1]], np.uint8)
        rgbaimage = Image.fromarray(rgbaarray, "L")

        newtexture.putalpha(rgbaimage)

    return newverts, newnormals, newuvs, [[i, i+1, i+2] for i in range(0, len(newverts), 3)], newtexture
