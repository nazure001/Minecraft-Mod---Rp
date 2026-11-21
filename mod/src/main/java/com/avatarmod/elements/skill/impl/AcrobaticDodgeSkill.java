package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.skill.SkillDefinition;
import net.minecraft.entity.effect.StatusEffectInstance;
import net.minecraft.entity.effect.StatusEffects;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.util.math.Vec3d;

/**
 * Acrobatic Dodge — Elite Non-Bender evasive movement.
 * Executes an agile cartwheel / tumble roll that provides brief damage immunity
 * (Resistance V) and explosive evasive repositioning.
 */
public final class AcrobaticDodgeSkill {

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        SkillTimeline timeline = PlayerBendingData.get(player).getTimeline();
        if (timeline.phase() != SkillTimeline.Phase.ACTIVE) return;
        if (timeline.ticksInPhase() != 1) return;

        ServerWorld world = player.getServerWorld();
        Vec3d look = player.getRotationVec(1.0f);
        Vec3d flatLook = new Vec3d(look.x, 0.0, look.z).normalize();

        // Propel player in looking direction with slight upward hop
        Vec3d leap = flatLook.multiply(1.35).add(0.0, 0.28, 0.0);
        player.setVelocity(leap);
        player.velocityModified = true;

        // Temporary i-frame resistance and agility surge
        player.addStatusEffect(new StatusEffectInstance(StatusEffects.RESISTANCE, 16, 4, false, false, false));
        player.addStatusEffect(new StatusEffectInstance(StatusEffects.SPEED, 30, 2, false, false, false));
        player.fallDistance = 0.0f;

        // Evasive whoosh particles and tumble audio
        world.spawnParticles(ParticleTypes.CLOUD, player.getX(), player.getY() + 0.2, player.getZ(), 8, 0.3, 0.1, 0.3, 0.05);
        world.spawnParticles(ParticleTypes.SWEEP_ATTACK, player.getX(), player.getY() + 0.6, player.getZ(), 1, 0.0, 0.0, 0.0, 0.0);
        world.playSound(null, player.getBlockPos(), SoundEvents.ENTITY_PLAYER_ATTACK_SWEEP, SoundCategory.PLAYERS, 1.2f, 1.6f);
    }

    private AcrobaticDodgeSkill() {}
}
