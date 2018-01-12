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