import bpy
from bpy.types import Panel

# using tutorial: https://www.youtube.com/watch?v=OEkrQGFqM10

# Class for the panel, derived by Panel
# creating simpleToolPanel inherited from Panel class
class SimpleToolPanel(Panel):
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
    bpy.utils.register_class(SimpleToolPanel)
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
    bpy.utils.unregister_class(SimpleToolPanel)
    del bpy.types.Scene.my_string_cloth_prop
    del bpy.types.Scene.my_string_cube_prop
    del bpy.types.Scene.my_string_wireframe_prop
    
# Needed to run script in Text Editor
if __name__ == '__main__':
    register()