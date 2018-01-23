bl_info = {
    "name": "Apply Cloth Materials",
    "category": "Object",
}

import bpy
import mathutils


class ApplyClothAnimationMaterial(bpy.types.Operator):
    """Apply Animation Object Material"""
    bl_idname = "object.apply_cloth_animation_material"
    bl_label = "Apply Cloth Animation Materials"
    bl_options = {'REGISTER', 'UNDO'}

    # my_string = bpy.props.StringProperty(name="Object Name")

    

    def execute(self, context):
        #scene = context.scene
        #cursor = scene.cursor_location
        #obj = scene.objects.active
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


def menu_func(self, context):
    self.layout.operator(ApplyClothAnimationMaterial.bl_idname)

# store keymaps here to access after registration
addon_keymaps = []


def register():
    bpy.utils.register_class(ApplyClothAnimationMaterial)

def unregister():
    bpy.utils.unregister_class(ApplyClothAnimationMaterial)

if __name__ == "__main__":
    register()