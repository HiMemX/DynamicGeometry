

def triangulate(faces):
    newfaces = []

    for face in faces:
        for facegen in range(1, len(face)-1):
            newfaces.append([face[0], face[facegen], face[facegen+1]])

    return newfaces