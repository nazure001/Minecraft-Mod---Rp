package com.avatarmod.elements.skill;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.network.SkillNetworking;
import com.avatarmod.elements.skill.impl.AirStaffAttackSkill;
import com.avatarmod.elements.skill.impl.AirVortexSkill;
import com.avatarmod.elements.skill.impl.EarthBoulderSkill;
import com.avatarmod.elements.skill.impl.FireGuardSkill;
import com.avatarmod.elements.skill.impl.FireJabSkill;
import com.avatarmod.elements.skill.impl.FireJetSkill;
import com.avatarmod.elements.skill.impl.FlameSweepSkill;
import com.avatarmod.elements.skill.impl.WaterWhipSkill;
import net.minecraft.server.network.ServerPlayerEntity;

/**
 * Called each server tick for every player.
 * Routes to the active skill's tick handler while the timeline is running.
 */
public final class SkillDispatcher {

    public static void tick(ServerPlayerEntity player) {
        PlayerBendingData data = PlayerBendingData.get(player);
        if (!data.hasActiveTimeline()) return;

        String activeSkill = data.getActiveSkillId();
        if (activeSkill == null) return;

        SkillTimeline timeline = data.getActiveTimeline();
        SkillTimeline.Phase phaseBefore = timeline.phase();

        // Advance timeline here (not in PlayerBendingData) so we can detect IDLE transition
        timeline.tick();

        SkillTimeline.Phase phaseAfter = timeline.phase();

        // Dispatch skill effects (hitbox, particles, etc.) — reads post-tick phase/ticksInPhase
        SkillRegistry.get(activeSkill).ifPresent(def -> dispatch(player, def));

        // Broadcast any phase transition, including IDLE when the skill completes naturally
        if (phaseBefore != phaseAfter) {
            int serial = SkillNetworking.currentSerial(player.getUuid());
            SkillNetworking.broadcastPhaseSync(player, activeSkill,
                    phaseAfter.name(), timeline.ticksInPhase(), serial);
        }

        // Clean up idle timeline after broadcasting
        if (timeline.isIdle()) {
            data.clearTimeline();
        }
    }

    private static void dispatch(ServerPlayerEntity player, SkillDefinition def) {
        switch (def.id()) {
            case "avatar:fire_jab"          -> FireJabSkill.tick(player, def);
            case "avatar:flame_sweep"       -> FlameSweepSkill.tick(player, def);
            case "avatar:fire_jet"          -> FireJetSkill.tick(player, def);
            case "avatar:fire_guard"        -> FireGuardSkill.tick(player, def);
            case "avatar:air_staff_attack"  -> AirStaffAttackSkill.tick(player, def);
            case "avatar:air_vortex"        -> AirVortexSkill.tick(player, def);
            case "avatar:water_whip"        -> WaterWhipSkill.tick(player, def);
            case "avatar:earth_boulder"     -> EarthBoulderSkill.tick(player, def);
        }
    }

    private SkillDispatcher() {}
}
