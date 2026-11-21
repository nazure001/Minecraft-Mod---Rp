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

    // Fabric attachment type — registered once at mod init, copied across player death/respawn
    public static final AttachmentType<PlayerBendingData> ATTACHMENT =
            AttachmentRegistry.<PlayerBendingData>builder()
                    .initializer(PlayerBendingData::new)
                    .copyOnDeath()
                    .buildAndRegister(AvatarElementsMod.id("bending_data"));

    private int chi;
    private final int maxChi;
    private int masteryLevel;
    private final Map<String, Integer> cooldowns; // skillId → ticks remaining
    private SkillTimeline activeTimeline;         // null when no skill in flight
    private final ChiManager chiManager;

    // T2-5 fire combo chain tracking
    private boolean activeCastCombo = false;
    private String lastComboSkillId = null;
    private long lastComboSkillTick = -9999L;
    private long comboExpiryTick = -9999L;

    // T2-6 air staff 3-hit combo
    private int airStaffComboStep = 0;
    private long airStaffLastCastTick = -9999L;

    // Active element selected by player ("NONE" by default until chosen, or "FIRE", "AIR", "WATER", "EARTH", "NON_BENDER")
    private String activeElement = "NONE";

    // Chi Blocking status (inflicted by Non-Bender pressure point strikes)
    private int chiBlockedTicks = 0;

    // Avatar State transcendence status (extended god-tier empowerment)
    private int avatarStateTicks = 0;

    // Creative / Sandbox testing bypass mode (unlimited chi, zero cooldowns, instant mastery)
    private boolean sandboxBypass = false;

    // Defeated elemental mini-bosses tracking (unlocks sub-bending trees in Option A + B)
    private final java.util.Set<String> defeatedBosses = new java.util.HashSet<>();

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

    public boolean isChiBlocked() {
        return chiBlockedTicks > 0;
    }

    public int getChiBlockedTicks() {
        return chiBlockedTicks;
    }

    public void applyChiBlock(int ticks) {
        this.chiBlockedTicks = Math.max(this.chiBlockedTicks, ticks);
        // Instant Chi disruption: lose 30% current chi
        this.chi = Math.max(0, this.chi - (int)(this.chi * 0.30f));
        // Cancel active bending cast immediately
        if (activeTimeline != null) {
            activeTimeline.cancel();
            activeTimeline = null;
        }
    }

    public void clearChiBlock() {
        this.chiBlockedTicks = 0;
    }

    public void drainChi(int amount) {
        this.chi = Math.max(0, this.chi - amount);
    }

    public void setChi(int chi) {
        this.chi = chiManager.clamp(chi, maxChi);
    }

    public boolean trySpendChi(int baseCost) {
        if (isChiBlocked()) return false;
        int actual = chiManager.computeCost(baseCost, chi);
        if (actual < 0) return false;
        chi = chiManager.clamp(chi - actual, maxChi);
        return true;
    }

    public void regenChi(int amount) {
        if (isChiBlocked()) return; // Severed Chi cannot regenerate
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
        startTimeline(skillId, windup, active, recovery, false, 0);
    }

    /** Start a new timeline with hold-release capability; cancels any current one. */
    public void startTimeline(String skillId, int windup, int active, int recovery, boolean isHoldSkill, int maxHoldTicks) {
        activeTimeline = new SkillTimeline(skillId, windup, active, recovery, isHoldSkill, maxHoldTicks);
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
        // Timeline.tick() is called by SkillDispatcher so it can detect phase transitions
        // and broadcast IDLE when the skill completes. We only clean up externally-cancelled timelines here.
        if (activeTimeline != null && activeTimeline.isIdle()) activeTimeline = null;
    }

    /** Called by SkillDispatcher after the timeline reaches IDLE. */
    public void clearTimeline() {
        activeTimeline = null;
    }

    // --- fire combo chain (T2-5) ---

    public boolean isActiveCastCombo() { return activeCastCombo; }
    public void setActiveCastCombo(boolean activeCastCombo) { this.activeCastCombo = activeCastCombo; }

    public void recordComboSkill(String skillId, long tick) {
        lastComboSkillId = skillId;
        lastComboSkillTick = tick;
    }

    public void recordComboCast(String skillId, long currentTick, int totalDurationTicks, int comboWindowTicks) {
        this.lastComboSkillId = skillId;
        this.lastComboSkillTick = currentTick;
        this.comboExpiryTick = currentTick + totalDurationTicks + comboWindowTicks;
    }

    public String getLastComboSkillId() { return lastComboSkillId; }
    public long getLastComboSkillTick() { return lastComboSkillTick; }
    public long getComboExpiryTick() { return comboExpiryTick; }

    // --- air staff combo step (T2-6) ---

    /** Returns 1, 2, or 3 — advances the step if within window, else resets to 1. */
    public int advanceAirStaffCombo(long currentTick, int windowTicks) {
        if (currentTick - airStaffLastCastTick > windowTicks) {
            airStaffComboStep = 0;
        }
        airStaffComboStep = (airStaffComboStep % 3) + 1;
        airStaffLastCastTick = currentTick;
        return airStaffComboStep;
    }
    public int getAirStaffComboStep() { return airStaffComboStep; }

    // --- mastery ---

    public int getMasteryLevel() { return masteryLevel; }
    public void setMasteryLevel(int level) { this.masteryLevel = Math.max(0, Math.min(5, level)); }

    public String getActiveElement() { return activeElement; }
    public void setActiveElement(String element) { this.activeElement = element; }

    public boolean isAvatarStateActive() { return avatarStateTicks > 0; }
    public int getAvatarStateTicks() { return avatarStateTicks; }
    public void enterAvatarState(int durationTicks) { this.avatarStateTicks = Math.max(this.avatarStateTicks, durationTicks); }
    public void exitAvatarState() { this.avatarStateTicks = 0; }

    // --- sandbox / creative testing bypass ---
    public boolean isSandboxBypass() { return sandboxBypass; }
    public void setSandboxBypass(boolean bypass) { this.sandboxBypass = bypass; }
    public void toggleSandboxBypass() { this.sandboxBypass = !this.sandboxBypass; }

    // --- defeated bosses & progression ---
    public boolean hasDefeatedBoss(String bossType) {
        if (sandboxBypass) return true;
        return defeatedBosses.contains(bossType.toUpperCase(java.util.Locale.ROOT));
    }

    public boolean addDefeatedBoss(String bossType) {
        return defeatedBosses.add(bossType.toUpperCase(java.util.Locale.ROOT));
    }

    public java.util.Set<String> getDefeatedBosses() {
        return java.util.Collections.unmodifiableSet(defeatedBosses);
    }

    // --- static helpers ---

    public static PlayerBendingData get(ServerPlayerEntity player) {
        return player.getAttachedOrCreate(ATTACHMENT);
    }

    public static void tick(ServerPlayerEntity player) {
        PlayerBendingData data = get(player);
        data.tickCooldowns();
        data.tickTimeline();
        if (data.chiBlockedTicks > 0) {
            data.chiBlockedTicks--;
        }

        // Active Avatar State: continuous energy surge, swift cooldown recovery & orbital elemental motes
        if (data.avatarStateTicks > 0) {
            data.avatarStateTicks--;
            data.regenChi(5);
            data.tickCooldowns(); // 2x faster cooldown recharge in Avatar State

            long worldTime = player.getServerWorld().getTime();
            if (worldTime % 3 == 0) {
                net.minecraft.server.world.ServerWorld world = player.getServerWorld();
                net.minecraft.util.math.Vec3d pos = player.getPos().add(0, 1.0, 0);
                double theta = (worldTime % 30) * (2 * Math.PI / 30.0);
                double r = 1.35;

                // Fire mote
                world.spawnParticles(net.minecraft.particle.ParticleTypes.FLAME,
                        pos.x + r * Math.cos(theta), pos.y + 0.3 * Math.sin(theta * 2), pos.z + r * Math.sin(theta),
                        1, 0, 0.02, 0, 0.01);
                // Water mote
                world.spawnParticles(net.minecraft.particle.ParticleTypes.SPLASH,
                        pos.x + r * Math.cos(theta + Math.PI * 0.5), pos.y - 0.2, pos.z + r * Math.sin(theta + Math.PI * 0.5),
                        2, 0, 0.02, 0, 0.01);
                // Earth mote
                world.spawnParticles(com.avatarmod.elements.particle.AvatarParticles.STONE_CHIP,
                        pos.x + r * Math.cos(theta + Math.PI), pos.y + 0.2, pos.z + r * Math.sin(theta + Math.PI),
                        1, 0, 0.01, 0, 0.01);
                // Air gust
                world.spawnParticles(com.avatarmod.elements.particle.AvatarParticles.GUST_CURL,
                        pos.x + r * Math.cos(theta + Math.PI * 1.5), pos.y - 0.1, pos.z + r * Math.sin(theta + Math.PI * 1.5),
                        1, 0, 0.02, 0, 0.02);
            }
        }

        long worldTime = player.getServerWorld().getTime();
        if (worldTime % ChiManager.REGEN_INTERVAL == 0) {
            int pulse = data.chiManager.computeRegenPulse(data.chi, data.maxChi);
            data.regenChi(pulse);
        }
    }
}
