import bpy
import mathutils

for obj in bpy.data.objects:
    if obj.name.startswith("0"):
        theobj = bpy.data.objects[obj.name]
        theobj.select = True
        theobj.scale=(2,2,2)
        vec = mathutils.Vector((0.0,0.0,2.0))
        theobj.location = theobj.location + vec