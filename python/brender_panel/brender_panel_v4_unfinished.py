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
import mathutils

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
	x_rot_float = FloatProperty(
		name = "X",
		description = "A float property",
		default = 0.0,
		step = 1.0,
		precision=1
		)

	y_rot_float = FloatProperty(
		name = "Y",
		description = "A float property",
		default = 0.0,
		step = 1.0,
		precision=1
		)

	z_rot_float = FloatProperty(
		name = "Z",
		description = "A float property",
		default = 0.0,
		step = 1.0,
		precision=1
		)

	x_scale_float = FloatProperty(
		name = "X",
		description = "A float property",
		default = 1.0,
		min = 0.01,
		max = 30.0,
		step = 1.0
		)

	y_scale_float = FloatProperty(
		name = "Y",
		description = "A float property",
		default = 1.0,
		min = 0.01,
		max = 30.0,
		step = 1.0
		)

	z_scale_float = FloatProperty(
		name = "Z",
		description = "A float property",
		default = 1.0,
		min = 0.01,
		max = 30.0,
		step = 1.0
		)

	x_trans_float = FloatProperty(
		name = "X",
		description = "A float property",
		default = 0.0,
		min = -100.0,
		max = 100.0,
		step = 1.0
		)

	y_trans_float = FloatProperty(
		name = "Y",
		description = "A float property",
		default = 0.0,
		min = -100.0,
		max = 100.0,
		step = 1.0
		)

	z_trans_float = FloatProperty(
		name = "Z",
		description = "A float property",
		default = 0.0,
		min = -100.0,
		max = 100.0,
		step = 1.0
		)
	
	wf_bevel_depth = FloatProperty(
		name = "Depth",
		description = "A float property",
		default = 0.001,
		min = 0.000,
		max = 0.500,
		step = 0.001,
		precision = 3
		)

	wf_bevel_resolution = IntProperty(
		name = "Resolution",
		description = "A float property",
		default = 2,
		min = 0,
		max = 10
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


class AnimationObjectResize(bpy.types.Operator):
	"""Animation Object Resizing"""
	bl_idname = "object.resize_animation_objects"
	bl_label = "Update"
	bl_options = {'REGISTER', 'UNDO'}

	# scale = bpy.props.IntProperty(name="scale", default=2, min=1, max=100)

	def execute(self, context):
		#scene = context.scene
		#cursor = scene.cursor_location
		#obj = scene.objects.active
		scene = context.scene
		myaddon = scene.my_addon
		brenderObjname = context.active_object.name

		if "_" in brenderObjname: # has naming scheme 00001_objname
			for obj in bpy.data.objects:
				if obj.name.endswith(brenderObjname.split("_", 1)[1]): # same last letters as brenderobj
					theobj = bpy.data.objects[obj.name]
					theobj.select = True
					theobj.scale=(myaddon.x_scale_float,myaddon.y_scale_float,myaddon.z_scale_float)
					theobj.select = False

		else: # just scale selected object
			theobj = bpy.data.objects[brenderObjname]
			theobj.scale=(myaddon.x_scale_float,myaddon.y_scale_float,myaddon.z_scale_float)
			theobj.select = False

		return {'FINISHED'}

# can be updated: maybe add rotation mode
class AnimationObjectRotate(bpy.types.Operator):
	"""Animation Object Resizing"""
	bl_idname = "object.rotate_animation_objects"
	bl_label = "Update"
	bl_options = {'REGISTER', 'UNDO'}

	# scale = bpy.props.IntProperty(name="scale", default=2, min=1, max=100)

	def execute(self, context):
		#scene = context.scene
		#cursor = scene.cursor_location
		#obj = scene.objects.active
		scene = context.scene
		myaddon = scene.my_addon
		brenderObjname = context.active_object.name

		if "_" in brenderObjname: # has naming scheme 00001_objname
			for obj in bpy.data.objects:
				if obj.name.endswith(brenderObjname.split("_", 1)[1]): # same last letters as brenderobj
					theobj = bpy.data.objects[obj.name]
					theobj.select = True
					theobj.rotation_euler = (myaddon.x_rot_float,myaddon.y_rot_float,myaddon.z_rot_float)
					theobj.select = False

		else: # just scale selected object
			theobj = bpy.data.objects[brenderObjname]
			theobj.rotation_euler = (myaddon.x_rot_float,myaddon.y_rot_float,myaddon.z_rot_float)
			theobj.select = False

		return {'FINISHED'}


class AnimationObjectTranslate(bpy.types.Operator):
	"""Animation Object Translating"""
	bl_idname = "object.translate_animation_objects"
	bl_label = "Update"
	bl_options = {'REGISTER', 'UNDO'}


	def execute(self, context):
		scene = context.scene
		myaddon = scene.my_addon
		brenderObjname = context.active_object.name
		#cursor = scene.cursor_location
		#obj = scene.objects.active
		xTrans = myaddon.x_trans_float
		yTrans = myaddon.y_trans_float
		zTrans = myaddon.z_trans_float
		
		if "_" in brenderObjname: # has naming scheme 00001_objname
			for obj in bpy.data.objects:
				if obj.name.endswith(brenderObjname.split("_", 1)[1]): # same last letters as brenderobj
					theobj = bpy.data.objects[obj.name]
					theobj.select = True
					vec = mathutils.Vector((xTrans,yTrans,zTrans))
					theobj.location = vec #theobj.location + vec
					theobj.select = False

		else: # just scale selected object
			theobj = bpy.data.objects[brenderObjname]
			vec = mathutils.Vector((xTrans,yTrans,zTrans))
			theobj.location = vec #theobj.location + vec
			theobj.select = False

		return {'FINISHED'}


class WireframeOverlay(bpy.types.Operator):
	"""Wireframe Overlay"""
	bl_idname = "object.wireframe_overlay"
	bl_label = "Create Wireframe Overlay for Objects"
	bl_options = {'REGISTER', 'UNDO'}

	# bevelDepth = bpy.props.FloatProperty(name="Bevel Depth", default=0.001, min=0.000, max=0.500, step=1, precision=3)
	# bevelResolution = bpy.props.IntProperty(name="Bevel Resolution", default=2, min=0, max=10)
	
	def execute(self, context):

		scn = context.scene
		myaddon = scn.my_addon
		dupobjects = []
		objectname = myaddon.wireframe_obj_string
		copynames = objectname + ".001"
		# -----------------------------------------
		# duplicate object loop
		for obj in bpy.data.objects:
			if obj.name.endswith(objectname):
				theobj = bpy.data.objects[obj.name]
				# duplicates and selects the new object
				new_obj = theobj.copy()
				new_obj.data = theobj.data.copy()
				new_obj.animation_data_clear()
				scn.objects.link(new_obj)
				dupobjects.append(new_obj)

		
		context.scene.frame_set(0)
		# --------------------------------------------
		# hide for keyframes
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


		# end of duplicating opjects
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
				obj.data.bevel_depth=myaddon.wf_bevel_depth  #0.002
				obj.data.fill_mode='FULL'
				obj.data.bevel_resolution = myaddon.wf_bevel_resolution
				#rehide object  
				obj.hide = obj.hide_render = True #hide mesh
				#deselect object
				obj.select=False

		return {'FINISHED'}

###############################################################################
#		Brender in Object mode
###############################################################################

# Class for the panel, derived by Panel
# creating BrenderPanel inherited from Panel class
class BrenderImportPanel(Panel):
	bl_idname = "OBJECT_PT_Brender_import_panel"
	bl_label = "Import Obj Animation"
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
		layout.operator("load.obj_as_anim") # fix this button


class BrenderTransformPanel(Panel):
	bl_idname = "OBJECT_PT_Brender_transform_panel"
	bl_label = "Object Transformation Tools"
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

		#layout.label(text="Scale:")

		split = layout.split()
		# Scale Column
		col = split.column(align=True)
		col.label(text="Scale:")
		col.prop(myaddon, "x_scale_float")
		col.prop(myaddon, "y_scale_float")
		col.prop(myaddon, "z_scale_float")
		col.operator("object.resize_animation_objects")

		# Location Column
		col = split.column(align=True)
		col.label(text="Location:")
		col.prop(myaddon, "x_trans_float")
		col.prop(myaddon, "y_trans_float")
		col.prop(myaddon, "z_trans_float")
		col.operator("object.translate_animation_objects")

		# Rotation Column
		col = split.column(align=True)
		col.label(text="Rotation:")
		col.prop(myaddon, "x_rot_float")
		col.prop(myaddon, "y_rot_float")
		col.prop(myaddon, "z_rot_float")
		col.operator("object.rotate_animation_objects")


class BrenderMaterialPanel(Panel):
	bl_idname = "OBJECT_PT_Brender_material_panel"
	bl_label = "Brender Material Tools"
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

		layout.prop(myaddon, "checker_mat_obj_string")
		layout.operator("object.apply_cloth_animation_material")
		layout.prop(myaddon, "blue_mat_obj_string")
		layout.operator("object.apply_cube_animation_material")


class BrenderRenderPanel(Panel):
	bl_idname = "OBJECT_PT_Brender_render_panel"
	bl_label = "Brender Render Tools"
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

		split = layout.split()
		col = split.column()
		col.label(text="Bevel: ")
		col.prop(myaddon, "wf_bevel_depth")
		col.prop(myaddon, "wf_bevel_resolution")

		col = split.column()
		col.label(text="Modification: ")
		col.prop(myaddon, "wireframe_obj_string")

		row = layout.row()
		row.operator("object.wireframe_overlay")

			
	

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