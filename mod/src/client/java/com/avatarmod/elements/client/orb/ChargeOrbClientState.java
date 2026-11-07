package com.avatarmod.elements.client.orb;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/**
 * Client-side state for charge orbs.
 * Updated via S2CPhaseSync packets; queried by ChargeOrbRenderer.
 */
public final class ChargeOrbClientState {

    public record OrbState(String skillId, String phase, int ticksIn) {
        public boolean isVisible() {
            return "WINDUP".equals(phase) || "ACTIVE".equals(phase);
        }
    }

    private static final Map<UUID, OrbState> states = new HashMap<>();

    public static void update(UUID casterUuid, String skillId, String phase, int ticksIn) {
        if ("IDLE".equals(phase)) {
            states.remove(casterUuid);
        } else {
            states.put(casterUuid, new OrbState(skillId, phase, ticksIn));
        }
    }

    /** Returns null if no visible orb for this player. */
    public static OrbState get(UUID casterUuid) {
        return states.get(casterUuid);
    }

    public static Map<UUID, OrbState> all() {
        return states;
    }

    public static void clear() {
        states.clear();
    }

    private ChargeOrbClientState() {}
}
