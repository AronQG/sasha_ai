import bpy
import math

# Удаление всех объектов
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Создание мокрого асфальта
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
plane = bpy.context.active_object
plane.name = 'Wet Asphalt'
bpy.ops.material.new()
asphalt_mat = bpy.data.materials['Material']
asphalt_mat.name = 'Asphalt Material'
asphalt_mat.use_nodes = True
nodes = asphalt_mat.node_tree.nodes
links = asphalt_mat.node_tree.links
bsdf = nodes.get('Principled BSDF')
bsdf.inputs['Roughness'].default_value = 0.1
bsdf.inputs['Metallic'].default_value = 0.0
bsdf.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1)
plane.data.materials.append(asphalt_mat)

# Создание светящихся шаров
for i, loc in enumerate([(2, 0, 1), (-2, 0, 1), (0, 2, 1)]):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=loc)
    sphere = bpy.context.active_object
    sphere.name = f'Glowing Sphere {i+1}'
    bpy.ops.material.new()
    glow_mat = bpy.data.materials.new(name=f'Glow Material {i+1}')
    glow_mat.use_nodes = True
    nodes = glow_mat.node_tree.nodes
    links = glow_mat.node_tree.links
    emission = nodes.new(type='ShaderNodeEmission')
    emission.inputs['Color'].default_value = (1, 0.5, 0, 1) if i == 0 else (0, 1, 0.5, 1) if i == 1 else (0.5, 0, 1, 1)
    emission.inputs['Strength'].default_value = 10
    output = nodes.get('Material Output')
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    sphere.data.materials.append(glow_mat)

# Создание неоновых огней
for i, loc in enumerate([(0, -3, 2), (3, 0, 2), (-3, 0, 2)]):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=6, location=loc, rotation=(0, 0, math.pi/2))
    neon = bpy.context.active_object
    neon.name = f'Neon Light {i+1}'
    bpy.ops.material.new()
    neon_mat = bpy.data.materials.new(name=f'Neon Material {i+1}')
    neon_mat.use_nodes = True
    nodes = neon_mat.node_tree.nodes
    links = neon_mat.node_tree.links
    emission = nodes.new(type='ShaderNodeEmission')
    emission.inputs['Color'].default_value = (1, 0, 0, 1) if i == 0 else (0, 1, 1, 1) if i == 1 else (1, 1, 0, 1)
    emission.inputs['Strength'].default_value = 20
    output = nodes.get('Material Output')
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    neon.data.materials.append(neon_mat)

# Настройка камеры
bpy.ops.object.camera_add(location=(0, -8, 3), rotation=(math.radians(75), 0, 0))
camera = bpy.context.active_object
bpy.context.scene.camera = camera

# Настройка рендера
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 128
bpy.context.scene.render.filepath = 'D:/sasha/output.png'

# Рендер сцены
bpy.ops.render.render(write_still=True)