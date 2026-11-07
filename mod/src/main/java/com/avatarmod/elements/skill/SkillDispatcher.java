package com.avatarmod.elements.skill;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.skill.impl.FireJabSkill;
import net.minecraft.server.network.ServerPlayerEntity;

/**
 * Called each server tick for every player.
 * Routes to the active skill's tick handler while the timeline is running.
 */
public final class SkillDispatcher {

    public static void tick(ServerPlayerEntity player) {
        PlayerBendingData data = PlayerBendingData.get(player);
        SkillTimeline timeline = data.getTimeline();

        if (timeline.isIdle()) return;

        String activeSkill = data.getActiveSkillId();
        if (activeSkill == null) return;

        SkillRegistry.get(activeSkill).ifPresent(def -> dispatch(player, def));
    }

    private static void dispatch(ServerPlayerEntity player, SkillDefinition def) {
        switch (def.id()) {
            case "avatar:fire_jab" -> FireJabSkill.tick(player, def);
            // T2-2+: add cases here
        }
    }

    private SkillDispatcher() {}
}
