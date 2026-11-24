package com.avatarmod.elements.client.render.entity;

import com.avatarmod.elements.client.render.entity.model.DaiLiAgentEntityModel;
import com.avatarmod.elements.entity.mob.DaiLiAgentEntity;
import net.minecraft.client.render.entity.EntityRendererFactory;
import net.minecraft.client.render.entity.MobEntityRenderer;
import net.minecraft.util.Identifier;

public class DaiLiAgentEntityRenderer extends MobEntityRenderer<DaiLiAgentEntity, DaiLiAgentEntityModel> {

    private static final Identifier TEXTURE = Identifier.of("avatar_elements", "textures/entity/mobs/dai_li_agent.png");

    public DaiLiAgentEntityRenderer(EntityRendererFactory.Context context) {
        super(context, new DaiLiAgentEntityModel(context.getPart(DaiLiAgentEntityModel.LAYER_LOCATION)), 0.5f);
    }

    @Override
    public Identifier getTexture(DaiLiAgentEntity entity) {
        return TEXTURE;
    }
}
