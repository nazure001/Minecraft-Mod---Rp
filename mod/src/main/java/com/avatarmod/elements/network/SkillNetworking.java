package com.avatarmod.elements.network;

import com.avatarmod.elements.AvatarElementsMod;
import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.skill.SkillDefinition;
import com.avatarmod.elements.skill.SkillRegistry;
import com.avatarmod.elements.skill.SkillValidator;
import net.fabricmc.fabric.api.networking.v1.PayloadTypeRegistry;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.text.Text;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public final class SkillNetworking {

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

                    // Anti-spam
                    long lastTick = lastSkillTick.getOrDefault(uuid, -RATE_LIMIT_TICKS - 1L);
                    if (currentTick - lastTick < RATE_LIMIT_TICKS) {
                        ServerPlayNetworking.send(player, new SkillPackets.S2CSkillResult(
                                skillId, false, SkillPackets.S2CSkillResult.DenyReason.RATE_LIMITED, 0));
                        return;
                    }
                    lastSkillTick.put(uuid, currentTick);

                    // Validate
                    SkillValidator.ValidationResult result = SkillValidator.validate(player, skillId);
                    PlayerBendingData data = PlayerBendingData.get(player);

                    if (!result.allowed()) {
                        ServerPlayNetworking.send(player, new SkillPackets.S2CSkillResult(
                                skillId, false, result.denyReason(), result.cooldownTicks()));
                        sendHudUpdate(player, data, skillId);
                        return;
                    }

                    // Apply
                    SkillDefinition def = SkillRegistry.get(skillId).orElseThrow();
                    SkillValidator.apply(player, skillId, def);

                    // Track combo chain state
                    data.recordComboSkill(skillId, currentTick);
                    if ("avatar:air_staff_attack".equals(skillId)) {
                        data.advanceAirStaffCombo(currentTick, def.comboWindowTicks());
                    }

                    AvatarElementsMod.LOGGER.info(
                            "Skill '{}' used by {} (chi: {}/{})",
                            skillId, player.getName().getString(),
                            data.getChi(), data.getMaxChi());

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
