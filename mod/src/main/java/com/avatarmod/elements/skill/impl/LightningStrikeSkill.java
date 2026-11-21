package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.particle.AvatarParticles;
import com.avatarmod.elements.skill.ElementalInteractions;
import com.avatarmod.elements.skill.SkillDefinition;
import com.avatarmod.elements.skill.SkillTargeting;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.entity.effect.StatusEffectInstance;
import net.minecraft.entity.effect.StatusEffects;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;

import java.util.List;

/**
 * Lightning Strike — Firebending Sub-Skill (Cold-Blooded Fire).
 *
 * Choreography & Mechanics:
 * 1. Windup (35 ticks / 1.75s): Yin-Yang circular martial charge. Blue/white electric current
 *    sparks and gathers between fingertips.
 * 2. Active (25 ticks / 1.25s): Release of a supersonic high-voltage piercing raycast beam
 *    up to 30 blocks. Deals massive piercing damage (18.0), inflicts stun/paralysis (Slowness IV),
 *    and ignites combustible blocks along the bolt trajectory!
 */
public final class LightningStrikeSkill {

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        PlayerBendingData data = PlayerBendingData.get(player);
        SkillTimeline timeline = data.getTimeline();
        ServerWorld world = player.getServerWorld();

        // 1. Windup: Electric charge buildup
        if (timeline.phase() == SkillTimeline.Phase.WINDUP) {
            int t = timeline.ticksInPhase();
            Vec3d handPos = player.getEyePos().add(player.getRotationVec(1.0f).multiply(0.6));

            // Gathering electric sparks
            world.spawnParticles(ParticleTypes.ELECTRIC_SPARK,
                    handPos.x, handPos.y, handPos.z,
                    t / 5 + 2, 0.25, 0.25, 0.25, 0.08);

            if (t % 8 == 0) {
                world.playSound(null, player.getBlockPos(),
                        SoundEvents.BLOCK_RESPAWN_ANCHOR_CHARGE,
                        SoundCategory.PLAYERS, 0.8f, 1.2f + (t * 0.02f));
            }
        }

        // 2. Active Tick 1: The lightning bolt discharge!
        if (timeline.phase() == SkillTimeline.Phase.ACTIVE && timeline.ticksInPhase() == 1) {
            dischargeLightning(player, world, def);
        }
    }

    private static void dischargeLightning(ServerPlayerEntity player, ServerWorld world, SkillDefinition def) {
        Vec3d origin = player.getEyePos();
        Vec3d look = player.getRotationVec(1.0f);
        double range = def.range();
        Vec3d end = origin.add(look.multiply(range));

        Box searchBox = SkillTargeting.segmentBounds(origin, end, 1.5);
        List<LivingEntity> targets = world.getEntitiesByClass(
                LivingEntity.class, searchBox,
                e -> e != player && e.isAlive()
                        && SkillTargeting.intersectsSegment(origin, end, e.getBoundingBox(), 1.5)
                        && SkillTargeting.hasLineOfSight(world, origin, e.getBoundingBox(), player)
        );

        DamageSource source = world.getDamageSources().lightningBolt();
        for (LivingEntity target : targets) {
            target.damage(source, def.damage());
            // High-voltage paralysis
            target.addStatusEffect(new StatusEffectInstance(StatusEffects.SLOWNESS, 80, 3));
            target.addStatusEffect(new StatusEffectInstance(StatusEffects.WEAKNESS, 80, 1));
            ElementalInteractions.applyFire(target, 100);

            Vec3d knock = look.multiply(def.knockback());
            target.addVelocity(knock.x, 0.35, knock.z);
            target.velocityModified = true;
        }

        // Raycast beam particles: dense electric sparks & critical energy
        for (double d = 0.5; d <= range; d += 0.5) {
            Vec3d pt = origin.add(look.multiply(d));
            world.spawnParticles(ParticleTypes.ELECTRIC_SPARK,
                    pt.x, pt.y, pt.z, 5, 0.1, 0.1, 0.1, 0.05);
            world.spawnParticles(ParticleTypes.CRIT,
                    pt.x, pt.y, pt.z, 2, 0.05, 0.05, 0.05, 0.02);
            world.spawnParticles(AvatarParticles.FLAME_TONGUE,
                    pt.x, pt.y, pt.z, 1, 0.05, 0.05, 0.05, 0.02);
        }

        // Terminal lightning impact detonation
        world.spawnParticles(ParticleTypes.EXPLOSION,
                end.x, end.y, end.z, 2, 0.3, 0.3, 0.3, 0.0);
        world.spawnParticles(AvatarParticles.IMPACT_FLASH,
                end.x, end.y, end.z, 2, 0.0, 0.0, 0.0, 0.0);

        // Thunderous sonic crack SFX
        world.playSound(null, player.getBlockPos(),
                SoundEvents.ENTITY_LIGHTNING_BOLT_THUNDER,
                SoundCategory.PLAYERS, 2.0f, 1.3f);
        world.playSound(null, player.getBlockPos(),
                SoundEvents.ENTITY_LIGHTNING_BOLT_IMPACT,
                SoundCategory.PLAYERS, 2.0f, 1.1f);
        world.playSound(null, player.getBlockPos(),
                SoundEvents.ITEM_TRIDENT_THUNDER.value(),
                SoundCategory.PLAYERS, 1.8f, 1.5f);

        // Ignite ground blocks at strike point
        ElementalInteractions.igniteBlocks(world, end, 2.0, player);
    }

    private LightningStrikeSkill() {}
}
