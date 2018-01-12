import bpy
import bmesh

scn = bpy.context.scene
#scn.layers = [True] * 20 # Show all layers

bpy.context.scene.frame_set(0)

for obj in bpy.data.objects:
    if obj.name.endswith("001"):
        #print(obj.name)
        # NEED TO MAKE THIS LOOP MORE DYNAMIC
        #unhide object
        obj.hide = obj.hide_render = False
        scn.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        
        bpy.ops.mesh.reveal()
        bpy.ops.mesh.select_all(action='SELECT')
        
        #execute any editmode tool
        bpy.ops.mesh.delete(type='ONLY_FACE')
        
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        obj.select=True
        bpy.ops.object.convert(target='CURVE')
        obj.data.bevel_depth=0.002
        obj.data.fill_mode='FULL'
        obj.data.bevel_resolution = 2
        #rehide object  
        obj.hide = obj.hide_render = True
        #deselect object
        obj.select=False