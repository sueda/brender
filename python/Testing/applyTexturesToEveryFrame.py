import bpy, os
import mathutils

# https://wiki.blender.org/index.php/Dev:Py/Scripts/Cookbook/Code_snippets/Materials_and_textures

# path to image and load image
texpath = os.path.expanduser('C:/Users/Gus/Documents/GitHub/Brender/brender/python/Textures/christmasPattern2.jpg')
try:
    img = bpy.data.images.load(texpath)
except:
    raise NameError("Cannot load image %s" % texpath)

# Create image texture from image
myTex = bpy.data.textures.new('ChristmasTex', type = 'IMAGE')
myTex.image = img

# Create material
mat = bpy.data.materials.new('TexMat')


# Add texture slot for color texture
mtex = mat.texture_slots.add()
mtex.texture = myTex
mtex.texture_coords = 'UV'
mtex.use_map_color_diffuse = True 
mtex.use_map_color_emission = True 
mtex.emission_color_factor = 0.5
mtex.use_map_density = True 
mtex.mapping = 'FLAT'

# enable use nodes
## mat.use_nodes = True
## nodes = mat.node_tree.nodes

# add diffuse shader and set location
## node = nodes.new('ShaderNodeBsdfDiffuse')
## node.location = (100,100)


for obj in bpy.data.objects:
    if obj.name.startswith("0"):
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