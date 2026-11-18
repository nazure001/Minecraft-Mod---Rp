package com.avatarmod.elements.network;

import com.avatarmod.elements.AvatarElementsMod;
import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.skill.ElementSlotMap;
import com.avatarmod.elements.skill.SkillDefinition;
import com.avatarmod.elements.skill.SkillRegistry;
import com.avatarmod.elements.skill.SkillValidator;
import net.fabricmc.fabric.api.networking.v1.PayloadTypeRegistry;
import net.fabricmc.fabric.api.networking.v1.PlayerLookup;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.text.Text;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;

public final class SkillNetworking {

    // Per-skill rate limit: UUID → (skillId → lastTick). Prevents single-skill spam
    // without blocking rapid Z→X cross-skill switching.
    private static final int RATE_LIMIT_TICKS = 3;
    private static final Map<UUID, Map<String, Long>> lastSkillTick = new HashMap<>();

    // castSerial: increments each time a new cast starts for a given player.
    // Sent in every S2CPhaseSync so the client can discard stale IDLE resets.
    private static final Map<UUID, AtomicInteger> castSerials = new HashMap<>();

    // Element cycle cooldown: prevents rapid successive element changes (300ms debounce).
    // Server-side throttle (client has 300ms, server validates too).
    private static final Map<UUID, Integer> elementCycleCooldown = new HashMap<>();
    private static final int ELEMENT_CYCLE_COOLDOWN_TICKS = 6;

    private static int nextSerial(UUID uuid) {
        return castSerials.computeIfAbsent(uuid, k -> new AtomicInteger(0))
                          .incrementAndGet();
    }

    /** Returns the current (most recently issued) serial for this player, or 0. */
    public static int currentSerial(UUID uuid) {
        AtomicInteger ai = castSerials.get(uuid);
        return ai == null ? 0 : ai.get();
    }

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
        PayloadTypeRegistry.playC2S().register(SkillPackets.C2SHoldStart.ID, SkillPackets.C2SHoldStart.CODEC);
        PayloadTypeRegistry.playC2S().register(SkillPackets.C2SHoldRelease.ID, SkillPackets.C2SHoldRelease.CODEC);
        PayloadTypeRegistry.playC2S().register(SkillPackets.C2SCycleElement.ID, SkillPackets.C2SCycleElement.CODEC);
        PayloadTypeRegistry.playC2S().register(SkillPackets.C2SSelectElement.ID, SkillPackets.C2SSelectElement.CODEC);
        PayloadTypeRegistry.playS2C().register(SkillPackets.S2CSkillResult.ID, SkillPackets.S2CSkillResult.CODEC);
        PayloadTypeRegistry.playS2C().register(SkillPackets.S2CHudUpdate.ID, SkillPackets.S2CHudUpdate.CODEC);
        PayloadTypeRegistry.playS2C().register(SkillPackets.S2CSyncElement.ID, SkillPackets.S2CSyncElement.CODEC);
        PayloadTypeRegistry.playS2C().register(SkillPackets.S2CPhaseSync.ID, SkillPackets.S2CPhaseSync.CODEC);
        PayloadTypeRegistry.playS2C().register(SkillPackets.S2CSkillPosition.ID, SkillPackets.S2CSkillPosition.CODEC);
    }

    public static void registerServerReceivers() {
        ServerPlayNetworking.registerGlobalReceiver(
                SkillPackets.C2SSkillInput.ID,
                (payload, context) -> {
                    ServerPlayerEntity player = context.player();
                    String skillId = payload.skillId();

                    if (skillId == null || skillId.isBlank() || skillId.length() > 64) {
                        AvatarElementsMod.LOGGER.warn(
                                "Invalid skillId from {}: '{}'", player.getName().getString(), skillId);
                        return;
                    }

                    executeCastPipeline(player, skillId);
                });

        ServerPlayNetworking.registerGlobalReceiver(
                SkillPackets.C2SHoldStart.ID,
                (payload, context) -> {
                    ServerPlayerEntity player = context.player();
                    handleHoldStart(player, payload.slotIndex());
                });

        ServerPlayNetworking.registerGlobalReceiver(
                SkillPackets.C2SHoldRelease.ID,
                (payload, context) -> {
                    ServerPlayerEntity player = context.player();
                    handleHoldRelease(player, payload.slotIndex(), payload.heldTicks());
                });
    }

    public static void handleHoldStart(ServerPlayerEntity player, int slotIndex) {
        handleHoldStart(player, slotIndex, null);
    }

    public static void handleHoldStart(ServerPlayerEntity player, int slotIndex, String skillId) {
        PlayerBendingData data = PlayerBendingData.get(player);
        if (skillId == null || skillId.isBlank()) {
            if (slotIndex >= 0 && slotIndex < ElementSlotMap.SLOT_COUNT) {
                skillId = ElementSlotMap.getSkillId(data.getActiveElement(), slotIndex);
            }
        }
        if (skillId == null || skillId.isBlank()) return;

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

        SkillDefinition def = SkillRegistry.get(skillId).orElse(null);
        if (def == null) return;

        // Spend chi upfront and start charging timeline without setting cooldown until release
        data.trySpendChi(def.chiCost());
        data.startTimeline(skillId, def.windupTicks(), def.activeTicks(), def.recoveryTicks(),
                def.isHoldRelease(), def.maxChargeTicks());

        int serial = nextSerial(uuid);
        SkillTimeline.Phase initialPhase = data.getTimeline().phase();
        if (initialPhase != SkillTimeline.Phase.IDLE) {
            broadcastPhaseSync(player, skillId, initialPhase.name(), 0, serial);
        }

        handleComboTracking(data, skillId, def, currentTick);

        ServerPlayNetworking.send(player, new SkillPackets.S2CSkillResult(
                skillId, true, SkillPackets.S2CSkillResult.DenyReason.NONE, 0));
        sendHudUpdate(player, data, skillId);
    }

    public static void handleHoldRelease(ServerPlayerEntity player, int slotIndex, int heldTicks) {
        PlayerBendingData data = PlayerBendingData.get(player);
        SkillTimeline timeline = data.getTimeline();

        if (timeline.phase() == SkillTimeline.Phase.HOLD || (timeline.isHoldSkill() && timeline.phase() == SkillTimeline.Phase.WINDUP)) {
            String activeSkill = timeline.skillId();
            timeline.releaseHold();
            SkillDefinition def = SkillRegistry.get(activeSkill).orElse(null);
            if (def != null) {
                data.setCooldown(activeSkill, def.cooldownTicks());
            }
            int serial = currentSerial(player.getUuid());
            broadcastPhaseSync(player, activeSkill, SkillTimeline.Phase.ACTIVE.name(), 0, serial);
            sendHudUpdate(player, data, activeSkill);
        }
    }

    public static void handleHoldRelease(ServerPlayerEntity player, int slotIndex, String skillId) {
        handleHoldRelease(player, slotIndex, 0);
    }

    public static void broadcastPhaseSync(ServerPlayerEntity caster, String skillId,
                                          String phase, int ticksIn, int serial) {
        var packet = new SkillPackets.S2CPhaseSync(caster.getUuid(), skillId, phase, ticksIn, serial);
        ServerPlayNetworking.send(caster, packet);
        for (var watcher : PlayerLookup.tracking(caster)) {
            ServerPlayNetworking.send(watcher, packet);
        }
    }

    public static void broadcastSkillPosition(ServerPlayerEntity caster, String skillId,
                                              int serial, double x, double y, double z) {
        var packet = new SkillPackets.S2CSkillPosition(caster.getUuid(), serial, skillId, x, y, z);
        ServerPlayNetworking.send(caster, packet);
        for (var watcher : PlayerLookup.tracking(caster)) {
            ServerPlayNetworking.send(watcher, packet);
        }
    }

    /** Force-reset orb for this caster on all nearby clients (cancel / death). */
    public static void broadcastOrbReset(ServerPlayerEntity caster) {
        int serial = currentSerial(caster.getUuid());
        PlayerBendingData data = PlayerBendingData.get(caster);
        String skillId = data.getActiveSkillId();
        if (skillId == null) return;
        broadcastPhaseSync(caster, skillId, "IDLE", 0, serial);
    }

    /**
     * Sent to a player who starts tracking a caster mid-cast.
     * Gives them the current phase so they can render the orb without waiting for
     * the next transition packet.
     */
    public static void syncOrbStateToNewWatcher(ServerPlayerEntity watcher,
                                                ServerPlayerEntity caster) {
        PlayerBendingData data = PlayerBendingData.get(caster);
        SkillTimeline timeline = data.getTimeline();
        if (timeline.isIdle()) return;
        String skillId = data.getActiveSkillId();
        if (skillId == null) return;
        int serial = currentSerial(caster.getUuid());
        var packet = new SkillPackets.S2CPhaseSync(
                caster.getUuid(), skillId, timeline.phase().name(),
                timeline.ticksInPhase(), serial);
        ServerPlayNetworking.send(watcher, packet);
    }

    public static void sendHudUpdate(ServerPlayerEntity player, PlayerBendingData data, String skillId) {
        String safeSkillId = skillId != null ? skillId : "";
        int cd = !safeSkillId.isEmpty() ? data.getCooldown(safeSkillId) : 0;
        String element = data.getActiveElement() != null ? data.getActiveElement() : "FIRE";
        ServerPlayNetworking.send(player, new SkillPackets.S2CHudUpdate(
                data.getChi(), data.getMaxChi(), safeSkillId, cd));
        ServerPlayNetworking.send(player, new SkillPackets.S2CSyncElement(element));
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
                    if (skillId == null) return;

                    executeCastPipeline(player, skillId);
                });
    }

    private static void executeCastPipeline(ServerPlayerEntity player, String skillId) {
        long currentTick = player.getServerWorld().getTime();
        UUID uuid = player.getUuid();
        PlayerBendingData data = PlayerBendingData.get(player);

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

        int serial = nextSerial(uuid);
        SkillTimeline.Phase initialPhase = data.getTimeline().phase();
        if (initialPhase != SkillTimeline.Phase.IDLE) {
            broadcastPhaseSync(player, skillId, initialPhase.name(), 0, serial);
        }
        handleComboTracking(data, skillId, def, currentTick);

        AvatarElementsMod.LOGGER.debug(
                "Skill '{}' used by {} (chi: {}/{})",
                skillId, player.getName().getString(),
                data.getChi(), data.getMaxChi());

        ServerPlayNetworking.send(player, new SkillPackets.S2CSkillResult(
                skillId, true, SkillPackets.S2CSkillResult.DenyReason.NONE, 0));
        sendHudUpdate(player, data, skillId);
    }

    // C2SCycleElement: advance the server-authoritative active element with debounce.
    public static void registerCycleElementReceiver() {
        ServerPlayNetworking.registerGlobalReceiver(
                SkillPackets.C2SCycleElement.ID,
                (payload, context) -> {
                    ServerPlayerEntity player = context.player();
                    UUID uuid = player.getUuid();

                    // Server-side debounce: ignore if cooldown active
                    int cooldown = elementCycleCooldown.getOrDefault(uuid, 0);
                    if (cooldown > 0) {
                        // Silently ignore duplicate requests within 300ms
                        return;
                    }

                    PlayerBendingData data = PlayerBendingData.get(player);
                    String element = ElementSlotMap.nextElement(data.getActiveElement());
                    applyElementSelection(player, data, element);
                    elementCycleCooldown.put(uuid, ELEMENT_CYCLE_COOLDOWN_TICKS);
                    player.sendMessage(Text.literal("[Avatar] Element: " + element), true);
                });
    }

    public static void registerSelectElementReceiver() {
        ServerPlayNetworking.registerGlobalReceiver(
                SkillPackets.C2SSelectElement.ID,
                (payload, context) -> {
                    ServerPlayerEntity player = context.player();
                    String element = payload.element();
                    if (!ElementSlotMap.isElement(element)) return;

                    UUID uuid = player.getUuid();
                    if (elementCycleCooldown.getOrDefault(uuid, 0) > 0) return;

                    PlayerBendingData data = PlayerBendingData.get(player);
                    if (element.equals(data.getActiveElement())) {
                        ServerPlayNetworking.send(player, new SkillPackets.S2CSyncElement(element));
                        return;
                    }

                    applyElementSelection(player, data, element);
                    elementCycleCooldown.put(uuid, ELEMENT_CYCLE_COOLDOWN_TICKS);
                });
    }

    private static void applyElementSelection(
            ServerPlayerEntity player, PlayerBendingData data, String element) {
        if (!data.getTimeline().isIdle()) {
            data.getTimeline().cancel();
            broadcastOrbReset(player);
        }
        data.setActiveElement(element);
        ServerPlayNetworking.send(player, new SkillPackets.S2CSyncElement(element));
    }

    /** Tick cooldowns on server (called once per tick). */
    public static void tickElementCycleCooldowns() {
        elementCycleCooldown.entrySet().removeIf(e -> {
            int remaining = e.getValue() - 1;
            if (remaining <= 0) {
                return true; // Remove this entry
            } else {
                e.setValue(remaining);
                return false;
            }
        });
    }

    public static void onPlayerDisconnect(UUID uuid) {
        lastSkillTick.remove(uuid);
        castSerials.remove(uuid);
        elementCycleCooldown.remove(uuid);
        com.avatarmod.elements.skill.impl.EarthBoulderSkill.clear(uuid);
        com.avatarmod.elements.skill.impl.EarthPillarSkill.clear(uuid);
        com.avatarmod.elements.skill.impl.BoulderLaunchSkill.clear(uuid);
        com.avatarmod.elements.skill.impl.FireBlastSkill.clearFireball(uuid);
    }

    private static void handleComboTracking(PlayerBendingData data, String skillId, SkillDefinition def, long currentTick) {
        boolean isCombo = false;
        if ("avatar:fire_jab".equals(skillId)) {
            int partnerWindow = SkillRegistry.get("avatar:flame_sweep").map(SkillDefinition::comboWindowTicks).orElse(8);
            isCombo = "avatar:flame_sweep".equals(data.getLastComboSkillId())
                    && (currentTick <= data.getComboExpiryTick() || (currentTick - data.getLastComboSkillTick()) <= partnerWindow);
        } else if ("avatar:flame_sweep".equals(skillId)) {
            int partnerWindow = SkillRegistry.get("avatar:fire_jab").map(SkillDefinition::comboWindowTicks).orElse(6);
            isCombo = "avatar:fire_jab".equals(data.getLastComboSkillId())
                    && (currentTick <= data.getComboExpiryTick() || (currentTick - data.getLastComboSkillTick()) <= partnerWindow);
        }
        data.setActiveCastCombo(isCombo);

        int totalDurationTicks = def.windupTicks() + def.activeTicks() + def.recoveryTicks();
        data.recordComboCast(skillId, currentTick, totalDurationTicks, def.comboWindowTicks());
        if ("avatar:air_staff_attack".equals(skillId)) {
            data.advanceAirStaffCombo(currentTick, def.comboWindowTicks());
        }
    }

    private SkillNetworking() {}
}
