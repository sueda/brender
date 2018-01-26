bl_info = {
    "name": "Brender Panel Addon",
    "description": "Creates a panel to edit Brender Animations.",
    "author": "Lopez, Gustavo",
    'version': (1, 1, 0),
    'blender': (2, 6, 7),
    "location": "3D View > Tools",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"

}

import bpy

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       EnumProperty,
                       PointerProperty,
                       )

from bpy.types import (Panel,
                       Operator,
                       PropertyGroup,
                       )

###############################################################################
#		Properties will be stored in active scene
###############################################################################

class BrenderSettings(PropertyGroup):

	# my_bool = BoolProperty(
 #        name="Enable or Disable",
 #        description="A bool property",
 #        default = False
 #        )

    # my_int = IntProperty(
    #     name = "Int Value",
    #     description="A integer property",
    #     default = 23,
    #     min = 10,
    #     max = 100
    #     )

    x_scale_float = FloatProperty(
        name = "X Scale Value",
        description = "A float property",
        default = 1.0,
        min = 0.01,
        max = 30.0
        )

    y_scale_float = FloatProperty(
	    name = "Y Scale Value",
	    description = "A float property",
	    default = 1.0,
	    min = 0.01,
	    max = 30.0
	    )

    z_scale_float = FloatProperty(
	    name = "Z Scale Value",
	    description = "A float property",
	    default = 1.0,
	    min = 0.01,
	    max = 30.0
	    )

    x_trans_float = FloatProperty(
        name = "X Translation Value",
        description = "A float property",
        default = 0.0,
        min = -100.0,
        max = 100.0
        )

    y_trans_float = FloatProperty(
	    name = "Y Translation Value",
	    description = "A float property",
	    default = 0.0,
	    min = -100.0,
	    max = 100.0
	    )

    z_trans_float = FloatProperty(
	    name = "Z Translation Value",
	    description = "A float property",
	    default = 0.0,
	    min = -100.0,
	    max = 100.0
	    )

    wireframe_obj_string = StringProperty(
        name="Wireframe Object Name",
        description=":",
        default="",
        maxlen=1024,
        )

    checker_mat_obj_string = StringProperty(
        name="Checker Material Object Name",
        description=":",
        default="",
        maxlen=1024,
        )

    blue_mat_obj_string = StringProperty(
        name="Blue Material Object Name",
        description=":",
        default="",
        maxlen=1024,
        )

    # my_enum = EnumProperty(
    #     name="Dropdown:",
    #     description="Apply Data to attribute.",
    #     items=[ ('OP1', "Option 1", ""),
    #             ('OP2', "Option 2", ""),
    #             ('OP3', "Option 3", ""),
    #            ]
    #     )

	# my_bool = BoolProperty(
 #        name="Enable or Disable",
 #        description="A bool property",
 #        default = False
 #        )

 #    my_int = IntProperty(
 #        name = "Int Value",
 #        description="A integer property",
 #        default = 23,
 #        min = 10,
 #        max = 100
 #        )

 #    my_float = FloatProperty(
 #        name = "Float Value",
 #        description = "A float property",
 #        default = 23.7,
 #        min = 0.01,
 #        max = 30.0
 #        )

 #    my_string = StringProperty(
 #        name="User Input",
 #        description=":",
 #        default="",
 #        maxlen=1024,
 #        )

 #    my_enum = EnumProperty(
 #        name="Dropdown:",
 #        description="Apply Data to attribute.",
 #        items=[ ('OP1', "Option 1", ""),
 #                ('OP2', "Option 2", ""),
 #                ('OP3', "Option 3", ""),
 #               ]
 #        )

	# my_bool = BoolProperty()
 #    scale_int = IntProperty()
 #    scale_float = FloatProperty()
 #    my_float = FloatProperty()
 #    obj_for_cube_mat = StringProperty()
 #    obj_for_cloth_mat = StringProperty()
 #    obj_for_wireframe = StringProperty()
 #    # other syntax
 #    custom_1 = bpy.props.FloatProperty(name="My Float")
 #    custom_2 = bpy.props.IntProperty(name="My Int")

####################################################
# Create Materials ------Temporary-----Clean up
####################################################
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

###############################################################################
#		Operators
###############################################################################

class ApplyClothAnimationMaterial(bpy.types.Operator):
    """Apply Animation Object Material"""
    bl_idname = "object.apply_cloth_animation_material"
    bl_label = "Apply Cloth Animation Materials"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mat = bpy.data.materials['ClothMaterial']
        scene = context.scene
        myaddon = scene.my_addon
        
        for obj in bpy.data.objects:
            if obj.name.endswith(myaddon.checker_mat_obj_string):
                theobj = bpy.data.objects[obj.name]
                theobj.select = True
                objdata = obj.data
                # append Material
                objdata.materials.append(mat)
                theobj.select = False

        return {'FINISHED'}



class ApplyCubeAnimationMaterial(bpy.types.Operator):
    """Apply Animation Object Material"""
    bl_idname = "object.apply_cube_animation_material"
    bl_label = "Apply Cube Animation Materials"
    bl_options = {'REGISTER', 'UNDO'}
      
    def execute(self, context):
        mat = bpy.data.materials['CubeMaterial']
        scene = context.scene
        myaddon = scene.my_addon
        
        for obj in bpy.data.objects:
            if obj.name.endswith(myaddon.blue_mat_obj_string):
                theobj = bpy.data.objects[obj.name]
                theobj.select = True
                objdata = obj.data
                # append Material
                objdata.materials.append(mat)
                theobj.select = False

        return {'FINISHED'}


# class HelloWorldOperator(bpy.types.Operator):
#     bl_idname = "wm.hello_world"
#     bl_label = "Print Values Operator"

#     def execute(self, context):
#         scene = context.scene
#         mytool = scene.my_addon

#         # print the values to the console
#         print("Hello World")
#         print("bool state:", mytool.my_bool)
#         print("int value:", mytool.my_int)
#         print("float value:", mytool.my_float)
#         print("string value:", mytool.my_string)
#         print("enum state:", mytool.my_enum)

#         return {'FINISHED'}

###############################################################################
#		Brender in Object mode
###############################################################################

# Class for the panel, derived by Panel
# creating BrenderPanel inherited from Panel class
class BrenderPanel(Panel):
	bl_idname = "OBJECT_PT_Brender_panel"
	bl_label = "Brender Panel"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"    # bl_category = "Tools" ## adds to tool panel
	bl_category = 'Brender'
	bl_context = "objectmode"


	# not sure about this one
	@classmethod
	def poll(self,context):
		return context.object is not None

	# Add UI elements here
	def draw(self, context):
		layout = self.layout
		scene = context.scene
		myaddon = scene.my_addon

		layout.prop(myaddon, "x_scale_float")
		layout.prop(myaddon, "y_scale_float")
		layout.prop(myaddon, "z_scale_float")
		layout.prop(myaddon, "x_trans_float")
		layout.prop(myaddon, "y_trans_float")
		layout.prop(myaddon, "z_trans_float")
		layout.prop(myaddon, "wireframe_obj_string")
		layout.prop(myaddon, "checker_mat_obj_string")
		layout.operator("object.apply_cloth_animation_material")
		layout.prop(myaddon, "blue_mat_obj_string")
		layout.operator("object.apply_cube_animation_material")

            
    

        # layout.operator('object.resize_animation_objects', text='Resize Objects')
        # layout.operator('object.translate_animation_objects', text='Translate Objects')
        # col = self.layout.column(align = True)
        # col.prop(context.scene, "my_string_wireframe_prop")
        # layout.operator('object.wireframe_overlay', text='Wireframe Overlay')
        # # testing Text Input
        # col = self.layout.column(align = True)
        # col.prop(context.scene, "my_string_cloth_prop")
        # layout.operator('object.apply_cloth_animation_material', text='Apply Cloth Mat')
        # col = self.layout.column(align = True)
        # col.prop(context.scene, "my_string_cube_prop")
        # layout.operator('object.apply_cube_animation_material', text='Apply Cube Mat')



# class OBJECT_PT_my_panel(Panel):
#     bl_idname = "OBJECT_PT_my_panel"
#     bl_label = "My Panel"
#     bl_space_type = "VIEW_3D"   
#     bl_region_type = "TOOLS"    
#     bl_category = "Tools"
#     bl_context = "objectmode"   

#     @classmethod
#     def poll(self,context):
#         return context.object is not None

#     def draw(self, context):
#         layout = self.layout
#         scene = context.scene
#         mytool = scene.my_addon

#         layout.prop(mytool, "my_bool")
#         layout.prop(mytool, "my_enum", text="") 
#         layout.prop(mytool, "my_int")
#         layout.prop(mytool, "my_float")
#         layout.prop(mytool, "my_string")
#         layout.operator("wm.hello_world")
#         layout.menu("OBJECT_MT_select_test", text="Presets", icon="SCENE")




# ------------------------------------------------------------------------
# register and unregister
# ------------------------------------------------------------------------

def register():
	bpy.utils.register_module(__name__)
	bpy.types.Scene.my_addon = PointerProperty(type=BrenderSettings)

def unregister():
	bpy.utils.unregister_module(__name__)
	del bpy.types.Scene.my_addon

if __name__ == "__main__":
	register()