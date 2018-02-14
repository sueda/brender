import bpy
import mathutils

# Notes:
# bpy.data.objects['Camera'].location = Vector((0.4446687400341034, 0.4998286962509155, 2.0081090927124023))
# bpy.data.objects['Camera'].rotation_euler = Euler((0.0, -0.0, 0.0), 'XYZ')

# Vector((0.4861869215965271, 0.4692015051841736, 2.3256802558898926))


bpy.data.objects['Camera'].location = mathutils.Vector((0.5, 0.5, 2.15))
bpy.data.objects['Camera'].rotation_euler = mathutils.Euler((0.0, -0.0, 0.0), 'XYZ')