package com.avatarmod.elements.client.render.entity.model;

import net.minecraft.client.model.*;
import net.minecraft.client.render.VertexConsumer;
import net.minecraft.client.render.entity.model.EntityModel;
import net.minecraft.client.render.entity.model.EntityModelLayer;
import net.minecraft.client.util.math.MatrixStack;
import net.minecraft.util.Identifier;
import net.minecraft.util.math.MathHelper;
import com.avatarmod.elements.entity.mob.ShirshuEntity;

public class ShirshuEntityModel extends EntityModel<ShirshuEntity> {
    public static final EntityModelLayer LAYER_LOCATION = new EntityModelLayer(Identifier.of("avatar_elements", "shirshuentity"), "main");

    private final ModelPart root;
    private final ModelPart body_pelvis;
    private final ModelPart body_mid;
    private final ModelPart body_shoulders;
    private final ModelPart neck;
    private final ModelPart head;
    private final ModelPart snout;
    private final ModelPart nose_star_top;
    private final ModelPart nose_star_left_u;
    private final ModelPart nose_star_right_u;
    private final ModelPart nose_star_left_l;
    private final ModelPart nose_star_right_l;
    private final ModelPart jaw;
    private final ModelPart tongue_base;
    private final ModelPart tongue_tip;
    private final ModelPart leg_fl_upper;
    private final ModelPart leg_fl_lower;
    private final ModelPart leg_fr_upper;
    private final ModelPart leg_fr_lower;
    private final ModelPart leg_bl_upper;
    private final ModelPart leg_bl_lower;
    private final ModelPart leg_br_upper;
    private final ModelPart leg_br_lower;
    private final ModelPart tail_1;
    private final ModelPart tail_2;
    private final ModelPart tail_3;
    private final ModelPart tail_tip;

    public ShirshuEntityModel(ModelPart root) {
        this.root = root;
        this.body_pelvis = root.getChild("body_pelvis");
        this.body_mid = root.getChild("body_pelvis").getChild("body_mid");
        this.body_shoulders = root.getChild("body_pelvis").getChild("body_mid").getChild("body_shoulders");
        this.neck = root.getChild("body_pelvis").getChild("body_mid").getChild("body_shoulders").getChild("neck");
        this.head = root.getChild("body_pelvis").getChild("body_mid").getChild("body_shoulders").getChild("neck").getChild("head");
        this.snout = root.getChild("body_pelvis").getChild("body_mid").getChild("body_shoulders").getChild("neck").getChild("head").getChild("snout");
        this.nose_star_top = root.getChild("body_pelvis").getChild("body_mid").getChild("body_shoulders").getChild("neck").getChild("head").getChild("snout").getChild("nose_star_top");
        this.nose_star_left_u = root.getChild("body_pelvis").getChild("body_mid").getChild("body_shoulders").getChild("neck").getChild("head").getChild("snout").getChild("nose_star_left_u");
        this.nose_star_right_u = root.getChild("body_pelvis").getChild("body_mid").getChild("body_shoulders").getChild("neck").getChild("head").getChild("snout").getChild("nose_star_right_u");
        this.nose_star_left_l = root.getChild("body_pelvis").getChild("body_mid").getChild("body_shoulders").getChild("neck").getChild("head").getChild("snout").getChild("nose_star_left_l");
        this.nose_star_right_l = root.getChild("body_pelvis").getChild("body_mid").getChild("body_shoulders").getChild("neck").getChild("head").getChild("snout").getChild("nose_star_right_l");
        this.jaw = root.getChild("body_pelvis").getChild("body_mid").getChild("body_shoulders").getChild("neck").getChild("head").getChild("jaw");
        this.tongue_base = root.getChild("body_pelvis").getChild("body_mid").getChild("body_shoulders").getChild("neck").getChild("head").getChild("jaw").getChild("tongue_base");
        this.tongue_tip = root.getChild("body_pelvis").getChild("body_mid").getChild("body_shoulders").getChild("neck").getChild("head").getChild("jaw").getChild("tongue_base").getChild("tongue_tip");
        this.leg_fl_upper = root.getChild("body_pelvis").getChild("body_mid").getChild("body_shoulders").getChild("leg_fl_upper");
        this.leg_fl_lower = root.getChild("body_pelvis").getChild("body_mid").getChild("body_shoulders").getChild("leg_fl_upper").getChild("leg_fl_lower");
        this.leg_fr_upper = root.getChild("body_pelvis").getChild("body_mid").getChild("body_shoulders").getChild("leg_fr_upper");
        this.leg_fr_lower = root.getChild("body_pelvis").getChild("body_mid").getChild("body_shoulders").getChild("leg_fr_upper").getChild("leg_fr_lower");
        this.leg_bl_upper = root.getChild("body_pelvis").getChild("leg_bl_upper");
        this.leg_bl_lower = root.getChild("body_pelvis").getChild("leg_bl_upper").getChild("leg_bl_lower");
        this.leg_br_upper = root.getChild("body_pelvis").getChild("leg_br_upper");
        this.leg_br_lower = root.getChild("body_pelvis").getChild("leg_br_upper").getChild("leg_br_lower");
        this.tail_1 = root.getChild("body_pelvis").getChild("tail_1");
        this.tail_2 = root.getChild("body_pelvis").getChild("tail_1").getChild("tail_2");
        this.tail_3 = root.getChild("body_pelvis").getChild("tail_1").getChild("tail_2").getChild("tail_3");
        this.tail_tip = root.getChild("body_pelvis").getChild("tail_1").getChild("tail_2").getChild("tail_3").getChild("tail_tip");
    }

    public static TexturedModelData getTexturedModelData() {
        ModelData modelData = new ModelData();
        ModelPartData root = modelData.getRoot();
        ModelPartData body_pelvis = root.addChild("body_pelvis", ModelPartBuilder.create().uv(2, 2).cuboid(-6.0f, -6.0f, -6.0f, 12.0f, 10.0f, 11.0f), ModelTransform.of(0.0f, 9.0f, 8.0f, (float) Math.toRadians(-6f), 0.0f, 0.0f));
        ModelPartData body_mid = body_pelvis.addChild("body_mid", ModelPartBuilder.create().uv(50, 2).cuboid(-6.5f, -6.0f, -9.0f, 13.0f, 11.0f, 10.0f).uv(98, 2).cuboid(-7.0f, -6.0f, -7.0f, 14.0f, 9.0f, 6.0f), ModelTransform.of(0.0f, -1.0f, -6.0f, (float) Math.toRadians(4f), 0.0f, 0.0f));
        ModelPartData body_shoulders = body_mid.addChild("body_shoulders", ModelPartBuilder.create().uv(140, 2).cuboid(-7.5f, -7.0f, -9.0f, 15.0f, 13.0f, 10.0f).uv(192, 2).cuboid(-8.5f, -8.0f, -10.0f, 17.0f, 10.0f, 11.0f), ModelTransform.of(0.0f, -1.0f, -9.0f, (float) Math.toRadians(8f), 0.0f, 0.0f));
        ModelPartData neck = body_shoulders.addChild("neck", ModelPartBuilder.create().uv(2, 27).cuboid(-5.0f, -5.0f, -6.0f, 10.0f, 9.0f, 7.0f), ModelTransform.of(0.0f, -1.0f, -9.0f, (float) Math.toRadians(-12f), 0.0f, 0.0f));
        ModelPartData head = neck.addChild("head", ModelPartBuilder.create().uv(38, 27).cuboid(-5.0f, -4.0f, -7.0f, 10.0f, 8.0f, 8.0f).uv(76, 27).cuboid(-6.0f, -7.0f, -3.0f, 2.0f, 5.0f, 3.0f).uv(88, 27).cuboid(4.0f, -7.0f, -3.0f, 2.0f, 5.0f, 3.0f), ModelTransform.of(0.0f, 0.0f, -6.0f, (float) Math.toRadians(14f), 0.0f, 0.0f));
        ModelPartData snout = head.addChild("snout", ModelPartBuilder.create().uv(100, 27).cuboid(-3.5f, -3.0f, -7.0f, 7.0f, 5.0f, 7.0f).uv(130, 27).cuboid(-2.5f, -2.5f, -11.0f, 5.0f, 4.0f, 4.0f), ModelTransform.of(0.0f, 1.0f, -7.0f, (float) Math.toRadians(6f), 0.0f, 0.0f));
        ModelPartData nose_star_top = snout.addChild("nose_star_top", ModelPartBuilder.create().uv(150, 27).cuboid(-1.0f, -2.0f, -3.0f, 2.0f, 2.0f, 3.0f), ModelTransform.of(0.0f, -2.0f, -11.0f, (float) Math.toRadians(-22.5f), 0.0f, 0.0f));
        ModelPartData nose_star_left_u = snout.addChild("nose_star_left_u", ModelPartBuilder.create().uv(162, 27).cuboid(-0.5f, -1.0f, -3.5f, 2.0f, 2.0f, 4.0f), ModelTransform.of(2.5f, -1.5f, -11.0f, (float) Math.toRadians(-12f), (float) Math.toRadians(-28f), 0.0f));
        ModelPartData nose_star_right_u = snout.addChild("nose_star_right_u", ModelPartBuilder.create().uv(176, 27).cuboid(-1.5f, -1.0f, -3.5f, 2.0f, 2.0f, 4.0f), ModelTransform.of(-2.5f, -1.5f, -11.0f, (float) Math.toRadians(-12f), (float) Math.toRadians(28f), 0.0f));
        ModelPartData nose_star_left_l = snout.addChild("nose_star_left_l", ModelPartBuilder.create().uv(190, 27).cuboid(-0.5f, -1.0f, -3.0f, 2.0f, 2.0f, 3.0f), ModelTransform.of(2.5f, 0.5f, -11.0f, (float) Math.toRadians(16f), (float) Math.toRadians(-24f), 0.0f));
        ModelPartData nose_star_right_l = snout.addChild("nose_star_right_l", ModelPartBuilder.create().uv(202, 27).cuboid(-1.5f, -1.0f, -3.0f, 2.0f, 2.0f, 3.0f), ModelTransform.of(-2.5f, 0.5f, -11.0f, (float) Math.toRadians(16f), (float) Math.toRadians(24f), 0.0f));
        ModelPartData jaw = head.addChild("jaw", ModelPartBuilder.create().uv(214, 27).cuboid(-3.0f, 0.0f, -8.0f, 6.0f, 2.0f, 8.0f), ModelTransform.of(0.0f, 3.0f, -6.0f, (float) Math.toRadians(8f), 0.0f, 0.0f));
        ModelPartData tongue_base = jaw.addChild("tongue_base", ModelPartBuilder.create().uv(2, 45).cuboid(-1.0f, -0.6f, -7.0f, 2.0f, 1.2f, 7.0f), ModelTransform.of(0.0f, 0.8f, -7.0f, (float) Math.toRadians(6f), 0.0f, 0.0f));
        ModelPartData tongue_tip = tongue_base.addChild("tongue_tip", ModelPartBuilder.create().uv(22, 45).cuboid(-0.8f, -0.5f, -6.0f, 1.6f, 1.0f, 6.0f), ModelTransform.of(0.0f, -0.0f, -7.0f, (float) Math.toRadians(10f), 0.0f, 0.0f));
        ModelPartData leg_fl_upper = body_shoulders.addChild("leg_fl_upper", ModelPartBuilder.create().uv(40, 45).cuboid(-2.0f, -1.0f, -3.0f, 5.0f, 9.0f, 6.0f), ModelTransform.of(7.5f, 3.0f, -5.0f, (float) Math.toRadians(14f), 0.0f, (float) Math.toRadians(-4f)));
        ModelPartData leg_fl_lower = leg_fl_upper.addChild("leg_fl_lower", ModelPartBuilder.create().uv(64, 45).cuboid(-2.0f, -1.0f, -2.5f, 4.0f, 7.0f, 5.0f).uv(84, 45).cuboid(-2.5f, 3.5f, -5.0f, 5.0f, 2.5f, 3.0f), ModelTransform.of(0.5f, 8.0f, 0.0f, (float) Math.toRadians(-18f), 0.0f, (float) Math.toRadians(4f)));
        ModelPartData leg_fr_upper = body_shoulders.addChild("leg_fr_upper", ModelPartBuilder.create().uv(102, 45).cuboid(-3.0f, -1.0f, -3.0f, 5.0f, 9.0f, 6.0f), ModelTransform.of(-7.5f, 3.0f, -5.0f, (float) Math.toRadians(-8f), 0.0f, (float) Math.toRadians(4f)));
        ModelPartData leg_fr_lower = leg_fr_upper.addChild("leg_fr_lower", ModelPartBuilder.create().uv(126, 45).cuboid(-2.0f, -1.0f, -2.5f, 4.0f, 7.0f, 5.0f).uv(146, 45).cuboid(-2.5f, 3.5f, -5.0f, 5.0f, 2.5f, 3.0f), ModelTransform.of(-0.5f, 8.0f, 0.0f, (float) Math.toRadians(10f), 0.0f, (float) Math.toRadians(-4f)));
        ModelPartData leg_bl_upper = body_pelvis.addChild("leg_bl_upper", ModelPartBuilder.create().uv(164, 45).cuboid(-2.0f, -1.0f, -3.0f, 5.0f, 9.0f, 6.0f), ModelTransform.of(6.5f, 1.0f, 0.0f, (float) Math.toRadians(-14f), 0.0f, (float) Math.toRadians(-3f)));
        ModelPartData leg_bl_lower = leg_bl_upper.addChild("leg_bl_lower", ModelPartBuilder.create().uv(188, 45).cuboid(-2.0f, -1.0f, -2.5f, 4.0f, 7.0f, 5.0f).uv(208, 45).cuboid(-2.5f, 3.5f, -5.0f, 5.0f, 2.5f, 3.0f), ModelTransform.of(0.5f, 8.0f, 0.0f, (float) Math.toRadians(16f), 0.0f, (float) Math.toRadians(3f)));
        ModelPartData leg_br_upper = body_pelvis.addChild("leg_br_upper", ModelPartBuilder.create().uv(226, 45).cuboid(-3.0f, -1.0f, -3.0f, 5.0f, 9.0f, 6.0f), ModelTransform.of(-6.5f, 1.0f, 0.0f, (float) Math.toRadians(10f), 0.0f, (float) Math.toRadians(3f)));
        ModelPartData leg_br_lower = leg_br_upper.addChild("leg_br_lower", ModelPartBuilder.create().uv(2, 62).cuboid(-2.0f, -1.0f, -2.5f, 4.0f, 7.0f, 5.0f).uv(22, 62).cuboid(-2.5f, 3.5f, -5.0f, 5.0f, 2.5f, 3.0f), ModelTransform.of(-0.5f, 8.0f, 0.0f, (float) Math.toRadians(-12f), 0.0f, (float) Math.toRadians(-3f)));
        ModelPartData tail_1 = body_pelvis.addChild("tail_1", ModelPartBuilder.create().uv(40, 62).cuboid(-2.5f, -2.0f, 0.0f, 5.0f, 4.0f, 8.0f), ModelTransform.of(0.0f, -1.0f, 5.0f, (float) Math.toRadians(-14f), (float) Math.toRadians(8f), 0.0f));
        ModelPartData tail_2 = tail_1.addChild("tail_2", ModelPartBuilder.create().uv(68, 62).cuboid(-2.0f, -1.5f, 0.0f, 4.0f, 3.0f, 8.0f), ModelTransform.of(0.0f, 0.0f, 8.0f, (float) Math.toRadians(-10f), (float) Math.toRadians(14f), 0.0f));
        ModelPartData tail_3 = tail_2.addChild("tail_3", ModelPartBuilder.create().uv(94, 62).cuboid(-1.5f, -1.5f, 0.0f, 3.0f, 2.5f, 8.0f), ModelTransform.of(0.0f, 0.0f, 8.0f, (float) Math.toRadians(12f), (float) Math.toRadians(16f), 0.0f));
        ModelPartData tail_tip = tail_3.addChild("tail_tip", ModelPartBuilder.create().uv(118, 62).cuboid(-1.0f, -1.2f, 0.0f, 2.0f, 2.0f, 6.0f), ModelTransform.of(0.0f, 0.0f, 8.0f, (float) Math.toRadians(18f), (float) Math.toRadians(12f), 0.0f));
        return TexturedModelData.of(modelData, 256, 256);
    }

    @Override
    public void render(MatrixStack matrices, VertexConsumer vertices, int light, int overlay, int color) {
        root.render(matrices, vertices, light, overlay, color);
    }

    @Override
    public void setAngles(ShirshuEntity entity, float limbAngle, float limbDistance, float animationProgress, float headYaw, float headPitch) {
        // Quadruped walk cycle
        this.leg_fl_upper.pitch = MathHelper.cos(limbAngle * 0.6662f) * 1.2f * limbDistance + (float) Math.toRadians(14.0f);
        this.leg_fr_upper.pitch = MathHelper.cos(limbAngle * 0.6662f + (float) Math.PI) * 1.2f * limbDistance - (float) Math.toRadians(8.0f);
        this.leg_bl_upper.pitch = MathHelper.cos(limbAngle * 0.6662f + (float) Math.PI) * 1.2f * limbDistance - (float) Math.toRadians(14.0f);
        this.leg_br_upper.pitch = MathHelper.cos(limbAngle * 0.6662f) * 1.2f * limbDistance + (float) Math.toRadians(10.0f);
        // Scent tracking / snout sniffing twitch
        this.nose_star_top.pitch = (float) Math.toRadians(-22.5f) + MathHelper.sin(animationProgress * 0.45f) * 0.15f;
        this.nose_star_left_u.yaw = (float) Math.toRadians(-28.0f) + MathHelper.cos(animationProgress * 0.40f) * 0.12f;
        this.nose_star_right_u.yaw = (float) Math.toRadians(28.0f) - MathHelper.cos(animationProgress * 0.40f) * 0.12f;
        // Head look tracking
        this.head.yaw = headYaw * 0.017453292f * 0.6f;
        this.head.pitch = headPitch * 0.017453292f * 0.6f + (float) Math.toRadians(14.0f);
        // Tail natural sway
        float tailSway = MathHelper.sin(animationProgress * 0.12f) * 0.2f + MathHelper.cos(limbAngle * 0.6662f) * 0.3f * limbDistance;
        this.tail_1.yaw = tailSway * 0.6f;
        this.tail_2.yaw = tailSway * 0.8f;
        this.tail_3.yaw = tailSway * 1.0f;
    }
}