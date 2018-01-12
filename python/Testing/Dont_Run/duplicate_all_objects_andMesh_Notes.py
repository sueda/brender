import bpy

scn = bpy.context.scene
#scn.layers = [True] * 20 # Show all layers
dupobjects = []

for obj in bpy.data.objects:
    if obj.name.startswith("0"):
        theobj = bpy.data.objects[obj.name]
        ##duplicates and selects the new object
        new_obj = theobj.copy()
        new_obj.data = theobj.data.copy()
        new_obj.animation_data_clear()
        scn.objects.link(new_obj)
        dupobjects.append(new_obj)

        
bpy.context.scene.frame_set(0)
        
for i, obj in enumerate(dupobjects):
    if i == 0:
        continue
    obj.hide = obj.hide_render = True
    obj.keyframe_insert(data_path='hide')
    obj.keyframe_insert(data_path='hide_render')

for f, obj in enumerate(dupobjects):
    if f == 0:
        continue
    # increment current frame to insert keyframe
    bpy.context.scene.frame_set(f) 
    
    obj_prev = dupobjects[f-1]
    obj_prev.hide = obj_prev.hide_render = True
    obj_prev.keyframe_insert(data_path='hide')
    obj_prev.keyframe_insert(data_path='hide_render')
            
    obj = dupobjects[f]
    obj.hide = obj.hide_render = False
    obj.keyframe_insert(data_path='hide')
    obj.keyframe_insert(data_path='hide_render')
    
    
    
        #scn.objects.active = new_obj
        #new_obj.select=True
        #bpy.ops.object.mode_set(mode='EDIT')
        #new_obj.mode_set(mode='EDIT')
        #bpy.ops.mesh.delete(type='ONLY_FACE')
        #bpy.ops.object.mode_set(mode='OBJECT')
        
        #new_obj.select=True
        #bpy.ops.object.convert(target='CURVE')
        
        #bpy.context.object.data.bevel_depth=0.002
        #bpy.context.object.data.fill_mode='FULL'
        #bpy.context.object.data.bevel_resolution=2
        #new_obj.select = False





