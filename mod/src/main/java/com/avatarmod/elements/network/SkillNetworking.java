package com.avatarmod.elements.network;

import com.avatarmod.elements.AvatarElementsMod;
import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.skill.ElementSlotMap;
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

    // Per-skill rate limit: UUID → (skillId → lastTick). Prevents single-skill spam
    // without blocking rapid Z→X cross-skill switching.
    private static final int RATE_LIMIT_TICKS = 3;
    private static final Map<UUID, Map<String, Long>> lastSkillTick = new HashMap<>();

    private static long getLastTick(UUID uuid, String skillId) {
        Map<String, Long> perSkill = lastSkillTick.get(uuid);
        if (perSkill == null) return -RATE_LIMIT_TICKS - 1L;
        return perSkill.getOrDefault(skillId, -RATE_LIMIT_TICKS - 1L);
    }

    private static void setLastTick(UUID uuid, String skillId, long tick) {
        lastSkillTick.computeIfAbsent(uuid, k -> new HashMap<>()).put(skillId, tick);
    }

    public static void registerPayloads() {
        PayloadTypeRegistry.playC2S().register(SkillPackets.C2SSkillInput.ID, SkillPackets.C2SSkillInput.CODEC);
        PayloadTypeRegistry.playC2S().register(SkillPackets.C2SSlotCast.ID, SkillPackets.C2SSlotCast.CODEC);
        PayloadTypeRegistry.playC2S().register(SkillPackets.C2SSetElement.ID, SkillPackets.C2SSetElement.CODEC);
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

                    // Anti-spam (per-skill: Z→X rapid switch allowed, Z→Z spam blocked)
                    long lastTick = getLastTick(uuid, skillId);
                    if (currentTick - lastTick < RATE_LIMIT_TICKS) {
                        ServerPlayNetworking.send(player, new SkillPackets.S2CSkillResult(
                                skillId, false, SkillPackets.S2CSkillResult.DenyReason.RATE_LIMITED, 0));
                        return;
                    }
                    setLastTick(uuid, skillId, currentTick);

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

                    AvatarElementsMod.LOGGER.debug(
                            "Skill '{}' used by {} (chi: {}/{})",
                            skillId, player.getName().getString(),
                            data.getChi(), data.getMaxChi());

                    ServerPlayNetworking.send(player, new SkillPackets.S2CSkillResult(
                            skillId, true, SkillPackets.S2CSkillResult.DenyReason.NONE, 0));
                    sendHudUpdate(player, data, skillId);
                });
    }

    private static void sendHudUpdate(ServerPlayerEntity player, PlayerBendingData data, String skillId) {
        ServerPlayNetworking.send(player, new SkillPackets.S2CHudUpdate(
                data.getChi(), data.getMaxChi(), skillId, data.getCooldown(skillId)));
    }

    // C2SSlotCast: resolve skillId from server-side element, then run normal pipeline
    public static void registerSlotCastReceiver() {
        ServerPlayNetworking.registerGlobalReceiver(
                SkillPackets.C2SSlotCast.ID,
                (payload, context) -> {
                    ServerPlayerEntity player = context.player();
                    int slot = payload.slotIndex();
                    if (slot < 0 || slot >= ElementSlotMap.SLOT_COUNT) return;

                    PlayerBendingData data = PlayerBendingData.get(player);
                    String element = data.getActiveElement();
                    String skillId = ElementSlotMap.getSkillId(element, slot);
                    if (skillId == null) return; // empty slot — no cast

                    long currentTick = player.getServerWorld().getTime();
                    UUID uuid = player.getUuid();
                    long lastTick = getLastTick(uuid, skillId);
                    if (currentTick - lastTick < RATE_LIMIT_TICKS) {
                        ServerPlayNetworking.send(player, new SkillPackets.S2CSkillResult(
                                skillId, false, SkillPackets.S2CSkillResult.DenyReason.RATE_LIMITED, 0));
                        return;
                    }
                    setLastTick(uuid, skillId, currentTick);

                    SkillValidator.ValidationResult result = SkillValidator.validate(player, skillId);
                    if (!result.allowed()) {
                        ServerPlayNetworking.send(player, new SkillPackets.S2CSkillResult(
                                skillId, false, result.denyReason(), result.cooldownTicks()));
                        sendHudUpdate(player, data, skillId);
                        return;
                    }

                    SkillDefinition def = SkillRegistry.get(skillId).orElseThrow();
                    SkillValidator.apply(player, skillId, def);
                    data.recordComboSkill(skillId, currentTick);
                    if ("avatar:air_staff_attack".equals(skillId)) {
                        data.advanceAirStaffCombo(currentTick, def.comboWindowTicks());
                    }

                    ServerPlayNetworking.send(player, new SkillPackets.S2CSkillResult(
                            skillId, true, SkillPackets.S2CSkillResult.DenyReason.NONE, 0));
                    sendHudUpdate(player, data, skillId);
                });
    }

    // C2SSetElement: update active element for this player
    public static void registerSetElementReceiver() {
        ServerPlayNetworking.registerGlobalReceiver(
                SkillPackets.C2SSetElement.ID,
                (payload, context) -> {
                    ServerPlayerEntity player = context.player();
                    String element = payload.element();
                    // Validate it's a known element
                    for (String known : ElementSlotMap.ELEMENTS) {
                        if (known.equals(element)) {
                            PlayerBendingData.get(player).setActiveElement(element);
                            player.sendMessage(
                                    Text.literal("[Avatar] Element: " + element), true); // action bar
                            return;
                        }
                    }
                });
    }

    public static void onPlayerDisconnect(UUID uuid) {
        lastSkillTick.remove(uuid); // cleans all per-skill entries for this player
    }

    private SkillNetworking() {}
}
