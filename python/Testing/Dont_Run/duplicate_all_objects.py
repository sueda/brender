import bpy
import mathutils

for obj in bpy.data.objects:
    if obj.name.startswith("0"):
        theobj = bpy.data.objects[obj.name]
        theobj.select = True
        ##theobj.duplicate()
        ##duplicates and selects the new object
        bpy.ops.object.duplicate()
        myobject = bpy.context.active_object
        print("Active Obj: ", myobject.name, "\n")