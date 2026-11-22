package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.particle.AvatarParticles;
import com.avatarmod.elements.skill.SkillDefinition;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.entity.effect.StatusEffectInstance;
import net.minecraft.entity.effect.StatusEffects;
import net.minecraft.entity.player.PlayerEntity;
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
 * Chi Strike — Canonical martial arts technique practiced by Ty Lee and Equalists.
 * Strikes the victim's pressure points with rapid pinpoint fist jabs.
 *
 * Gameplay Effects:
 * 1. Deals 5.0 physical martial damage.
 * 2. If target is a player: inflicts Chi Blocked for 6.0s (120 ticks).
 *    Drains 30% Chi, cancels active skill casting, and locks all bending slots.
 * 3. If target is a mob: applies Slowness III and Weakness II for 6.0s.
 */
public final class ChiStrikeSkill {

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

            // Pressure point chi block
            if (target instanceof ServerPlayerEntity targetPlayer) {
                PlayerBendingData targetData = PlayerBendingData.get(targetPlayer);
                targetData.applyChiBlock(120); // 6 seconds chi block
                targetPlayer.sendMessage(Text.literal("§c[Avatar] Titik Chi Anda dihantam oleh Chi Blocker! Bending terkunci!"), true);
                targetPlayer.playSound(SoundEvents.BLOCK_RESPAWN_ANCHOR_DEPLETE.value(), 1.2f, 0.6f);
            } else {
                target.addStatusEffect(new StatusEffectInstance(StatusEffects.SLOWNESS, 120, 2));
                target.addStatusEffect(new StatusEffectInstance(StatusEffects.WEAKNESS, 120, 1));
            }

            // Punchy knockback
            Vec3d knock = look.multiply(def.knockback());
            target.addVelocity(knock.x, 0.15, knock.z);
            target.velocityModified = true;

            // Pressure point impact VFX: Chi filament + Avatar Chi burst
            Vec3d hitPos = target.getBoundingBox().getCenter();
            world.spawnParticles(AvatarParticles.IMPACT_FLASH, hitPos.x, hitPos.y, hitPos.z, 2, 0.1, 0.1, 0.1, 0.0);
            world.spawnParticles(AvatarParticles.BLOOD_CHI_FILAMENT, hitPos.x, hitPos.y, hitPos.z, 4, 0.15, 0.15, 0.15, 0.04);
            world.spawnParticles(AvatarParticles.AVATAR_CHI, hitPos.x, hitPos.y, hitPos.z, 3, 0.15, 0.15, 0.15, 0.03);
        }

        // Kinetic fist whoosh and punch impact audio
        world.playSound(null, player.getBlockPos(), SoundEvents.ENTITY_PLAYER_ATTACK_KNOCKBACK, SoundCategory.PLAYERS, 1.2f, 1.3f);
        world.playSound(null, player.getBlockPos(), SoundEvents.ENTITY_PLAYER_ATTACK_CRIT, SoundCategory.PLAYERS, 1.1f, 1.5f);
    }

    private ChiStrikeSkill() {}
}
