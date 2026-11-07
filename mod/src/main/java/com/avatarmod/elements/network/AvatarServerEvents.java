package com.avatarmod.elements.network;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.skill.SkillDispatcher;
import com.avatarmod.elements.skill.impl.FireGuardSkill;
import net.fabricmc.fabric.api.entity.event.v1.ServerLivingEntityEvents;
import net.fabricmc.fabric.api.entity.event.v1.ServerPlayerEvents;
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

        // Reset orb on player death; cancel active skill timeline first
        ServerLivingEntityEvents.ALLOW_DAMAGE.register((entity, source, amount) -> {
            if (!(entity instanceof ServerPlayerEntity player)) return true;
            return !FireGuardSkill.shouldBlockDamage(player, source);
        });

        ServerPlayerEvents.AFTER_RESPAWN.register((oldPlayer, newPlayer, alive) -> {
            // Cancel any in-flight skill and broadcast IDLE so orbs clear on all clients
            PlayerBendingData data = PlayerBendingData.get(newPlayer);
            if (!data.getTimeline().isIdle()) {
                data.getTimeline().cancel();
                SkillNetworking.broadcastOrbReset(newPlayer);
            }
        });

        // A player who starts tracking a caster mid-cast receives current phase immediately
        ServerPlayConnectionEvents.JOIN.register((handler, sender, server) -> {
            ServerPlayerEntity joining = handler.player;
            for (ServerPlayerEntity other : server.getPlayerManager().getPlayerList()) {
                if (other == joining) continue;
                SkillNetworking.syncOrbStateToNewWatcher(joining, other);
            }
        });
    }

    private AvatarServerEvents() {}
}
