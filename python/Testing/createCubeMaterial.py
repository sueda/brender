import bpy

mat_name = "CubeMaterial"
mat = bpy.data.materials.new(mat_name)
mat.use_nodes = True 
nodes = mat.node_tree.nodes

diffnode = nodes["Diffuse BSDF"]


# apply checker primary and secondary colors
diffnode.inputs[0].default_value = (0.198, 0.371, 0.694, 1)