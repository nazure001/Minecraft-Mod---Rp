package com.avatarmod.elements.client.render.entity.model;

import com.avatarmod.elements.entity.mob.FireNationSpearmanEntity;
import net.minecraft.client.model.*;
import net.minecraft.client.render.VertexConsumer;
import net.minecraft.client.render.entity.model.EntityModel;
import net.minecraft.client.render.entity.model.EntityModelLayer;
import net.minecraft.client.util.math.MatrixStack;
import net.minecraft.util.Identifier;
import net.minecraft.util.math.MathHelper;

public class FireNationSpearmanEntityModel extends EntityModel<FireNationSpearmanEntity> {
    public static final EntityModelLayer LAYER_LOCATION = new EntityModelLayer(Identifier.of("avatar_elements", "firenationspearmanentity"), "main");

    private final ModelPart root;
    private final ModelPart body;
    private final ModelPart head;
    private final ModelPart helmet;
    private final ModelPart right_arm;
    private final ModelPart left_arm;
    private final ModelPart right_leg;
    private final ModelPart left_leg;

    public FireNationSpearmanEntityModel(ModelPart root) {
        this.root = root;
        this.body = root.getChild("body");
        this.head = this.body.getChild("head");
        this.helmet = this.head.getChild("helmet");
        this.right_arm = this.body.getChild("right_arm");
        this.left_arm = this.body.getChild("left_arm");
        this.right_leg = root.getChild("right_leg");
        this.left_leg = root.getChild("left_leg");
    }

    public static TexturedModelData getTexturedModelData() {
        ModelData modelData = new ModelData();
        ModelPartData root = modelData.getRoot();

        ModelPartData body = root.addChild("body", ModelPartBuilder.create()
                .uv(16, 16).cuboid(-4.0f, 0.0f, -2.0f, 8.0f, 12.0f, 4.0f)
                .uv(0, 32).cuboid(-4.5f, 0.0f, -2.5f, 9.0f, 8.0f, 5.0f),
                ModelTransform.pivot(0.0f, 0.0f, 0.0f));

        ModelPartData head = body.addChild("head", ModelPartBuilder.create()
                .uv(0, 0).cuboid(-4.0f, -8.0f, -4.0f, 8.0f, 8.0f, 8.0f),
                ModelTransform.pivot(0.0f, 0.0f, 0.0f));

        head.addChild("helmet", ModelPartBuilder.create()
                .uv(32, 0).cuboid(-4.5f, -8.5f, -4.5f, 9.0f, 9.0f, 9.0f)
                .uv(32, 18).cuboid(-1.0f, -12.0f, -1.0f, 2.0f, 4.0f, 2.0f),
                ModelTransform.pivot(0.0f, 0.0f, 0.0f));

        body.addChild("right_arm", ModelPartBuilder.create()
                .uv(40, 32).cuboid(-3.0f, -2.0f, -2.0f, 4.0f, 12.0f, 4.0f),
                ModelTransform.pivot(-5.0f, 2.0f, 0.0f));

        body.addChild("left_arm", ModelPartBuilder.create()
                .uv(40, 32).cuboid(-1.0f, -2.0f, -2.0f, 4.0f, 12.0f, 4.0f),
                ModelTransform.pivot(5.0f, 2.0f, 0.0f));

        root.addChild("right_leg", ModelPartBuilder.create()
                .uv(0, 16).cuboid(-2.0f, 0.0f, -2.0f, 4.0f, 12.0f, 4.0f),
                ModelTransform.pivot(-1.9f, 12.0f, 0.0f));

        root.addChild("left_leg", ModelPartBuilder.create()
                .uv(0, 16).cuboid(-2.0f, 0.0f, -2.0f, 4.0f, 12.0f, 4.0f),
                ModelTransform.pivot(1.9f, 12.0f, 0.0f));

        return TexturedModelData.of(modelData, 128, 128);
    }

    @Override
    public void setAngles(FireNationSpearmanEntity entity, float limbAngle, float limbDistance, float animationProgress, float headYaw, float headPitch) {
        this.head.pitch = headPitch * ((float) Math.PI / 180F);
        this.head.yaw = headYaw * ((float) Math.PI / 180F);

        this.right_leg.pitch = MathHelper.cos(limbAngle * 0.6662F) * 1.4F * limbDistance;
        this.left_leg.pitch = MathHelper.cos(limbAngle * 0.6662F + (float) Math.PI) * 1.4F * limbDistance;
        this.right_arm.pitch = -0.4F + MathHelper.cos(limbAngle * 0.6662F) * 0.8F * limbDistance;
        this.left_arm.pitch = MathHelper.cos(limbAngle * 0.6662F) * 0.8F * limbDistance;
    }

    @Override
    public void render(MatrixStack matrices, VertexConsumer vertices, int light, int overlay, int color) {
        root.render(matrices, vertices, light, overlay, color);
    }
}
