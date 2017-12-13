import bpy, os
import mathutils

# Create material
mat = bpy.data.materials.new(name='MeshMat')
mat.diffuse_color = (0.000811812, 0.8, 0.683532)



# enable use nodes
## mat.use_nodes = True
## nodes = mat.node_tree.nodes

# add diffuse shader and set location
## node = nodes.new('ShaderNodeBsdfDiffuse')
## node.location = (100,100)


for obj in bpy.data.objects:
    if obj.name.startswith("0") and obj.name.endswith("001"):
        theobj = bpy.data.objects[obj.name]
        theobj.select = True
        objdata = obj.data
        # append Material
        objdata.materials.append(mat)
        theobj.select = False
        # mat = bpy.data.materials['Material']
        # tex = bpy.data.textures.new("christmas1", 'C:\\Users\\Gus\\Desktop\\christmasPattern2.jpg')
        
        # bpy.ops.material.new()
        
        #theobj.material_slots.add(mat)
        # matslot = theobj.material_slots
        
        # tex = bpy.data.textures.new("christmas1", 'C:\\Users\\Gus\\Desktop\\christmasPattern2.jpg')
        # slot = mat.texture_slots.add()
        # slot.texture = tex
        # theobj.material.new()
        # bpy.context.space_data.bookmarks_active = 0
        
        # obj.data.materials[0] = mat
        
        # theobj.scale=(2,2,2)
        # vec = mathutils.Vector((0.0,0.0,0.5))
        # theobj.location = theobj.location + vec