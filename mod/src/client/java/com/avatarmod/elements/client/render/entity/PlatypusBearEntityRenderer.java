package com.avatarmod.elements.client.render.entity;

import com.avatarmod.elements.client.render.entity.model.PlatypusBearEntityModel;
import com.avatarmod.elements.entity.mob.PlatypusBearEntity;
import net.minecraft.client.render.entity.EntityRendererFactory;
import net.minecraft.client.render.entity.MobEntityRenderer;
import net.minecraft.util.Identifier;

public class PlatypusBearEntityRenderer extends MobEntityRenderer<PlatypusBearEntity, PlatypusBearEntityModel> {

    private static final Identifier TEXTURE = Identifier.of("avatar_elements", "textures/entity/mobs/platypus_bear.png");

    public PlatypusBearEntityRenderer(EntityRendererFactory.Context context) {
        super(context, new PlatypusBearEntityModel(context.getPart(PlatypusBearEntityModel.LAYER_LOCATION)), 1.3f);
    }

    @Override
    public Identifier getTexture(PlatypusBearEntity entity) {
        return TEXTURE;
    }
}
