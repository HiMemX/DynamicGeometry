# DynamicGeometry
A "Spongebobs Truth or Square" (2009) StaticGeometry editor.

DynamicGeometry is an editor written in Python using the Ursina wrapper, capable of dissecting a SB09 (And partially Up) .ho files StaticGeometries and SkinGeometries.


Settings:

Rotate -> If the model viewer automatically spins around the object

Wireframe -> If the models wireframe is shown (Helpful with transparency bugs)

Texture Interpolation -> If the textures get smoothened out by Ursina



Adjust Imported Colors -> If the imported models textures get adjusted to be less bright

Note:
Imported textures sizes get clamped down to the nearest power of 2 (16, 32, 64, 128, 256...). This will mess up UVs, so make sure to properly format your textures.
