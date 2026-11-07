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

/** ARC 180° sweep — fires damage on first tick of each ACTIVE sub-window (ticks 1, 4, 7). */
public final class FlameSweepSkill {

    private static final float COMBO_DAMAGE_BONUS = 1.3f;
    // fire_jab comboWindowTicks = 6
    private static final int FIRE_JAB_COMBO_WINDOW = 6;

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        PlayerBendingData data = PlayerBendingData.get(player);
        SkillTimeline timeline = data.getTimeline();

        if (timeline.phase() != SkillTimeline.Phase.ACTIVE) return;
        // Fire on ticks 1, 4, 7 — spread hits through the sweep arc
        int t = timeline.ticksInPhase();
        if (t != 1 && t != 4 && t != 7) return;

        boolean isCombo = isFireJabCombo(data, player.getServerWorld().getTime());
        executeArc(player, def, isCombo ? COMBO_DAMAGE_BONUS : 1.0f);
    }

    private static boolean isFireJabCombo(PlayerBendingData data, long currentTick) {
        return "avatar:fire_jab".equals(data.getLastComboSkillId())
                && (currentTick - data.getLastComboSkillTick()) <= FIRE_JAB_COMBO_WINDOW;
    }

    private static void executeArc(ServerPlayerEntity player, SkillDefinition def, float damageMultiplier) {
        ServerWorld world = player.getServerWorld();
        Vec3d origin = player.getPos().add(0, player.getStandingEyeHeight() / 2.0, 0);
        Vec3d look = player.getRotationVec(1.0f);
        double r = def.range();

        Box box = Box.of(origin, r * 2, r * 2, r * 2);
        List<LivingEntity> targets = world.getEntitiesByClass(
                LivingEntity.class, box,
                e -> {
                    if (e == player || !e.isAlive()) return false;
                    Vec3d toTarget = e.getPos().subtract(origin);
                    double dist = toTarget.length();
                    if (dist > r) return false;
                    // 180° arc: dot product with look direction > 0
                    return toTarget.normalize().dotProduct(look) > 0;
                }
        );

        DamageSource source = world.getDamageSources().playerAttack(player);
        for (LivingEntity target : targets) {
            target.damage(source, def.damage() * damageMultiplier);
            Vec3d knockDir = target.getPos().subtract(player.getPos()).normalize();
            target.addVelocity(
                    knockDir.x * def.knockback(),
                    0.08 + def.knockback() * 0.2,
                    knockDir.z * def.knockback()
            );
            target.velocityModified = true;
        }

        // VFX: arc of fire particles
        for (int i = -3; i <= 3; i++) {
            double angle = Math.toRadians(i * 25);
            double cos = Math.cos(angle), sin = Math.sin(angle);
            double px = origin.x + (look.x * cos - look.z * sin) * r * 0.8;
            double pz = origin.z + (look.x * sin + look.z * cos) * r * 0.8;
            world.spawnParticles(ParticleTypes.FLAME, px, origin.y, pz, 3, 0.15, 0.2, 0.15, 0.04);
        }
        world.spawnParticles(ParticleTypes.LAVA, origin.x, origin.y, origin.z, 2, 0.3, 0.1, 0.3, 0.0);

        // SFX
        world.playSound(null, player.getBlockPos(),
                SoundEvents.ITEM_FIRECHARGE_USE,
                SoundCategory.PLAYERS, 0.8f, 0.9f);
    }

    private FlameSweepSkill() {}
}
