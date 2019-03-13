import bpy
from random import randint


# STEP 1 - ENTER EDIT MODE

# setting the mesh to edit mode
# scene = bpy.context.scene
# scene.layers = [True] * 20 # Show all layers

# for obj in scene.objects:
#     if obj.type == 'MESH':
#         scene.objects.active = obj

#         bpy.ops.object.mode_set(mode='EDIT')


# setting it back to object mode
#         bpy.ops.object.mode_set(mode='OBJECT')

# STEP 2 - SET ALL OBJECTS AND MARK AS FREESTYLE EDGE

# context = bpy.context
# mesh = context.object.data

# for e in mesh.edges:
#     e.use_freestyle_mark = True


# STEP 3 - ENABLE FREESTYLE IN PROPERTIES EDITOR --> RENDER SETTINGS --> FREESTYLE



# STEP 4 - ENABLE EDGE MARKS IN PROPERTIES EDITOR --> RENDER LAYERS --> FREESTYLE LINESET --> EDGE MARKS



# this makes a bunch of cubes

if __name__ == "__main__":
	object_count = 1
	frame_count = 10


	for c in range(object_count):
		# x = randint(-10,10)
		# y = randint(-10,10)
		# z = randint(-10,10)
		bpy.ops.mesh.primitive_cube_add(location=(0,0,0), radius=1)
		#ob = bpy.context.selected_objects[0]
		for edge in bpy.context.selected_objects[0].data.edges:
			edge.use_freestyle_mark = True

	for f in range(-1*frame_count, frame_count):
		bpy.context.scene.frame_set(f+frame_count)
		bpy.context.selected_objects[0].location = (f,f,f)
		bpy.context.selected_objects[0].keyframe_insert(data_path='location')


	bpy.context.scene.frame_set(0)
