import bpy
import mathutils
## the following code parses though the objects in the scene and finds how many
## different objects there are
nameslist = []
for obj in bpy.data.objects:
    if obj.name.startswith("000000"):
        theobj = bpy.data.objects[obj.name]
        nameslist.append(theobj.name[7:])

list1 = []
list2 = []
## the following code separates each object into its own list 
## need to generalize into forloop for size of nameslist
for obj in bpy.data.objects:
    if obj.name.startswith(nameslist[0],7):
        theobj = bpy.data.objects[obj.name]
        list1.append(theobj.name)
    elif obj.name.startswith(nameslist[1],7):
        theobj = bpy.data.objects[obj.name]
        list2.append(theobj.name)
        