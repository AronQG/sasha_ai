import os

def generate_blender_script(prompt):
    # ... (тот же скрипт, только render.filepath не "output.png", а полный путь)
    return f'''
import bpy

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

for i, color in enumerate([(1,0,0,1), (0,1,0,1), (0,0,1,1)]):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(i*3,0,1))
    mat = bpy.data.materials.new(f"Color{{i}}")
    mat.diffuse_color = color
    bpy.context.active_object.data.materials.append(mat)

bpy.ops.mesh.primitive_plane_add(size=10, location=(3,0,0))
bpy.context.active_object.location.z = 0

bpy.ops.object.light_add(type='SUN', location=(5,5,10))
bpy.ops.object.camera_add(location=(7, -10, 5), rotation=(1.1, 0, 0.8))
bpy.context.scene.camera = bpy.context.object

bpy.context.scene.render.filepath = r"{os.path.abspath('output.png').replace('\\', '/')}"
bpy.ops.render.render(write_still=True)
'''
