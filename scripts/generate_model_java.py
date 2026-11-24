import json

def generate_java(geo_path, class_name, package_name, entity_name):
    with open(geo_path, 'r', encoding='utf-8') as f:
        d = json.load(f)
    geom = d['minecraft:geometry'][0]
    tw = geom['description'].get('texture_width', 256)
    th = geom['description'].get('texture_height', 256)
    bones = geom['bones']
    bone_map = {b['name']: b for b in bones}
    
    # Hierarchy check
    lines = []
    lines.append(f"package {package_name};")
    lines.append("")
    lines.append("import net.minecraft.client.model.*;")
    lines.append("import net.minecraft.client.render.VertexConsumer;")
    lines.append("import net.minecraft.client.render.entity.model.EntityModel;")
    lines.append("import net.minecraft.client.render.entity.model.EntityModelLayer;")
    lines.append("import net.minecraft.client.util.math.MatrixStack;")
    lines.append("import net.minecraft.util.Identifier;")
    lines.append("import net.minecraft.util.math.MathHelper;")
    lines.append(f"import com.avatarmod.elements.entity.mob.{entity_name};" if "Shirshu" in entity_name else f"import com.avatarmod.elements.entity.boss.{entity_name};")
    lines.append("")
    lines.append(f"public class {class_name} extends EntityModel<{entity_name}> {{")
    lines.append(f"    public static final EntityModelLayer LAYER_LOCATION = new EntityModelLayer(Identifier.of(\"avatar_elements\", \"{entity_name.lower()}\"), \"main\");")
    lines.append("")
    lines.append("    private final ModelPart root;")
    
    # Store key bones for animation
    key_bones = [b['name'] for b in bones if b['name'] != 'root']
    for kb in key_bones:
        lines.append(f"    private final ModelPart {kb};")
    lines.append("")
    
    lines.append(f"    public {class_name}(ModelPart root) {{")
    lines.append("        this.root = root;")
    for kb in key_bones:
        # build path
        curr = kb
        path = [curr]
        while bone_map.get(curr, {}).get('parent') and bone_map[curr]['parent'] != 'root':
            curr = bone_map[curr]['parent']
            path.append(curr)
        path.reverse()
        getter = "root"
        for p in path:
            getter += f".getChild(\"{p}\")"
        lines.append(f"        this.{kb} = {getter};")
    lines.append("    }")
    lines.append("")
    
    lines.append("    public static TexturedModelData getTexturedModelData() {")
    lines.append("        ModelData modelData = new ModelData();")
    lines.append("        ModelPartData root = modelData.getRoot();")
    
    declared = {'root': 'root'}
    for b in bones:
        b_name = b['name']
        if b_name == 'root':
            continue
        p_name = b.get('parent', 'root')
        parent_var = declared.get(p_name, 'root')
        
        pivot = b.get('pivot', [0,0,0])
        parent_pivot = bone_map[p_name].get('pivot', [0,0,0]) if p_name in bone_map else [0,0,0]
        
        if p_name == 'root' or p_name is None:
            rel_px = pivot[0]
            rel_py = 24.0 - pivot[1]
            rel_pz = pivot[2]
        else:
            rel_px = pivot[0] - parent_pivot[0]
            rel_py = -(pivot[1] - parent_pivot[1])
            rel_pz = pivot[2] - parent_pivot[2]
            
        rot = b.get('rotation', [0,0,0])
        if rot is None: rot = [0,0,0]
        rx = f"(float) Math.toRadians({rot[0]}f)" if rot[0] != 0 else "0.0f"
        ry = f"(float) Math.toRadians({rot[1]}f)" if rot[1] != 0 else "0.0f"
        rz = f"(float) Math.toRadians({rot[2]}f)" if rot[2] != 0 else "0.0f"
        
        cubes = b.get('cubes', [])
        cuboid_chain = ""
        for c in cubes:
            u, v = c['uv'][0], c['uv'][1]
            ox, oy, oz = c['origin']
            sx, sy, sz = c['size']
            cx = ox - pivot[0]
            cy = pivot[1] - (oy + sy)
            cz = oz - pivot[2]
            cuboid_chain += f".uv({u}, {v}).cuboid({cx:.1f}f, {cy:.1f}f, {cz:.1f}f, {sx:.1f}f, {sy:.1f}f, {sz:.1f}f)"
            
        builder = "ModelPartBuilder.create()" + cuboid_chain
        transform = f"ModelTransform.of({rel_px:.1f}f, {rel_py:.1f}f, {rel_pz:.1f}f, {rx}, {ry}, {rz})"
        var_name = b_name.replace('-', '_')
        lines.append(f"        ModelPartData {var_name} = {parent_var}.addChild(\"{b_name}\", {builder}, {transform});")
        declared[b_name] = var_name
        
    lines.append(f"        return TexturedModelData.of(modelData, {tw}, {th});")
    lines.append("    }")
    lines.append("")
    
    # Render method
    lines.append("    @Override")
    lines.append("    public void render(MatrixStack matrices, VertexConsumer vertices, int light, int overlay, int color) {")
    lines.append("        root.render(matrices, vertices, light, overlay, color);")
    lines.append("    }")
    lines.append("")
    
    # Custom animations
    lines.append("    @Override")
    lines.append(f"    public void setAngles({entity_name} entity, float limbAngle, float limbDistance, float animationProgress, float headYaw, float headPitch) {{")
    if "Shirshu" in class_name:
        lines.append("        // Quadruped walk cycle")
        lines.append("        this.leg_fl_upper.pitch = MathHelper.cos(limbAngle * 0.6662f) * 1.2f * limbDistance + (float) Math.toRadians(14.0f);")
        lines.append("        this.leg_fr_upper.pitch = MathHelper.cos(limbAngle * 0.6662f + (float) Math.PI) * 1.2f * limbDistance - (float) Math.toRadians(8.0f);")
        lines.append("        this.leg_bl_upper.pitch = MathHelper.cos(limbAngle * 0.6662f + (float) Math.PI) * 1.2f * limbDistance - (float) Math.toRadians(14.0f);")
        lines.append("        this.leg_br_upper.pitch = MathHelper.cos(limbAngle * 0.6662f) * 1.2f * limbDistance + (float) Math.toRadians(10.0f);")
        lines.append("        // Scent tracking / snout sniffing twitch")
        lines.append("        this.nose_star_top.pitch = (float) Math.toRadians(-22.5f) + MathHelper.sin(animationProgress * 0.45f) * 0.15f;")
        lines.append("        this.nose_star_left_u.yaw = (float) Math.toRadians(-28.0f) + MathHelper.cos(animationProgress * 0.40f) * 0.12f;")
        lines.append("        this.nose_star_right_u.yaw = (float) Math.toRadians(28.0f) - MathHelper.cos(animationProgress * 0.40f) * 0.12f;")
        lines.append("        // Head look tracking")
        lines.append("        this.head.yaw = headYaw * 0.017453292f * 0.6f;")
        lines.append("        this.head.pitch = headPitch * 0.017453292f * 0.6f + (float) Math.toRadians(14.0f);")
        lines.append("        // Tail natural sway")
        lines.append("        float tailSway = MathHelper.sin(animationProgress * 0.12f) * 0.2f + MathHelper.cos(limbAngle * 0.6662f) * 0.3f * limbDistance;")
        lines.append("        this.tail_1.yaw = tailSway * 0.6f;")
        lines.append("        this.tail_2.yaw = tailSway * 0.8f;")
        lines.append("        this.tail_3.yaw = tailSway * 1.0f;")
    else:
        # Vaatu
        lines.append("        // Titanic floating undulation")
        lines.append("        float floatWave = MathHelper.sin(animationProgress * 0.08f);")
        lines.append("        this.core_body.pitch = (float) Math.toRadians(4.0f) + floatWave * 0.06f;")
        lines.append("        // Mantle wing breathing")
        lines.append("        this.mantle_left_1.roll = (float) Math.toRadians(-12.0f) + floatWave * 0.12f;")
        lines.append("        this.mantle_right_1.roll = (float) Math.toRadians(12.0f) - floatWave * 0.12f;")
        lines.append("        // Undulating dark tentacles")
        lines.append("        this.t_l1_base.yaw = (float) Math.toRadians(34.0f) + MathHelper.sin(animationProgress * 0.10f + 0.0f) * 0.22f;")
        lines.append("        this.t_l2_base.yaw = (float) Math.toRadians(40.0f) + MathHelper.sin(animationProgress * 0.10f + 1.2f) * 0.22f;")
        lines.append("        this.t_l3_base.yaw = (float) Math.toRadians(38.0f) + MathHelper.sin(animationProgress * 0.10f + 2.4f) * 0.22f;")
        lines.append("        this.t_l4_base.yaw = (float) Math.toRadians(28.0f) + MathHelper.sin(animationProgress * 0.10f + 3.6f) * 0.22f;")
        lines.append("        this.t_r1_base.yaw = (float) Math.toRadians(-34.0f) - MathHelper.sin(animationProgress * 0.10f + 0.0f) * 0.22f;")
        lines.append("        this.t_r2_base.yaw = (float) Math.toRadians(-40.0f) - MathHelper.sin(animationProgress * 0.10f + 1.2f) * 0.22f;")
        lines.append("        this.t_r3_base.yaw = (float) Math.toRadians(-38.0f) - MathHelper.sin(animationProgress * 0.10f + 2.4f) * 0.22f;")
        lines.append("        this.t_r4_base.yaw = (float) Math.toRadians(-28.0f) - MathHelper.sin(animationProgress * 0.10f + 3.6f) * 0.22f;")
        lines.append("        this.tail_ribbon_1.pitch = (float) Math.toRadians(14.0f) + MathHelper.sin(animationProgress * 0.08f) * 0.25f;")
        lines.append("        this.tail_ribbon_2.pitch = (float) Math.toRadians(-18.0f) + MathHelper.cos(animationProgress * 0.08f) * 0.25f;")
    lines.append("    }")
    lines.append("}")
    
    return "\n".join(lines)

import os
target_dir = r"d:\repo\Minecraft Mod & Rp\mod\src\client\java\com\avatarmod\elements\client\render\entity\model"
os.makedirs(target_dir, exist_ok=True)

shirshu_java = generate_java(
    r"d:\repo\Minecraft Mod & Rp\mod\src\main\resources\assets\avatar_elements\models\entity\shirshu.geo.json",
    "ShirshuEntityModel",
    "com.avatarmod.elements.client.render.entity.model",
    "ShirshuEntity"
)
with open(os.path.join(target_dir, "ShirshuEntityModel.java"), "w", encoding="utf-8") as f:
    f.write(shirshu_java)
print("ShirshuEntityModel.java written!")

vaatu_java = generate_java(
    r"d:\repo\Minecraft Mod & Rp\mod\src\main\resources\assets\avatar_elements\models\entity\vaatu_spirit_titan.geo.json",
    "VaatuEntityModel",
    "com.avatarmod.elements.client.render.entity.model",
    "VaatuSpiritTitanEntity"
)
with open(os.path.join(target_dir, "VaatuEntityModel.java"), "w", encoding="utf-8") as f:
    f.write(vaatu_java)
print("VaatuEntityModel.java written!")
