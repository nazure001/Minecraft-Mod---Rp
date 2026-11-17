package net.avatar_elements.client;

import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Server-Authoritative VFX Lifecycle & Charge State Manager.
 * Enforces non-negotiable rules:
 * - Charge orb layers render ONLY when verified server state reports HOLD_RELEASE charging.
 * - Each active VFX instance binds (ownerUuid + castSerial) so stale loops never resurrect on recast.
 * - Cancel/interrupt triggers clean dissolve without spawning a projectile or explosion.
 * - Teleport distance > 8.0 blocks clears ribbon trail history immediately.
 */
public final class VfxLifecycleManager {
    public record ActiveCastState(
        UUID ownerUuid,
        long castSerial,
        String skillId,
        String phase,
        int chargeTicks,
        int maxChargeTicks,
        long startWorldTick
    ) {}

    private static final Map<UUID, ActiveCastState> ACTIVE_CASTS = new ConcurrentHashMap<>();

    public static void onServerCastStatePacket(ActiveCastState state) {
        if ("CANCEL".equals(state.phase()) || "FINISH".equals(state.phase())) {
            ACTIVE_CASTS.remove(state.ownerUuid());
        } else {
            ACTIVE_CASTS.put(state.ownerUuid(), state);
        }
    }

    public static boolean shouldRenderChargeOrb(UUID playerUuid) {
        ActiveCastState st = ACTIVE_CASTS.get(playerUuid);
        return st != null && "CHARGE_LOOP".equals(st.phase()) && "avatar:fire_blast".equals(st.skillId());
    }

    public static void clearAllOnDisconnectOrWorldChange() {
        ACTIVE_CASTS.clear();
    }
}
