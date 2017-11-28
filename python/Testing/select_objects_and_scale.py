import bpy
import mathutils

for obj in bpy.data.objects:
    if obj.name.startswith("0"):
        theobj = bpy.data.objects[obj.name]
        theobj.select = True
        theobj.scale=(3,3,3)
        vec = mathutils.Vector((0.0,0.0,1.0))
        theobj.location = theobj.location + vec
        theobj.select = False