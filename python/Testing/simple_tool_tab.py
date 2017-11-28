import bpy
from bpy.types import Panel

# using tutorial: https://www.youtube.com/watch?v=OEkrQGFqM10

# Class for the panel, derived by Panel
# creating simpleToolPanel inherited from Panel class
class SimpleToolPanel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'Tools Tab Label'
    bl_context = 'objectmode'
    # tab on left
    bl_category = 'Brender'
    
    # Add UI elements here
    def draw(self, context):
        layout = self.layout
        # layout.operator("<operator>", text='Add new cube')
        layout.operator('mesh.primitive_cube_add', text='Add new cube')
        
# Registering addon & Unregistering addon
# Register
def register():
    bpy.utils.register_class(SimpleToolPanel)
    
# Unregister
def unregister():
    bpy.utils.unregister_class(SimpleToolPanel)
    
# Needed to run script in Text Editor
if __name__ == '__main__':
    register()