package com.avatarmod.elements.client.render.entity;

import com.avatarmod.elements.client.render.entity.model.FireNationSpearmanEntityModel;
import com.avatarmod.elements.entity.mob.FireNationSpearmanEntity;
import net.minecraft.client.render.entity.EntityRendererFactory;
import net.minecraft.client.render.entity.MobEntityRenderer;
import net.minecraft.util.Identifier;

public class FireNationSpearmanEntityRenderer extends MobEntityRenderer<FireNationSpearmanEntity, FireNationSpearmanEntityModel> {

    private static final Identifier TEXTURE = Identifier.of("avatar_elements", "textures/entity/mobs/fire_nation_spearman.png");

    public FireNationSpearmanEntityRenderer(EntityRendererFactory.Context context) {
        super(context, new FireNationSpearmanEntityModel(context.getPart(FireNationSpearmanEntityModel.LAYER_LOCATION)), 0.5f);
    }

    @Override
    public Identifier getTexture(FireNationSpearmanEntity entity) {
        return TEXTURE;
    }
}
