import bpy, os
import mathutils

mat = bpy.data.materials['CubeMaterial']

for obj in bpy.data.objects:
    if obj.name.endswith("Sphere"):
        theobj = bpy.data.objects[obj.name]
        theobj.select = True
        objdata = obj.data
        # append Material
        objdata.materials.append(mat)
        theobj.select = False