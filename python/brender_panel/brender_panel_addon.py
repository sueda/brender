bl_info = {
	"name": "Brender Panel Addon",
	"description": "Creates a panel to edit Brender Animations.",
	"author": "Lopez, Gustavo",
	'version': (1, 5, 5),
	'blender': (2, 6, 7),
	"location": "3D View > Tools",
	"warning": "", # used for warning icon and text in addons panel
	"wiki_url": "",
	"tracker_url": "",
	"category": "Development"

}

####################################################
# ToDo's
####################################################
# 1. create wireframe preview option--------------------------------------DONE
# 2. create import every # of frames--------------------------------------DONE
# 3. create get common name method to use across other methods------------DONE
# 	(obtaining selected object name)--------------------------------------DONE
# 4. use get common name function in other methods to simplify------------DONE
# 5. lookup @classmethod specifics----------------------------------------DONE
####################################################
####################################################

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

class View3DPanel:
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'

class CyclesButtonsPanel:
	bl_space_type = "PROPERTIES"
	bl_region_type = "TOOLS"
	bl_context = "objectmode"
	COMPAT_ENGINES = {'CYCLES'}

	@classmethod
	def poll(cls, context):
		rd = context.scene.render
		return rd.engine in cls.COMPAT_ENGINES

###############################################################################
#		Properties will be stored in active scene
###############################################################################

class BrenderSettings(PropertyGroup):


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

	frameskip = IntProperty(
		name = "FrameSkip",
		description = "An integer property",
		default = 0,
		min = 0,
		max = 100
		)

	wf_offset = FloatProperty(
		name = "Offset",
		description = "A float property",
		default = 0.000,
		min = 0.000,
		max = 0.500,
		step = 0.001,
		precision = 3
		)

	wf_extrude = FloatProperty(
		name = "Extrude",
		description = "A float property",
		default = 0.000,
		min = 0.000,
		max = 0.500,
		step = 0.001,
		precision = 3
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
# Run on Import
####################################################
import bpy




###############################################################################
#		Operators
###############################################################################

# The following Function is a modification of 'cmomoney's blender_import_obj_anim method
import bpy, os
from bpy.props import *

class LoadObjAsAnimationAdvanced(bpy.types.Operator):
	bl_idname = 'load.obj_as_anim_advanced'
	bl_label = 'Advanced Import'
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Import Obj sequence as animation(s)"
	cFrame = 0
	filepath = StringProperty(name="File path", description="File filepath of Obj", maxlen=4096, default="")
	filter_folder = BoolProperty(name="Filter folders", description="", default=True, options={'HIDDEN'})
	filter_glob = StringProperty(default="*.obj", options={'HIDDEN'})
	files = CollectionProperty(name='File path', type=bpy.types.OperatorFileListElement)
	filename_ext = '.obj'
	objects = []
	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):
		self.objects=[]
		scene = context.scene
		myaddon = scene.my_addon
		#get file names, sort, and set target mesh
		spath = os.path.split(self.filepath)
		files = [file.name for file in self.files]
		files.sort()
		#add all objs to scene
		# this makes the frame skip option available
		count=0
		modval = myaddon.frameskip + 1
		for f in files:
			if count % modval == 0:
				fp = spath[0] + "/" + f
				self.load_obj(fp,f)

			count+=1
		
		bpy.context.scene.frame_set(0)
		for i, ob in enumerate(self.objects):
			if i == 0:
				continue
			ob.hide = ob.hide_render = True
			ob.keyframe_insert(data_path='hide')
			ob.keyframe_insert(data_path='hide_render')

		for f, ob in enumerate(self.objects):
			if f == 0:
				continue
			# increment current frame to insert keyframe
			bpy.context.scene.frame_set(f)

			# Insert only as many keyframes as really needed
			ob_prev = self.objects[f-1]
			ob_prev.hide = ob_prev.hide_render = True
			ob_prev.keyframe_insert(data_path='hide')
			ob_prev.keyframe_insert(data_path='hide_render')
			
			ob = self.objects[f]
			ob.hide = ob.hide_render = False
			ob.keyframe_insert(data_path='hide')
			ob.keyframe_insert(data_path='hide_render')
				
		return{'FINISHED'}

	def invoke(self, context, event):
		wm = context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}

	def load_obj(self, fp,fname):
		bpy.ops.object.select_all(action='DESELECT')
		bpy.ops.import_scene.obj(filepath=fp, filter_glob="*.obj;*.mtl",  use_edges=True, use_smooth_groups=True, use_split_objects=True, use_split_groups=True, use_groups_as_vgroups=False, use_image_search=True, split_mode='ON', global_clamp_size=0, axis_forward='Y', axis_up='Z')
		self.objects.append(bpy.context.selected_objects[0])
		return 



def GetCommonName(brenderObjname):
	returnBrenderName = brenderObjname
	if "_" in brenderObjname: # has naming scheme 00001_objname
		returnBrenderName = brenderObjname.split("_", 1)[1] # same last letters as brenderobj

	else: # just scale selected object
		returnBrenderName = brenderObjname

	return returnBrenderName


class BatchDelete(bpy.types.Operator):
	"""Animation Object Resizing"""
	bl_idname = "object.delete_all"
	bl_label = "Delete all objects of same name"
	bl_options = {'REGISTER', 'UNDO'}


	def execute(self, context):
		scene = context.scene
		myaddon = scene.my_addon
		brenderObjname = context.active_object.name

		brenderObjname = GetCommonName(brenderObjname)

		for obj in bpy.data.objects:
			if obj.name.endswith(brenderObjname): # same last letters as brenderobj
				obj.hide = obj.hide_render = False
				obj.select = True
				bpy.ops.object.delete(use_global=False)
				obj.select = False
		for mesh in bpy.data.meshes:
			if mesh.name.endswith(brenderObjname): # same last letters as brenderobj
				bpy.data.meshes.remove(mesh)

		return {'FINISHED'}


class CreateDefaultMaterials(bpy.types.Operator):
	"""Animation Object Resizing"""
	bl_idname = "object.create_default_mats"
	bl_label = "Create Default Materials"
	bl_options = {'REGISTER', 'UNDO'}


	def execute(self, context):
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

		if bpy.data.materials.get("CubeMaterial") is None:
			# create cube material
			mat_name2 = "CubeMaterial"
			mat2 = bpy.data.materials.new(mat_name2)
			mat2.use_nodes = True 
			nodes2 = mat2.node_tree.nodes
			diffnode2 = nodes2["Diffuse BSDF"]
			# apply checker primary and secondary colors
			diffnode2.inputs[0].default_value = (0.198, 0.371, 0.694, 1)

		return {'FINISHED'}


class ApplyMaterialToAll(bpy.types.Operator):
	"""Apply Animation Object Material"""
	bl_idname = "object.apply_material_to_all"
	bl_label = "Apply Selected Material"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		mat = bpy.context.object.active_material
		scene = context.scene
		myaddon = scene.my_addon
		brenderObjname = context.active_object.name
		brenderObjname = GetCommonName(brenderObjname)

		for obj in bpy.data.objects:
			if obj.name.endswith(brenderObjname): # same last letters as brenderobj
				obj.select = True
				# append Material
				if obj.data.materials:
					obj.data.materials[0] = mat
				else:
					obj.data.materials.append(mat)
				obj.select = False			

		return {'FINISHED'}



class AnimationObjectResize(bpy.types.Operator):
	"""Animation Object Resizing"""
	bl_idname = "object.resize_animation_objects"
	bl_label = "Update"
	bl_options = {'REGISTER', 'UNDO'}


	def execute(self, context):
		#scene = context.scene
		#cursor = scene.cursor_location
		#obj = scene.objects.active
		scene = context.scene
		myaddon = scene.my_addon
		brenderObjname = context.active_object.name
		brenderObjname = GetCommonName(brenderObjname)

		for obj in bpy.data.objects:
			if obj.name.endswith(brenderObjname): # same last letters as brenderobj
				theobj = bpy.data.objects[obj.name]
				theobj.select = True
				theobj.scale=(myaddon.x_scale_float,myaddon.y_scale_float,myaddon.z_scale_float)
				theobj.select = False


		return {'FINISHED'}


class AnimationObjectRotate(bpy.types.Operator):
	"""Animation Object Resizing"""
	bl_idname = "object.rotate_animation_objects"
	bl_label = "Update"
	bl_options = {'REGISTER', 'UNDO'}


	def execute(self, context):
		scene = context.scene
		myaddon = scene.my_addon
		brenderObjname = context.active_object.name
		brenderObjname = GetCommonName(brenderObjname)

		for obj in bpy.data.objects:
			if obj.name.endswith(brenderObjname): # same last letters as brenderobj
				theobj = bpy.data.objects[obj.name]
				theobj.select = True
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
		brenderObjname = GetCommonName(brenderObjname)

		xTrans = myaddon.x_trans_float
		yTrans = myaddon.y_trans_float
		zTrans = myaddon.z_trans_float
		
		for obj in bpy.data.objects:
			if obj.name.endswith(brenderObjname): # same last letters as brenderobj
				theobj = bpy.data.objects[obj.name]
				theobj.select = True
				vec = mathutils.Vector((xTrans,yTrans,zTrans))
				theobj.location = vec #theobj.location + vec
				theobj.select = False


		return {'FINISHED'}


class WireframeOverlay(bpy.types.Operator):
	"""Wireframe Overlay"""
	bl_idname = "object.wireframe_overlay"
	bl_label = "Create/Update Wireframe Overlay"
	bl_options = {'REGISTER', 'UNDO'}


	def DoesObjExist(self, objname):
		self.objname = objname
		for obj in bpy.data.objects:
			if obj.name.endswith(objname):
				return True

		return False


	def execute(self, context):

		scn = context.scene
		myaddon = scn.my_addon
		dupobjects = []

		# Check if name is typed in, if not, use selected object
		if myaddon.wireframe_obj_string is not "":
			objectname = myaddon.wireframe_obj_string
		else:
			brenderObjname = context.active_object.name
			objectname = GetCommonName(brenderObjname)

		copynames = objectname + ".001"

		if self.DoesObjExist(copynames):
			# object copies exist. dont copy
			# update parameters
			context.scene.frame_set(0)

			for obj in bpy.data.objects:
				if obj.name.endswith(copynames):
					obj.select=True
					obj.data.bevel_depth=myaddon.wf_bevel_depth  #0.002
					obj.data.fill_mode='FULL'
					obj.data.bevel_resolution = myaddon.wf_bevel_resolution
					obj.data.offset = myaddon.wf_offset
					obj.data.extrude = myaddon.wf_extrude
					#deselect object
					obj.select=False

			return {'FINISHED'}

		else:
			# create copies
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
					obj.data.offset = myaddon.wf_offset
					obj.data.extrude = myaddon.wf_extrude
					#rehide object  
					obj.hide = obj.hide_render = True #hide mesh
					#deselect object
					obj.select=False

			return {'FINISHED'}


class wireframePreview(bpy.types.Operator):
	"""Wireframe Overlay Preview"""
	bl_idname = "object.wireframe_overlay_preview"
	bl_label = "Preview Wireframe Overlay"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		scene = context.scene
		myaddon = scene.my_addon
		obj = context.object

		if obj.type in ['CURVE']:
			obj.data.bevel_depth=myaddon.wf_bevel_depth  #0.002
			obj.data.fill_mode='FULL'
			obj.data.bevel_resolution = myaddon.wf_bevel_resolution
			obj.data.offset = myaddon.wf_offset
			obj.data.extrude = myaddon.wf_extrude
		else:
			self.report({'ERROR'},'You must have a wireframe/curve object selected to preview.')

		return {'FINISHED'}


###############################################################################
#		Brender in Object mode UI Panels
###############################################################################

# Class for the panel, derived by Panel
# creating BrenderPanel inherited from Panel class
class BrenderEditPanel(View3DPanel, Panel):
	bl_idname = "SCENE_PT_Brender_edit_panel"
	bl_label = "Import/Edit Obj Animation"
	bl_category = "Brender"
	bl_context = "objectmode"
	# Removed poll classmethod so that this 
	# panel is always visible

	# Add UI elements here
	def draw(self, context):
		layout = self.layout
		scene = context.scene
		myaddon = scene.my_addon

		layout.operator("load.obj_as_anim")
		row = layout.row()
		split = row.split()
		split.operator("load.obj_as_anim_advanced")
		split.prop(myaddon, "frameskip")
		layout.operator("object.create_default_mats")
		layout.operator("object.delete_all") 


class BrenderTransformPanel(View3DPanel, Panel):
	bl_idname = "OBJECT_PT_Brender_transform_panel"
	bl_label = "Object Transformation Tools"
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


class BrenderMaterialPanel(View3DPanel, Panel):
	bl_idname = "OBJECT_PT_Brender_material_panel"
	bl_label = "Brender Material Tools"
	bl_category = 'Brender'
	bl_context = "objectmode"


	@classmethod
	def poll(self,context):
		return context.object is not None

	def draw(self, context):
		layout = self.layout
		scene = context.scene
		myaddon = scene.my_addon
		ob = context.object

		split = layout.split()

		if ob:
			layout.template_ID(ob, "active_material", new="material.new")
			row = layout.row()
			row.operator("object.apply_material_to_all")
			


class BrenderRenderPanel(View3DPanel, Panel):
	bl_idname = "OBJECT_PT_Brender_render_panel"
	bl_label = "Brender Render Tools"
	bl_category = 'Brender'
	bl_context = "objectmode"
	# Removed poll classmethod so that this 
	# panel is always visible

	# Add UI elements here
	def draw(self, context):
		layout = self.layout
		scene = context.scene
		myaddon = scene.my_addon

		row = layout.row()
		row.prop(myaddon, "wireframe_obj_string")

		split = layout.split()
		col = split.column()
		col.label(text="Bevel: ")
		col.prop(myaddon, "wf_bevel_depth")
		col.prop(myaddon, "wf_bevel_resolution")

		col = split.column()
		col.label(text="Modification: (Under Construction)")
		col.prop(myaddon, "wf_offset")
		col.prop(myaddon, "wf_extrude")

		row = layout.row()
		row.operator("object.wireframe_overlay_preview")

		row = layout.row()
		row.operator("object.wireframe_overlay")



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