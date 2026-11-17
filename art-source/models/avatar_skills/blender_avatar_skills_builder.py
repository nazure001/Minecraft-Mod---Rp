"""
Blender 3D Avatar Skills Builder
Built according to blender-modeler and voxel-style discipline guidelines.

Usage in Blender:
1. Open Blender 4.x+
2. Open Scripting workspace -> New Text
3. Paste or open this script -> Run Script (Alt+P)
   Or via Blender MCP execute_blender_code tool.
"""

import bpy
import math

def clean_scene():
    """Wipe default cube, lights, and orphan meshes."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

def get_or_create_collection(name, parent=None):
    """Hierarchical collection creator per blender-modeler spec."""
    if name in bpy.data.collections:
        col = bpy.data.collections[name]
    else:
        col = bpy.data.collections.new(name)
        if parent:
            parent.children.link(col)
        else:
            bpy.context.scene.collection.children.link(col)
    return col

def setup_scene_hierarchy():
    """Sets up standard AAA scene collection hierarchy."""
    col_project = get_or_create_collection("COL_Avatar_Skills")
    col_ref = get_or_create_collection("COL_Reference", col_project)
    col_blockout = get_or_create_collection("COL_Blockout", col_project)
    col_geo = get_or_create_collection("COL_Geo", col_project)
    col_collision = get_or_create_collection("COL_Collision", col_project)
    col_lighting = get_or_create_collection("COL_Lighting", col_project)
    col_camera = get_or_create_collection("COL_Camera", col_project)
    return {
        "project": col_project,
        "geo": col_geo,
        "collision": col_collision,
        "lighting": col_lighting,
        "camera": col_camera
    }

def create_pbr_material(name, base_color, roughness=0.8, metallic=0.0, transmission=0.0, emission_color=(0,0,0,1), emission_strength=0.0):
    """Creates a Principled BSDF PBR material."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    
    if bsdf:
        bsdf.inputs['Base Color'].default_value = base_color
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Metallic'].default_value = metallic
        if 'Transmission Weight' in bsdf.inputs:
            bsdf.inputs['Transmission Weight'].default_value = transmission
        elif 'Transmission' in bsdf.inputs:
            bsdf.inputs['Transmission'].default_value = transmission
            
        if emission_strength > 0:
            if 'Emission Color' in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = emission_color
                bsdf.inputs['Emission Strength'].default_value = emission_strength
            elif 'Emission' in bsdf.inputs:
                bsdf.inputs['Emission'].default_value = emission_color

    return mat

def build_earth_boulder(collections, origin=(0, 0, 0)):
    """
    Constructs SM_Earth_Boulder_A:
    Faceted, stepped voxel rock with stratified tiers and jade inclusions.
    Pivot: (0, 0, 0) at ground contact.
    """
    u = 0.0625 # 1 Minecraft pixel = 1/16 m
    
    # 1. Main Core Rock
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(origin[0], origin[1], origin[2] + 8 * u),
        scale=(10 * u, 10 * u, 10 * u)
    )
    core = bpy.context.active_object
    core.name = "SM_Earth_Boulder_A"
    
    # Move to COL_Geo
    for col in core.users_collection:
        col.objects.unlink(core)
    collections["geo"].objects.link(core)
    
    # Apply Scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # 2. Add Top Stratified Crag
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(origin[0] + 0.5 * u, origin[1], origin[2] + 14.5 * u),
        scale=(6 * u, 8 * u, 3 * u)
    )
    top_crag = bpy.context.active_object
    top_crag.name = "Boulder_Top_Crag"
    for col in top_crag.users_collection:
        col.objects.unlink(top_crag)
    collections["geo"].objects.link(top_crag)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # 3. Add Jade Crystal Accent
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(origin[0] - 5.5 * u, origin[1], origin[2] + 8 * u),
        scale=(2 * u, 6 * u, 8 * u)
    )
    jade = bpy.context.active_object
    jade.name = "Boulder_Jade_Vein"
    jade.rotation_euler = (0, math.radians(22.5), 0)
    for col in jade.users_collection:
        col.objects.unlink(jade)
    collections["geo"].objects.link(jade)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Parent sub-elements to core
    top_crag.parent = core
    jade.parent = core
    
    # 4. Modifiers (Non-destructive bevel & weighted normals)
    bev = core.modifiers.new(name="Bevel_Micro", type='BEVEL')
    bev.width = 0.004 # 4mm subtle bevel for block edge highlight
    bev.segments = 2
    bev.limit_method = 'ANGLE'
    bev.angle_limit = math.radians(35)
    
    wn = core.modifiers.new(name="WeightedNormal", type='WEIGHTED_NORMAL')
    wn.keep_sharp = True
    core.data.use_auto_smooth = True
    
    # 5. Materials
    mat_stone = create_pbr_material("M_Earth_Stone", (0.35, 0.33, 0.31, 1.0), roughness=0.9)
    mat_jade = create_pbr_material("M_Earth_Jade", (0.15, 0.72, 0.35, 1.0), roughness=0.3, metallic=0.1, emission_color=(0.2, 0.9, 0.4, 1.0), emission_strength=1.5)
    
    core.data.materials.append(mat_stone)
    top_crag.data.materials.append(mat_stone)
    jade.data.materials.append(mat_jade)
    
    # 6. Collision Proxy (UCX_Earth_Boulder_01)
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(origin[0], origin[1], origin[2] + 8 * u),
        scale=(12 * u, 12 * u, 16 * u)
    )
    col_proxy = bpy.context.active_object
    col_proxy.name = "UCX_Earth_Boulder_01"
    for col in col_proxy.users_collection:
        col.objects.unlink(col_proxy)
    collections["collision"].objects.link(col_proxy)
    col_proxy.display_type = 'WIRE'
    col_proxy.hide_render = True
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    col_proxy.parent = core
    
    return core

def build_water_whip(collections, origin=(2.0, 0, 0)):
    """
    Constructs SM_Water_Whip_A:
    Segmented, flowing water tendril with transmission and aqua fresnel.
    Pivot: (0, 0, 0) at hand handle.
    """
    u = 0.0625
    
    # Root Grip Node
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(origin[0], origin[1], origin[2] + 2.5 * u),
        scale=(2 * u, 2 * u, 5 * u)
    )
    root = bpy.context.active_object
    root.name = "SM_Water_Whip_A"
    for col in root.users_collection:
        col.objects.unlink(root)
    collections["geo"].objects.link(root)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Arc Segment 1
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(origin[0], origin[1] - 1.5 * u, origin[2] + 7.5 * u),
        scale=(3 * u, 3 * u, 6 * u)
    )
    seg1 = bpy.context.active_object
    seg1.name = "Water_Arc_1"
    seg1.rotation_euler = (math.radians(-22.5), 0, 0)
    for col in seg1.users_collection:
        col.objects.unlink(seg1)
    collections["geo"].objects.link(seg1)
    seg1.parent = root
    
    # Arc Segment 2 (Crest)
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(origin[0], origin[1] - 4.5 * u, origin[2] + 11.5 * u),
        scale=(4 * u, 4 * u, 5 * u)
    )
    seg2 = bpy.context.active_object
    seg2.name = "Water_Arc_Crest"
    seg2.rotation_euler = (math.radians(-45.0), 0, 0)
    for col in seg2.users_collection:
        col.objects.unlink(seg2)
    collections["geo"].objects.link(seg2)
    seg2.parent = root
    
    # Whip Lashing Tip
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(origin[0] + 1.0 * u, origin[1] - 10.0 * u, origin[2] + 12.0 * u),
        scale=(2 * u, 7 * u, 2 * u)
    )
    seg3 = bpy.context.active_object
    seg3.name = "Water_Tip_Lash"
    seg3.rotation_euler = (0, 0, math.radians(22.5))
    for col in seg3.users_collection:
        col.objects.unlink(seg3)
    collections["geo"].objects.link(seg3)
    seg3.parent = root
    
    # Droplet Splash
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(origin[0] - 2.5 * u, origin[1] - 2.0 * u, origin[2] + 9.0 * u),
        scale=(2 * u, 2 * u, 2 * u)
    )
    splash = bpy.context.active_object
    splash.name = "Water_Splash_Droplet"
    for col in splash.users_collection:
        col.objects.unlink(splash)
    collections["geo"].objects.link(splash)
    splash.parent = root
    
    # Material
    mat_water = create_pbr_material(
        "M_Water_Fluid",
        (0.1, 0.6, 0.9, 0.85),
        roughness=0.1,
        transmission=0.75,
        emission_color=(0.15, 0.75, 1.0, 1.0),
        emission_strength=0.8
    )
    for obj in [root, seg1, seg2, seg3, splash]:
        obj.data.materials.append(mat_water)
        bev = obj.modifiers.new(name="Bevel", type='BEVEL')
        bev.width = 0.003
        bev.segments = 2
        obj.data.use_auto_smooth = True
        
    return root

def build_avatar_relic_3d(collections, origin=(-2.0, 0, 0)):
    """
    Constructs SM_Avatar_Relic_3D:
    Floating kinetic relic with central Chi core and 4 elemental rune bezels.
    """
    u = 0.0625
    
    # Central Glowing Chi Sphere/Cube
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(origin[0], origin[1], origin[2] + 8 * u),
        scale=(5 * u, 5 * u, 5 * u)
    )
    core = bpy.context.active_object
    core.name = "SM_Avatar_Relic_3D"
    for col in core.users_collection:
        col.objects.unlink(core)
    collections["geo"].objects.link(core)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Orbital Gold Frame Ring
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(origin[0], origin[1], origin[2] + 8 * u),
        scale=(10 * u, 10 * u, 2 * u)
    )
    ring = bpy.context.active_object
    ring.name = "Relic_Gold_Frame"
    for col in ring.users_collection:
        col.objects.unlink(ring)
    collections["geo"].objects.link(ring)
    
    # Cut out the inner frame center via non-destructive Boolean
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(origin[0], origin[1], origin[2] + 8 * u),
        scale=(8 * u, 8 * u, 4 * u)
    )
    cutter = bpy.context.active_object
    cutter.name = "CUT_Relic_Center"
    cutter.display_type = 'WIRE'
    cutter.hide_render = True
    for col in cutter.users_collection:
        col.objects.unlink(cutter)
    collections["geo"].objects.link(cutter)
    
    bool_mod = ring.modifiers.new(name="Hollow_Frame", type='BOOLEAN')
    bool_mod.object = cutter
    bool_mod.operation = 'DIFFERENCE'
    cutter.parent = ring
    ring.parent = core
    
    # Materials
    mat_chi = create_pbr_material("M_Chi_Core", (0.8, 0.95, 1.0, 1.0), roughness=0.1, emission_color=(0.4, 0.85, 1.0, 1.0), emission_strength=4.0)
    mat_gold = create_pbr_material("M_Ancient_Gold", (0.85, 0.65, 0.15, 1.0), roughness=0.3, metallic=0.9)
    
    core.data.materials.append(mat_chi)
    ring.data.materials.append(mat_gold)
    
    return core

def setup_lighting_and_camera(collections):
    """Sets up standard cinematic three-point lighting & isometric camera."""
    # Key light
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
    sun = bpy.context.active_object
    sun.name = "SUN_KeyLight"
    sun.data.energy = 3.5
    for col in sun.users_collection:
        col.objects.unlink(sun)
    collections["lighting"].objects.link(sun)
    
    # Fill Light
    bpy.ops.object.light_add(type='POINT', location=(-4, -4, 4))
    fill = bpy.context.active_object
    fill.name = "LIGHT_Fill"
    fill.data.energy = 80
    fill.data.color = (0.7, 0.85, 1.0)
    for col in fill.users_collection:
        col.objects.unlink(fill)
    collections["lighting"].objects.link(fill)
    
    # Rim light
    bpy.ops.object.light_add(type='POINT', location=(0, 6, 5))
    rim = bpy.context.active_object
    rim.name = "LIGHT_Rim"
    rim.data.energy = 120
    rim.data.color = (1.0, 0.9, 0.7)
    for col in rim.users_collection:
        col.objects.unlink(rim)
    collections["lighting"].objects.link(rim)
    
    # Isometric Camera
    bpy.ops.object.camera_add(location=(5.0, -5.0, 4.5))
    cam = bpy.context.active_object
    cam.name = "CAM_Isometric_Preview"
    cam.rotation_euler = (math.radians(60), 0, math.radians(45))
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = 3.2
    for col in cam.users_collection:
        col.objects.unlink(cam)
    collections["camera"].objects.link(cam)
    bpy.context.scene.camera = cam

def main():
    print("Executing Avatar Skills 3D Asset generation via blender-modeler...")
    clean_scene()
    cols = setup_scene_hierarchy()
    
    # 1. Earth Boulder (SM_Earth_Boulder_A)
    boulder = build_earth_boulder(cols, origin=(0, 0, 0))
    
    # 2. Water Whip (SM_Water_Whip_A)
    whip = build_water_whip(cols, origin=(1.5, 0, 0))
    
    # 3. Avatar Relic 3D (SM_Avatar_Relic_3D)
    relic = build_avatar_relic_3d(cols, origin=(-1.5, 0, 0))
    
    # 4. Studio Camera & Lights
    setup_lighting_and_camera(cols)
    
    print("Done! SM_Earth_Boulder_A, SM_Water_Whip_A, and SM_Avatar_Relic_3D generated successfully.")

if __name__ == "__main__":
    main()
