import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

from threading import Thread
import time

import HkLib.HoLib as HoLib
import ModelDecompile.Decompiler as Decompiler
import ModelCompile.Compiler as Compiler
import ModelViewer
import Helpers.LongestDistance as LongestDistance
import Helpers.MidPoint as MidPoint
import Helpers.UrsinaMesher as UrsinaMesher
import Helpers.Wavefront as Wavefront
import Helpers.Mtl as Mtl
import Helpers.Png as Png


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("DynamicGeometry")
        self.parent.geometry("500x520")
        self.parent.resizable(False, False) 
        self.parent.iconbitmap("icon.ico")

        self.parent.bind('<KeyPress>', self.keypress)
        self.parent.bind('<KeyRelease>', self.unpress)
        self.pressed = False

        self.menu = tk.Menu(self.parent)
        self.parent.config(menu=self.menu)

        self.filemenu = tk.Menu(self.menu, tearoff=0)
        self.filemenu.add_command(label="Open   [CTRL+O]", command=self.openfile)
        self.filemenu.add_command(label="Build    [CTRL+S]", command=self.savefile)
        self.filemenu.add_command(label="Build new", command=self.saveasfile)

        self.settingsmenu = tk.Menu(self.menu, tearoff=0)
        self.rotatevar = tk.IntVar(value=1)
        self.wireframevar = tk.IntVar(value=0)
        self.interpolvar = tk.IntVar(value=1)
        self.importintervar = tk.IntVar(value=1)
        self.settingsmenu.add_checkbutton(label="Rotate", command=self.togglerotate, variable=self.rotatevar, onvalue=1, offvalue=0)
        self.settingsmenu.add_checkbutton(label="Wireframe", variable=self.wireframevar, onvalue=1, offvalue=0)
        self.settingsmenu.add_checkbutton(label="Texture Interpolation", command=self.toggleinterpolation, variable=self.interpolvar, onvalue=1, offvalue=0)
        self.settingsmenu.add_separator()
        self.settingsmenu.add_checkbutton(label="Adjust Imported Colors", variable=self.importintervar, onvalue=1, offvalue=0)

        self.infomenu = tk.Menu(self.menu, tearoff=0)
        self.infomenu.add_command(label="Namespaces", command=self.infonamespaces)

        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.menu.add_cascade(label="Settings", menu=self.settingsmenu)
        self.menu.add_cascade(label="Info", menu=self.infomenu)


        self.geomlistframe = ttk.LabelFrame(self.parent, text="Geometries", height=440, width=490)
        self.geomlistframe.pack()

        self.geomlist = tk.Listbox(self.geomlistframe, width=67, height=25)
        self.geomlist.place(x=6, y=5)
        self.geomlist.bind("<<ListboxSelect>>", self.onlistboxselect)


        self.extractframe = ttk.LabelFrame(self.parent, text="Extract", height=50, width=237)
        self.extractframe.place(x=5, y=445)
        
        self.editframe = ttk.LabelFrame(self.parent, text="Edit", height=50, width=237)
        self.editframe.place(x=255, y=445)

        
        self.extractbutton = ttk.Button(self.extractframe, text="Extract Model", command=self.extract, width=14)
        self.extractbutton.place(x=5, y=0)

        self.extractallbutton = ttk.Button(self.extractframe, text="Extract All", command=self.extractall, width=14)
        self.extractallbutton.place(x=120, y=0)

        self.replacebutton = ttk.Button(self.editframe, text="Replace Model", command=self.replace, width=14)
        self.replacebutton.place(x=5, y=0)
        
        self.zerobutton = ttk.Button(self.editframe, text="Zero Model out", command=self.zeroout, width=14)
        self.zerobutton.place(x=120, y=0)


        self.geometries = []
        self.selection = 0
        self.archive = None


    def toggleinterpolation(self):
        if self.interpolvar.get() == 1:
            ModelViewer.urs.Texture.default_filtering = "bilinear"
        else:
            ModelViewer.urs.Texture.default_filtering = None


    def zeroout(self):
        if self.archive == None: return
        if self.geometries[self.selection][3] == False: return

        # Update Ursina Model
        modelvertices = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        modeluvs = [[0, 0], [0, 0], [0, 0]]
        modelfaces = [[0, 1, 2]]

        self.geometries[self.selection][1].model = ModelViewer.urs.Mesh(vertices=modelvertices, uvs=modeluvs, triangles=modelfaces)
        self.geometries[self.selection][1].texture.apply()
        self.geometries[self.selection][2].model = ModelViewer.urs.Mesh(vertices=modelvertices, triangles=modelfaces, mode="line")

        # Update Archive Model
        data = self.geometries[self.selection][0].data
        animamount      = Decompiler.getanimamount(data)
        referenceamount = Decompiler.getreferenceamount(data)
        
        faceid          = Decompiler.getfaceid(data)
        facecoords      = self.getassetcoordinate(faceid)

        indices = b""
        for index in range(3):
            indices += bytes(animamount)
            indices += bytes(referenceamount*2)

        zerodata = b"\x90\x00\x03" + indices

        self.setcoordinatesdata(facecoords, zerodata)

        self.updateselection(self.selection, self.selection)

        tk.messagebox.showinfo("Success", f"Successfully zeroed out {self.geometries[self.selection][0].name}")

    def extractall(self):
        if self.archive == None: return
        if self.geometries[self.selection][3] == False: return

        directory = filedialog.askdirectory()

        if directory=="":
            return
       
        if not tk.messagebox.askokcancel("Warning", "This will create seperate .obj, .mtl and .png files for every model.\nDo you want to continue?"): return

        for index in range(len(self.geometries)):
            self.extractmodel(index, directory)
        
        tk.messagebox.showinfo("Success", f"Successfully extracted {len(self.geometries)} StaticGeometries!")

    def extract(self):
        if self.archive == None: return
        if self.geometries[self.selection][3] == False: return

        directory = filedialog.askdirectory()

        if directory=="":
            return
        
        self.extractmodel(self.selection, directory)

        tk.messagebox.showinfo("Success", f"Successfully extracted {self.geometries[self.selection][0].name}!")

    def extractmodel(self, index, directory):

        data = self.geometries[index][0].data

        textureasset = self.getasset(self.geometries[index][5])
        texture      = Decompiler.rawblobtotexture(textureasset.data)
    
        animamount      = Decompiler.getanimamount(data)
        referenceamount = Decompiler.getreferenceamount(data)
        uvfactor        = self.geometries[index][4]

        vertexid        = Decompiler.getvertexid(data)
        uvid            = Decompiler.getuvid(data)
        faceid          = Decompiler.getfaceid(data)

        vertexasset = self.getasset(vertexid)
        uvasset     = self.getasset(uvid)
        faceasset   = self.getasset(faceid)

        vertices = Decompiler.rawblobtoverts(vertexasset.data)
        uvs      = Decompiler.rawblobtouvs(uvasset.data, uvfactor)
        faces    = Decompiler.rawblobtofaces(faceasset.data, animamount, referenceamount)

        name = self.geometries[index][0].name + f" [{hex(int.from_bytes(self.geometries[index][0].assetid, 'big'))}]"

        Png.savepng(directory, texture, f"{name}")
        Wavefront.saveobj(open(directory+"/"+f"{name}.obj", "w+"), name, vertices, uvs, faces)
        Mtl.savemtl(open(directory+"/"+f"{name}.mtl", "w+"), name)

    def replace(self):
        if self.archive == None: return
        if self.geometries[self.selection][3] == False: return

        directory = filedialog.askopenfilename()

        if directory=="":
            return

        basedirectory = "/".join(directory.split("/")[:-1])

        vertices, uvs, faces, mtllib, usemtl = Wavefront.readobj(open(directory, "r"))
        materials = Mtl.readmtl(open(basedirectory+"/"+mtllib, "r"))
        if materials[usemtl][1] == ":":
            texture = Png.readpng(materials[usemtl])
        else:
            texture = Png.readpng(basedirectory+"/"+materials[usemtl])

        texture = Png.clamp(texture)

        # Update Ursina Model
        modelvertices, modeluvs, modelfaces, modeltexture = UrsinaMesher.mesh(vertices, uvs, faces, texture)
        linefaces = [tri+[tri[0]] for tri in modelfaces]

        self.geometries[self.selection][1].model = ModelViewer.urs.Mesh(vertices=modelvertices, uvs=modeluvs, triangles=modelfaces)
        self.geometries[self.selection][1].texture = ModelViewer.urs.Texture(modeltexture)
        self.geometries[self.selection][1].texture.apply()
        self.geometries[self.selection][2].model = ModelViewer.urs.Mesh(vertices=modelvertices, triangles=linefaces, mode="line")

        # Update Archive Model
        data = self.geometries[self.selection][0].data
        vertexid        = Decompiler.getvertexid(data)
        uvid            = Decompiler.getuvid(data)
        faceid          = Decompiler.getfaceid(data)
        textureid       = self.geometries[self.selection][5]
        animamount      = Decompiler.getanimamount(data)
        referenceamount = Decompiler.getreferenceamount(data)
        uvfactor        = self.geometries[self.selection][4]

        vertexcoords    = self.getassetcoordinate(vertexid)
        uvcoords        = self.getassetcoordinate(uvid)
        facecoords      = self.getassetcoordinate(faceid)
        texturecoords   = self.getassetcoordinate(textureid)

        vertexdata      = Compiler.vertextorawblob(vertices)
        uvdata          = Compiler.uvtorawblob(uvs, uvfactor)
        facedata        = Compiler.facestorawblob(faces, animamount, referenceamount)
        texturedata     = Compiler.texturetorawblob(texture, self.importintervar.get())

        self.setcoordinatesdata(vertexcoords, vertexdata)
        self.setcoordinatesdata(uvcoords, uvdata)
        self.setcoordinatesdata(facecoords, facedata)
        self.setcoordinatesdata(texturecoords, texturedata)

        self.updateselection(self.selection, self.selection)

        tk.messagebox.showinfo("Success", f"Successfully replaced {self.geometries[self.selection][0].name}")

    def setcoordinatesdata(self, coords, data):
        self.archive.mast.sections[0].layers[coords[0]].sublayer.tables[coords[1]].assets[coords[2]].data = data

    def togglerotate(self):
        ModelViewer.rotatespeed = 0.5-ModelViewer.rotatespeed

    def infonamespaces(self):
        if self.archive == None: return

        output = ""
        for namespace in self.archive.mast.sections[0].imports:
            output += namespace + ", "
        tk.messagebox.showinfo("Namespaces", output)

    def updateselection(self, prevselection, newselection):
        self.geometries[prevselection][1].visible = False
        self.geometries[prevselection][2].visible = False

        if not self.geometries[newselection][3]:
            self.replacebutton["state"] = "disabled"
            self.extractbutton["state"] = "disabled"
            self.replacebutton["text"] = "disabled"
            self.extractbutton["text"] = "disabled"
            ModelViewer.debugtext.text = "[Unsupported Model Type]"
            return

        centerpoint = MidPoint.getavrg(self.geometries[newselection][1].model.vertices)
        
        ModelViewer.orbit.position = centerpoint
        ModelViewer.urs.camera.rotation_y = 180
        ModelViewer.urs.camera.rotation_x = 0
        ModelViewer.urs.camera.position = (0, 0, LongestDistance.getlongestdist(centerpoint, self.geometries[newselection][1].model.vertices)*5)

        self.geometries[newselection][1].visible = True
        if self.wireframevar.get():
            self.geometries[newselection][2].visible = True

        #print(type(self.geometries[self.selection][2].texture))

        self.replacebutton["state"] = "normal"
        self.extractbutton["state"] = "normal"
        self.replacebutton["text"] = "Replace Model"
        self.extractbutton["text"] = "Extract Model"

        ModelViewer.debugtext.text = ""

    def onlistboxselect(self, e):
        widget = e.widget
        
        self.updateselection(self.selection, int(widget.curselection()[0]))

        self.selection = int(widget.curselection()[0])

    def getassetcoordinate(self, assetid):
        for li, layer in enumerate(self.archive.mast.sections[0].layers):
            if layer.sublayer_magic == "PSLD": continue
            for ti, table in enumerate(layer.sublayer.tables):
                for ai, asset in enumerate(table.assets):
                    if asset.assetid == assetid:
                        return [li, ti, ai]

    def getasset(self, assetid):
        for layer in self.archive.mast.sections[0].layers:
            if layer.sublayer_magic == "PSLD": continue
            for table in layer.sublayer.tables:
                for asset in table.assets:
                    if asset.assetid == assetid:
                        return asset

    def updatelistbox(self):
        self.geomlist.delete(0,'end')
        starttime = time.time()
        for layer in self.archive.mast.sections[0].layers:
            if layer.sublayer_magic == "PSLD": continue
            for table in layer.sublayer.tables:
                for asset in table.assets:
                    if asset.assettype == b"\x86\xEF\x29\x78" or asset.assettype == b"\x66\xEC\x03\x1B":
                        data = asset.data

                        if Decompiler.checkskin(data):
                            self.geometries.append([asset, ModelViewer.urs.Entity(model="cube", visible=False), ModelViewer.urs.Entity(model="cube", visible=False), False]) # -> Assetclass, Entity, IsEditable
                            continue

                        vertexid        = Decompiler.getvertexid(data)
                        uvid            = Decompiler.getuvid(data)
                        faceid          = Decompiler.getfaceid(data)
                        animamount      = Decompiler.getanimamount(data)
                        referenceamount = Decompiler.getreferenceamount(data)
                        
                        materialid      = Decompiler.getmaterialid(data)
                        materialasset   = self.getasset(materialid)

                        if not Decompiler.getvalidmaterial(materialasset.data):
                            self.geometries.append([asset, ModelViewer.urs.Entity(model="cube", visible=False), ModelViewer.urs.Entity(model="cube", visible=False), False]) # -> Assetclass, Entity, IsEditable
                            continue

                        effectid        = Decompiler.geteffectassetid(materialasset.data)
                        textureassetid  = Decompiler.gettextureassetid(materialasset.data)

                        effectasset     = self.getasset(effectid)
                        textureastasset = self.getasset(textureassetid)
                        genericshaderid = Decompiler.getgenericshaderid(effectasset.data)
                        textureid       = Decompiler.gettextureid(textureastasset.data)
                        genshaderasset  = self.getasset(genericshaderid)
                        uvfactor        = Decompiler.getuvfactor(genshaderasset.data)

                        vertexasset = self.getasset(vertexid)
                        uvasset     = self.getasset(uvid)
                        faceasset   = self.getasset(faceid)
                        textureasset= self.getasset(textureid)

                        vertices = Decompiler.rawblobtoverts(vertexasset.data)
                        uvs      = Decompiler.rawblobtouvs(uvasset.data, uvfactor)
                        faces    = Decompiler.rawblobtofaces(faceasset.data, animamount, referenceamount)
                        texture  = Decompiler.rawblobtotexture(textureasset.data)

                        try: # Try and except cause I can't anymore
                            vertices, uvs, faces, texture = UrsinaMesher.mesh(vertices, uvs, faces, texture)
                            linefaces = [tri+[tri[0]] for tri in faces]

                        except:
                            self.geometries.append([asset, ModelViewer.urs.Entity(model="cube", visible=False), ModelViewer.urs.Entity(model="cube", visible=False), False]) # -> Assetclass, Entity, IsEditable
                            continue

                        self.geometries.append([asset,
                            ModelViewer.urs.Entity(model=ModelViewer.urs.Mesh(vertices=vertices, uvs=uvs, triangles=faces), texture=ModelViewer.urs.Texture(texture), double_sided = True, visible=False),
                            ModelViewer.urs.Entity(model=ModelViewer.urs.Mesh(vertices=vertices, triangles=linefaces, mode="line"), visible=False),
                            True,
                            uvfactor,
                            textureid])
        
        self.updateselection(0, 0)
        self.selection = 0
        
        for asset in self.geometries:
            self.geomlist.insert("end", asset[0].name)

        totaltime = time.time()-starttime
        tk.messagebox.showinfo("Success", f"Decompiled {len(self.geometries)} StaticGeometries in {totaltime}s!")

    def cleanup(self):
        for geometry in self.geometries:
            ModelViewer.urs.destroy(geometry[1])
            ModelViewer.urs.destroy(geometry[2])
            del geometry[1]
            del geometry[2]
        
        self.geometries = []

    def openfile(self):
        directory = filedialog.askopenfilename(filetypes=(("HkOArchives", "*.ho"),))

        if directory=="":
            return

        self.cleanup()
        temparchive = HoLib.hkOArchive(directory)
        if not temparchive.game in ["SB09", "Up", "UFCT"]:
            tk.messagebox.showerror("Failed", f"'{temparchive.game}' isn't supported!")
            return

        self.archive = temparchive
        self.archive.username = "dyngeometry_autobuild"
        self.archive.compiler = "DynGeometry:hkOArchive.Save"


        self.parent.title(f"DynamicGeometry - [{self.archive.path}]")

        tk.messagebox.showinfo("Success", f"""Compilation Date:   {self.archive.date}

Magic:   {self.archive.magic}
Endianess:   {self.archive.endian}
Platform:   {self.archive.platform}
Username:   {self.archive.username}
Target:   {self.archive.game}
Compiler:   {self.archive.compiler}
Hash:   {self.archive.hash}""")

        self.updatelistbox()

    def savefile(self):
        if self.archive == None: return

        starttime = time.time()

        self.archive.Update()
        self.archive.Save()

        totaltime = time.time()-starttime
        tk.messagebox.showinfo("Success", f"Built in {totaltime}s!")
    
    def saveasfile(self):
        if self.archive == None: return

        starttime = time.time()
        f = filedialog.asksaveasfile(mode='wb', defaultextension=".ho")

        self.archive.compiler = "DynGeometry:hkOArchive.SaveAs"

        self.archive.Update()
        self.archive.SaveAs(f)

        totaltime = time.time()-starttime
        tk.messagebox.showinfo("Success", f"Built in {totaltime}s!")

    def unpress(self, e):
        self.pressed = False

    def keypress(self, e):
        if self.pressed: return

        if e.keycode == 79: self.openfile()
        elif e.keycode == 67: self.savefile()

        else: return

        self.pressed = True

def run():
    global root
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
    
    ModelViewer.destroy = True
    
    
if __name__ == "__main__":
    main = Thread(target=run).start()
    
    ModelViewer.init()
    ModelViewer.app.run()