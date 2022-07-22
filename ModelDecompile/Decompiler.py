import ModelDecompile.Assets.RawBlobs.VertexRawBlob as Vertex
import ModelDecompile.Assets.RawBlobs.UVRawBlob as UV
import ModelDecompile.Assets.RawBlobs.FaceRawBlob as Face
import ModelDecompile.Assets.RawBlobs.TextureRawBlob as Texture
import ModelDecompile.Assets.RawBlobs.NormalRawBlob as Normal
import ModelDecompile.Assets.RawBlobs.PfstVertexRawBlob as PfstVertex

import ModelDecompile.Assets.StaticGeometry as StaticGeometry
import ModelDecompile.Assets.Material as Material
import ModelDecompile.Assets.Effect as Effect
import ModelDecompile.Assets.GenericShader as GenericShader
import ModelDecompile.Assets.Texture as TextureAsset

def getvalidmaterial(data):
    return len(Material.getids(data)) > 1

def getuvfactor(data):
    return GenericShader.getfactor(data)

def gettextureid(data):
    return TextureAsset.getid(data)

def getgenericshaderid(data):
    return Effect.getid(data)

def geteffectassetid(data):
    ids = Material.getids(data)
    
    if len(ids) == 0:
        return None

    return ids[0]

def gettextureassetid(data):
    ids = Material.getids(data)
    
    if len(ids) == 0:
        return None

    return ids[1]


def getmaterialid(data):
    return StaticGeometry.getids(data)[0]

def getvertexid(data):
    return StaticGeometry.getids(data)[1]

def getuvid(data):
    return StaticGeometry.getids(data)[-2]

def getfaceid(data):
    return StaticGeometry.getids(data)[-1]

def getnormalid(data):
    return StaticGeometry.getids(data)[2]

def getgeomtextureassetid(data):
    return StaticGeometry.gettextureids(data)


def rawblobtoverts(data):
    return Vertex.toverts(data)

def rawblobtouvs(data, uvfactor):
    return UV.touvs(data, uvfactor)
    
def rawblobtofaces(data, animamount, referenceamount, pfst):
    return Face.tofaces(data, animamount, referenceamount, pfst)

def rawblobtotexture(data):
    return Texture.totexture(data)

def rawblobtonormals(data):
    return Normal.tonormals(data)

def pfstrawblobtoverts(data):
    return PfstVertex.toverts(data)

def pfstrawblobtonormals(data):
    return PfstVertex.tonormals(data)


def checkskin(data):
    return StaticGeometry.checkskin(data)

def getanimamount(data):
    return StaticGeometry.getanimamount(data)

def getreferenceamount(data):
    return StaticGeometry.getreferenceamount(data)