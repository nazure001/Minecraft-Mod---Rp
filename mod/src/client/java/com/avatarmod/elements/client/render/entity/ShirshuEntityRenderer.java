package com.avatarmod.elements.client.render.entity;

import com.avatarmod.elements.client.render.entity.model.ShirshuEntityModel;
import com.avatarmod.elements.entity.mob.ShirshuEntity;
import net.minecraft.client.render.entity.EntityRendererFactory;
import net.minecraft.client.render.entity.MobEntityRenderer;
import net.minecraft.util.Identifier;

public class ShirshuEntityRenderer extends MobEntityRenderer<ShirshuEntity, ShirshuEntityModel> {

    private static final Identifier TEXTURE = Identifier.of("avatar_elements", "textures/entity/mobs/shirshu.png");

    public ShirshuEntityRenderer(EntityRendererFactory.Context context) {
        super(context, new ShirshuEntityModel(context.getPart(ShirshuEntityModel.LAYER_LOCATION)), 1.1f);
    }

    @Override
    public Identifier getTexture(ShirshuEntity entity) {
        return TEXTURE;
    }
}
