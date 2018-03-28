import bpy
import mathutils

if bpy.data.materials.get("Wireframe2DMaterial") is None:
	# create cube material
	mat_name = "Wireframe2DMaterial"
	mat = bpy.data.materials.new(mat_name)
	mat.use_nodes = True 
	nodes = mat.node_tree.nodes
	emissnode = nodes.new(type='ShaderNodeEmission')
	diffnode = nodes["Diffuse BSDF"]
	outputnode = nodes["Material Output"]
	# delete the diffuse node
	nodes.remove(diffnode)
	# apply emission defaults
	# emission color
	emissnode.inputs[0].default_value = (0.8, 0.8, 0.8, 1)
	#emission strength
	emissnode.inputs[1].default_value = (5.0)
	# link node to output
	links = mat.node_tree.links
	links.new(emissnode.outputs[0], outputnode.inputs[0])