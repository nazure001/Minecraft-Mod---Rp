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

        // Extended reach: 4.5m base, 5.8m on combo
        double reach = Math.max(4.5, def.range()) * (finalCombo ? FINAL_COMBO_RANGE_BONUS : 1.0f);
        Vec3d reachEnd = eyePos.add(look.multiply(reach));
        Box scanBox = new Box(eyePos, reachEnd).expand(1.4);

        List<LivingEntity> targets = world.getEntitiesByClass(
                LivingEntity.class, scanBox,
                e -> {
                    if (e == player || !e.isAlive()) return false;
                    Vec3d toCenter = e.getBoundingBox().getCenter().subtract(eyePos);
                    double distSq = toCenter.lengthSquared();
                    if (distSq > (reach + 0.8) * (reach + 0.8)) return false;
                    if (distSq <= 2.8) return true; // Point-blank automatic hit
                    return toCenter.normalize().dotProduct(look) > 0.15; // Generous forward strike cone
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

        // 2. Continuous flame jet streaming along punch path
        for (double d = 0.4; d <= reach; d += 0.45) {
            Vec3d p = fistPos.add(look.multiply(d));
            world.spawnParticles(ParticleTypes.FLAME,
                    p.x, p.y, p.z,
                    finalCombo ? 4 : 2, 0.06, 0.06, 0.06, 0.04);
            world.spawnParticles(AvatarParticles.FLAME_TONGUE,
                    p.x, p.y, p.z,
                    finalCombo ? 3 : 2, 0.05, 0.05, 0.05, 0.03);
            world.spawnParticles(AvatarParticles.EMBER,
                    p.x, p.y, p.z,
                    1, 0.04, 0.04, 0.04, 0.02);
        }

        // 3. Apex burst at terminal reach
        Vec3d apexPos = fistPos.add(look.multiply(Math.min(reach, 3.0)));

        world.spawnParticles(AvatarParticles.IMPACT_FLASH,
                apexPos.x, apexPos.y, apexPos.z,
                1, 0.0, 0.0, 0.0, 0.0);
        world.spawnParticles(AvatarParticles.FLAME_BURST,
                apexPos.x, apexPos.y, apexPos.z,
                finalCombo ? 4 : 2, 0.10, 0.10, 0.10, 0.05);
        world.spawnParticles(ParticleTypes.SMOKE,
                apexPos.x, apexPos.y, apexPos.z,
                finalCombo ? 6 : 4, 0.15, 0.15, 0.15, 0.02);

        // Combo accents: ParticleTypes.LAVA (4) and ParticleTypes.CRIT (6) at P_apex on combo
        if (finalCombo) {
            world.spawnParticles(ParticleTypes.LAVA,
                    apexPos.x, apexPos.y, apexPos.z,
                    4, 0.20, 0.20, 0.20, 0.0);
            world.spawnParticles(ParticleTypes.CRIT,
                    apexPos.x, apexPos.y, apexPos.z,
                    6, 0.30, 0.30, 0.30, 0.10);
        }

        // Ignite flammable ground/blocks safely without burning caster's feet
        ElementalInteractions.igniteBlocks(world, apexPos, 1.2, player);

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
