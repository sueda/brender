bl_info = {
    "name": "Brender",
    "author": "Lopez, Gustavo",
    'version': (1, 1),
    'blender': (2, 6, 7),
    "description": "Creates a panel to edit Brender Animations.",
    "category": "Object"

}

import bpy

def createClothMaterial():
	if bpy.data.materials.get("ClothMaterial") is None:
		# create cloth material
		mat_name = "ClothMaterial"
		mat = bpy.data.materials.new(mat_name)
		mat.use_nodes = True 
		nodes = mat.node_tree.nodes
		# diffuse node is made by default
		diffnode = nodes["Diffuse BSDF"]
		checkernode = nodes.new('ShaderNodeTexChecker')
		uvmapnode = nodes.new('ShaderNodeUVMap')
		# organize nodes
		diffnode.location = (100,300)
		checkernode.location = (-100,300)
		uvmapnode.location = (-300,300)
		# apply checker primary and secondary colors
		checkernode.inputs[1].default_value = (0.456, 0.386, 0.150, 1)
		checkernode.inputs[2].default_value = (0.080, 0, 0, 1)
		# link nodes
		links = mat.node_tree.links
		links.new(checkernode.outputs[0], diffnode.inputs[0]) 
		links.new(uvmapnode.outputs[0], checkernode.inputs[0])

def createCubeMaterial():
	if bpy.data.materials.get("CubeMaterial") is None:
		# create cube material
		mat_name2 = "CubeMaterial"
		mat2 = bpy.data.materials.new(mat_name2)
		mat2.use_nodes = True 
		nodes2 = mat2.node_tree.nodes
		diffnode2 = nodes2["Diffuse BSDF"]
		# apply checker primary and secondary colors
		diffnode2.inputs[0].default_value = (0.198, 0.371, 0.694, 1)

createClothMaterial()
createCubeMaterial()

import bpy
import mathutils


bl_info = {
    "name": "Apply Cloth Materials",
    "category": "Object",
}

class ApplyClothAnimationMaterial(bpy.types.Operator):
    """Apply Animation Object Material"""
    bl_idname = "object.apply_cloth_animation_material"
    bl_label = "Apply Cloth Animation Materials"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        mat = bpy.data.materials['ClothMaterial']
        
        for obj in bpy.data.objects:
            if obj.name.endswith(context.scene.my_string_cloth_prop):
                theobj = bpy.data.objects[obj.name]
                theobj.select = True
                objdata = obj.data
                # append Material
                objdata.materials.append(mat)
                theobj.select = False

        return {'FINISHED'}



bl_info = {
    "name": "Apply Cube Materials",
    "category": "Object",
}

class ApplyCubeAnimationMaterial(bpy.types.Operator):
    """Apply Animation Object Material"""
    bl_idname = "object.apply_cube_animation_material"
    bl_label = "Apply Cube Animation Materials"
    bl_options = {'REGISTER', 'UNDO'}
      
      
    def execute(self, context):
        mat = bpy.data.materials['CubeMaterial']
        
        for obj in bpy.data.objects:
            if obj.name.endswith(context.scene.my_string_cube_prop):
                theobj = bpy.data.objects[obj.name]
                theobj.select = True
                objdata = obj.data
                # append Material
                objdata.materials.append(mat)
                theobj.select = False

        return {'FINISHED'}


# store keymaps here to access after registration
addon_keymaps = []

def menu_func(self, context):
    self.layout.operator(ApplyClothAnimationMaterial.bl_idname)
    self.layout.operator(ApplyCubeAnimationMaterial.bl_idname)

def register():
    bpy.utils.register_class(ApplyClothAnimationMaterial)
    bpy.utils.register_class(ApplyCubeAnimationMaterial)

def unregister():
    bpy.utils.unregister_class(ApplyClothAnimationMaterial)
    bpy.utils.unregister_class(ApplyCubeAnimationMaterial)

if __name__ == "__main__":
    register()



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

        scn = context.scene
        dupobjects = []

        objectname = context.scene.my_string_wireframe_prop
        copynames = objectname + ".001"
        for obj in bpy.data.objects:
            # make this dynamic by changing to endswith
            # and refer to context.string from panel
            # if obj.name.startswith("0"):
            if obj.name.endswith(objectname):
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



        context.scene.frame_set(0)
        # make mesh
		
        for obj in bpy.data.objects:
            if obj.name.endswith(copynames):
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



bl_info = {
    "name": "Resize Animation Objects",
    "category": "Object",
}

import bpy
import mathutils


class AnimationObjectResize(bpy.types.Operator):
    """Animation Object Resizing"""
    bl_idname = "object.resize_animation_objects"
    bl_label = "Resize Animation Objects"
    bl_options = {'REGISTER', 'UNDO'}

    scale = bpy.props.IntProperty(name="scale", default=2, min=1, max=100)

    def execute(self, context):
        #scene = context.scene
        #cursor = scene.cursor_location
        #obj = scene.objects.active

        for obj in bpy.data.objects:
            if obj.name.startswith("0"):
                theobj = bpy.data.objects[obj.name]
                theobj.select = True
                theobj.scale=(self.scale,self.scale,self.scale)
                theobj.select = False

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(AnimationObjectResize.bl_idname)

# store keymaps here to access after registration
addon_keymaps = []


def register():
    bpy.utils.register_class(AnimationObjectResize)

def unregister():
    bpy.utils.unregister_class(AnimationObjectResize)

if __name__ == "__main__":
    register()



bl_info = {
    "name": "Translate Animation Objects",
    "category": "Object",
}

import bpy
import mathutils


class AnimationObjectTranslate(bpy.types.Operator):
    """Animation Object Translating"""
    bl_idname = "object.translate_animation_objects"
    bl_label = "Translate Animation Objects"
    bl_options = {'REGISTER', 'UNDO'}

    xTrans = bpy.props.IntProperty(name="X Displacement", default=0, min=-100, max=100)
    yTrans = bpy.props.IntProperty(name="Y Displacement", default=0, min=-100, max=100)
    zTrans = bpy.props.IntProperty(name="Z Displacement", default=0, min=-100, max=100)

    def execute(self, context):
        #scene = context.scene
        #cursor = scene.cursor_location
        #obj = scene.objects.active

        for obj in bpy.data.objects:
            if obj.name.startswith("0"):
                theobj = bpy.data.objects[obj.name]
                theobj.select = True
                vec = mathutils.Vector((self.xTrans,self.yTrans,self.zTrans))
                theobj.location = theobj.location + vec
                theobj.select = False

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(AnimationObjectTranslate.bl_idname)

# store keymaps here to access after registration
addon_keymaps = []


def register():
    bpy.utils.register_class(AnimationObjectTranslate)

def unregister():
    bpy.utils.unregister_class(AnimationObjectTranslate)

if __name__ == "__main__":
    register()



import bpy
from bpy.types import Panel

# using tutorial: https://www.youtube.com/watch?v=OEkrQGFqM10

# Class for the panel, derived by Panel
# creating BrenderPanel inherited from Panel class
class BrenderPanel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'Brender Object Transformations'
    bl_context = 'objectmode'
    # tab on left
    bl_category = 'Brender'
    
    # Add UI elements here
    def draw(self, context):
        layout = self.layout
        # layout.operator("<operator>", text='Add new cube')
        layout.operator('object.resize_animation_objects', text='Resize Objects')
        layout.operator('object.translate_animation_objects', text='Translate Objects')
        col = self.layout.column(align = True)
        col.prop(context.scene, "my_string_wireframe_prop")
        layout.operator('object.wireframe_overlay', text='Wireframe Overlay')
        # testing Text Input
        col = self.layout.column(align = True)
        col.prop(context.scene, "my_string_cloth_prop")
        layout.operator('object.apply_cloth_animation_material', text='Apply Cloth Mat')
        col = self.layout.column(align = True)
        col.prop(context.scene, "my_string_cube_prop")
        layout.operator('object.apply_cube_animation_material', text='Apply Cube Mat')
        
# Registering addon & Unregistering addon
# Register
def register():
    bpy.utils.register_class(BrenderPanel)
    bpy.types.Scene.my_string_wireframe_prop = bpy.props.StringProperty \
      (
        name = "Wireframe Object Name",
        description = "Wireframe Animation Object Name",
        default = ""
      )
    bpy.types.Scene.my_string_cloth_prop = bpy.props.StringProperty \
      (
        name = "Cloth Name",
        description = "Cloth Animation Object Name",
        default = ""
      )
    bpy.types.Scene.my_string_cube_prop = bpy.props.StringProperty \
      (
        name = "Cube Name",
        description = "Cube Animation Object Name",
        default = ""
      )
# Unregister
def unregister():
    bpy.utils.unregister_class(BrenderPanel)
    del bpy.types.Scene.my_string_cloth_prop
    del bpy.types.Scene.my_string_cube_prop
    del bpy.types.Scene.my_string_wireframe_prop
    
# Needed to run script in Text Editor
if __name__ == '__main__':
    register()