package com.avatarmod.elements.network;

import com.avatarmod.elements.AvatarElementsMod;
import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import net.fabricmc.fabric.api.networking.v1.PayloadTypeRegistry;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.text.Text;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public final class SkillNetworking {

    // Placeholder chi costs until SkillValidator (T1-6) reads from skill_definitions
    private static final Map<String, Integer> TEMP_CHI_COSTS = Map.of(
            "avatar:fire_jab", 8,
            "avatar:flame_sweep", 15,
            "avatar:fire_jet", 25,
            "avatar:fire_guard", 10,
            "avatar:air_palm", 6,
            "avatar:air_blast", 12
    );
    private static final int TEMP_CHI_COST_DEFAULT = 10;

    // Placeholder cooldowns (ticks) — same source as above
    private static final Map<String, Integer> TEMP_COOLDOWNS = Map.of(
            "avatar:fire_jab", 6,
            "avatar:flame_sweep", 12,
            "avatar:fire_jet", 30,
            "avatar:fire_guard", 8,
            "avatar:air_palm", 5,
            "avatar:air_blast", 10
    );
    private static final int TEMP_COOLDOWN_DEFAULT = 10;

    // [windup, active, recovery] — from CONTENT_SPEC.md; replaced by SkillValidator in T1-6
    private record SkillTiming(int windup, int active, int recovery) {}
    private static final Map<String, SkillTiming> TEMP_TIMINGS = Map.of(
            "avatar:fire_jab",    new SkillTiming(2, 3, 4),
            "avatar:flame_sweep", new SkillTiming(3, 8, 6),
            "avatar:fire_jet",    new SkillTiming(1, 1, 10),
            "avatar:fire_guard",  new SkillTiming(2, 60, 5),
            "avatar:air_palm",    new SkillTiming(2, 2, 4),
            "avatar:air_blast",   new SkillTiming(3, 4, 6)
    );
    private static final SkillTiming TEMP_TIMING_DEFAULT = new SkillTiming(2, 3, 4);

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

                    if (skillId == null || skillId.isBlank() || skillId.length() > 64) {
                        AvatarElementsMod.LOGGER.warn(
                                "Invalid skillId from {}: '{}'", player.getName().getString(), skillId);
                        return;
                    }

                    // Anti-spam rate limit
                    long lastTick = lastSkillTick.getOrDefault(uuid, -RATE_LIMIT_TICKS - 1L);
                    if (currentTick - lastTick < RATE_LIMIT_TICKS) {
                        ServerPlayNetworking.send(player, new SkillPackets.S2CSkillResult(
                                skillId, false, SkillPackets.S2CSkillResult.DenyReason.RATE_LIMITED, 0));
                        return;
                    }
                    lastSkillTick.put(uuid, currentTick);

                    PlayerBendingData data = PlayerBendingData.get(player);

                    // Check cooldown
                    if (data.isOnCooldown(skillId)) {
                        int remaining = data.getCooldown(skillId);
                        ServerPlayNetworking.send(player, new SkillPackets.S2CSkillResult(
                                skillId, false, SkillPackets.S2CSkillResult.DenyReason.COOLDOWN, remaining));
                        sendHudUpdate(player, data, skillId);
                        return;
                    }

                    // Check chi
                    int chiCost = TEMP_CHI_COSTS.getOrDefault(skillId, TEMP_CHI_COST_DEFAULT);
                    if (!data.trySpendChi(chiCost)) {
                        ServerPlayNetworking.send(player, new SkillPackets.S2CSkillResult(
                                skillId, false, SkillPackets.S2CSkillResult.DenyReason.NOT_ENOUGH_CHI, 0));
                        sendHudUpdate(player, data, skillId);
                        return;
                    }

                    // Apply cooldown, start timeline, confirm
                    int cooldown = TEMP_COOLDOWNS.getOrDefault(skillId, TEMP_COOLDOWN_DEFAULT);
                    data.setCooldown(skillId, cooldown);

                    SkillTiming timing = TEMP_TIMINGS.getOrDefault(skillId, TEMP_TIMING_DEFAULT);
                    data.startTimeline(skillId, timing.windup(), timing.active(), timing.recovery());

                    AvatarElementsMod.LOGGER.info(
                            "Skill '{}' used by {} (chi: {}/{}, phase: WINDUP→{}t)",
                            skillId, player.getName().getString(),
                            data.getChi(), data.getMaxChi(), timing.windup());

                    player.sendMessage(Text.literal("[Avatar] " + skillId + " — OK"), false);
                    ServerPlayNetworking.send(player, new SkillPackets.S2CSkillResult(
                            skillId, true, SkillPackets.S2CSkillResult.DenyReason.NONE, 0));
                    sendHudUpdate(player, data, skillId);
                });
    }

    private static void sendHudUpdate(ServerPlayerEntity player, PlayerBendingData data, String skillId) {
        ServerPlayNetworking.send(player, new SkillPackets.S2CHudUpdate(
                data.getChi(), data.getMaxChi(), skillId, data.getCooldown(skillId)));
    }

    public static void onPlayerDisconnect(UUID uuid) {
        lastSkillTick.remove(uuid);
    }

    private SkillNetworking() {}
}
