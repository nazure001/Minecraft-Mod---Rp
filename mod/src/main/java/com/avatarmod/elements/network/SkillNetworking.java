package com.avatarmod.elements.network;

import com.avatarmod.elements.AvatarElementsMod;
import net.fabricmc.fabric.api.networking.v1.PayloadTypeRegistry;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.text.Text;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public final class SkillNetworking {

    // Minimum ticks between any C2SSkillInput from one player (anti-spam)
    private static final int RATE_LIMIT_TICKS = 5;
    private static final Map<UUID, Long> lastSkillTick = new HashMap<>();

    public static void registerPayloads() {
        PayloadTypeRegistry.playC2S().register(SkillPackets.C2SSkillInput.ID, SkillPackets.C2SSkillInput.CODEC);
        PayloadTypeRegistry.playS2C().register(SkillPackets.S2CSkillResult.ID, SkillPackets.S2CSkillResult.CODEC);
        PayloadTypeRegistry.playS2C().register(SkillPackets.S2CHudUpdate.ID, SkillPackets.S2CHudUpdate.CODEC);
    }

    public static void registerServerReceivers() {
        ServerPlayNetworking.registerGlobalReceiver(
                SkillPackets.C2SSkillInput.ID,
                (payload, context) -> {
                    ServerPlayerEntity player = context.player();
                    long currentTick = player.getServerWorld().getTime();
                    UUID uuid = player.getUuid();
                    String skillId = payload.skillId();

                    // Sanitize: reject unknown / oversized skill IDs before any processing
                    if (skillId == null || skillId.isBlank() || skillId.length() > 64) {
                        AvatarElementsMod.LOGGER.warn(
                                "Invalid skillId from {}: '{}'", player.getName().getString(), skillId);
                        return;
                    }

                    // Rate limiting
                    long lastTick = lastSkillTick.getOrDefault(uuid, -RATE_LIMIT_TICKS - 1L);
                    if (currentTick - lastTick < RATE_LIMIT_TICKS) {
                        ServerPlayNetworking.send(player, new SkillPackets.S2CSkillResult(
                                skillId, false,
                                SkillPackets.S2CSkillResult.DenyReason.RATE_LIMITED, 0));
                        return;
                    }
                    lastSkillTick.put(uuid, currentTick);

                    AvatarElementsMod.LOGGER.info(
                            "Skill input '{}' from {}", skillId, player.getName().getString());

                    // Placeholder validation — real SkillValidator comes in T1-6.
                    // For now: always allow, echo back success + mock HUD values.
                    player.sendMessage(
                            Text.literal("[Avatar] Skill: " + skillId + " — acknowledged."), false);

                    ServerPlayNetworking.send(player, new SkillPackets.S2CSkillResult(
                            skillId, true, SkillPackets.S2CSkillResult.DenyReason.NONE, 0));

                    // Send a mock HUD update so the client pipeline can be verified.
                    ServerPlayNetworking.send(player, new SkillPackets.S2CHudUpdate(
                            80, 100, skillId, 10));
                });
    }

    public static void onPlayerDisconnect(UUID uuid) {
        lastSkillTick.remove(uuid);
    }

    private SkillNetworking() {}
}
