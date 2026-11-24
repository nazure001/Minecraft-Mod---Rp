package com.avatarmod.elements.client.render.entity;

import com.avatarmod.elements.client.render.entity.feature.OzaiGlowFeatureRenderer;
import com.avatarmod.elements.client.render.entity.model.PhoenixKingOzaiEntityModel;
import com.avatarmod.elements.entity.boss.PhoenixKingOzaiEntity;
import net.minecraft.client.render.entity.EntityRendererFactory;
import net.minecraft.client.render.entity.MobEntityRenderer;
import net.minecraft.util.Identifier;

public class PhoenixKingOzaiEntityRenderer extends MobEntityRenderer<PhoenixKingOzaiEntity, PhoenixKingOzaiEntityModel> {

    private static final Identifier TEXTURE = Identifier.of("avatar_elements", "textures/entity/boss/phoenix_king_ozai.png");

    public PhoenixKingOzaiEntityRenderer(EntityRendererFactory.Context context) {
        super(context, new PhoenixKingOzaiEntityModel(context.getPart(PhoenixKingOzaiEntityModel.LAYER_LOCATION)), 0.6f);
        this.addFeature(new OzaiGlowFeatureRenderer(this));
    }

    @Override
    public Identifier getTexture(PhoenixKingOzaiEntity entity) {
        return TEXTURE;
    }
}
