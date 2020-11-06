###############################################################################
#       Brender Panel
#
#       Author: Nick Weidner
#       Version: 1.0.0
###############################################################################

import bpy
import os
import json
import string
import math
import bmesh

###############################################################################
#       Settings Structures
###############################################################################

class BrenderSettings(bpy.types.PropertyGroup):

    obj_frame_skip: bpy.props.IntProperty(
        name = "obj_frame_skip",
        description = "An integer property",
        default = 0,
        min = 0,
        max = 100
    )

    obj_frame_pause: bpy.props.IntProperty(
        name = "obj_frame_pause",
        description = "An integer property",
        default = 1,
        min = 1,
        max = 100
    )

    obj_frame_start: bpy.props.IntProperty(
        name = "obj_frame_start",
        description = "An integer property",
        default = 1,
        min = 0,
        max = 100
    )

    obj_axis_forward: bpy.props.StringProperty(
        name = "obj_axis_forward",
        description = "A string property",
        default = "-Z",
        maxlen = 2
    )

    obj_axis_up: bpy.props.StringProperty(
        name = "obj_axis_up",
        description = "A string property",
        default = "Y",
        maxlen = 2
    )

    ply_frame_skip: bpy.props.IntProperty(
        name = "ply_frame_skip",
        description = "An integer property",
        default = 0,
        min = 0,
        max = 100
    )

    ply_frame_pause: bpy.props.IntProperty(
        name = "ply_frame_pause",
        description = "An integer property",
        default = 1,
        min = 1,
        max = 100
    )

    ply_frame_start: bpy.props.IntProperty(
        name = "ply_frame_start",
        description = "An integer property",
        default = 1,
        min = 0,
        max = 100
    )

    ply_scaling: bpy.props.FloatProperty(
        name = "ply_scaling",
        description = "A float property",
        default = 1.0,
        min = 0.0,
        max = 100.0
    )

    rigid_frame_skip: bpy.props.IntProperty(
        name = "rigid_frame_skip",
        description = "An integer property",
        default = 0,
        min = 0,
        max = 100
    )

    matset_object_name_head: bpy.props.StringProperty(
        name = "matset_object_name_head",
        description = "A string property",
        default = "",
        maxlen = 30
    )

    transform_name_head: bpy.props.StringProperty(
        name = "transform_name_head",
        description = "A string property",
        default = "",
        maxlen = 30
    )

    transform_location_x: bpy.props.IntProperty(
        name = "transform_location_x",
        description = "An integer property",
        default = 0
    )

    transform_location_x: bpy.props.FloatProperty(
        name = "transform_location_x",
        description = "A float property",
        default = 0.0
    )

    transform_location_y: bpy.props.FloatProperty(
        name = "transform_location_y",
        description = "A float property",
        default = 0.0
    )

    transform_location_z: bpy.props.FloatProperty(
        name = "transform_location_z",
        description = "A float property",
        default = 0.0
    )

    transform_lock_x: bpy.props.BoolProperty(
        name = "transform_lock_x",
        description = "A bool property",
        default = False
    )

class MaterialSetCollection(bpy.types.PropertyGroup):
    #name: StringProperty() -> Instantiated by default
    material: bpy.props.PointerProperty(
        name="Material",
        type=bpy.types.Material)

###############################################################################
#       Worker Functions
###############################################################################

class LOAD_OT_obj_as_anim(bpy.types.Operator):
    bl_idname = "load.obj_as_anim"
    bl_label = "Load OBJ as Anim"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Import Obj sequence as animation(s)"

    filepath: bpy.props.StringProperty(name="File path", description="File filepath of Obj", maxlen=4096, default="")
    filter_folder: bpy.props.BoolProperty(name="Filter folders", description="", default=True, options={'HIDDEN'})
    filter_glob: bpy.props.StringProperty(default="*.obj", options={'HIDDEN'})
    files: bpy.props.CollectionProperty(name='File path', type=bpy.types.OperatorFileListElement)
    obj_frame_skip: bpy.props.IntProperty()
    obj_frame_pause: bpy.props.IntProperty()
    obj_frame_start: bpy.props.IntProperty()
    obj_axis_forward: bpy.props.StringProperty()
    obj_axis_up: bpy.props.StringProperty()

    objects: []

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        self.objects=[]
        self.obj_frame_skip = bpy.context.scene.BrenderSettings.obj_frame_skip
        self.obj_frame_pause = bpy.context.scene.BrenderSettings.obj_frame_pause
        self.obj_frame_start = bpy.context.scene.BrenderSettings.obj_frame_start
        self.obj_axis_forward = bpy.context.scene.BrenderSettings.obj_axis_forward
        self.obj_axis_up = bpy.context.scene.BrenderSettings.obj_axis_up

        # #get file names, sort, and set target mesh
        spath = os.path.split(self.filepath)
        files = {};
        for file in self.files:
            file_name = ''.join(os.path.splitext(file.name)[0])
            file_head = file_name.rstrip(string.digits)
            print(file_head)
            if file_head in files.keys():
                files[file_head].append(file.name)
            else:
                files[file_head] = []
                files[file_head].append(file.name)

        for file_head in files:
            files[file_head].sort()

        # #add all objs to scene
        # # this makes the frame skip option available
        lastframemax = -1;
        for file_head in files:
            count=0
            lastframe = 0
            modval = self.obj_frame_skip + 1
            for f in files[file_head]:
                fp = spath[0] + "/" + f
                if (self.obj_frame_skip == 0) or (count % modval == 0):
                    fp = spath[0] + "/" + f
                    self.load_obj(fp,f,self.obj_axis_forward,self.obj_axis_up)
                    lastframe+=1
                count+=1
            if lastframe > lastframemax:
                lastframemax = lastframe

        objects = {};
        for obj in self.objects:
            obj_name_head = obj.name.rstrip(string.digits)
            if obj_name_head in objects.keys():
                objects[obj_name_head].append(obj)
            else:
                objects[obj_name_head] = []
                objects[obj_name_head].append(obj)

        bpy.context.scene.frame_start = self.obj_frame_start
        bpy.context.scene.frame_end = (lastframemax + self.obj_frame_start) + (lastframemax * (self.obj_frame_pause - 1)) - 1
        #print(files)

        for obj_name_head in objects:
            bpy.context.scene.frame_set(1)
            for i, ob in enumerate(objects[obj_name_head]):
                ob.hide_viewport = ob.hide_render = True
                ob.keyframe_insert(data_path='hide_viewport')
                ob.keyframe_insert(data_path='hide_render')

            for f, ob in enumerate(objects[obj_name_head]):
                # adjust f based on start and pause
                adjustedf = f + self.obj_frame_start
                if f > 0:
                    adjustedf += f * (self.obj_frame_pause - 1)
                # increment current frame to insert keyframe
                bpy.context.scene.frame_set(adjustedf)

                # Insert only as many keyframes as really needed
                if f > 0:
                    ob_prev = objects[obj_name_head][f-1]
                    ob_prev.hide_viewport = ob_prev.hide_render = True
                    ob_prev.keyframe_insert(data_path='hide_viewport')
                    ob_prev.keyframe_insert(data_path='hide_render')

                ob = objects[obj_name_head][f]
                ob.hide_viewport = ob.hide_render = False
                ob.keyframe_insert(data_path='hide_viewport')
                ob.keyframe_insert(data_path='hide_render')

                # Remove duplicate materials
                mats = bpy.data.materials
                for slot in ob.material_slots:
                    #print(slot.name)
                    part = slot.name.rpartition('.')
                    mat =  mats.get(part[0])
                    if part[2].isnumeric() and mat is not None:
                        slot.material = mat



        # Uncomment Following to keep track of Brender Objects
        # for name in files:
        #   BRENDER_object_names.append(name.split('.', 1)[0]) # takes off .obj


        return{'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def load_obj(self, fp,fname):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.import_scene.obj(filepath=fp, filter_glob="*.obj;*.mtl",  use_edges=True, use_smooth_groups=True, use_split_objects=True, use_split_groups=True, use_groups_as_vgroups=False, use_image_search=True, split_mode='ON', global_clight_size=0.0, axis_forward='Z', axis_up='-Y')
        self.objects.append(bpy.context.selected_objects[0])
        return

    def load_obj(self, fp,fname, afor, aup):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.import_scene.obj(filepath=fp, filter_glob="*.obj;*.mtl",  use_edges=True, use_smooth_groups=True, use_split_objects=True, use_split_groups=True, use_groups_as_vgroups=False, use_image_search=True, split_mode='ON', global_clight_size=0.0, axis_forward=afor, axis_up=aup)
        self.objects.append(bpy.context.selected_objects[0])
        return

class LOAD_OT_ply_as_anim(bpy.types.Operator):
    bl_idname = "load.ply_as_anim"
    bl_label = "Load PLY as Anim"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Import Obj sequence as animation(s)"

    filepath: bpy.props.StringProperty(name="File path", description="File filepath of Obj", maxlen=4096, default="")
    filter_folder: bpy.props.BoolProperty(name="Filter folders", description="", default=True, options={'HIDDEN'})
    filter_glob: bpy.props.StringProperty(default="*.ply", options={'HIDDEN'})
    files: bpy.props.CollectionProperty(name='File path', type=bpy.types.OperatorFileListElement)
    obj_frame_skip: bpy.props.IntProperty()
    obj_frame_pause: bpy.props.IntProperty()
    obj_frame_start: bpy.props.IntProperty()
    obj_axis_forward: bpy.props.StringProperty()
    obj_axis_up: bpy.props.StringProperty()

    objects: []

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        self.objects=[]
        self.ply_frame_skip = bpy.context.scene.BrenderSettings.ply_frame_skip
        self.ply_frame_pause = bpy.context.scene.BrenderSettings.ply_frame_pause
        self.ply_frame_start = bpy.context.scene.BrenderSettings.ply_frame_start
        self.ply_scaling = bpy.context.scene.BrenderSettings.ply_scaling

        # #get file names, sort, and set target mesh
        spath = os.path.split(self.filepath)
        #files = [file.name for file in self.files]
        #files.sort()
        files = {};
        for file in self.files:
            file_name = ''.join(os.path.splitext(file.name)[0])
            file_head = file_name.rstrip(string.digits)
            print(file_head)
            if file_head in files.keys():
                files[file_head].append(file.name)
            else:
                files[file_head] = []
                files[file_head].append(file.name)

        for file_head in files:
            files[file_head].sort()

        # #add all objs to scene
        # # this makes the frame skip option available
        lastframemax = -1;
        for file_head in files:
            count=0
            lastframe = 0
            modval = self.ply_frame_skip + 1
            for f in files[file_head]:
                fp = spath[0] + "/" + f
                if (self.ply_frame_skip == 0) or (count % modval == 0):
                    fp = spath[0] + "/" + f
                    self.load_ply(fp)
                    lastframe+=1
                count+=1
            if lastframe > lastframemax:
                lastframemax = lastframe

        objects = {};
        for obj in self.objects:
            obj.scale = (self.ply_scaling, self.ply_scaling, self.ply_scaling);
            # TODO :: This is all hacked in for now, GUI this up
            obj.rotation_euler = (math.pi/2,0,0)
            me = obj.data
            #bm = bmesh.from_edit_mesh(me)
            #bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0)
            #bmesh.update_edit_mesh(obj.data)
            bm = bmesh.new()
            bm.from_mesh(me)
            bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
            for f in bm.faces:
                f.smooth = True
            bm.to_mesh(me)
            me.update()
            bm.clear()
            bm.free()
            # END TODO
            obj_name_head = obj.name.rstrip(string.digits)
            if obj_name_head in objects.keys():
                objects[obj_name_head].append(obj)
            else:
                objects[obj_name_head] = []
                objects[obj_name_head].append(obj)

        bpy.context.scene.frame_start = self.ply_frame_start
        bpy.context.scene.frame_end = (lastframemax + self.ply_frame_start) + (lastframemax * (self.ply_frame_pause - 1)) - 1
        #print(files)

        for obj_name_head in objects:
            bpy.context.scene.frame_set(1)
            for i, ob in enumerate(objects[obj_name_head]):
                ob.hide_viewport = ob.hide_render = True
                ob.keyframe_insert(data_path='hide_viewport')
                ob.keyframe_insert(data_path='hide_render')

            for f, ob in enumerate(objects[obj_name_head]):
                # adjust f based on start and pause
                adjustedf = f + self.ply_frame_start
                if f > 0:
                    adjustedf += f * (self.ply_frame_pause - 1)
                # increment current frame to insert keyframe
                bpy.context.scene.frame_set(adjustedf)

                # Insert only as many keyframes as really needed
                if f > 0:
                    ob_prev = objects[obj_name_head][f-1]
                    ob_prev.hide_viewport = ob_prev.hide_render = True
                    ob_prev.keyframe_insert(data_path='hide_viewport')
                    ob_prev.keyframe_insert(data_path='hide_render')

                ob = objects[obj_name_head][f]
                ob.hide_viewport = ob.hide_render = False
                ob.keyframe_insert(data_path='hide_viewport')
                ob.keyframe_insert(data_path='hide_render')

                # Remove duplicate materials
                mats = bpy.data.materials
                for slot in ob.material_slots:
                    #print(slot.name)
                    part = slot.name.rpartition('.')
                    mat =  mats.get(part[0])
                    if part[2].isnumeric() and mat is not None:
                        slot.material = mat



        # Uncomment Following to keep track of Brender Objects
        # for name in files:
        #   BRENDER_object_names.append(name.split('.', 1)[0]) # takes off .obj


        return{'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def load_ply(self, fp):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.import_mesh.ply(filepath=fp)
        self.objects.append(bpy.context.selected_objects[0])
        return

class LOAD_OT_rigid_as_anim(bpy.types.Operator):
    bl_idname = "load.rigid_as_anim"
    bl_label = "Load RIGID Json as Animation"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = 'Import Rigids for each frame of animation'

    filepath: bpy.props.StringProperty(name="File path", description="Filepath of Json", maxlen=4096, default="")
    filter_folder: bpy.props.BoolProperty(name="Filter folders", description="", default=True, options={'HIDDEN'})
    filter_glob: bpy.props.StringProperty(default="*.json", options={'HIDDEN'})
    files: bpy.props.CollectionProperty(name='File path', type=bpy.types.OperatorFileListElement)
    filename_ext = '.json'

    frames: bpy.props.IntProperty()
    objects = dict()
    states = dict()

    @classmethod
    def poll(cls, context):
        return True

    def execute (self, context):
        # get the first transformation file given
        spath = os.path.split(self.filepath)
        files = [file.name for file in self.files]
        for file in files:
            fp = spath[0] + "/" + file
            with open(fp) as f:
                transformations = json.load(f)
            fname = os.path.splitext(file)[0]
            self.load_states(transformations, fname)

        for frame in transformations["body"]:
            self.load_frame(frame)

        bpy.context.scene.frame_set(0)

        # sets last frame to the last transformation
        if self.frames > 0:
            bpy.context.scene.frame_end = self.frames - 1
        else:
            bpy.context.scene.frame_end = 0

        return{'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def load_states(self, transformations, fname):

        for state in transformations["header"]["states"]:
            # we receive the corresponding object index and name
            # then, we add that name to a dictionary, with the file path as key
            index = state["obj"]
            name = state["name"]
            self.states[name] = transformations["header"]["objs"][index]
            self.load_obj(self.states[name], name)

        return

    def load_obj(self, fp, name):
        # this implementation can let multiple objects be imported, but let's assume it is just one...
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.import_scene.obj(filepath=fp, filter_glob="*.obj;*.mtl",  use_edges=True, use_smooth_groups=True, use_split_objects=True, use_split_groups=True, use_groups_as_vgroups=False, use_image_search=True, split_mode='ON', global_clight_size=0, axis_forward='Y', axis_up='Z')
        # take the first element of the newly created objects (ideally there's just one) and
        bpy.context.selected_objects[0].name = name
        return

    def load_frame(self, frame):
        # make frame-1 to frame in order to fix the indexing problem
        bpy.context.scene.frame_set(frame["frame"]-1)
        for obj_to_load in frame:
            if obj_to_load == "frame": # we do not process anything with "frame"
                continue
            # obj = self.objects[obj_to_load] # gets the object from the name
            self.report({'INFO'}, obj_to_load)
            obj = bpy.data.objects[obj_to_load]
            self.report({'INFO'}, obj.name)
            # SRT
            obj.rotation_mode = 'QUATERNION'
            obj.scale = (frame[obj_to_load]["scale"][0],frame[obj_to_load]["scale"][1],frame[obj_to_load]["scale"][2])
            obj.rotation_quaternion = (frame[obj_to_load]["quat"][3],frame[obj_to_load]["quat"][0],frame[obj_to_load]["quat"][1],frame[obj_to_load]["quat"][2])
            obj.location = (frame[obj_to_load]["location"][0],frame[obj_to_load]["location"][1],frame[obj_to_load]["location"][2])
            obj.keyframe_insert(data_path='scale')
            obj.keyframe_insert(data_path='rotation_quaternion')
            obj.keyframe_insert(data_path='location')

        return

class CREATE_OT_matlab_material_set(bpy.types.Operator):
    bl_idname = "create.matlab_material_set"
    bl_label = "Create matlab material set"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = 'Creates a material set of the matlab colors'

    which_set: bpy.props.EnumProperty(
        items=(
            ('MATLAB', "Matlab", ""),
            ('OTHER', "Other", "")))

    def execute(self, context):
        if self.which_set == 'MATLAB':
            self.add_material('MCDarkBlue', 0.0, 0.4470, 0.7410)
            self.add_material('MCOrange', 0.8500, 0.3250, 0.0980)
            self.add_material('MCYellow', 0.9290, 0.6940, 0.1250)
            self.add_material('MCPurple', 0.4940, 0.1840, 0.5560)
            self.add_material('MCGreen', 0.4660, 0.6740, 0.1880)
            self.add_material('MCLightBlue', 0.3010, 0.7450, 0.9330)
            self.add_material('MCRed', 0.6350, 0.0780, 0.1840)
        if self.which_set == 'OTHER':
            self.add_material('MCDarkBlue', 0.0, 0.4470, 0.7410)
            self.add_material('MCDarkBlue', 0.0, 0.4470, 0.7410)

        return {'FINISHED'}

    def add_material(self, material_name, r, g, b):
        material = bpy.data.materials.get(material_name)
        if material is None:
            material = bpy.data.materials.new(material_name)
        material.use_nodes = True
        principled_bsdf = material.node_tree.nodes.get('Principled BSDF')
        if principled_bsdf is not None:
            principled_bsdf.inputs[0].default_value = (r, g, b, 1)

class TAKE_OT_material_action(bpy.types.Operator):
    bl_idname = "take.material_action"
    bl_label = "Action for material tab"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = 'Different actions for the materials tab'

    mat_name: bpy.props.StringProperty(name="String Value")

    action: bpy.props.EnumProperty(
        items=(
            ('ADD', "Add", ""),
            ('REMOVE', "Remove", "")))

    def invoke(self, context, event):
        scn = context.scene
        idx = scn.BrenderMaterialSetSelectionIndex

        if self.action == 'ADD':
            item = scn.BrenderMaterialSet.add()
            item.material = bpy.data.materials[self.mat_name]
        if self.action == 'REMOVE':
            scn.BrenderMaterialSet.remove(idx)
        return {'FINISHED'}

class APPLY_OT_material_to_all(bpy.types.Operator):
    """Apply Animation Object Material"""
    bl_idname = "apply.material_to_all"
    bl_label = "Apply Selected Material"
    bl_options = {'REGISTER', 'UNDO'}

    matset_object_name_head: bpy.props.StringProperty()

    def execute(self, context):
        scn = context.scene
        self.matset_object_name_head = bpy.context.scene.BrenderSettings.matset_object_name_head
        print(self.matset_object_name_head)
        subset = [s for s in bpy.data.objects if self.matset_object_name_head in s.name]
        objhead = [];
        for obj in subset:
            objname = obj.name.rstrip(string.digits)
            if objname not in objhead:
                objhead.append(objname)
            idx = objhead.index(objname) % len(scn.BrenderMaterialSet)
            item = scn.BrenderMaterialSet[idx]
            mat = item.material
            obj.select_set(True)
            if obj.data.materials:
                obj.data.materials[0] = mat
            else:
                obj.data.materials.append(mat)
            obj.select_set(False)
        # for obj in bpy.data.objects:
            # print(obj.name)
        # for item in scn.BrenderMaterialSet:
            # mat = item.material
            # print(mat.name)
        # for obj in bpy.data.objects:
            # if obj.name.endswith(brenderObjname): # same last letters as brenderobj
                # obj.select_set(True)
                # # append Material
                # if obj.data.materials:
                    # obj.data.materials[0] = mat
                # else:
                    # obj.data.materials.append(mat)
                # obj.select_set(False)
        return {'FINISHED'}

class APPLY_OT_translate(bpy.types.Operator):
    """Apply Animation Object Material"""
    bl_idname = "apply.translate"
    bl_label = "Apply Translate to Object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = context.scene
        self.transform_name_head = bpy.context.scene.BrenderSettings.transform_name_head
        self.tX = bpy.context.scene.BrenderSettings.transform_location_x
        self.tY = bpy.context.scene.BrenderSettings.transform_location_y
        self.tZ = bpy.context.scene.BrenderSettings.transform_location_z
        print(self.transform_name_head)
        subset = [s for s in bpy.data.objects if self.transform_name_head in s.name]
        objhead = [];
        for obj in subset:
            #print(obj)
            #print(obj.location)
            obj.location[0] = self.tX
            obj.location[1] = self.tY
            obj.location[2] = self.tZ
        return {'FINISHED'}

###############################################################################
#       Brender Menus
###############################################################################

class BRENDER_MT_material_set_menu(bpy.types.Menu):
    bl_label = "Material Set"
    bl_idname = "BRENDER_MT_material_set_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("create.matlab_material_set", text="Matlab Colors").which_set = 'MATLAB'
        layout.operator("create.matlab_material_set", text="Other Colors").which_set = 'OTHER'

class BRENDER_MT_add_material_menu(bpy.types.Menu):
    bl_label = "Add MAterial"
    bl_idname = "BRENDER_MT_add_material_menu"

    def draw(self, context):
        layout = self.layout
        for mat in bpy.data.materials:
            op = layout.operator("take.material_action", text=mat.name, icon="MATERIAL")
            op.action = 'ADD'
            op.mat_name = mat.name

###############################################################################
#       Brender UL items
###############################################################################

class BRENDER_UL_material_set_items(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        mat = item.material
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(mat, "name", text="", emboss=False, icon_value=layout.icon(mat))

    def invoke(self, context, event):
        pass

###############################################################################
#       Brender Panels
###############################################################################

class BRENDER_PT_import_obj_anim(bpy.types.Panel):
    bl_label = "Import OBJ as Anim"
    bl_category = "Brender"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        props = bpy.context.scene.BrenderSettings
        layout = self.layout

        col0 = layout.column(align=True)
        rowsub = col0.row(align=True)
        rowsub.label(text="Skip Frames")
        rowsub.prop(props, "obj_frame_skip", text="")

        col1 = layout.column(align=True)
        rowsub = col1.row(align=True)
        rowsub.label(text="Puase Frames")
        rowsub.prop(props, "obj_frame_pause", text="")

        col2 = layout.column(align=True)
        rowsub = col2.row(align=True)
        rowsub.label(text="Start Frame")
        rowsub.prop(props, "obj_frame_start", text="")

        col3 = layout.column()
        rowsub2 = col3.row(align=True)
        rowsub2.label(text="Forward Axis")
        rowsub2.prop(props, "obj_axis_forward", text="")

        col4 = layout.column()
        rowsub3 = col4.row(align=True)
        rowsub3.label(text="Up Axis")
        rowsub3.prop(props, "obj_axis_up", text="")

        col5 = layout.column()
        rowsub4 = col5.row(align=True)
        rowsub4.operator("load.obj_as_anim")

        #rowsub.label(text="Forward Axis")
        #rowsub.prop(props, "obj_axis_forward", text="")

        #rowsub = col.row(align=True)
        #col2 = layout.column()
        #rowsub2 = col2.row()
        #rowsub2.operator("load.obj_as_anim")

class BRENDER_PT_import_ply_anim(bpy.types.Panel):
    bl_label = "Import PLY as Anim"
    bl_category = "Brender"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        props = bpy.context.scene.BrenderSettings
        layout = self.layout

        col0 = layout.column(align=True)
        rowsub = col0.row(align=True)
        rowsub.label(text="Skip Frames")
        rowsub.prop(props, "ply_frame_skip", text="")

        col1 = layout.column(align=True)
        rowsub = col1.row(align=True)
        rowsub.label(text="Puase Frames")
        rowsub.prop(props, "ply_frame_pause", text="")

        col2 = layout.column(align=True)
        rowsub = col2.row(align=True)
        rowsub.label(text="Start Frame")
        rowsub.prop(props, "ply_frame_start", text="")

        col3 = layout.column()
        rowsub2 = col3.row(align=True)
        rowsub2.label(text="Scaling")
        rowsub2.prop(props, "ply_scaling", text="")

        col5 = layout.column()
        rowsub4 = col5.row(align=True)
        rowsub4.operator("load.ply_as_anim")

class BRENDER_PT_import_rigid_anim(bpy.types.Panel):
    bl_label = "Import RIGID as Anim"
    bl_category = "Brender"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        props = bpy.context.scene.BrenderSettings
        layout = self.layout

        col = layout.column(align=True)
        rowsub = col.row(align=True)

        rowsub.label(text="Skip Frames")
        rowsub.prop(props, "rigid_frame_skip", text="")

        col2 = layout.column()
        rowsub2 = col2.row(align=True)
        rowsub2.operator("load.rigid_as_anim")

class BRENDER_PT_apply_materials(bpy.types.Panel):
    bl_label = "Apply Materials"
    bl_category = "Brender"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"

    def draw(self, context):
        props = bpy.context.scene.BrenderSettings
        layout = self.layout
        scn = bpy.context.scene

        layout.menu(BRENDER_MT_material_set_menu.bl_idname, text="Load Material Presets", icon="MATERIAL")

        # https://gist.github.com/p2or/30b8b30c89871b8ae5c97803107fd494
        rows = 2
        row = layout.row()
        row.template_list("BRENDER_UL_material_set_items", "custom_def_list", scn, "BrenderMaterialSet",
            scn, "BrenderMaterialSetSelectionIndex")

        col = row.column(align=True)
        #col.operator("object.select_random", icon='ADD', text="")
        col.menu(BRENDER_MT_add_material_menu.bl_idname, text="", icon="ADD")
        col.operator("take.material_action", icon='REMOVE', text="").action = 'REMOVE'
        col.operator("object.select_random", icon='PANEL_CLOSE', text="")

        col2 = layout.column()
        rowsub2 = col2.row(align=True)
        rowsub2.label(text="Object Name")
        rowsub2.prop(props, "matset_object_name_head", text="")

        col3 = layout.column()
        rowsub3 = col3.row(align=True)
        rowsub3.operator("apply.material_to_all", text="Apply Materials")

class BRENDER_PT_translate_brenders(bpy.types.Panel):
    bl_label = "Translate Brenders"
    bl_category = "Brender"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"

    def draw(self, context):
        props = bpy.context.scene.BrenderSettings
        layout = self.layout
        scn = bpy.context.scene

        col = layout.column()
        rowsub = col.row(align=True)
        split = rowsub.split(factor=0.8)
        c = split.column()
        c.prop(props, "transform_location_x", text="X", text_ctxt="MM")
        # split = split.split()
        # c = split.column()
        # icon = "LOCKED" if props.transform_lock_x else "UNLOCKED"
        # c.prop(props, "transform_lock_x", icon=icon, text="", emboss=False)

        col2 = layout.column()
        rowsub2 = col2.row(align=True)
        split2 = rowsub2.split(factor=0.8)
        c2 = split2.column()
        c2.prop(props, "transform_location_y", text="Y", text_ctxt="MM")

        col3 = layout.column()
        rowsub3 = col3.row(align=True)
        split3 = rowsub3.split(factor=0.8)
        c3 = split3.column()
        c3.prop(props, "transform_location_z", text="Z", text_ctxt="MM")

        col4 = layout.column()
        rowsub4 = col4.row(align=True)
        rowsub4.label(text="Object Name")
        rowsub4.prop(props, "transform_name_head", text="")

        col5 = layout.column()
        rowsub5 = col5.row(align=True)
        rowsub5.operator("apply.translate", text="Translate")

###############################################################################
#       Brender Register & Unregister
###############################################################################

classes = (
    BrenderSettings,
    MaterialSetCollection,
    LOAD_OT_obj_as_anim,
    LOAD_OT_ply_as_anim,
    LOAD_OT_rigid_as_anim,
    APPLY_OT_material_to_all,
    APPLY_OT_translate,
    CREATE_OT_matlab_material_set,
    TAKE_OT_material_action,
    BRENDER_MT_material_set_menu,
    BRENDER_MT_add_material_menu,
    BRENDER_UL_material_set_items,
    BRENDER_PT_import_obj_anim,
    BRENDER_PT_import_ply_anim,
    BRENDER_PT_import_rigid_anim,
    BRENDER_PT_apply_materials,
    BRENDER_PT_translate_brenders,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.BrenderSettings = bpy.props.PointerProperty(type=BrenderSettings)
    bpy.types.Scene.BrenderMaterialSet = bpy.props.CollectionProperty(type=MaterialSetCollection)
    bpy.types.Scene.BrenderMaterialSetSelectionIndex = bpy.props.IntProperty()


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del(bpy.types.Scene.BrenderSettings)
    del(bpy.types.Scene.BrenderMaterialSetSelectionIndex)

if __name__ == "__main__":
    register()
