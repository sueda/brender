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