package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.particle.AvatarParticles;
import com.avatarmod.elements.skill.ElementalInteractions;
import com.avatarmod.elements.skill.SkillDefinition;
import com.avatarmod.elements.skill.SkillTargeting;
import com.avatarmod.elements.sound.ModSounds;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;

import java.util.List;

public final class FireJabSkill {

    /**
     * Called every server tick while the player has fire_jab in timeline.
     * Triggers hitbox exactly on the first tick of the ACTIVE phase (Tick 3).
     */
    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        PlayerBendingData data = PlayerBendingData.get(player);
        SkillTimeline timeline = data.getTimeline();

        if (timeline.phase() != SkillTimeline.Phase.ACTIVE) return;
        if (timeline.ticksInPhase() != 1) return; // fire only on first active tick (Tick 3)

        executeHitbox(player, def);
    }

    // flame_sweep comboWindowTicks = 8
    private static final int SWEEP_COMBO_WINDOW = 8;
    private static final float FINAL_COMBO_DAMAGE_BONUS = 1.5f;
    private static final float FINAL_COMBO_RANGE_BONUS = 1.3f;

    private static void executeHitbox(ServerPlayerEntity player, SkillDefinition def) {
        PlayerBendingData data = PlayerBendingData.get(player);
        long currentTick = player.getServerWorld().getTime();
        boolean isFinalCombo = data.isActiveCastCombo()
                || ("avatar:flame_sweep".equals(data.getLastComboSkillId())
                && (currentTick <= data.getComboExpiryTick() || (currentTick - data.getLastComboSkillTick()) <= SWEEP_COMBO_WINDOW));
        executeHitbox(player, def, isFinalCombo);
    }

    private static void executeHitbox(ServerPlayerEntity player, SkillDefinition def, boolean finalCombo) {
        ServerWorld world = player.getServerWorld();
        Vec3d eyePos = player.getEyePos();
        Vec3d pos = player.getPos().add(0, player.getStandingEyeHeight() / 2.0, 0);
        Vec3d look = player.getRotationVec(1.0f);

        // Center hitbox slightly in front of player
        Vec3d center = pos.add(look.multiply(def.range() * 0.6));

        double r = def.range() * (finalCombo ? FINAL_COMBO_RANGE_BONUS : 1.0f);
        Box box = Box.of(center, (r + 1.0) * 2, (r + 1.0) * 2, (r + 1.0) * 2);

        List<LivingEntity> targets = world.getEntitiesByClass(
                LivingEntity.class, box,
                e -> {
                    if (e == player || !e.isAlive()) return false;
                    var targetBounds = e.getBoundingBox();
                    Vec3d targetCenter = targetBounds.getCenter();
                    if (!SkillTargeting.hasLineOfSight(world, eyePos, targetBounds, player)) return false;
                    if (!SkillTargeting.isWithinRange(eyePos, targetBounds, r + 0.5)) return false;

                    Vec3d toTarget = targetCenter.subtract(eyePos);
                    // Retain point-blank hits while checking aim from the eye position.
                    return toTarget.lengthSquared() <= 1.44 || toTarget.normalize().dotProduct(look) > 0.0;
                }
        );

        DamageSource source = world.getDamageSources().playerAttack(player);
        // Base damage = 4.0, Combo damage = 4.0 * 1.5 = 6.0
        float damage = def.damage() * (finalCombo ? FINAL_COMBO_DAMAGE_BONUS : 1.0f);

        for (LivingEntity target : targets) {
            target.damage(source, damage);
            ElementalInteractions.applyFire(target, finalCombo ? 70 : 40);

            // Knockback away from player
            Vec3d knockDir = target.getPos().subtract(player.getPos()).normalize();
            target.addVelocity(
                    knockDir.x * def.knockback(),
                    0.1 + def.knockback() * 0.3,
                    knockDir.z * def.knockback()
            );
            target.velocityModified = true;
        }

        // --- Multi-stage flame/smoke burst VFX ---
        double horizLen = Math.sqrt(look.x * look.x + look.z * look.z);
        Vec3d right = horizLen > 1e-5
                ? new Vec3d(-look.z / horizLen, 0.0, look.x / horizLen)
                : new Vec3d(1.0, 0.0, 0.0);

        // 1. Knuckle fist position: P_fist = player.getPos() + (0, 1.20, 0) + u_right * 0.28 + u_look * 0.40
        Vec3d fistPos = player.getPos().add(0, 1.20, 0)
                .add(right.multiply(0.28))
                .add(look.multiply(0.40));

        // 2. Strike jet midpoint: P_mid = P_fist + u_look * 0.55
        Vec3d jetMid = fistPos.add(look.multiply(0.55));

        // 3. Apex burst: P_apex = fistPos + u_look * 1.20 (aligned with strike vector, below eye level)
        Vec3d apexPos = fistPos.add(look.multiply(1.20));

        // Knuckle flash: ParticleTypes.FLAME (4/6) and ParticleTypes.SMALL_FLAME (4/6)
        world.spawnParticles(ParticleTypes.FLAME,
                fistPos.x, fistPos.y, fistPos.z,
                finalCombo ? 6 : 4, 0.04, 0.04, 0.04, 0.02);
        world.spawnParticles(ParticleTypes.SMALL_FLAME,
                fistPos.x, fistPos.y, fistPos.z,
                finalCombo ? 6 : 4, 0.03, 0.03, 0.03, 0.01);
        world.spawnParticles(AvatarParticles.FLAME_TONGUE,
                fistPos.x, fistPos.y, fistPos.z,
                finalCombo ? 6 : 4, 0.04, 0.04, 0.04, 0.02);
        world.spawnParticles(AvatarParticles.EMBER,
                fistPos.x, fistPos.y, fistPos.z,
                finalCombo ? 6 : 4, 0.03, 0.03, 0.03, 0.01);

        // Strike jet: ParticleTypes.FLAME (10/16)
        world.spawnParticles(ParticleTypes.FLAME,
                jetMid.x, jetMid.y, jetMid.z,
                finalCombo ? 16 : 10, 0.12, 0.12, 0.12, 0.08);
        world.spawnParticles(AvatarParticles.FLAME_TONGUE,
                jetMid.x, jetMid.y, jetMid.z,
                finalCombo ? 12 : 8, 0.10, 0.10, 0.10, 0.06);

        // Apex burst: ParticleTypes.FLAME (8/14) and ParticleTypes.SMOKE (4/6)
        world.spawnParticles(ParticleTypes.FLAME,
                apexPos.x, apexPos.y, apexPos.z,
                finalCombo ? 14 : 8, 0.25, 0.25, 0.25, 0.05);
        world.spawnParticles(ParticleTypes.SMOKE,
                apexPos.x, apexPos.y, apexPos.z,
                finalCombo ? 6 : 4, 0.15, 0.15, 0.15, 0.02);
        world.spawnParticles(AvatarParticles.FLAME_BURST,
                apexPos.x, apexPos.y, apexPos.z,
                finalCombo ? 3 : 1, 0.05, 0.05, 0.05, 0.0);
        world.spawnParticles(AvatarParticles.IMPACT_FLASH,
                apexPos.x, apexPos.y, apexPos.z,
                1, 0.0, 0.0, 0.0, 0.0);

        // Combo accents: ParticleTypes.LAVA (4) and ParticleTypes.CRIT (6) at P_apex on combo
        if (finalCombo) {
            world.spawnParticles(ParticleTypes.LAVA,
                    apexPos.x, apexPos.y, apexPos.z,
                    4, 0.20, 0.20, 0.20, 0.0);
            world.spawnParticles(ParticleTypes.CRIT,
                    apexPos.x, apexPos.y, apexPos.z,
                    6, 0.30, 0.30, 0.30, 0.10);
        }

        // Ignite flammable ground/blocks at punch apex
        ElementalInteractions.igniteBlocks(world, apexPos, 1.2);

        // SFX: Synchronize SFX with ModSounds.FIRE_RELEASE at player position
        float volume = finalCombo ? 1.0f : 0.85f;
        float pitch = 0.95f + (world.getRandom().nextFloat() * 0.1f);
        world.playSound(
                null,
                player.getX(), player.getY(), player.getZ(),
                ModSounds.FIRE_RELEASE,
                SoundCategory.PLAYERS,
                volume, pitch
        );
    }

    private FireJabSkill() {}
}
