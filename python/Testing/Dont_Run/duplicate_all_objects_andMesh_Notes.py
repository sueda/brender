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
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.delete(type='ONLY_FACE')
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.convert(target='CURVE')
        myobject.data.bevel_depth=0.031
        myobject.data.fill_mode='FULL'
        myobject.data.bevel_resolution = 2
        


