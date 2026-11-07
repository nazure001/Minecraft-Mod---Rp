package com.avatarmod.elements.data;

/**
 * Tracks the phase of a single active skill cast:
 *   WINDUP → ACTIVE → RECOVERY → IDLE
 *
 * Durations come from CONTENT_SPEC.md; pass them in at construction.
 * Call tick() once per server tick; query phase() / isIdle() as needed.
 */
public final class SkillTimeline {

    public enum Phase { IDLE, WINDUP, ACTIVE, RECOVERY }

    /** Shared sentinel returned when no skill is in flight — always IDLE, never mutated. */
    public static final SkillTimeline IDLE_INSTANCE = new SkillTimeline(null, 0, 0, 0);

    private final String skillId;
    private final int windupTicks;
    private final int activeTicks;
    private final int recoveryTicks;

    private Phase phase;
    private int ticksInPhase;

    public SkillTimeline(String skillId, int windupTicks, int activeTicks, int recoveryTicks) {
        this.skillId = skillId;
        this.windupTicks = windupTicks;
        this.activeTicks = activeTicks;
        this.recoveryTicks = recoveryTicks;
        this.phase = Phase.IDLE;
        this.ticksInPhase = 0;
    }

    /** Start the timeline from WINDUP. No-op if already running. */
    public void start() {
        if (phase != Phase.IDLE) return;
        phase = windupTicks > 0 ? Phase.WINDUP : Phase.ACTIVE;
        ticksInPhase = 0;
    }

    /** Advance one server tick. Returns the phase AFTER this tick. */
    public Phase tick() {
        if (phase == Phase.IDLE) return Phase.IDLE;

        ticksInPhase++;

        switch (phase) {
            case WINDUP -> {
                if (ticksInPhase >= windupTicks) advance();
            }
            case ACTIVE -> {
                if (ticksInPhase >= activeTicks) advance();
            }
            case RECOVERY -> {
                if (ticksInPhase >= recoveryTicks) phase = Phase.IDLE;
            }
            default -> {}
        }
        return phase;
    }

    private void advance() {
        phase = switch (phase) {
            case WINDUP -> Phase.ACTIVE;
            case ACTIVE -> recoveryTicks > 0 ? Phase.RECOVERY : Phase.IDLE;
            default -> Phase.IDLE;
        };
        ticksInPhase = 0;
    }

    public Phase phase() { return phase; }
    public String skillId() { return skillId; }
    public boolean isIdle() { return phase == Phase.IDLE; }
    public boolean isActive() { return phase == Phase.ACTIVE; }
    public int ticksInPhase() { return ticksInPhase; }

    /** Force-cancel (e.g. player takes damage, cancel_on_hit). */
    public void cancel() { phase = Phase.IDLE; ticksInPhase = 0; }
}
