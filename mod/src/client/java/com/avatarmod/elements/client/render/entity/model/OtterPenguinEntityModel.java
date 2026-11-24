package com.avatarmod.elements.client.render.entity.model;

import com.avatarmod.elements.entity.mob.OtterPenguinEntity;
import net.minecraft.client.model.*;
import net.minecraft.client.render.VertexConsumer;
import net.minecraft.client.render.entity.model.EntityModel;
import net.minecraft.client.render.entity.model.EntityModelLayer;
import net.minecraft.client.util.math.MatrixStack;
import net.minecraft.util.Identifier;
import net.minecraft.util.math.MathHelper;

public class OtterPenguinEntityModel extends EntityModel<OtterPenguinEntity> {
    public static final EntityModelLayer LAYER_LOCATION = new EntityModelLayer(Identifier.of("avatar_elements", "otterpenguinentity"), "main");

    private final ModelPart root;
    private final ModelPart body;
    private final ModelPart head;
    private final ModelPart flipper_left;
    private final ModelPart flipper_right;
    private final ModelPart feet;
    private final ModelPart tail;

    public OtterPenguinEntityModel(ModelPart root) {
        this.root = root;
        this.body = root.getChild("body");
        this.head = this.body.getChild("head");
        this.flipper_left = this.body.getChild("flipper_left");
        this.flipper_right = this.body.getChild("flipper_right");
        this.feet = root.getChild("feet");
        this.tail = this.body.getChild("tail");
    }

    public static TexturedModelData getTexturedModelData() {
        ModelData modelData = new ModelData();
        ModelPartData root = modelData.getRoot();

        ModelPartData body = root.addChild("body", ModelPartBuilder.create()
                .uv(0, 0).cuboid(-3.5f, -6.0f, -3.0f, 7.0f, 12.0f, 6.0f),
                ModelTransform.pivot(0.0f, 16.0f, 0.0f));

        ModelPartData head = body.addChild("head", ModelPartBuilder.create()
                .uv(0, 18).cuboid(-2.5f, -4.5f, -3.0f, 5.0f, 5.0f, 5.0f)
                .uv(20, 18).cuboid(-1.0f, -2.0f, -5.5f, 2.0f, 2.0f, 3.0f),
                ModelTransform.pivot(0.0f, -6.0f, 0.0f));

        body.addChild("flipper_left", ModelPartBuilder.create()
                .uv(26, 0).cuboid(0.0f, 0.0f, -1.5f, 1.5f, 8.0f, 3.0f),
                ModelTransform.pivot(3.5f, -5.0f, 0.0f));

        body.addChild("flipper_right", ModelPartBuilder.create()
                .uv(26, 0).cuboid(-1.5f, 0.0f, -1.5f, 1.5f, 8.0f, 3.0f),
                ModelTransform.pivot(-3.5f, -5.0f, 0.0f));

        root.addChild("feet", ModelPartBuilder.create()
                .uv(0, 28).cuboid(-3.5f, 0.0f, -3.0f, 7.0f, 2.0f, 4.0f),
                ModelTransform.pivot(0.0f, 22.0f, 0.0f));

        body.addChild("tail", ModelPartBuilder.create()
                .uv(22, 28).cuboid(-1.5f, -1.0f, 0.0f, 3.0f, 2.0f, 4.0f),
                ModelTransform.pivot(0.0f, 4.5f, 2.5f));

        return TexturedModelData.of(modelData, 64, 64);
    }

    @Override
    public void setAngles(OtterPenguinEntity entity, float limbAngle, float limbDistance, float animationProgress, float headYaw, float headPitch) {
        this.head.pitch = headPitch * ((float) Math.PI / 180F);
        this.head.yaw = headYaw * ((float) Math.PI / 180F);

        this.flipper_left.roll = (float) Math.toRadians(15f) + MathHelper.cos(limbAngle * 0.8F) * 0.25F * limbDistance;
        this.flipper_right.roll = (float) Math.toRadians(-15f) - MathHelper.cos(limbAngle * 0.8F) * 0.25F * limbDistance;
    }

    @Override
    public void render(MatrixStack matrices, VertexConsumer vertices, int light, int overlay, int color) {
        root.render(matrices, vertices, light, overlay, color);
    }
}
