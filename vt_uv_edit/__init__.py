bl_info = {
    "name": "VT UV Edit",
    "description": "",
    "author": "lai001",
    "version": (0, 0, 1),
    "blender": (3, 5, 1),
    "location": "View 3D > Sidebar > Tool > VT UV Edit",
    "warning": "",
    "doc_url":"",
    "category":"UV",
}

import bpy
import mathutils
from bpy.types import (Panel,)

class UVEditOperator(bpy.types.Operator):
    bl_idname = "vt.uv_edit"
    bl_label = "VT UV Edit"
    bl_options = { "REGISTER", "UNDO" }

    tile_size: bpy.props.IntProperty(name="Tile Size", default=256)
    virtual_texture_width: bpy.props.IntProperty(name="Virtual Texture Width", default=512*1000)
    virtual_texture_height: bpy.props.IntProperty(name="Virtual Texture Height", default=512*1000)
    physical_texture_width: bpy.props.IntProperty(name="Physical Texture Width", default=4096)
    physical_texture_height: bpy.props.IntProperty(name="Physical Texture Height", default=4096)
    virtual_texture_page_x: bpy.props.IntProperty(name="Virtual Texture Page X", default=0)
    virtual_texture_page_y: bpy.props.IntProperty(name="Virtual Texture Page Y", default=0)

    def item_callback(self, context):
        selected_objects = bpy.context.selected_objects
        if selected_objects is not None and len(selected_objects) > 0:
            selected_object = selected_objects[0]
            uv_layers = selected_object.data.uv_layers
            items = []
            for uv_layer in uv_layers:
                items.append((uv_layer.name, uv_layer.name, uv_layer.name))
            return items
        return (
            ('NONE', 'None', "No uv map found"),
        )

    physical_uv_map_name: bpy.props.EnumProperty(
        items=item_callback,
        name="Physical UV Map Name")

    virtual_uv_map_name: bpy.props.EnumProperty(
        items=item_callback,
        name="Virtual UV Map Name")

    def invoke(self, context, event):
        result = context.window_manager.invoke_props_dialog(self)
        return result

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        if selected_objects is not None and len(selected_objects) > 0:
            selected_object = selected_objects[0]
            uv_layers = selected_object.data.uv_layers
            if self.virtual_uv_map_name in uv_layers and self.physical_uv_map_name in uv_layers:
                if self.virtual_uv_map_name != self.physical_uv_map_name:
                    virtual_uv_layer = uv_layers[self.virtual_uv_map_name]
                    physical_uv_layer = uv_layers[self.physical_uv_map_name]
                    if len(virtual_uv_layer.data) == len(physical_uv_layer.data):
                        for (virtual_uv_data, physical_uv_data) in zip(virtual_uv_layer.data, physical_uv_layer.data):
                            virtual_uv_data.uv.x = self.virtual_texture_page_x * self.tile_size + self.physical_texture_width * physical_uv_data.uv.x
                            virtual_uv_data.uv.y = self.virtual_texture_page_y * self.tile_size + self.physical_texture_height * physical_uv_data.uv.y
                            print(virtual_uv_data.uv)
        return { "FINISHED" }

class UVEDITPANEL_PT_Tool(bpy.types.Panel):
    bl_idname = "UVEDITPANEL_PT_Tool"
    bl_label = "VT UV Edit"
    bl_category = "Tool"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("vt.uv_edit", text="Apply", icon="CUBE")

classes = {UVEditOperator, UVEDITPANEL_PT_Tool}

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == '__main__':
    register()