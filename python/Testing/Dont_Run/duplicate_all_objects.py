# import bpy
# import mathutils

# for obj in bpy.data.objects:
#     if obj.name.startswith("0"):
#         theobj = bpy.data.objects[obj.name]
#         theobj.select = True
#         ##theobj.duplicate()
#         ##duplicates and selects the new object
#         bpy.ops.object.duplicate()
#         myobject = bpy.context.active_object
#         print("Active Obj: ", myobject.name, "\n")

import bpy
import mathutils

scn = bpy.context.scene

for obj in bpy.data.objects:
    if obj.name.startswith("0"):
        theobj = bpy.data.objects[obj.name]
        theobj.select = True
        ##duplicates and selects the new object
        new_obj = theobj.copy()
        new_obj.data = theobj.data.copy()
        new_obj.animation_data_clear()
        scn.objects.link(new_obj)
        #new_obj.data.delete(type = 'ONLY_FACE')

import bpy
import mathutils
import bmesh

scn = bpy.context.scene

for obj in bpy.data.objects:
    if obj.name.startswith("0"):
        theobj = bpy.data.objects[obj.name]
        ##duplicates and selects the new object
        new_obj = theobj.copy()
        new_obj.data = theobj.data.copy()
        new_obj.animation_data_clear()
        scn.objects.link(new_obj)
        new_obj.select = True
        #get active mesh
        meshobj = bpy.context.edit_object
        mymesh = meshobj.data
        #get Bmesh representation
        mybmesh = bmesh.from_edit_mesh(mymesh)
        faces_select = [f for f in mybmesh.faces if f.select]
        bmesh.ops.delete(mybmesh, geom=faces_select, context=3)
        #show updates and recalculate n-gon tesselation
        bmesh.update_edit_mesh(mymesh, True)

##-------------------------------------

import bpy
import mathutils
import bmesh

scn = bpy.context.scene

for obj in bpy.data.objects:
    if obj.name.startswith("0"):
        theobj = bpy.data.objects[obj.name]
        ##duplicates and selects the new object
        new_obj = theobj.copy()
        new_obj.data = theobj.data.copy()
        new_obj.animation_data_clear()
        scn.objects.link(new_obj)
        
        scn.objects.active = new_obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.delete(type='ONLY_FACE')
        bpy.ops.object.mode_set(mode='OBJECT')
        
        new_obj.select=True
        bpy.ops.object.convert(target='CURVE')
        
        bpy.context.object.data.bevel_depth=0.002
        bpy.context.object.data.fill_mode='FULL'
        bpy.context.object.data.bevel_resolution=2
        new_obj.select = False
        
        #new_obj.select = True
        #get active mesh
        ##meshobj = bpy.context.edit_object
        ##mymesh = meshobj.data
        #get Bmesh representation
        ##mybmesh = bmesh.from_edit_mesh(mymesh)
        ##faces_select = [f for f in mybmesh.faces if f.select]
        ##bmesh.ops.delete(mybmesh, geom=faces_select, context=3)
        #show updates and recalculate n-gon tesselation
        ##bmesh.update_edit_mesh(mymesh, True)


import bpy

scn = bpy.context.scene
scn.layers = [True] * 20 # Show all layers

for obj in bpy.data.objects:
    if obj.name.startswith("0"):
        theobj = bpy.data.objects[obj.name]
        ##duplicates and selects the new object
        new_obj = theobj.copy()
        new_obj.data = theobj.data.copy()
        new_obj.animation_data_clear()
        scn.objects.link(new_obj)
        
        scn.objects.active = new_obj
        #new_obj.select=True
        #bpy.ops.object.mode_set(mode='EDIT')
        new_obj.mode_set(mode='EDIT')
        bpy.ops.mesh.delete(type='ONLY_FACE')
        bpy.ops.object.mode_set(mode='OBJECT')
        
        new_obj.select=True
        bpy.ops.object.convert(target='CURVE')
        
        bpy.context.object.data.bevel_depth=0.002
        bpy.context.object.data.fill_mode='FULL'
        bpy.context.object.data.bevel_resolution=2
        new_obj.select = False