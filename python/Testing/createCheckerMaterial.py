import bpy

mat_name = "ClothMaterial"
mat = bpy.data.materials.new(mat_name)
mat.use_nodes = True 
nodes = mat.node_tree.nodes

# diffuse node is made by default
# node = nodes.new('ShaderNodeBsdfDiffuse')
# node.location = (100,100)
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