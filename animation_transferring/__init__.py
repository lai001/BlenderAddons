bl_info = {
    "name": "Animation transferring",
    "description": "A plugin for transfer animation",
    "author": "lai001",
    "version": (0, 0, 1),
    "blender": (3, 2, 1),
    "location": "View 3D > Sidebar > Tool > Animation transferring",
    "warning": "",
    "doc_url":"",
    "category":"Animation",
}

import bpy
from bpy.types import (Panel,)

class AnimationTransferOperator(bpy.types.Operator):
    bl_idname = "animation.transferring"
    bl_label = "Animation transferring"
    bl_options = { "REGISTER", "UNDO" }

    source: bpy.props.StringProperty(name="Source", default="")
    target: bpy.props.StringProperty(name="Target", default="")
    frame_from: bpy.props.IntProperty(name="Begin frame", default=0)
    frame_to: bpy.props.IntProperty(name="End frame", default=0)

    def invoke(self, context, event):
        result = context.window_manager.invoke_props_dialog(self)
        return result

    def execute(self, context):
        # self.report({ "INFO" }, self.source)
        keying_sets_all = bpy.data.scenes["Scene"].keying_sets_all
        keying_sets_all.active = keying_sets_all['Whole Character']
        ob = bpy.data.objects[self.target]
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.mode_set(mode='POSE')
        self.addConstraints()
        self.applyAnimation()
        self.delConstraints()
        return { "FINISHED" }

    def addConstraints(self):
        source_ob = bpy.data.objects[self.target]
        for bone in source_ob.pose.bones:
            sel_bone = source_ob.data.bones[bone.name]
            sel_bone.select = True
            bpy.context.object.data.bones.active = sel_bone
            trans_bone = bpy.context.object.pose.bones[bone.name]
            if trans_bone.constraints.find('Copy Transforms') == -1:
                if bpy.data.objects[self.source].pose.bones.get(bone.name) is not None:
                    bpy.ops.pose.constraint_add(type='COPY_TRANSFORMS')
                    trans_bone.constraints[len(trans_bone.constraints) - 1].target = bpy.data.objects[self.source]
                    trans_bone.constraints[len(trans_bone.constraints) - 1].subtarget = bone.name
                    # bpy.ops.constraint.apply(constraint='Copy Transforms', owner='BONE', report=False)

    def delConstraints(self):
        for bone in bpy.context.selected_pose_bones:
            copyLocConstraints = [c for c in bone.constraints if c.type == 'COPY_TRANSFORMS']
            for c in copyLocConstraints:
                bone.constraints.remove(c)

    def applyAnimation(self):
        scene = bpy.context.scene
        for frame in range(self.frame_from, self.frame_to):
            scene.frame_current = frame
            scene.frame_set(scene.frame_current)
            bpy.ops.pose.visual_transform_apply()
            bpy.ops.anim.keyframe_insert_menu(type='__ACTIVE__', always_prompt=True)


class AnimationTransferringPanel(bpy.types.Panel):
    bl_idname = "animation.transferringpanel"
    bl_label = "Animation transferring"
    bl_category = "Tool"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        # layout.label(text="Panel", icon="BLENDER")
        row = layout.row()
        row.operator("animation.transferring", text="Transfer", icon="CUBE")

classes = { AnimationTransferOperator, AnimationTransferringPanel }

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == '__main__':
    register()