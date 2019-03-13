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
unique_objs = []
# get name of 1 copy of each unique object
for obj in bpy.data.objects:
	if obj.type in ['CURVE'] or obj.type in ['MESH']:
		if "_" in obj.name:
			testname = "000000_" + obj.name.split("_",1)[1]
		else:
			testname = obj.name

		if testname not in unique_objs:
			unique_objs.append(testname)

# get material name for each unique object
# now form of: "objectName:Material"
unique_objs[:] = [name + ':' + bpy.data.objects[name].active_material.name for name in unique_objs]

for strval in unique_objs:
	mat = bpy.data.materials[strval.split(":", 1)[1]]
	# for nodes in mat.node_tree.nodes:
	# 	print(nodes.name + "_")
	# 	count = 0
	# 	for inputs in nodes:
			



print(unique_objs)
# for mat in bpy.data.materials:
# 	if mat.use_nodes:
# 		print(mat.name)
