package com.avatarmod.elements.client.render.entity.model;

import com.avatarmod.elements.entity.pet.WingedLemurEntity;
import net.minecraft.client.model.*;
import net.minecraft.client.render.VertexConsumer;
import net.minecraft.client.render.entity.model.EntityModel;
import net.minecraft.client.render.entity.model.EntityModelLayer;
import net.minecraft.client.util.math.MatrixStack;
import net.minecraft.util.Identifier;
import net.minecraft.util.math.MathHelper;

public class WingedLemurEntityModel extends EntityModel<WingedLemurEntity> {
    public static final EntityModelLayer LAYER_LOCATION = new EntityModelLayer(Identifier.of("avatar_elements", "wingedlemurentity"), "main");

    private final ModelPart root;
    private final ModelPart body;
    private final ModelPart head;
    private final ModelPart ear_left;
    private final ModelPart ear_right;
    private final ModelPart wing_left;
    private final ModelPart wing_right;
    private final ModelPart tail;

    public WingedLemurEntityModel(ModelPart root) {
        this.root = root;
        this.body = root.getChild("body");
        this.head = this.body.getChild("head");
        this.ear_left = this.head.getChild("ear_left");
        this.ear_right = this.head.getChild("ear_right");
        this.wing_left = this.body.getChild("wing_left");
        this.wing_right = this.body.getChild("wing_right");
        this.tail = this.body.getChild("tail");
    }

    public static TexturedModelData getTexturedModelData() {
        ModelData modelData = new ModelData();
        ModelPartData root = modelData.getRoot();

        ModelPartData body = root.addChild("body", ModelPartBuilder.create()
                .uv(0, 0).cuboid(-2.5f, -3.0f, -3.0f, 5.0f, 6.0f, 6.0f),
                ModelTransform.pivot(0.0f, 19.0f, 0.0f));

        ModelPartData head = body.addChild("head", ModelPartBuilder.create()
                .uv(0, 12).cuboid(-2.5f, -3.5f, -4.0f, 5.0f, 5.0f, 4.0f)
                .uv(18, 12).cuboid(-1.5f, -1.0f, -5.5f, 3.0f, 2.5f, 2.0f),
                ModelTransform.pivot(0.0f, -2.0f, -2.5f));

        head.addChild("ear_left", ModelPartBuilder.create()
                .uv(22, 0).cuboid(-0.5f, -7.0f, -0.5f, 4.0f, 7.0f, 1.0f),
                ModelTransform.of(2.0f, -2.5f, -1.5f, 0.0f, 0.0f, (float) Math.toRadians(25f)));

        head.addChild("ear_right", ModelPartBuilder.create()
                .uv(22, 8).cuboid(-3.5f, -7.0f, -0.5f, 4.0f, 7.0f, 1.0f),
                ModelTransform.of(-2.0f, -2.5f, -1.5f, 0.0f, 0.0f, (float) Math.toRadians(-25f)));

        body.addChild("wing_left", ModelPartBuilder.create()
                .uv(0, 21).cuboid(0.0f, 0.0f, -1.0f, 7.0f, 8.0f, 1.0f),
                ModelTransform.pivot(2.5f, -2.0f, 0.0f));

        body.addChild("wing_right", ModelPartBuilder.create()
                .uv(16, 21).cuboid(-7.0f, 0.0f, -1.0f, 7.0f, 8.0f, 1.0f),
                ModelTransform.pivot(-2.5f, -2.0f, 0.0f));

        body.addChild("tail", ModelPartBuilder.create()
                .uv(32, 0).cuboid(-1.0f, -1.0f, 0.0f, 2.0f, 2.0f, 12.0f),
                ModelTransform.of(0.0f, 1.0f, 3.0f, (float) Math.toRadians(20f), 0.0f, 0.0f));

        return TexturedModelData.of(modelData, 64, 64);
    }

    @Override
    public void setAngles(WingedLemurEntity entity, float limbAngle, float limbDistance, float animationProgress, float headYaw, float headPitch) {
        this.head.pitch = headPitch * ((float) Math.PI / 180F);
        this.head.yaw = headYaw * ((float) Math.PI / 180F);

        if (entity.isOnGround()) {
            this.wing_left.roll = (float) Math.toRadians(15f);
            this.wing_right.roll = (float) Math.toRadians(-15f);
            this.tail.yaw = MathHelper.cos(animationProgress * 0.1F) * 0.2F;
        } else {
            // Gliding flap
            this.wing_left.roll = (float) Math.toRadians(75f) + MathHelper.sin(animationProgress * 0.3F) * 0.15F;
            this.wing_right.roll = (float) Math.toRadians(-75f) - MathHelper.sin(animationProgress * 0.3F) * 0.15F;
            this.tail.pitch = (float) Math.toRadians(-10f);
        }
    }

    @Override
    public void render(MatrixStack matrices, VertexConsumer vertices, int light, int overlay, int color) {
        root.render(matrices, vertices, light, overlay, color);
    }
}
