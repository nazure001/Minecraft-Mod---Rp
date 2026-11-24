package com.avatarmod.elements.client.render.entity;

import com.avatarmod.elements.client.render.entity.model.FlyingBisonEntityModel;
import com.avatarmod.elements.entity.pet.FlyingBisonEntity;
import net.minecraft.client.render.entity.EntityRendererFactory;
import net.minecraft.client.render.entity.MobEntityRenderer;
import net.minecraft.util.Identifier;

public class FlyingBisonEntityRenderer extends MobEntityRenderer<FlyingBisonEntity, FlyingBisonEntityModel> {

    private static final Identifier TEXTURE = Identifier.of("avatar_elements", "textures/entity/pet/flying_bison.png");

    public FlyingBisonEntityRenderer(EntityRendererFactory.Context context) {
        super(context, new FlyingBisonEntityModel(context.getPart(FlyingBisonEntityModel.LAYER_LOCATION)), 2.2f);
    }

    @Override
    public Identifier getTexture(FlyingBisonEntity entity) {
        return TEXTURE;
    }
}
