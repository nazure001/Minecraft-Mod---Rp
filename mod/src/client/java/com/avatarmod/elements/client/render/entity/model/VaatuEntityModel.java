package com.avatarmod.elements.client.render.entity.model;

import net.minecraft.client.model.*;
import net.minecraft.client.render.VertexConsumer;
import net.minecraft.client.render.entity.model.EntityModel;
import net.minecraft.client.render.entity.model.EntityModelLayer;
import net.minecraft.client.util.math.MatrixStack;
import net.minecraft.util.Identifier;
import net.minecraft.util.math.MathHelper;
import com.avatarmod.elements.entity.boss.VaatuSpiritTitanEntity;

public class VaatuEntityModel extends EntityModel<VaatuSpiritTitanEntity> {
    public static final EntityModelLayer LAYER_LOCATION = new EntityModelLayer(Identifier.of("avatar_elements", "vaatuspirittitanentity"), "main");

    private final ModelPart root;
    private final ModelPart core_body;
    private final ModelPart crest_left;
    private final ModelPart crest_right;
    private final ModelPart mantle_left_1;
    private final ModelPart mantle_left_2;
    private final ModelPart mantle_right_1;
    private final ModelPart mantle_right_2;
    private final ModelPart t_l1_base;
    private final ModelPart t_l1_tip;
    private final ModelPart t_l2_base;
    private final ModelPart t_l2_tip;
    private final ModelPart t_l3_base;
    private final ModelPart t_l3_tip;
    private final ModelPart t_l4_base;
    private final ModelPart t_l4_tip;
    private final ModelPart t_r1_base;
    private final ModelPart t_r1_tip;
    private final ModelPart t_r2_base;
    private final ModelPart t_r2_tip;
    private final ModelPart t_r3_base;
    private final ModelPart t_r3_tip;
    private final ModelPart t_r4_base;
    private final ModelPart t_r4_tip;
    private final ModelPart tail_ribbon_1;
    private final ModelPart tail_ribbon_2;

    public VaatuEntityModel(ModelPart root) {
        this.root = root;
        this.core_body = root.getChild("core_body");
        this.crest_left = root.getChild("core_body").getChild("crest_left");
        this.crest_right = root.getChild("core_body").getChild("crest_right");
        this.mantle_left_1 = root.getChild("core_body").getChild("mantle_left_1");
        this.mantle_left_2 = root.getChild("core_body").getChild("mantle_left_1").getChild("mantle_left_2");
        this.mantle_right_1 = root.getChild("core_body").getChild("mantle_right_1");
        this.mantle_right_2 = root.getChild("core_body").getChild("mantle_right_1").getChild("mantle_right_2");
        this.t_l1_base = root.getChild("core_body").getChild("t_l1_base");
        this.t_l1_tip = root.getChild("core_body").getChild("t_l1_base").getChild("t_l1_tip");
        this.t_l2_base = root.getChild("core_body").getChild("t_l2_base");
        this.t_l2_tip = root.getChild("core_body").getChild("t_l2_base").getChild("t_l2_tip");
        this.t_l3_base = root.getChild("core_body").getChild("t_l3_base");
        this.t_l3_tip = root.getChild("core_body").getChild("t_l3_base").getChild("t_l3_tip");
        this.t_l4_base = root.getChild("core_body").getChild("t_l4_base");
        this.t_l4_tip = root.getChild("core_body").getChild("t_l4_base").getChild("t_l4_tip");
        this.t_r1_base = root.getChild("core_body").getChild("t_r1_base");
        this.t_r1_tip = root.getChild("core_body").getChild("t_r1_base").getChild("t_r1_tip");
        this.t_r2_base = root.getChild("core_body").getChild("t_r2_base");
        this.t_r2_tip = root.getChild("core_body").getChild("t_r2_base").getChild("t_r2_tip");
        this.t_r3_base = root.getChild("core_body").getChild("t_r3_base");
        this.t_r3_tip = root.getChild("core_body").getChild("t_r3_base").getChild("t_r3_tip");
        this.t_r4_base = root.getChild("core_body").getChild("t_r4_base");
        this.t_r4_tip = root.getChild("core_body").getChild("t_r4_base").getChild("t_r4_tip");
        this.tail_ribbon_1 = root.getChild("core_body").getChild("tail_ribbon_1");
        this.tail_ribbon_2 = root.getChild("core_body").getChild("tail_ribbon_1").getChild("tail_ribbon_2");
    }

    public static TexturedModelData getTexturedModelData() {
        ModelData modelData = new ModelData();
        ModelPartData root = modelData.getRoot();
        ModelPartData core_body = root.addChild("core_body", ModelPartBuilder.create().uv(2, 2).cuboid(-8.0f, -8.0f, -4.0f, 16.0f, 16.0f, 8.0f).uv(52, 2).cuboid(-6.0f, -16.0f, -3.0f, 12.0f, 8.0f, 6.0f).uv(90, 2).cuboid(-5.0f, 8.0f, -3.0f, 10.0f, 9.0f, 6.0f).uv(124, 2).cuboid(-3.0f, 17.0f, -2.0f, 6.0f, 8.0f, 4.0f), ModelTransform.of(0.0f, -10.0f, 0.0f, (float) Math.toRadians(4f), 0.0f, 0.0f));
        ModelPartData crest_left = core_body.addChild("crest_left", ModelPartBuilder.create().uv(146, 2).cuboid(-1.0f, -10.0f, -2.0f, 4.0f, 10.0f, 4.0f).uv(164, 2).cuboid(0.0f, -17.0f, -1.5f, 3.0f, 7.0f, 3.0f), ModelTransform.of(5.0f, -14.0f, 0.0f, (float) Math.toRadians(-8f), 0.0f, (float) Math.toRadians(-24f)));
        ModelPartData crest_right = core_body.addChild("crest_right", ModelPartBuilder.create().uv(178, 2).cuboid(-3.0f, -10.0f, -2.0f, 4.0f, 10.0f, 4.0f).uv(196, 2).cuboid(-3.0f, -17.0f, -1.5f, 3.0f, 7.0f, 3.0f), ModelTransform.of(-5.0f, -14.0f, 0.0f, (float) Math.toRadians(-8f), 0.0f, (float) Math.toRadians(24f)));
        ModelPartData mantle_left_1 = core_body.addChild("mantle_left_1", ModelPartBuilder.create().uv(210, 2).cuboid(0.0f, -8.0f, -2.0f, 12.0f, 16.0f, 4.0f), ModelTransform.of(8.0f, -2.0f, 0.0f, 0.0f, (float) Math.toRadians(14f), (float) Math.toRadians(-12f)));
        ModelPartData mantle_left_2 = mantle_left_1.addChild("mantle_left_2", ModelPartBuilder.create().uv(2, 28).cuboid(0.0f, -6.0f, -1.5f, 10.0f, 11.0f, 3.0f), ModelTransform.of(12.0f, 0.0f, 0.0f, 0.0f, (float) Math.toRadians(18f), (float) Math.toRadians(-18f)));
        ModelPartData mantle_right_1 = core_body.addChild("mantle_right_1", ModelPartBuilder.create().uv(30, 28).cuboid(-12.0f, -8.0f, -2.0f, 12.0f, 16.0f, 4.0f), ModelTransform.of(-8.0f, -2.0f, 0.0f, 0.0f, (float) Math.toRadians(-14f), (float) Math.toRadians(12f)));
        ModelPartData mantle_right_2 = mantle_right_1.addChild("mantle_right_2", ModelPartBuilder.create().uv(64, 28).cuboid(-10.0f, -6.0f, -1.5f, 10.0f, 11.0f, 3.0f), ModelTransform.of(-12.0f, 0.0f, 0.0f, 0.0f, (float) Math.toRadians(-18f), (float) Math.toRadians(18f)));
        ModelPartData t_l1_base = core_body.addChild("t_l1_base", ModelPartBuilder.create().uv(92, 28).cuboid(0.0f, -1.5f, -1.5f, 11.0f, 3.0f, 3.0f), ModelTransform.of(8.0f, -9.0f, 4.0f, (float) Math.toRadians(18f), (float) Math.toRadians(34f), (float) Math.toRadians(-42f)));
        ModelPartData t_l1_tip = t_l1_base.addChild("t_l1_tip", ModelPartBuilder.create().uv(122, 28).cuboid(0.0f, -1.0f, -1.0f, 10.0f, 2.0f, 2.0f), ModelTransform.of(11.0f, 0.0f, 0.0f, (float) Math.toRadians(24f), (float) Math.toRadians(26f), (float) Math.toRadians(-28f)));
        ModelPartData t_l2_base = core_body.addChild("t_l2_base", ModelPartBuilder.create().uv(148, 28).cuboid(0.0f, -1.5f, -1.5f, 11.0f, 3.0f, 3.0f), ModelTransform.of(8.0f, -1.0f, 6.0f, (float) Math.toRadians(8f), (float) Math.toRadians(40f), (float) Math.toRadians(-14f)));
        ModelPartData t_l2_tip = t_l2_base.addChild("t_l2_tip", ModelPartBuilder.create().uv(178, 28).cuboid(0.0f, -1.0f, -1.0f, 10.0f, 2.0f, 2.0f), ModelTransform.of(11.0f, 0.0f, 0.0f, (float) Math.toRadians(16f), (float) Math.toRadians(30f), (float) Math.toRadians(-12f)));
        ModelPartData t_l3_base = core_body.addChild("t_l3_base", ModelPartBuilder.create().uv(204, 28).cuboid(0.0f, -1.5f, -1.5f, 11.0f, 3.0f, 3.0f), ModelTransform.of(8.0f, 9.0f, 6.0f, (float) Math.toRadians(-10f), (float) Math.toRadians(38f), (float) Math.toRadians(18f)));
        ModelPartData t_l3_tip = t_l3_base.addChild("t_l3_tip", ModelPartBuilder.create().uv(2, 50).cuboid(0.0f, -1.0f, -1.0f, 10.0f, 2.0f, 2.0f), ModelTransform.of(11.0f, 0.0f, 0.0f, (float) Math.toRadians(-16f), (float) Math.toRadians(28f), (float) Math.toRadians(24f)));
        ModelPartData t_l4_base = core_body.addChild("t_l4_base", ModelPartBuilder.create().uv(28, 50).cuboid(0.0f, -1.5f, -1.5f, 11.0f, 3.0f, 3.0f), ModelTransform.of(8.0f, 17.0f, 4.0f, (float) Math.toRadians(-20f), (float) Math.toRadians(28f), (float) Math.toRadians(42f)));
        ModelPartData t_l4_tip = t_l4_base.addChild("t_l4_tip", ModelPartBuilder.create().uv(58, 50).cuboid(0.0f, -1.0f, -1.0f, 10.0f, 2.0f, 2.0f), ModelTransform.of(11.0f, 0.0f, 0.0f, (float) Math.toRadians(-24f), (float) Math.toRadians(22f), (float) Math.toRadians(32f)));
        ModelPartData t_r1_base = core_body.addChild("t_r1_base", ModelPartBuilder.create().uv(84, 50).cuboid(-11.0f, -1.5f, -1.5f, 11.0f, 3.0f, 3.0f), ModelTransform.of(-8.0f, -9.0f, 4.0f, (float) Math.toRadians(18f), (float) Math.toRadians(-34f), (float) Math.toRadians(42f)));
        ModelPartData t_r1_tip = t_r1_base.addChild("t_r1_tip", ModelPartBuilder.create().uv(114, 50).cuboid(-10.0f, -1.0f, -1.0f, 10.0f, 2.0f, 2.0f), ModelTransform.of(-11.0f, 0.0f, 0.0f, (float) Math.toRadians(24f), (float) Math.toRadians(-26f), (float) Math.toRadians(28f)));
        ModelPartData t_r2_base = core_body.addChild("t_r2_base", ModelPartBuilder.create().uv(140, 50).cuboid(-11.0f, -1.5f, -1.5f, 11.0f, 3.0f, 3.0f), ModelTransform.of(-8.0f, -1.0f, 6.0f, (float) Math.toRadians(8f), (float) Math.toRadians(-40f), (float) Math.toRadians(14f)));
        ModelPartData t_r2_tip = t_r2_base.addChild("t_r2_tip", ModelPartBuilder.create().uv(170, 50).cuboid(-10.0f, -1.0f, -1.0f, 10.0f, 2.0f, 2.0f), ModelTransform.of(-11.0f, 0.0f, 0.0f, (float) Math.toRadians(16f), (float) Math.toRadians(-30f), (float) Math.toRadians(12f)));
        ModelPartData t_r3_base = core_body.addChild("t_r3_base", ModelPartBuilder.create().uv(196, 50).cuboid(-11.0f, -1.5f, -1.5f, 11.0f, 3.0f, 3.0f), ModelTransform.of(-8.0f, 9.0f, 6.0f, (float) Math.toRadians(-10f), (float) Math.toRadians(-38f), (float) Math.toRadians(-18f)));
        ModelPartData t_r3_tip = t_r3_base.addChild("t_r3_tip", ModelPartBuilder.create().uv(226, 50).cuboid(-10.0f, -1.0f, -1.0f, 10.0f, 2.0f, 2.0f), ModelTransform.of(-11.0f, 0.0f, 0.0f, (float) Math.toRadians(-16f), (float) Math.toRadians(-28f), (float) Math.toRadians(-24f)));
        ModelPartData t_r4_base = core_body.addChild("t_r4_base", ModelPartBuilder.create().uv(2, 58).cuboid(-11.0f, -1.5f, -1.5f, 11.0f, 3.0f, 3.0f), ModelTransform.of(-8.0f, 17.0f, 4.0f, (float) Math.toRadians(-20f), (float) Math.toRadians(-28f), (float) Math.toRadians(-42f)));
        ModelPartData t_r4_tip = t_r4_base.addChild("t_r4_tip", ModelPartBuilder.create().uv(32, 58).cuboid(-10.0f, -1.0f, -1.0f, 10.0f, 2.0f, 2.0f), ModelTransform.of(-11.0f, 0.0f, 0.0f, (float) Math.toRadians(-24f), (float) Math.toRadians(-22f), (float) Math.toRadians(-32f)));
        ModelPartData tail_ribbon_1 = core_body.addChild("tail_ribbon_1", ModelPartBuilder.create().uv(58, 58).cuboid(-2.0f, 0.0f, -1.5f, 4.0f, 8.0f, 3.0f), ModelTransform.of(0.0f, 25.0f, 0.0f, (float) Math.toRadians(14f), 0.0f, 0.0f));
        ModelPartData tail_ribbon_2 = tail_ribbon_1.addChild("tail_ribbon_2", ModelPartBuilder.create().uv(74, 58).cuboid(-1.5f, 0.0f, -1.0f, 3.0f, 7.0f, 2.0f), ModelTransform.of(0.0f, 8.0f, 0.0f, (float) Math.toRadians(-18f), 0.0f, 0.0f));
        return TexturedModelData.of(modelData, 256, 256);
    }

    @Override
    public void render(MatrixStack matrices, VertexConsumer vertices, int light, int overlay, int color) {
        root.render(matrices, vertices, light, overlay, color);
    }

    @Override
    public void setAngles(VaatuSpiritTitanEntity entity, float limbAngle, float limbDistance, float animationProgress, float headYaw, float headPitch) {
        // Titanic floating undulation
        float floatWave = MathHelper.sin(animationProgress * 0.08f);
        this.core_body.pitch = (float) Math.toRadians(4.0f) + floatWave * 0.06f;
        // Mantle wing breathing
        this.mantle_left_1.roll = (float) Math.toRadians(-12.0f) + floatWave * 0.12f;
        this.mantle_right_1.roll = (float) Math.toRadians(12.0f) - floatWave * 0.12f;
        // Undulating dark tentacles
        this.t_l1_base.yaw = (float) Math.toRadians(34.0f) + MathHelper.sin(animationProgress * 0.10f + 0.0f) * 0.22f;
        this.t_l2_base.yaw = (float) Math.toRadians(40.0f) + MathHelper.sin(animationProgress * 0.10f + 1.2f) * 0.22f;
        this.t_l3_base.yaw = (float) Math.toRadians(38.0f) + MathHelper.sin(animationProgress * 0.10f + 2.4f) * 0.22f;
        this.t_l4_base.yaw = (float) Math.toRadians(28.0f) + MathHelper.sin(animationProgress * 0.10f + 3.6f) * 0.22f;
        this.t_r1_base.yaw = (float) Math.toRadians(-34.0f) - MathHelper.sin(animationProgress * 0.10f + 0.0f) * 0.22f;
        this.t_r2_base.yaw = (float) Math.toRadians(-40.0f) - MathHelper.sin(animationProgress * 0.10f + 1.2f) * 0.22f;
        this.t_r3_base.yaw = (float) Math.toRadians(-38.0f) - MathHelper.sin(animationProgress * 0.10f + 2.4f) * 0.22f;
        this.t_r4_base.yaw = (float) Math.toRadians(-28.0f) - MathHelper.sin(animationProgress * 0.10f + 3.6f) * 0.22f;
        this.tail_ribbon_1.pitch = (float) Math.toRadians(14.0f) + MathHelper.sin(animationProgress * 0.08f) * 0.25f;
        this.tail_ribbon_2.pitch = (float) Math.toRadians(-18.0f) + MathHelper.cos(animationProgress * 0.08f) * 0.25f;
    }
}