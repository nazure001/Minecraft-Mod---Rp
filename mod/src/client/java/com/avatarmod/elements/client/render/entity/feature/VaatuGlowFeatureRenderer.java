package com.avatarmod.elements.client.render.entity.feature;

import com.avatarmod.elements.client.render.entity.model.VaatuEntityModel;
import com.avatarmod.elements.entity.boss.VaatuSpiritTitanEntity;
import net.minecraft.client.render.RenderLayer;
import net.minecraft.client.render.VertexConsumer;
import net.minecraft.client.render.VertexConsumerProvider;
import net.minecraft.client.render.entity.feature.EyesFeatureRenderer;
import net.minecraft.client.render.entity.feature.FeatureRendererContext;
import net.minecraft.client.util.math.MatrixStack;
import net.minecraft.util.Identifier;

public class VaatuGlowFeatureRenderer extends EyesFeatureRenderer<VaatuSpiritTitanEntity, VaatuEntityModel> {

    private static final RenderLayer GLOW_LAYER = RenderLayer.getEyes(
            Identifier.of("avatar_elements", "textures/entity/boss/vaatu_spirit_titan_glow.png")
    );

    public VaatuGlowFeatureRenderer(FeatureRendererContext<VaatuSpiritTitanEntity, VaatuEntityModel> featureRendererContext) {
        super(featureRendererContext);
    }

    @Override
    public RenderLayer getEyesTexture() {
        return GLOW_LAYER;
    }
}
