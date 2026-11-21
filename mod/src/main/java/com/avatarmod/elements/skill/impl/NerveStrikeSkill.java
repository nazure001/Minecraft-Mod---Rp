package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.particle.AvatarParticles;
import com.avatarmod.elements.skill.SkillDefinition;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.entity.effect.StatusEffectInstance;
import net.minecraft.entity.effect.StatusEffects;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.text.Text;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;

import java.util.List;

/**
 * Nerve Strike — Master Chi Blocker ultimate technique.
 * Delivers a crippling blow to major neuro-chi junctions, completely shutting down
 * elemental bending for 8 seconds and heavily paralyzing the target.
 */
public final class NerveStrikeSkill {

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        SkillTimeline timeline = PlayerBendingData.get(player).getTimeline();
        if (timeline.phase() != SkillTimeline.Phase.ACTIVE) return;
        if (timeline.ticksInPhase() != 1) return;

        ServerWorld world = player.getServerWorld();
        Vec3d eyePos = player.getEyePos();
        Vec3d look = player.getRotationVec(1.0f);
        double reach = def.range();

        Vec3d strikeEnd = eyePos.add(look.multiply(reach));
        Box box = new Box(eyePos, strikeEnd).expand(1.2);

        List<LivingEntity> targets = world.getEntitiesByClass(
                LivingEntity.class, box,
                e -> e != player && e.isAlive()
                        && e.getBoundingBox().getCenter().subtract(eyePos).normalize().dotProduct(look) > 0.2
        );

        DamageSource source = world.getDamageSources().playerAttack(player);
        for (LivingEntity target : targets) {
            target.damage(source, def.damage());

            if (target instanceof ServerPlayerEntity targetPlayer) {
                PlayerBendingData targetData = PlayerBendingData.get(targetPlayer);
                targetData.applyChiBlock(160); // 8.0 seconds total lock
                targetData.drainChi(35); // Heavy chi disruption drain
                targetPlayer.addStatusEffect(new StatusEffectInstance(StatusEffects.SLOWNESS, 160, 3));
                targetPlayer.addStatusEffect(new StatusEffectInstance(StatusEffects.WEAKNESS, 160, 2));

                targetPlayer.sendMessage(Text.literal("§4[Avatar] Titik syaraf utama Anda lumpuh! Seluruh chi dan kemampuan bender terkunci total!"), true);
                targetPlayer.playSound(SoundEvents.BLOCK_BEACON_DEACTIVATE, 1.4f, 0.5f);
                targetPlayer.playSound(SoundEvents.ENTITY_LIGHTNING_BOLT_THUNDER, 0.6f, 1.8f);
            } else {
                target.addStatusEffect(new StatusEffectInstance(StatusEffects.SLOWNESS, 160, 3));
                target.addStatusEffect(new StatusEffectInstance(StatusEffects.WEAKNESS, 160, 2));
                target.addStatusEffect(new StatusEffectInstance(StatusEffects.MINING_FATIGUE, 160, 2));
            }

            // High impact knockback
            Vec3d knock = look.multiply(def.knockback());
            target.addVelocity(knock.x, 0.2, knock.z);
            target.velocityModified = true;

            // Disruption particles
            Vec3d hitPos = target.getBoundingBox().getCenter();
            world.spawnParticles(AvatarParticles.SPARK, hitPos.x, hitPos.y, hitPos.z, 20, 0.2, 0.2, 0.2, 0.1);
            world.spawnParticles(AvatarParticles.CRACKLE, hitPos.x, hitPos.y, hitPos.z, 10, 0.2, 0.2, 0.2, 0.1);
            world.spawnParticles(AvatarParticles.IMPACT_FLASH, hitPos.x, hitPos.y, hitPos.z, 4, 0.1, 0.1, 0.1, 0.0);
            world.spawnParticles(ParticleTypes.DAMAGE_INDICATOR, hitPos.x, hitPos.y, hitPos.z, 5, 0.2, 0.2, 0.2, 0.1);
        }

        world.playSound(null, player.getBlockPos(), SoundEvents.ENTITY_PLAYER_ATTACK_CRIT, SoundCategory.PLAYERS, 1.3f, 0.9f);
        world.playSound(null, player.getBlockPos(), SoundEvents.BLOCK_ANVIL_LAND, SoundCategory.PLAYERS, 0.8f, 1.6f);
    }

    private NerveStrikeSkill() {}
}
