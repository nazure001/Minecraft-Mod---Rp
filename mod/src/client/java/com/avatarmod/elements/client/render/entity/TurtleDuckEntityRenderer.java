package com.avatarmod.elements.client.render.entity;

import com.avatarmod.elements.client.render.entity.model.TurtleDuckEntityModel;
import com.avatarmod.elements.entity.mob.TurtleDuckEntity;
import net.minecraft.client.render.entity.EntityRendererFactory;
import net.minecraft.client.render.entity.MobEntityRenderer;
import net.minecraft.util.Identifier;

public class TurtleDuckEntityRenderer extends MobEntityRenderer<TurtleDuckEntity, TurtleDuckEntityModel> {

    private static final Identifier TEXTURE = Identifier.of("avatar_elements", "textures/entity/mobs/turtle_duck.png");

    public TurtleDuckEntityRenderer(EntityRendererFactory.Context context) {
        super(context, new TurtleDuckEntityModel(context.getPart(TurtleDuckEntityModel.LAYER_LOCATION)), 0.4f);
    }

    @Override
    public Identifier getTexture(TurtleDuckEntity entity) {
        return TEXTURE;
    }
}
