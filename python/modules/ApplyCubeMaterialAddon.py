bl_info = {
    "name": "Apply Cube Materials",
    "category": "Object",
}

import bpy
import mathutils


class ApplyCubeAnimationMaterial(bpy.types.Operator):
    """Apply Animation Object Material"""
    bl_idname = "object.apply_cube_animation_material"
    bl_label = "Apply Cube Animation Materials"
    bl_options = {'REGISTER', 'UNDO'}

    # my_string = bpy.props.StringProperty(name="Object Name")

    

    def execute(self, context):
        #scene = context.scene
        #cursor = scene.cursor_location
        #obj = scene.objects.active
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


def menu_func(self, context):
    self.layout.operator(ApplyCubeAnimationMaterial.bl_idname)

# store keymaps here to access after registration
addon_keymaps = []


def register():
    bpy.utils.register_class(ApplyCubeAnimationMaterial)

def unregister():
    bpy.utils.unregister_class(ApplyCubeAnimationMaterial)

if __name__ == "__main__":
    register()