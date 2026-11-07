package com.avatarmod.elements.network;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.skill.SkillDispatcher;
import com.avatarmod.elements.skill.impl.FireGuardSkill;
import net.fabricmc.fabric.api.entity.event.v1.ServerLivingEntityEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerEntityEvents;
import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;
import net.minecraft.entity.EntityType;
import net.minecraft.server.network.ServerPlayerEntity;

public final class AvatarServerEvents {

    public static void register() {
        ServerPlayConnectionEvents.DISCONNECT.register((handler, server) -> {
            AvatarNetworking.onPlayerDisconnect(handler.player.getUuid());
            SkillNetworking.onPlayerDisconnect(handler.player.getUuid());
        });

        // Tick chi regen + cooldowns for every online player each server tick
        ServerEntityEvents.ENTITY_LOAD.register((entity, world) -> {
            // We hook per-tick via ServerTickEvents instead — see below.
        });

        net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents.END_SERVER_TICK.register(server -> {
            for (ServerPlayerEntity player : server.getPlayerManager().getPlayerList()) {
                PlayerBendingData.tick(player);
                SkillDispatcher.tick(player);
            }
        });

        SkillNetworking.registerSlotCastReceiver();
        SkillNetworking.registerSetElementReceiver();

        // T2-4: Fire Guard — block incoming damage while guard is ACTIVE
        ServerLivingEntityEvents.ALLOW_DAMAGE.register((entity, source, amount) -> {
            if (!(entity instanceof ServerPlayerEntity player)) return true;
            return !FireGuardSkill.shouldBlockDamage(player, source);
        });
    }

    private AvatarServerEvents() {}
}
