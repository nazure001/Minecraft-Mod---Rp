package com.avatarmod.elements.data;

import com.avatarmod.elements.AvatarElementsMod;
import net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;
import net.minecraft.server.network.ServerPlayerEntity;

import java.util.HashMap;
import java.util.Map;

/**
 * Per-player bending state: chi pool, per-skill cooldowns, mastery level.
 * Stored via Fabric AttachmentType on ServerPlayerEntity.
 * Not persistent across sessions yet — persistence added in T1-9 (config/data layer).
 */
public final class PlayerBendingData {

    public static final int MAX_CHI_DEFAULT = ChiManager.BASE_MAX_CHI;

    // Fabric attachment type — registered once at mod init
    public static final AttachmentType<PlayerBendingData> ATTACHMENT =
            AttachmentRegistry.createDefaulted(
                    AvatarElementsMod.id("bending_data"),
                    PlayerBendingData::new
            );

    private int chi;
    private final int maxChi;
    private int masteryLevel;
    private final Map<String, Integer> cooldowns; // skillId → ticks remaining
    private SkillTimeline activeTimeline;         // null when no skill in flight
    private final ChiManager chiManager;

    public PlayerBendingData() {
        this.chi = MAX_CHI_DEFAULT;
        this.maxChi = MAX_CHI_DEFAULT;
        this.masteryLevel = 0;
        this.cooldowns = new HashMap<>();
        this.activeTimeline = null;
        this.chiManager = new ChiManager();
    }

    public ChiManager getChiManager() { return chiManager; }

    // --- chi ---

    public int getChi() { return chi; }
    public int getMaxChi() { return maxChi; }

    public boolean trySpendChi(int baseCost) {
        int actual = chiManager.computeCost(baseCost, chi);
        if (actual < 0) return false;
        chi = chiManager.clamp(chi - actual, maxChi);
        return true;
    }

    public void regenChi(int amount) {
        chi = chiManager.clamp(chi + amount, maxChi);
    }

    // --- cooldowns ---

    public int getCooldown(String skillId) {
        return cooldowns.getOrDefault(skillId, 0);
    }

    public boolean isOnCooldown(String skillId) {
        return getCooldown(skillId) > 0;
    }

    public void setCooldown(String skillId, int ticks) {
        if (ticks <= 0) cooldowns.remove(skillId);
        else cooldowns.put(skillId, ticks);
    }

    /** Call once per server tick to decrement all cooldowns. */
    public void tickCooldowns() {
        cooldowns.replaceAll((id, ticks) -> ticks - 1);
        cooldowns.entrySet().removeIf(e -> e.getValue() <= 0);
    }

    // --- timeline ---

    /** Start a new timeline; cancels any current one. */
    public void startTimeline(String skillId, int windup, int active, int recovery) {
        activeTimeline = new SkillTimeline(skillId, windup, active, recovery);
        activeTimeline.start();
    }

    public SkillTimeline getActiveTimeline() { return activeTimeline; }

    /** Returns the shared idle-safe timeline (never null). */
    public SkillTimeline getTimeline() {
        return activeTimeline != null ? activeTimeline : SkillTimeline.IDLE_INSTANCE;
    }

    public String getActiveSkillId() {
        return activeTimeline != null ? activeTimeline.skillId() : null;
    }

    public boolean hasActiveTimeline() {
        return activeTimeline != null && !activeTimeline.isIdle();
    }

    private void tickTimeline() {
        if (activeTimeline != null) {
            activeTimeline.tick();
            if (activeTimeline.isIdle()) activeTimeline = null;
        }
    }

    // --- mastery ---

    public int getMasteryLevel() { return masteryLevel; }
    public void setMasteryLevel(int level) { this.masteryLevel = Math.max(0, Math.min(5, level)); }

    // --- static helpers ---

    public static PlayerBendingData get(ServerPlayerEntity player) {
        return player.getAttachedOrCreate(ATTACHMENT);
    }

    public static void tick(ServerPlayerEntity player) {
        PlayerBendingData data = get(player);
        data.tickCooldowns();
        data.tickTimeline();
        long worldTime = player.getServerWorld().getTime();
        if (worldTime % ChiManager.REGEN_INTERVAL == 0) {
            int pulse = data.chiManager.computeRegenPulse(data.chi, data.maxChi);
            data.chi += pulse;
        }
    }
}
