package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.particle.AvatarParticles;
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

        // Slight forward lunge
        Vec3d lunge = look.multiply(0.25);
        player.addVelocity(lunge.x, 0.05, lunge.z);
        player.velocityModified = true;

        // Volumetric 180° Curved Shaolin Flame Slash (11-point parabolic sweep)
        double horizLen = Math.sqrt(look.x * look.x + look.z * look.z);
        Vec3d right = horizLen > 1e-5
                ? new Vec3d(-look.z / horizLen, 0.0, look.x / horizLen)
                : new Vec3d(1.0, 0.0, 0.0);
        Vec3d upVec = right.crossProduct(look).normalize();

        double[][] arcPoints = {
                {-2.20, -0.20, 2.00},
                {-1.80, -0.10, 2.60},
                {-1.40,  0.00, 3.30},
                {-0.90,  0.10, 4.00},
                {-0.40,  0.20, 4.70},
                { 0.00,  0.25, 5.20},
                { 0.40,  0.20, 4.70},
                { 0.90,  0.10, 4.00},
                { 1.40,  0.00, 3.30},
                { 1.80, -0.10, 2.60},
                { 2.20, -0.20, 2.00}
        };

        for (double[] pt : arcPoints) {
            Vec3d worldPt = origin.add(right.multiply(-pt[0]))
                    .add(upVec.multiply(pt[1]))
                    .add(look.multiply(pt[2] * (r / 5.2)));

            world.spawnParticles(ParticleTypes.FLAME, worldPt.x, worldPt.y, worldPt.z, 8, 0.15, 0.15, 0.15, 0.04);
            world.spawnParticles(ParticleTypes.SMALL_FLAME, worldPt.x, worldPt.y, worldPt.z, 5, 0.10, 0.10, 0.10, 0.02);
            world.spawnParticles(AvatarParticles.FLAME_TONGUE, worldPt.x, worldPt.y, worldPt.z, 3, 0.10, 0.10, 0.10, 0.03);
            world.spawnParticles(AvatarParticles.EMBER, worldPt.x, worldPt.y, worldPt.z, 2, 0.08, 0.08, 0.08, 0.02);
            world.spawnParticles(ParticleTypes.LAVA, worldPt.x, worldPt.y, worldPt.z, 1, 0.05, 0.05, 0.05, 0.0);
        }

        // Apex explosion & flash
        Vec3d apex = origin.add(look.multiply(r * 0.9)).add(upVec.multiply(0.25));
        world.spawnParticles(AvatarParticles.FLAME_BURST, apex.x, apex.y, apex.z, 4, 0.2, 0.2, 0.2, 0.02);
        world.spawnParticles(AvatarParticles.IMPACT_FLASH, apex.x, apex.y, apex.z, 2, 0.0, 0.0, 0.0, 0.0);

        // Multi-layered punchy SFX
        world.playSound(null, player.getBlockPos(),
                SoundEvents.ITEM_FIRECHARGE_USE,
                SoundCategory.PLAYERS, 1.8f, 1.1f);
        world.playSound(null, player.getBlockPos(),
                SoundEvents.ENTITY_BLAZE_SHOOT,
                SoundCategory.PLAYERS, 1.5f, 1.2f);
        world.playSound(null, player.getBlockPos(),
                SoundEvents.ENTITY_GENERIC_BURN,
                SoundCategory.PLAYERS, 1.2f, 1.0f);
    }

    private FlameSweepSkill() {}
}
