import ModelCompile.Assets.RawBlobs.VertexRawBlob as Vertex
import ModelCompile.Assets.RawBlobs.UVRawBlob as UV
import ModelCompile.Assets.RawBlobs.FaceRawBlob as Face
import ModelCompile.Assets.RawBlobs.TextureRawBlob as Texture
import ModelCompile.Assets.RawBlobs.NormalRawBlob as Normal

def vertextorawblob(verts):
    return Vertex.torawblob(verts)

def uvtorawblob(uvs, factor):
    return UV.torawblob(uvs, factor)

def normaltorawblob(normals):
    return Normal.torawblob(normals)

def facestorawblob(faces, animamount, referenceamount):
    return Face.torawblob(faces, animamount, referenceamount)
    
def texturetorawblob(texture, interpolate):
    return Texture.torawblob(texture, interpolate)