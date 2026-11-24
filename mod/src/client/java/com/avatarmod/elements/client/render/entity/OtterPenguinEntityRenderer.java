package com.avatarmod.elements.client.render.entity;

import com.avatarmod.elements.client.render.entity.model.OtterPenguinEntityModel;
import com.avatarmod.elements.entity.mob.OtterPenguinEntity;
import net.minecraft.client.render.entity.EntityRendererFactory;
import net.minecraft.client.render.entity.MobEntityRenderer;
import net.minecraft.util.Identifier;

public class OtterPenguinEntityRenderer extends MobEntityRenderer<OtterPenguinEntity, OtterPenguinEntityModel> {

    private static final Identifier TEXTURE = Identifier.of("avatar_elements", "textures/entity/mobs/otter_penguin.png");

    public OtterPenguinEntityRenderer(EntityRendererFactory.Context context) {
        super(context, new OtterPenguinEntityModel(context.getPart(OtterPenguinEntityModel.LAYER_LOCATION)), 0.5f);
    }

    @Override
    public Identifier getTexture(OtterPenguinEntity entity) {
        return TEXTURE;
    }
}
