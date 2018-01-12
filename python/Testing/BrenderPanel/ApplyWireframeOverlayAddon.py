bl_info = {
    "name": "Wireframe Overlay",
    "category": "Object",
}

import bpy
import mathutils


class WireframeOverlay(bpy.types.Operator):
    """Wireframe Overlay"""
    bl_idname = "object.wireframe_overlay"
    bl_label = "Create Wireframe Overlay for Objects"
    bl_options = {'REGISTER', 'UNDO'}

    bevelDepth = bpy.props.FloatProperty(name="Bevel Depth", default=0.001, min=0.000, max=0.500, step=1, precision=3)
    bevelResolution = bpy.props.IntProperty(name="Bevel Resolution", default=2, min=0, max=10)
    
    def execute(self, context):
        #scene = context.scene
        #cursor = scene.cursor_location
        #obj = scene.objects.active

        scn = context.scene
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

        
        context.scene.frame_set(0)
        
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
            context.scene.frame_set(f) 
    
            obj_prev = dupobjects[f-1]
            obj_prev.hide = obj_prev.hide_render = True
            obj_prev.keyframe_insert(data_path='hide')
            obj_prev.keyframe_insert(data_path='hide_render')
            
            obj = dupobjects[f]
            obj.hide = obj.hide_render = False
            obj.keyframe_insert(data_path='hide')
            obj.keyframe_insert(data_path='hide_render')


            #scn.layers = [True] * 20 # Show all layers

        context.scene.frame_set(0)
# make mesh
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
                obj.data.bevel_depth=self.bevelDepth  #0.002
                obj.data.fill_mode='FULL'
                obj.data.bevel_resolution = self.bevelResolution
                #rehide object  
                obj.hide = obj.hide_render = True #hide mesh
                #deselect object
                obj.select=False

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(WireframeOverlay.bl_idname)

# store keymaps here to access after registration
addon_keymaps = []


def register():
    bpy.utils.register_class(WireframeOverlay)

def unregister():
    bpy.utils.unregister_class(WireframeOverlay)

if __name__ == "__main__":
    register()