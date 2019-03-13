import bpy
import mathutils

bpy.ops.mesh.primitive_plane_add()
pln = bpy.context.active_object
pln.name = "background"
pln.location = mathutils.Vector((0.0, 0.0, -0.025))
pln.scale =  mathutils.Vector((5.0, 5.0, 5.0))

if bpy.data.materials.get("BlackMaterial") is None:
	# create cube material
	mat_name = "BlackMaterial"
	mat = bpy.data.materials.new(mat_name)
	mat.use_nodes = True 
	nodes = mat.node_tree.nodes
	diffnode = nodes["Diffuse BSDF"]
	# apply checker primary and secondary colors
	diffnode.inputs[0].default_value = (0.0, 0.0, 0.0, 1)
	diffnode.inputs[1].default_value = (0.0)

pln = bpy.data.objects['background']
mat = bpy.data.materials.get("BlackMaterial")
pln.select = True

if pln.data.materials:
	pln.data.materials[0] = mat
else:
	pln.data.materials.append(mat)
pln.select = False	
