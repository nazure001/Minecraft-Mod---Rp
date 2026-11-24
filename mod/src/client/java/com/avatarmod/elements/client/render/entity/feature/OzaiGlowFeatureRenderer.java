package com.avatarmod.elements.client.render.entity.feature;

import com.avatarmod.elements.client.render.entity.model.PhoenixKingOzaiEntityModel;
import com.avatarmod.elements.entity.boss.PhoenixKingOzaiEntity;
import net.minecraft.client.render.RenderLayer;
import net.minecraft.client.render.VertexConsumerProvider;
import net.minecraft.client.render.entity.feature.EyesFeatureRenderer;
import net.minecraft.client.render.entity.feature.FeatureRendererContext;
import net.minecraft.client.util.math.MatrixStack;
import net.minecraft.util.Identifier;

public class OzaiGlowFeatureRenderer extends EyesFeatureRenderer<PhoenixKingOzaiEntity, PhoenixKingOzaiEntityModel> {

    private static final RenderLayer GLOW_LAYER = RenderLayer.getEyes(
            Identifier.of("avatar_elements", "textures/entity/boss/phoenix_king_ozai_glow.png")
    );

    public OzaiGlowFeatureRenderer(FeatureRendererContext<PhoenixKingOzaiEntity, PhoenixKingOzaiEntityModel> featureRendererContext) {
        super(featureRendererContext);
    }

    @Override
    public RenderLayer getEyesTexture() {
        return GLOW_LAYER;
    }

    @Override
    public void render(MatrixStack matrices, VertexConsumerProvider vertexConsumers, int light, PhoenixKingOzaiEntity entity, float limbAngle, float limbDistance, float tickDelta, float animationProgress, float headYaw, float headPitch) {
        super.render(matrices, vertexConsumers, light, entity, limbAngle, limbDistance, tickDelta, animationProgress, headYaw, headPitch);
    }
}
