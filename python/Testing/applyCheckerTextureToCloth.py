import bpy, os
import mathutils

mat = bpy.data.materials['ClothMaterial']

for obj in bpy.data.objects:
    if obj.name.endswith("Cloth1"):
        theobj = bpy.data.objects[obj.name]
        theobj.select = True
        objdata = obj.data
        # append Material
        objdata.materials.append(mat)
        theobj.select = False