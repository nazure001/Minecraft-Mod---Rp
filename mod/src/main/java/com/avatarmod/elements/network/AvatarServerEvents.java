package com.avatarmod.elements.network;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.skill.SkillDispatcher;
import com.avatarmod.elements.skill.impl.FireBlastSkill;
import com.avatarmod.elements.skill.impl.FireGuardSkill;
import net.fabricmc.fabric.api.entity.event.v1.ServerEntityWorldChangeEvents;
import net.fabricmc.fabric.api.entity.event.v1.ServerLivingEntityEvents;
import net.fabricmc.fabric.api.entity.event.v1.ServerPlayerEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerEntityEvents;
import net.fabricmc.fabric.api.networking.v1.EntityTrackingEvents;
import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;
import net.minecraft.entity.EntityType;
import net.minecraft.server.network.ServerPlayerEntity;

public final class AvatarServerEvents {

    public static void register() {
        ServerPlayConnectionEvents.JOIN.register((handler, sender, server) -> {
            ServerPlayerEntity player = handler.player;
            PlayerBendingData data = PlayerBendingData.get(player);
            SkillNetworking.sendHudUpdate(player, data, data.getActiveSkillId());
        });

        ServerPlayConnectionEvents.DISCONNECT.register((handler, server) -> {
            AvatarNetworking.onPlayerDisconnect(handler.player.getUuid());
            SkillNetworking.onPlayerDisconnect(handler.player.getUuid());
            FireBlastSkill.clearFireball(handler.player.getUuid());
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
            FireBlastSkill.tickAllFireballs(server);
            SkillNetworking.tickElementCycleCooldowns();
        });

        SkillNetworking.registerSlotCastReceiver();
        SkillNetworking.registerCycleElementReceiver();
        SkillNetworking.registerSelectElementReceiver();

        // Reset orb on player death; cancel active skill timeline first
        ServerLivingEntityEvents.ALLOW_DAMAGE.register((entity, source, amount) -> {
            if (!(entity instanceof ServerPlayerEntity player)) return true;
            return !FireGuardSkill.shouldBlockDamage(player, source);
        });

        ServerPlayerEvents.AFTER_RESPAWN.register((oldPlayer, newPlayer, alive) -> {
            FireBlastSkill.clearFireball(newPlayer.getUuid());
            // Cancel any in-flight skill and broadcast IDLE so orbs clear on all clients
            PlayerBendingData data = PlayerBendingData.get(newPlayer);
            if (!data.getTimeline().isIdle()) {
                data.getTimeline().cancel();
                SkillNetworking.broadcastOrbReset(newPlayer);
            }
            SkillNetworking.sendHudUpdate(newPlayer, data, data.getActiveSkillId());
        });

        // Cancel in-flight skill timelines and broadcast orb reset on dimension/world switch
        ServerEntityWorldChangeEvents.AFTER_PLAYER_CHANGE_WORLD.register((player, origin, destination) -> {
            FireBlastSkill.clearFireball(player.getUuid());
            PlayerBendingData data = PlayerBendingData.get(player);
            if (!data.getTimeline().isIdle()) {
                data.getTimeline().cancel();
                SkillNetworking.broadcastOrbReset(player);
            }
        });

        // A player who starts tracking a caster mid-cast receives current phase immediately
        EntityTrackingEvents.START_TRACKING.register((trackedEntity, trackingPlayer) -> {
            if (trackedEntity instanceof ServerPlayerEntity otherPlayer) {
                SkillNetworking.syncOrbStateToNewWatcher(trackingPlayer, otherPlayer);
            }
        });

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
