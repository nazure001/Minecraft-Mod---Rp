package com.avatarmod.elements.client.render.entity;

import com.avatarmod.elements.client.render.entity.model.WingedLemurEntityModel;
import com.avatarmod.elements.entity.pet.WingedLemurEntity;
import net.minecraft.client.render.entity.EntityRendererFactory;
import net.minecraft.client.render.entity.MobEntityRenderer;
import net.minecraft.util.Identifier;

public class WingedLemurEntityRenderer extends MobEntityRenderer<WingedLemurEntity, WingedLemurEntityModel> {

    private static final Identifier TEXTURE = Identifier.of("avatar_elements", "textures/entity/pet/winged_lemur.png");

    public WingedLemurEntityRenderer(EntityRendererFactory.Context context) {
        super(context, new WingedLemurEntityModel(context.getPart(WingedLemurEntityModel.LAYER_LOCATION)), 0.35f);
    }

    @Override
    public Identifier getTexture(WingedLemurEntity entity) {
        return TEXTURE;
    }
}
