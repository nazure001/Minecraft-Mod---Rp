package com.avatarmod.elements.skill;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CastAnimationGateTest {

    @Test
    void startsOnlyOnceForEachCastSerial() {
        CastAnimationGate gate = new CastAnimationGate();
        UUID caster = UUID.randomUUID();

        assertTrue(gate.shouldStart(caster, 1, "WINDUP"));
        assertFalse(gate.shouldStart(caster, 1, "ACTIVE"));
        assertFalse(gate.shouldStart(caster, 1, "RECOVERY"));
        assertTrue(gate.shouldStart(caster, 2, "ACTIVE"));
    }

    @Test
    void startsHoldAndTracksCastersIndependently() {
        CastAnimationGate gate = new CastAnimationGate();
        UUID firstCaster = UUID.randomUUID();
        UUID secondCaster = UUID.randomUUID();

        assertTrue(gate.shouldStart(firstCaster, 1, "HOLD"));
        assertFalse(gate.shouldStart(firstCaster, 1, "ACTIVE"));
        assertTrue(gate.shouldStart(secondCaster, 1, "WINDUP"));
    }

    @Test
    void ignoresIdleInvalidAndStalePhaseUpdates() {
        CastAnimationGate gate = new CastAnimationGate();
        UUID caster = UUID.randomUUID();

        assertFalse(gate.shouldStart(caster, 1, "IDLE"));
        assertFalse(gate.shouldStart(caster, 0, "WINDUP"));
        assertTrue(gate.shouldStart(caster, 2, "ACTIVE"));
        assertFalse(gate.shouldStart(caster, 1, "WINDUP"));
    }

    @Test
    void clearAllowsAReconnectedSessionToReuseSerials() {
        CastAnimationGate gate = new CastAnimationGate();
        UUID caster = UUID.randomUUID();

        assertTrue(gate.shouldStart(caster, 1, "WINDUP"));
        gate.clear();
        assertTrue(gate.shouldStart(caster, 1, "WINDUP"));
    }
}
