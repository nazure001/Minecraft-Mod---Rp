package com.avatarmod.elements.skill;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public final class CastAnimationGate {

    private final Map<UUID, Integer> lastAnimationSerialByCaster = new HashMap<>();

    public boolean shouldStart(UUID casterUuid, int castSerial, String phase) {
        if (casterUuid == null || castSerial <= 0 || !isStartPhase(phase)) {
            return false;
        }

        Integer lastSerial = lastAnimationSerialByCaster.get(casterUuid);
        if (lastSerial != null && castSerial <= lastSerial) {
            return false;
        }

        lastAnimationSerialByCaster.put(casterUuid, castSerial);
        return true;
    }

    public void clear() {
        lastAnimationSerialByCaster.clear();
    }

    private static boolean isStartPhase(String phase) {
        return "WINDUP".equals(phase) || "HOLD".equals(phase) || "ACTIVE".equals(phase);
    }
}
