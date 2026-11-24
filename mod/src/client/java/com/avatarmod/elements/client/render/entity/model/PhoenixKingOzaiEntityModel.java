package com.avatarmod.elements.client.render.entity.model;

import com.avatarmod.elements.entity.boss.PhoenixKingOzaiEntity;
import net.minecraft.client.model.*;
import net.minecraft.client.render.VertexConsumer;
import net.minecraft.client.render.entity.model.EntityModel;
import net.minecraft.client.render.entity.model.EntityModelLayer;
import net.minecraft.client.util.math.MatrixStack;
import net.minecraft.util.Identifier;
import net.minecraft.util.math.MathHelper;

public class PhoenixKingOzaiEntityModel extends EntityModel<PhoenixKingOzaiEntity> {
    public static final EntityModelLayer LAYER_LOCATION = new EntityModelLayer(Identifier.of("avatar_elements", "phoenixkingozaientity"), "main");

    private final ModelPart root;
    private final ModelPart head;
    private final ModelPart body;
    private final ModelPart right_arm;
    private final ModelPart left_arm;
    private final ModelPart right_leg;
    private final ModelPart left_leg;
    private final ModelPart crown;
    private final ModelPart mantle;

    public PhoenixKingOzaiEntityModel(ModelPart root) {
        this.root = root;
        this.body = root.getChild("body");
        this.head = this.body.getChild("head");
        this.crown = this.head.getChild("crown");
        this.mantle = this.body.getChild("mantle");
        this.right_arm = this.body.getChild("right_arm");
        this.left_arm = this.body.getChild("left_arm");
        this.right_leg = root.getChild("right_leg");
        this.left_leg = root.getChild("left_leg");
    }

    public static TexturedModelData getTexturedModelData() {
        ModelData modelData = new ModelData();
        ModelPartData root = modelData.getRoot();

        // Fire Lord armored chest and robes
        ModelPartData body = root.addChild("body", ModelPartBuilder.create()
                .uv(16, 16).cuboid(-4.5f, 0.0f, -2.5f, 9.0f, 13.0f, 5.0f)
                .uv(0, 36).cuboid(-5.0f, 11.0f, -3.0f, 10.0f, 8.0f, 6.0f),
                ModelTransform.pivot(0.0f, -1.0f, 0.0f));

        // Fierce head with wild flowing dark hair
        ModelPartData head = body.addChild("head", ModelPartBuilder.create()
                .uv(0, 0).cuboid(-4.0f, -8.0f, -4.0f, 8.0f, 8.0f, 8.0f)
                .uv(32, 0).cuboid(-4.5f, -8.5f, -4.5f, 9.0f, 12.0f, 9.0f),
                ModelTransform.pivot(0.0f, 0.0f, 0.0f));

        // Phoenix King golden flame headpiece crown
        head.addChild("crown", ModelPartBuilder.create()
                .uv(0, 52).cuboid(-2.0f, -14.0f, -2.0f, 4.0f, 6.0f, 4.0f)
                .uv(16, 52).cuboid(-3.5f, -13.0f, -1.5f, 7.0f, 5.0f, 3.0f),
                ModelTransform.pivot(0.0f, 0.0f, 0.0f));

        // Imperial royal shoulder mantle
        body.addChild("mantle", ModelPartBuilder.create()
                .uv(36, 52).cuboid(-6.5f, -1.0f, -3.5f, 13.0f, 5.0f, 7.0f),
                ModelTransform.pivot(0.0f, 0.0f, 0.0f));

        // Arms in combat stance
        body.addChild("right_arm", ModelPartBuilder.create()
                .uv(40, 16).cuboid(-3.0f, -2.0f, -2.0f, 4.0f, 14.0f, 4.0f)
                .uv(56, 16).cuboid(-3.5f, -2.5f, -2.5f, 5.0f, 6.0f, 5.0f),
                ModelTransform.pivot(-5.5f, 2.0f, 0.0f));

        body.addChild("left_arm", ModelPartBuilder.create()
                .uv(32, 48).cuboid(-1.0f, -2.0f, -2.0f, 4.0f, 14.0f, 4.0f)
                .uv(48, 48).cuboid(-1.5f, -2.5f, -2.5f, 5.0f, 6.0f, 5.0f),
                ModelTransform.pivot(5.5f, 2.0f, 0.0f));

        // Legs with Fire Nation grieves
        root.addChild("right_leg", ModelPartBuilder.create()
                .uv(0, 16).cuboid(-2.0f, 0.0f, -2.0f, 4.0f, 12.0f, 4.0f),
                ModelTransform.pivot(-2.0f, 12.0f, 0.0f));

        root.addChild("left_leg", ModelPartBuilder.create()
                .uv(16, 48).cuboid(-2.0f, 0.0f, -2.0f, 4.0f, 12.0f, 4.0f),
                ModelTransform.pivot(2.0f, 12.0f, 0.0f));

        return TexturedModelData.of(modelData, 128, 128);
    }

    @Override
    public void setAngles(PhoenixKingOzaiEntity entity, float limbAngle, float limbDistance, float animationProgress, float headYaw, float headPitch) {
        this.head.pitch = headPitch * ((float) Math.PI / 180F);
        this.head.yaw = headYaw * ((float) Math.PI / 180F);

        this.right_leg.pitch = MathHelper.cos(limbAngle * 0.6662F) * 1.4F * limbDistance;
        this.left_leg.pitch = MathHelper.cos(limbAngle * 0.6662F + (float) Math.PI) * 1.4F * limbDistance;

        // Fierce firebending dual-arm casting stance
        this.right_arm.pitch = -0.5F + MathHelper.sin(animationProgress * 0.1F) * 0.15F;
        this.left_arm.pitch = -0.5F - MathHelper.sin(animationProgress * 0.1F) * 0.15F;
        this.right_arm.yaw = -0.2F;
        this.left_arm.yaw = 0.2F;
    }

    @Override
    public void render(MatrixStack matrices, VertexConsumer vertices, int light, int overlay, int color) {
        root.render(matrices, vertices, light, overlay, color);
    }
}
