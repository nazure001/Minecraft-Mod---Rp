package com.avatarmod.elements.client.render.entity;

import com.avatarmod.elements.client.render.entity.feature.VaatuGlowFeatureRenderer;
import com.avatarmod.elements.client.render.entity.model.VaatuEntityModel;
import com.avatarmod.elements.entity.boss.VaatuSpiritTitanEntity;
import net.minecraft.client.render.entity.EntityRendererFactory;
import net.minecraft.client.render.entity.MobEntityRenderer;
import net.minecraft.util.Identifier;

public class VaatuEntityRenderer extends MobEntityRenderer<VaatuSpiritTitanEntity, VaatuEntityModel> {

    private static final Identifier TEXTURE = Identifier.of("avatar_elements", "textures/entity/boss/vaatu_spirit_titan.png");

    public VaatuEntityRenderer(EntityRendererFactory.Context context) {
        super(context, new VaatuEntityModel(context.getPart(VaatuEntityModel.LAYER_LOCATION)), 2.0f);
        this.addFeature(new VaatuGlowFeatureRenderer(this));
    }

    @Override
    public Identifier getTexture(VaatuSpiritTitanEntity entity) {
        return TEXTURE;
    }
}
