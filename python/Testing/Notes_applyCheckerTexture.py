import bpy, os
import mathutils

#mat = bpy.ops.object.material_slot_add()
#bpy.ops.material.new()

#bpy.context.object.active_material.name = "TestMat"

#create material
mat = bpy.data.materials.new('ClothMat')
#get mat nodes
#nodes = mat.node_tree.nodes
mat.use_nodes = True
# get some specific node:
# returns None if the node does not exist
#diffuse = nodes.get("Diffuse BSDF")

# source batvh from blenderartists.org
#create new texture
tex = bpy.data.textures.new("CheckerTex", 'IMAGE')

#add texture slot to mat
mat.texture_slots.add()
# Enable 'use nodes' on the texture to use default checkerboard pattern (red/white)
tex.use_nodes = True
# Assign the texture to the new texture slot (currently active)
mat.active_texture = tex

tex.node_tree.nodes["CheckerTex"].inputs['Color1'].default_value=(0.456,0.386,0.150,1.0)
tex.node_tree.nodes["CheckerTex"].inputs['Color1'].default_value=(0.080,0.0,0.0,1.0)