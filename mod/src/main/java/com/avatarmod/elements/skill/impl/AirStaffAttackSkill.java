package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.skill.SkillDefinition;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;

import java.util.List;

/**
 * Air Staff 3-hit combo:
 *   Step 1 — quick forward strike (range 2.0, dmg 3.0, knockback 0.4)
 *   Step 2 — wider sweep (range 2.5, dmg 4.5, knockback 0.6)
 *   Step 3 — heavy upward slam (range 3.0, dmg 7.0, knockback 1.5 upward)
 *
 * Requires holding the air_staff item. Combo resets after comboWindowTicks gap.
 */
public final class AirStaffAttackSkill {

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        SkillTimeline timeline = PlayerBendingData.get(player).getTimeline();
        if (timeline.phase() != SkillTimeline.Phase.ACTIVE) return;
        if (timeline.ticksInPhase() != 1) return;

        int step = PlayerBendingData.get(player).getAirStaffComboStep();
        executeComboStep(player, def, step);
    }

    private static void executeComboStep(ServerPlayerEntity player, SkillDefinition def, int step) {
        ServerWorld world = player.getServerWorld();
        Vec3d origin = player.getPos().add(0, player.getStandingEyeHeight() / 2.0, 0);
        Vec3d look = player.getRotationVec(1.0f);

        float damage;
        double range;
        float knockback;
        boolean upwardSlam = false;

        switch (step) {
            case 2 -> { damage = 4.5f; range = 2.5; knockback = 0.6f; }
            case 3 -> { damage = 7.0f; range = 3.0; knockback = 1.5f; upwardSlam = true; }
            default -> { damage = def.damage(); range = def.range(); knockback = def.knockback(); }
        }

        Vec3d center = origin.add(look.multiply(range * 0.6));
        Box box = Box.of(center, range * 2, range * 2, range * 2);

        List<LivingEntity> targets = world.getEntitiesByClass(
                LivingEntity.class, box,
                e -> e != player && e.isAlive() && e.squaredDistanceTo(center) <= range * range
        );

        DamageSource source = world.getDamageSources().playerAttack(player);
        for (LivingEntity target : targets) {
            target.damage(source, damage);
            Vec3d knockDir = target.getPos().subtract(player.getPos()).normalize();
            double vy = upwardSlam ? knockback * 0.9 : 0.1 + knockback * 0.2;
            target.addVelocity(
                    knockDir.x * knockback * (upwardSlam ? 0.3 : 1.0),
                    vy,
                    knockDir.z * knockback * (upwardSlam ? 0.3 : 1.0)
            );
            target.velocityModified = true;
        }

        // VFX
        int particleCount = 6 + step * 4;
        world.spawnParticles(ParticleTypes.CLOUD,
                center.x, center.y, center.z,
                particleCount, range * 0.3, range * 0.3, range * 0.3, 0.04);
        if (step == 3) {
            world.spawnParticles(ParticleTypes.SWEEP_ATTACK,
                    center.x, center.y, center.z, 3, range * 0.4, 0.2, range * 0.4, 0.0);
        }

        // SFX — higher pitch for final hit
        float pitch = switch (step) { case 2 -> 1.1f; case 3 -> 0.8f; default -> 1.3f; };
        world.playSound(null, player.getBlockPos(),
                SoundEvents.ENTITY_PLAYER_ATTACK_SWEEP,
                SoundCategory.PLAYERS, 0.8f, pitch);
    }

    private AirStaffAttackSkill() {}
}
