package com.avatarmod.elements.client.render.entity.model;

import com.avatarmod.elements.entity.pet.FlyingBisonEntity;
import net.minecraft.client.model.*;
import net.minecraft.client.render.VertexConsumer;
import net.minecraft.client.render.entity.model.EntityModel;
import net.minecraft.client.render.entity.model.EntityModelLayer;
import net.minecraft.client.util.math.MatrixStack;
import net.minecraft.util.Identifier;
import net.minecraft.util.math.MathHelper;

public class FlyingBisonEntityModel extends EntityModel<FlyingBisonEntity> {
    public static final EntityModelLayer LAYER_LOCATION = new EntityModelLayer(Identifier.of("avatar_elements", "flyingbisonentity"), "main");

    private final ModelPart root;
    private final ModelPart body;
    private final ModelPart neck;
    private final ModelPart head;
    private final ModelPart horn_left;
    private final ModelPart horn_right;
    private final ModelPart tail;
    private final ModelPart leg_fl;
    private final ModelPart leg_fr;
    private final ModelPart leg_ml;
    private final ModelPart leg_mr;
    private final ModelPart leg_bl;
    private final ModelPart leg_br;

    public FlyingBisonEntityModel(ModelPart root) {
        this.root = root;
        this.body = root.getChild("body");
        this.neck = this.body.getChild("neck");
        this.head = this.neck.getChild("head");
        this.horn_left = this.head.getChild("horn_left");
        this.horn_right = this.head.getChild("horn_right");
        this.tail = this.body.getChild("tail");
        this.leg_fl = this.body.getChild("leg_fl");
        this.leg_fr = this.body.getChild("leg_fr");
        this.leg_ml = this.body.getChild("leg_ml");
        this.leg_mr = this.body.getChild("leg_mr");
        this.leg_bl = this.body.getChild("leg_bl");
        this.leg_br = this.body.getChild("leg_br");
    }

    public static TexturedModelData getTexturedModelData() {
        ModelData modelData = new ModelData();
        ModelPartData root = modelData.getRoot();

        // Colossal Sky Bison torso
        ModelPartData body = root.addChild("body", ModelPartBuilder.create()
                .uv(0, 0).cuboid(-16.0f, -14.0f, -24.0f, 32.0f, 26.0f, 48.0f)
                .uv(0, 74).cuboid(-18.0f, -16.0f, -18.0f, 36.0f, 24.0f, 36.0f),
                ModelTransform.pivot(0.0f, 4.0f, 0.0f));

        // Muscular broad neck
        ModelPartData neck = body.addChild("neck", ModelPartBuilder.create()
                .uv(144, 74).cuboid(-12.0f, -10.0f, -14.0f, 24.0f, 20.0f, 16.0f),
                ModelTransform.pivot(0.0f, -4.0f, -24.0f));

        // Broad bison head with snout
        ModelPartData head = neck.addChild("head", ModelPartBuilder.create()
                .uv(112, 0).cuboid(-10.0f, -8.0f, -14.0f, 20.0f, 18.0f, 16.0f)
                .uv(184, 0).cuboid(-8.0f, 0.0f, -18.0f, 16.0f, 10.0f, 6.0f),
                ModelTransform.pivot(0.0f, 0.0f, -12.0f));

        // Curved sweeping horns
        head.addChild("horn_left", ModelPartBuilder.create()
                .uv(0, 134).cuboid(-2.0f, -12.0f, -2.0f, 4.0f, 12.0f, 4.0f)
                .uv(16, 134).cuboid(2.0f, -16.0f, -2.0f, 8.0f, 4.0f, 4.0f),
                ModelTransform.of(9.0f, -6.0f, -4.0f, 0.0f, 0.0f, (float) Math.toRadians(25f)));

        head.addChild("horn_right", ModelPartBuilder.create()
                .uv(40, 134).cuboid(-2.0f, -12.0f, -2.0f, 4.0f, 12.0f, 4.0f)
                .uv(56, 134).cuboid(-10.0f, -16.0f, -2.0f, 8.0f, 4.0f, 4.0f),
                ModelTransform.of(-9.0f, -6.0f, -4.0f, 0.0f, 0.0f, (float) Math.toRadians(-25f)));

        // Flat beaver-like airbender tail
        body.addChild("tail", ModelPartBuilder.create()
                .uv(0, 150).cuboid(-12.0f, -2.0f, 0.0f, 24.0f, 4.0f, 28.0f)
                .uv(0, 182).cuboid(-10.0f, -1.5f, 28.0f, 20.0f, 3.0f, 14.0f),
                ModelTransform.of(0.0f, 0.0f, 24.0f, (float) Math.toRadians(-8f), 0.0f, 0.0f));

        // Six sturdy columnar legs (front, middle, back)
        body.addChild("leg_fl", ModelPartBuilder.create().uv(104, 134).cuboid(-4.0f, 0.0f, -4.0f, 8.0f, 14.0f, 8.0f), ModelTransform.pivot(14.0f, 6.0f, -18.0f));
        body.addChild("leg_fr", ModelPartBuilder.create().uv(136, 134).cuboid(-4.0f, 0.0f, -4.0f, 8.0f, 14.0f, 8.0f), ModelTransform.pivot(-14.0f, 6.0f, -18.0f));
        body.addChild("leg_ml", ModelPartBuilder.create().uv(168, 134).cuboid(-4.0f, 0.0f, -4.0f, 8.0f, 14.0f, 8.0f), ModelTransform.pivot(14.0f, 6.0f, 0.0f));
        body.addChild("leg_mr", ModelPartBuilder.create().uv(200, 134).cuboid(-4.0f, 0.0f, -4.0f, 8.0f, 14.0f, 8.0f), ModelTransform.pivot(-14.0f, 6.0f, 0.0f));
        body.addChild("leg_bl", ModelPartBuilder.create().uv(72, 156).cuboid(-4.0f, 0.0f, -4.0f, 8.0f, 14.0f, 8.0f), ModelTransform.pivot(14.0f, 6.0f, 18.0f));
        body.addChild("leg_br", ModelPartBuilder.create().uv(104, 156).cuboid(-4.0f, 0.0f, -4.0f, 8.0f, 14.0f, 8.0f), ModelTransform.pivot(-14.0f, 6.0f, 18.0f));

        return TexturedModelData.of(modelData, 512, 512);
    }

    @Override
    public void setAngles(FlyingBisonEntity entity, float limbAngle, float limbDistance, float animationProgress, float headYaw, float headPitch) {
        this.head.pitch = headPitch * ((float) Math.PI / 180F);
        this.head.yaw = headYaw * ((float) Math.PI / 180F);

        // 6-legged walking or flying paddle animation
        if (entity.isOnGround()) {
            this.leg_fl.pitch = MathHelper.cos(limbAngle * 0.4F) * 0.8F * limbDistance;
            this.leg_fr.pitch = MathHelper.cos(limbAngle * 0.4F + (float) Math.PI) * 0.8F * limbDistance;
            this.leg_ml.pitch = MathHelper.cos(limbAngle * 0.4F + (float) Math.PI) * 0.8F * limbDistance;
            this.leg_mr.pitch = MathHelper.cos(limbAngle * 0.4F) * 0.8F * limbDistance;
            this.leg_bl.pitch = MathHelper.cos(limbAngle * 0.4F) * 0.8F * limbDistance;
            this.leg_br.pitch = MathHelper.cos(limbAngle * 0.4F + (float) Math.PI) * 0.8F * limbDistance;
            this.tail.pitch = (float) Math.toRadians(-8f) + MathHelper.sin(animationProgress * 0.05F) * 0.08F;
        } else {
            // Airborne flight paddle
            float flightWave = MathHelper.sin(animationProgress * 0.15F);
            this.leg_fl.pitch = 0.4F + flightWave * 0.15F;
            this.leg_fr.pitch = 0.4F + flightWave * 0.15F;
            this.leg_ml.pitch = 0.2F + flightWave * 0.12F;
            this.leg_mr.pitch = 0.2F + flightWave * 0.12F;
            this.leg_bl.pitch = -0.3F + flightWave * 0.18F;
            this.leg_br.pitch = -0.3F + flightWave * 0.18F;
            this.tail.pitch = (float) Math.toRadians(4f) + flightWave * 0.25F; // Tail steers airflow!
        }
    }

    @Override
    public void render(MatrixStack matrices, VertexConsumer vertices, int light, int overlay, int color) {
        root.render(matrices, vertices, light, overlay, color);
    }
}
