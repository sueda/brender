bl_info = {
	'name': 'Load Obj and Rigid Sequence as Base Frame',
	'author': 'Khemakhem, Feras',
	'version': (0, 1),
	'blender': (2, 6, 7),
	'category': 'Import-Export',
	'location': 'File > Import/Export',
	'wiki_url': ''}

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy, os
from bpy.props import *

# # The following function imports rigid files
# class LoadRigidAsAnimation(bpy.types.Operator):
# 	bl_idname = 'load.rigid_as_anim'
# 	bl_label = 'Import RIGID as Aniamtion'
# 	bl_options = {'REGISTER', 'UNDO'}
# 	bl_description = 'Import Rigids for each frame of animation'



# The following function imports one object file as the base file for keyframe calculation in rigid bodies
class LoadObjAsBase(bpy.types.Operator):
	bl_idname = 'load.obj_as_base'
	bl_label = 'Import OBJ as Base Frame'
	bl_options = {'REGISTER', 'UNDO'}
	cFrame = 0
	bl_description = 'Import single Obj as base frame'
	filepath = StringProperty(name='File path', description='Filepath of Obj', maxlen=4096, default='')
	filter_folder = BoolProperty(name='Filter folders', description='', default=True, options={'HIDDEN'})
	filter_glob = StringProperty(default='*.obj', options={'HIDDEN'})
	files = CollectionProperty(name='File path', type=bpy.types.OperatorFileListElement)
	filename_ext = '.obj'
	object = bpy.data.objects.new(name='Dummy', object_data=None) # dummy of object is made so that we can rewrite later
	@classmethod
	def poll(cls, context):
		return True	

	def execute(self, context):
		# gets the file names, sorts, and sets target mesh
		spath = os.path.split(self.filepath)
		# extracts all if files if multiple chosen and sorts them to take the first obj in order
		files = [file.name for file in self.files] 
		files.sort()
		f = files[0]
		fp = spath[0] + "/" + f
		self.load_obj(fp, f) # calls the load function on the obj file

		bpy.context.scene.frame_set(0) # since there is only one obj file, multiple frame sets not necessary
		# bpy.context.scene.frame_end = 0 ... defaulted
		return{'FINISHED'}

	def invoke(self, context, event):
		wm = context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}

	def load_obj(self, fp, fname):
		bpy.ops.object.select_all(action='DSELECT')
		bpy.ops.import_scene.obj(filepath=fp, filter_glob='*.obj;*.mtl', use_edges=True, 
			use_smooth_groups=True, use_split_objects=True, use_split_groups=True, 
			use_groups_as_vgroups=False, use_image_search=True, split_mode='ON', 
			global_clamp_size=0, axis_forward='Y', axis_up='Z')
		self.object = bpy.context.selected_objects[0]
		return

def menu_func_import(self, context):
	self.layout.operator(LoadObjAsBase.bl_idname, text='Obj As Base Frame')

def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_file_import.append(menu_func_import)

def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.INFO_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
	register()
