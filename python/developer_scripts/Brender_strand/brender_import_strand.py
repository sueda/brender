bl_info = {
	'name': 'Load Strand obj',
	'author': 'Nick Weidner',
	'version': (0, 1),
	'blender': (2, 6, 7),
	'category': 'Import-Export',
	'location': 'File > Import/Export',
	'wiki_url': ''}

import bpy, os
from bpy.props import *
import json
import re
import time
from pprint import pprint

class LoadStrandAsAnimation(bpy.types.Operator):
	bl_idname = 'load.strand_as_anim'
	bl_label = 'Import Strand as Aniamtion'
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = 'Import strand for each frame of animation'
	filepath = StringProperty(name="File path", description="Filepath of Strand", maxlen=4096, default="")
	filter_folder = BoolProperty(name="Filter folders", description="", default=True, options={'HIDDEN'})
	filter_glob = StringProperty(default="*.strand", options={'HIDDEN'})
	files = CollectionProperty(name='File path', type=bpy.types.OperatorFileListElement)
	filename_ext = '.strand'
	objects = dict()
	states = dict()
	@classmethod
	def poll(cls, context):
		return True

	def execute (self, context):


		###### this is for deleting old frames #####
		# gather list of items of interest.
		candidate_list = [item.name for item in bpy.data.objects if item.type == "MESH"]

		# select them only.
		for object_name in candidate_list:
			bpy.data.objects[object_name].select = True

		# remove all selected.
		bpy.ops.object.delete()

		# remove the meshes, they have no users anymore.
		for item in bpy.data.meshes:
  			bpy.data.meshes.remove(item)
		self.objects.clear()
		self.states.clear()
		######## end of deleting frames #######

		spath = os.path.split(self.filepath)
		files = [file.name for file in self.files]
		files.sort()

		frame = -1 # Frame count
		curve_depth = 0.01
		curve_res = 3 # Curve resolution

		startt = time.time()
		help = 0
		for file in files:

			# self.report({'INFO'}, "currently on frame " + str(bpy.context.scene.frame_current))

			strand_file = spath[0] + "/" + file
			
			### FIRST PLACE TO OPTIMIZE
			frame = int((re.findall('\d+', file))[0])
			self.report({'INFO'}, str(frame))
				

			# list of object names
			obj_names = []

			# list of xn and Xn
			xns = []
			Xns = []
			
			# list of geometric vertices
			xn = []

			# list of texture vertices
			Xn = []

			for line in open(strand_file, "r"):
				### MAYBE OPTIMIZE IDK
				tag = line.split(None, 1)[0]

				if tag == '#': continue
				elif tag == 'o':
					val = line.split()
					obj_names.append(val[1])
					xns.append(xn)
					Xns.append(Xn)
					xn = []
					Xn = []
				elif tag == 'v':
					val = line.split()
					x = (float(val[1]), float(val[2]), float(val[3]))
					xn.append(x)
				elif tag == 'vt':
					val = line.split()
					X = float(val[1])
					Xn.append(X)
					
			xns.append(xn)
			Xns.append(Xn)
			xn = []
			Xn = []

			#middle = time.time()
			#self.report({'INFO'}, str(middle - start))
		    
			# if len(xn) != len(Xn):
				# print("x nodes size does not equal X nodes size in frame ")
				# print(frame)
				# continue

			for strand in range(1,len(xns)):

				# for timing
				start = time.time()

				obj_name = obj_names[strand-1]
				# xns[0] and Xns[0] are empty
				xn = xns[strand]
				Xn = Xns[strand]
				if len(xn) != len(Xn):
					print("x nodes size does not equal X nodes size in frame ")
					print(frame)
					continue
				
				# create the Curve Datablock
				curveData = bpy.data.curves.new('myCurve', type='CURVE')
				curveData.dimensions = '3D'

				### consider render_resolution_u for resolution in rendering, not preview
				curveData.resolution_u = 2

				# map coords to spline
				polyline = curveData.splines.new('POLY')
				polyline.points.add(len(xn)-1)
				for i, coord in enumerate(xn):
					x,y,z = coord
					polyline.points[i].co = (x + help, y-20, z, 1)

				# create Object
				curveOB = bpy.data.objects.new('myCurve', curveData)
				curveData.fill_mode = "FULL"
				curveData.bevel_depth = curve_depth
				curveData.bevel_resolution = curve_res
				curveData.use_uv_as_generated = True

				cm = curveOB.to_mesh(bpy.context.scene, False, 'PREVIEW')

				# These are the rows and columns of the UV grid
				#cols = (4 + 2 * curve_res)
				#rows = len(xn)
				cols = len(xn)
				rows = (4 + 2 * curve_res)

				col_i = 0
				row_i = 0
				poly_i = 0
				obj_create = time.time()

				
				# This loop updates the UV coordaintes based on the Xn values
				for f in cm.polygons:
					if row_i == rows:
						row_i = 0
						col_i = col_i + 1
						
					poly_i = 0
					for i in f.loop_indices:
						l = cm.loops[i]
						v = cm.vertices[l.vertex_index]
						for j,ul in enumerate(cm.uv_layers):
							if col_i == 0:
								if poly_i == 1 or poly_i == 2:
									ul.data[l.index].uv[0] = Xn[1]
							elif col_i == cols-3: # Don't edit the last column. -2 because -1 for indexing and n vertex columns is n-1 polygon columns
								if poly_i == 0 or poly_i == 3:
									ul.data[l.index].uv[0] = Xn[len(Xn)-2] # second to last
							else:
								if poly_i == 1 or poly_i == 2:
									ul.data[l.index].uv[0] = Xn[col_i+1]
								elif poly_i == 0 or poly_i == 3:
									ul.data[l.index].uv[0] = Xn[col_i]
							
						poly_i = poly_i + 1
						
					row_i = row_i + 1
				uv_time = time.time()			

				# Set the object name
				# Use frame+1 so our name matches our frame
				#print(os.path.splitext(file)[0])
				#obj_name = os.path.splitext(file)[0]
				cmo = bpy.data.objects.new(obj_name,cm)            

				scn = bpy.context.scene
				scn.objects.link(cmo)

				# Set material
				#cmo.data.materials.append(mat)
				# first_frame_time = time.time()



				# Display on frame+1 so our animation starts on frame 1 not 0
				# Don't show it before this frame
				bpy.context.scene.frame_set(frame)
				cmo.hide = cmo.hide_render = False
				cmo.keyframe_insert(data_path='hide')
				cmo.keyframe_insert(data_path='hide_render')

				# second_frame_time = time.time()

				# # Only show it this frame
				# bpy.context.scene.frame_set(frame+1)
				# cmo.hide = cmo.hide_render = False
				# cmo.keyframe_insert(data_path='hide')
				# cmo.keyframe_insert(data_path='hide_render')


				# # Don't show it after this frame
				# bpy.context.scene.frame_set(frame+2)
				# cmo.hide = cmo.hide_render = True
				# cmo.keyframe_insert(data_path='hide')
				# cmo.keyframe_insert(data_path='hide_render')

				end = time.time()
				#self.report({'INFO'}, "creating object takes " + str(obj_create - start))
				#self.report({'INFO'}, "update UV coordinates takes " + str(uv_time - obj_create))
				# self.report({'INFO'}, "umm " + str(first_frame_time - uv_time))
				# self.report({'INFO'}, "first frame takes " + str(second_frame_time - first_frame_time))
				# self.report({'INFO'}, "displaying frame+1 takes " + str(end - uv_time))

			#frame += 1
			help += 2.4

			

		bpy.context.scene.frame_end = frame - 1

		self.report({'INFO'}, "total elapsed time is " + str(time.time() - startt))


		return{'FINISHED'}

	def invoke(self, context, event):
		wm = context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}

def menu_func_import(self, context):
	self.layout.operator(LoadStrandAsAnimation.bl_idname, text="Strand As Animation")

def register():
	bpy.utils.register_class(LoadStrandAsAnimation)
	bpy.types.INFO_MT_file_import.append(menu_func_import)

def unregister():
	bpy.utils.unregister_class(LoadStrandAsAnimation)
	bpy.types.INFO_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
	register()