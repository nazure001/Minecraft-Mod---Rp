package com.avatarmod.elements.client.render.entity.model;

import com.avatarmod.elements.entity.mob.TurtleDuckEntity;
import net.minecraft.client.model.*;
import net.minecraft.client.render.VertexConsumer;
import net.minecraft.client.render.entity.model.EntityModel;
import net.minecraft.client.render.entity.model.EntityModelLayer;
import net.minecraft.client.util.math.MatrixStack;
import net.minecraft.util.Identifier;
import net.minecraft.util.math.MathHelper;

public class TurtleDuckEntityModel extends EntityModel<TurtleDuckEntity> {
    public static final EntityModelLayer LAYER_LOCATION = new EntityModelLayer(Identifier.of("avatar_elements", "turtleduckentity"), "main");

    private final ModelPart root;
    private final ModelPart shell;
    private final ModelPart head;
    private final ModelPart bill;
    private final ModelPart flipper_left;
    private final ModelPart flipper_right;
    private final ModelPart foot_left;
    private final ModelPart foot_right;

    public TurtleDuckEntityModel(ModelPart root) {
        this.root = root;
        this.shell = root.getChild("shell");
        this.head = this.shell.getChild("head");
        this.bill = this.head.getChild("bill");
        this.flipper_left = this.shell.getChild("flipper_left");
        this.flipper_right = this.shell.getChild("flipper_right");
        this.foot_left = this.shell.getChild("foot_left");
        this.foot_right = this.shell.getChild("foot_right");
    }

    public static TexturedModelData getTexturedModelData() {
        ModelData modelData = new ModelData();
        ModelPartData root = modelData.getRoot();

        ModelPartData shell = root.addChild("shell", ModelPartBuilder.create()
                .uv(0, 0).cuboid(-3.5f, -2.5f, -4.5f, 7.0f, 5.0f, 9.0f)
                .uv(0, 14).cuboid(-3.0f, -3.5f, -4.0f, 6.0f, 1.0f, 8.0f),
                ModelTransform.pivot(0.0f, 21.0f, 0.0f));

        ModelPartData head = shell.addChild("head", ModelPartBuilder.create()
                .uv(24, 14).cuboid(-1.5f, -4.0f, -2.5f, 3.0f, 5.0f, 3.0f),
                ModelTransform.pivot(0.0f, -1.0f, -4.5f));

        head.addChild("bill", ModelPartBuilder.create()
                .uv(24, 22).cuboid(-1.5f, -1.5f, -4.5f, 3.0f, 1.5f, 2.0f),
                ModelTransform.pivot(0.0f, 0.0f, 0.0f));

        shell.addChild("flipper_left", ModelPartBuilder.create()
                .uv(0, 23).cuboid(0.0f, 0.0f, -1.5f, 4.0f, 1.0f, 3.0f),
                ModelTransform.pivot(3.5f, 1.5f, -2.0f));

        shell.addChild("flipper_right", ModelPartBuilder.create()
                .uv(0, 27).cuboid(-4.0f, 0.0f, -1.5f, 4.0f, 1.0f, 3.0f),
                ModelTransform.pivot(-3.5f, 1.5f, -2.0f));

        shell.addChild("foot_left", ModelPartBuilder.create()
                .uv(14, 23).cuboid(-1.0f, 0.0f, -1.0f, 2.0f, 2.0f, 3.0f),
                ModelTransform.pivot(2.0f, 2.0f, 3.5f));

        shell.addChild("foot_right", ModelPartBuilder.create()
                .uv(14, 23).cuboid(-1.0f, 0.0f, -1.0f, 2.0f, 2.0f, 3.0f),
                ModelTransform.pivot(-2.0f, 2.0f, 3.5f));

        return TexturedModelData.of(modelData, 64, 64);
    }

    @Override
    public void setAngles(TurtleDuckEntity entity, float limbAngle, float limbDistance, float animationProgress, float headYaw, float headPitch) {
        this.head.pitch = headPitch * ((float) Math.PI / 180F);
        this.head.yaw = headYaw * ((float) Math.PI / 180F);

        this.foot_left.pitch = MathHelper.cos(limbAngle * 0.7F) * 1.2F * limbDistance;
        this.foot_right.pitch = MathHelper.cos(limbAngle * 0.7F + (float) Math.PI) * 1.2F * limbDistance;

        if (entity.isTouchingWater()) {
            this.flipper_left.roll = MathHelper.sin(animationProgress * 0.25F) * 0.4F;
            this.flipper_right.roll = -MathHelper.sin(animationProgress * 0.25F) * 0.4F;
        }
    }

    @Override
    public void render(MatrixStack matrices, VertexConsumer vertices, int light, int overlay, int color) {
        root.render(matrices, vertices, light, overlay, color);
    }
}
