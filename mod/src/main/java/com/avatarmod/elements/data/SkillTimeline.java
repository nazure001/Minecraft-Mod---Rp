package com.avatarmod.elements.data;

/**
 * Tracks the phase of a single active skill cast:
 *   WINDUP → (HOLD) → ACTIVE → RECOVERY → IDLE
 *
 * Durations come from CONTENT_SPEC.md; pass them in at construction.
 * Call tick() once per server tick; query phase() / isIdle() as needed.
 */
public final class SkillTimeline {

    public enum Phase { IDLE, WINDUP, HOLD, ACTIVE, RECOVERY }

    /** Shared sentinel returned when no skill is in flight — always IDLE, never mutated. */
    public static final SkillTimeline IDLE_INSTANCE = new SkillTimeline(null, 0, 0, 0);

    private final String skillId;
    private final int windupTicks;
    private final int activeTicks;
    private final int recoveryTicks;
    private final boolean isHoldSkill;
    private final int maxHoldTicks;

    private Phase phase;
    private int ticksInPhase;
    private int holdChargedTicks;

    public SkillTimeline(String skillId, int windupTicks, int activeTicks, int recoveryTicks) {
        this(skillId, windupTicks, activeTicks, recoveryTicks, false, 0);
    }

    public SkillTimeline(String skillId, int windupTicks, int activeTicks, int recoveryTicks,
                         boolean isHoldSkill, int maxHoldTicks) {
        this.skillId = skillId;
        this.windupTicks = windupTicks;
        this.activeTicks = activeTicks;
        this.recoveryTicks = recoveryTicks;
        this.isHoldSkill = isHoldSkill;
        this.maxHoldTicks = maxHoldTicks;
        this.phase = Phase.IDLE;
        this.ticksInPhase = 0;
        this.holdChargedTicks = 0;
    }

    /** Start the timeline from WINDUP or HOLD. No-op if already running. */
    public void start() {
        if (phase != Phase.IDLE) return;
        if (windupTicks > 0) {
            phase = Phase.WINDUP;
        } else if (isHoldSkill) {
            phase = Phase.HOLD;
        } else {
            phase = Phase.ACTIVE;
        }
        ticksInPhase = 0;
        holdChargedTicks = 0;
    }

    /** Advance one server tick. Returns the phase AFTER this tick. */
    public Phase tick() {
        if (phase == Phase.IDLE) return Phase.IDLE;

        ticksInPhase++;

        switch (phase) {
            case WINDUP -> {
                if (ticksInPhase >= windupTicks) {
                    if (isHoldSkill) {
                        phase = Phase.HOLD;
                        ticksInPhase = 0;
                    } else {
                        advance();
                    }
                }
            }
            case HOLD -> {
                int limit = maxHoldTicks > 0 ? maxHoldTicks : 40;
                holdChargedTicks = Math.min(ticksInPhase, limit);
                // Auto-release safety if held twice past max charge (prevents orphaned hold state)
                if (ticksInPhase >= limit * 2) {
                    releaseHold();
                }
            }
            case ACTIVE -> {
                if (ticksInPhase >= activeTicks) advance();
            }
            case RECOVERY -> {
                if (ticksInPhase >= recoveryTicks) {
                    phase = Phase.IDLE;
                    ticksInPhase = 0;
                }
            }
            default -> {}
        }
        return phase;
    }

    private void advance() {
        phase = switch (phase) {
            case WINDUP -> isHoldSkill ? Phase.HOLD : Phase.ACTIVE;
            case HOLD -> Phase.ACTIVE;
            case ACTIVE -> recoveryTicks > 0 ? Phase.RECOVERY : Phase.IDLE;
            default -> Phase.IDLE;
        };
        ticksInPhase = 0;
    }

    /** Releases the hold state, transitioning immediately to ACTIVE phase. */
    public void releaseHold() {
        if (phase == Phase.HOLD) {
            int limit = maxHoldTicks > 0 ? maxHoldTicks : 40;
            holdChargedTicks = Math.max(1, Math.min(ticksInPhase, limit));
            phase = Phase.ACTIVE;
            ticksInPhase = 0;
        } else if (phase == Phase.WINDUP && isHoldSkill) {
            holdChargedTicks = 1;
            phase = Phase.ACTIVE;
            ticksInPhase = 0;
        }
    }

    public Phase phase() { return phase; }
    public String skillId() { return skillId; }
    public boolean isIdle() { return phase == Phase.IDLE; }
    public boolean isActive() { return phase == Phase.ACTIVE; }
    public boolean isHolding() { return phase == Phase.HOLD; }
    public boolean isHoldSkill() { return isHoldSkill; }
    public int ticksInPhase() { return ticksInPhase; }
    public int holdChargedTicks() { return holdChargedTicks; }
    public int chargeTicks() { return holdChargedTicks(); }
    public boolean isCharging() { return isHolding(); }
    public void releaseCharge() { releaseHold(); }

    public static SkillTimeline startCharging(String skillId, int windupTicks, int maxChargeTicks, int recoveryTicks) {
        SkillTimeline tl = new SkillTimeline(skillId, windupTicks, 25, recoveryTicks, true, maxChargeTicks);
        tl.start();
        return tl;
    }

    /** Returns normalized charge ratio in range [0.0, 1.0]. */
    public float getChargeRatio() {
        int limit = maxHoldTicks > 0 ? maxHoldTicks : 40;
        return Math.min(1.0f, (float) Math.max(1, holdChargedTicks) / (float) limit);
    }

    /** Force-cancel (e.g. player takes damage, cancel_on_hit, world transition). */
    public void cancel() {
        phase = Phase.IDLE;
        ticksInPhase = 0;
        holdChargedTicks = 0;
    }
}
