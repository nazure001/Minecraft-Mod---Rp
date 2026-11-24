package com.avatarmod.elements.client.render.entity.model;

import com.avatarmod.elements.entity.mob.PlatypusBearEntity;
import net.minecraft.client.model.*;
import net.minecraft.client.render.VertexConsumer;
import net.minecraft.client.render.entity.model.EntityModel;
import net.minecraft.client.render.entity.model.EntityModelLayer;
import net.minecraft.client.util.math.MatrixStack;
import net.minecraft.util.Identifier;
import net.minecraft.util.math.MathHelper;

public class PlatypusBearEntityModel extends EntityModel<PlatypusBearEntity> {
    public static final EntityModelLayer LAYER_LOCATION = new EntityModelLayer(Identifier.of("avatar_elements", "platypusbearentity"), "main");

    private final ModelPart root;
    private final ModelPart body;
    private final ModelPart head;
    private final ModelPart snout;
    private final ModelPart leg_front_left;
    private final ModelPart leg_front_right;
    private final ModelPart leg_back_left;
    private final ModelPart leg_back_right;
    private final ModelPart tail;

    public PlatypusBearEntityModel(ModelPart root) {
        this.root = root;
        this.body = root.getChild("body");
        this.head = this.body.getChild("head");
        this.snout = this.head.getChild("snout");
        this.leg_front_left = this.body.getChild("leg_front_left");
        this.leg_front_right = this.body.getChild("leg_front_right");
        this.leg_back_left = this.body.getChild("leg_back_left");
        this.leg_back_right = this.body.getChild("leg_back_right");
        this.tail = this.body.getChild("tail");
    }

    public static TexturedModelData getTexturedModelData() {
        ModelData modelData = new ModelData();
        ModelPartData root = modelData.getRoot();

        // Massive muscular bear body
        ModelPartData body = root.addChild("body", ModelPartBuilder.create()
                .uv(0, 0).cuboid(-7.5f, -7.0f, -9.0f, 15.0f, 14.0f, 18.0f)
                .uv(66, 0).cuboid(-8.5f, -8.0f, -8.0f, 17.0f, 15.0f, 10.0f),
                ModelTransform.pivot(0.0f, 11.0f, 0.0f));

        // Broad bear head with round ears
        ModelPartData head = body.addChild("head", ModelPartBuilder.create()
                .uv(0, 32).cuboid(-5.0f, -4.5f, -7.0f, 10.0f, 9.0f, 7.0f)
                .uv(34, 32).cuboid(-5.5f, -6.5f, -4.0f, 2.5f, 2.5f, 1.5f)
                .uv(42, 32).cuboid(3.0f, -6.5f, -4.0f, 2.5f, 2.5f, 1.5f),
                ModelTransform.pivot(0.0f, -2.0f, -9.0f));

        // Iconic wide duck bill / platypus snout!
        head.addChild("snout", ModelPartBuilder.create()
                .uv(0, 48).cuboid(-4.0f, -0.5f, -7.0f, 8.0f, 3.5f, 7.0f)
                .uv(30, 48).cuboid(-4.5f, 0.5f, -8.0f, 9.0f, 2.0f, 3.0f),
                ModelTransform.pivot(0.0f, 1.5f, -6.5f));

        // Four powerful limbs
        body.addChild("leg_front_left", ModelPartBuilder.create()
                .uv(54, 32).cuboid(-2.5f, 0.0f, -2.5f, 5.0f, 11.0f, 5.0f),
                ModelTransform.pivot(6.5f, 2.0f, -6.0f));

        body.addChild("leg_front_right", ModelPartBuilder.create()
                .uv(74, 32).cuboid(-2.5f, 0.0f, -2.5f, 5.0f, 11.0f, 5.0f),
                ModelTransform.pivot(-6.5f, 2.0f, -6.0f));

        body.addChild("leg_back_left", ModelPartBuilder.create()
                .uv(94, 32).cuboid(-2.5f, 0.0f, -3.0f, 5.0f, 11.0f, 6.0f),
                ModelTransform.pivot(6.5f, 2.0f, 6.0f));

        body.addChild("leg_back_right", ModelPartBuilder.create()
                .uv(116, 32).cuboid(-2.5f, 0.0f, -3.0f, 5.0f, 11.0f, 6.0f),
                ModelTransform.pivot(-6.5f, 2.0f, 6.0f));

        // Wide paddle beaver tail
        body.addChild("tail", ModelPartBuilder.create()
                .uv(0, 60).cuboid(-3.5f, -1.0f, 0.0f, 7.0f, 2.5f, 10.0f),
                ModelTransform.of(0.0f, -2.0f, 9.0f, (float) Math.toRadians(-12f), 0.0f, 0.0f));

        return TexturedModelData.of(modelData, 256, 256);
    }

    @Override
    public void setAngles(PlatypusBearEntity entity, float limbAngle, float limbDistance, float animationProgress, float headYaw, float headPitch) {
        this.head.pitch = headPitch * ((float) Math.PI / 180F);
        this.head.yaw = headYaw * ((float) Math.PI / 180F);

        // Quadruped walking gait
        this.leg_front_left.pitch = MathHelper.cos(limbAngle * 0.6662F) * 1.4F * limbDistance;
        this.leg_front_right.pitch = MathHelper.cos(limbAngle * 0.6662F + (float) Math.PI) * 1.4F * limbDistance;
        this.leg_back_left.pitch = MathHelper.cos(limbAngle * 0.6662F + (float) Math.PI) * 1.4F * limbDistance;
        this.leg_back_right.pitch = MathHelper.cos(limbAngle * 0.6662F) * 1.4F * limbDistance;
    }

    @Override
    public void render(MatrixStack matrices, VertexConsumer vertices, int light, int overlay, int color) {
        root.render(matrices, vertices, light, overlay, color);
    }
}
