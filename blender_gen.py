# blender_gen.py
def generate_blender_scene_code(prompt):
    # --- тут можно будет парсить prompt и строить сцену из шаблонов ---
    # Пока что вернем шаблон “3 шара на зеркальной плоскости”
    return '''
import bpy
import os

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, 0))
plane = bpy.context.active_object
mat_plane = bpy.data.materials.new(name="MirrorMaterial")
mat_plane.use_nodes = True
bsdf = mat_plane.node_tree.nodes.get("Principled BSDF")
bsdf.inputs['Metallic'].default_value = 1
bsdf.inputs['Roughness'].default_value = 0.02
plane.data.materials.append(mat_plane)
colors = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)]
positions = [(-2, 0, 1), (0, 0, 1), (2, 0, 1)]
for i in range(3):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=positions[i])
    sphere = bpy.context.active_object
    mat = bpy.data.materials.new(name=f"SphereMaterial_{i}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = colors[i]
    bsdf.inputs['Roughness'].default_value = 0.3
    sphere.data.materials.append(mat)
cam = bpy.data.cameras.new("Camera")
cam_obj = bpy.data.objects.new("Camera", cam)
bpy.context.collection.objects.link(cam_obj)
cam_obj.location = (0, -7, 5)
cam_obj.rotation_euler = (1.1, 0, 0)
bpy.context.scene.camera = cam_obj
light_data = bpy.data.lights.new(name="MainLight", type='AREA')
light = bpy.data.objects.new(name="MainLight", object_data=light_data)
bpy.context.collection.objects.link(light)
light.location = (0, -3, 7)
light.data.energy = 1000
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 64
bpy.context.scene.render.filepath = os.path.abspath("output/output.png").replace("\\\\", "/")
bpy.ops.render.render(write_still=True)
'''
