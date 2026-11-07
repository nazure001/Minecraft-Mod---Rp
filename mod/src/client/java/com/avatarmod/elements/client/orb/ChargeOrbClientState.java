package com.avatarmod.elements.client.orb;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/**
 * Client-side state for charge orbs.
 * Updated via S2CPhaseSync packets; queried by ChargeOrbRenderer.
 *
 * Packet frequency: sent only on phase transitions, NOT every tick.
 * Renderers use receivedAtMs + (ticksIn * 50ms) to interpolate the orb
 * size without needing a continuous packet stream.
 *
 * castSerial: monotonically increasing per caster. A stale IDLE packet
 * from a previous cast (lower serial) is ignored so it cannot accidentally
 * clear a visual for a newer cast that started immediately after.
 */
public final class ChargeOrbClientState {

    public record OrbState(String skillId, String phase, int ticksIn,
                           int castSerial, long receivedAtMs) {
        /** Effective ticksIn, linearly interpolated from receive time. */
        public float interpolatedTicks() {
            long elapsed = System.currentTimeMillis() - receivedAtMs;
            return ticksIn + elapsed / 50f; // 50 ms per tick
        }

        public boolean isVisible() {
            return OrbVisualConfig.shouldShow(skillId, phase);
        }
    }

    // UUID → current orb state; entries removed when phase → IDLE
    private static final Map<UUID, OrbState> states = new HashMap<>();

    public static void update(UUID casterUuid, String skillId,
                               String phase, int ticksIn, int castSerial) {
        OrbState current = states.get(casterUuid);

        // Drop stale resets: an IDLE packet from an older cast cannot clear a newer one
        if ("IDLE".equals(phase)) {
            if (current != null && current.castSerial() > castSerial) return;
            states.remove(casterUuid);
            return;
        }

        // Ignore packets from an older cast that arrived out of order
        if (current != null && current.castSerial() > castSerial) return;

        states.put(casterUuid, new OrbState(skillId, phase, ticksIn,
                castSerial, System.currentTimeMillis()));
    }

    /** Returns null if no visible orb for this player. */
    public static OrbState get(UUID casterUuid) {
        return states.get(casterUuid);
    }

    public static Map<UUID, OrbState> all() {
        return states;
    }

    /** Call on disconnect, world change, or screen reload. */
    public static void clear() {
        states.clear();
    }

    private ChargeOrbClientState() {}
}
