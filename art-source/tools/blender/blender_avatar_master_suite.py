"""
Blender Master 3D Suite - Avatar Elements
Adheres strictly to /blender-director, /blender-modeler, /animation, and /anime-style skills.
"""
import bpy
import math

def setup_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    col_project = bpy.data.collections.new("COL_Project")
    bpy.context.scene.collection.children.link(col_project)
    
    col_ref = bpy.data.collections.new("COL_Reference")
    col_blockout = bpy.data.collections.new("COL_Blockout")
    col_geo = bpy.data.collections.new("COL_Geo")
    col_collision = bpy.data.collections.new("COL_Collision")
    col_export = bpy.data.collections.new("COL_Export")
    
    for c in [col_ref, col_blockout, col_geo, col_collision, col_export]:
        col_project.children.link(c)
        
    return {"project": col_project, "geo": col_geo, "collision": col_collision, "export": col_export}

def create_anime_toon_material(name, base_color, shadow_color, specular_tint=(1,1,1,1)):
    """Creates a 2-tone Anime Toon Cel Shader with hard shadow breaks."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    diffuse = nodes.new(type='ShaderNodeBsdfDiffuse')
    s2rgb = nodes.new(type='ShaderNodeShaderToRGB')
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    
    # Constant interpolation for crisp anime breaks
    color_ramp.color_ramp.interpolation = 'CONSTANT'
    color_ramp.color_ramp.elements[0].position = 0.45
    color_ramp.color_ramp.elements[0].color = shadow_color
    color_ramp.color_ramp.elements[1].position = 0.46
    color_ramp.color_ramp.elements[1].color = base_color
    
    links.new(diffuse.outputs['BSDF'], s2rgb.inputs['Shader'])
    links.new(s2rgb.outputs['Color'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], output.inputs['Surface'])
    
    return mat

def build_weapon_mesh(col_geo, name="SM_Dual_Swords"):
    u = 0.0625 # 1 Minecraft unit = 1/16 meter
    
    # Grip (Origin at 0,0,0)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 4.5 * u), scale=(1.2 * u, 1.2 * u, 9 * u))
    grip = bpy.context.active_object
    grip.name = f"{name}_Grip"
    
    # Guard
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 9.5 * u), scale=(4.0 * u, 2.5 * u, 1.0 * u))
    guard = bpy.context.active_object
    guard.name = f"{name}_Guard"
    
    # Blade with Bevel Modifier (Non-destructive)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 20.0 * u), scale=(2.4 * u, 0.8 * u, 20.0 * u))
    blade = bpy.context.active_object
    blade.name = f"{name}_Blade"
    
    bevel = blade.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = 0.015
    bevel.segments = 2
    
    # Add Locators
    loc_tip = bpy.data.objects.new(f"{name}_locator_trail_end", None)
    loc_tip.location = (0, 0, 30.0 * u)
    col_geo.objects.link(loc_tip)
    
    loc_base = bpy.data.objects.new(f"{name}_locator_trail_begin", None)
    loc_base.location = (0, 0, 10.0 * u)
    col_geo.objects.link(loc_base)

def build_combat_animation():
    """Sets up combat swing action keyframes on active object."""
    obj = bpy.context.active_object
    if not obj:
        return
    obj.animation_data_create()
    action = bpy.data.actions.new(name="AN_Combat_Slash_Arc")
    obj.animation_data.action = action
    
    # Frame 1: Anticipation / Windup
    obj.rotation_euler = (0, -math.radians(45), math.radians(25))
    obj.keyframe_insert(data_path="rotation_euler", frame=1)
    
    # Frame 6: Active Strike Arc
    obj.rotation_euler = (0, math.radians(75), -math.radians(40))
    obj.keyframe_insert(data_path="rotation_euler", frame=6)
    
    # Frame 12: Recovery Pose
    obj.rotation_euler = (0, 0, 0)
    obj.keyframe_insert(data_path="rotation_euler", frame=12)

if __name__ == "__main__":
    cols = setup_scene()
    toon_mat = create_anime_toon_material("M_Anime_Blade", (0.85, 0.90, 0.95, 1.0), (0.25, 0.30, 0.40, 1.0))
    build_weapon_mesh(cols["geo"], "SM_Dual_Swords")
    print("Blender Master Scene and Weapon Suite successfully initialized.")
