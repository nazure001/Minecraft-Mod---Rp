package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.skill.SkillDefinition;
import net.minecraft.entity.LivingEntity;
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
 * Smoke Bomb — Non-Bender tactical escape and disorienting canister.
 * Blinds and slows surrounding enemies in a 5-meter radius while shrouding
 * the user in invisibility and speed.
 */
public final class SmokeBombSkill {

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        SkillTimeline timeline = PlayerBendingData.get(player).getTimeline();
        if (timeline.phase() != SkillTimeline.Phase.ACTIVE) return;
        if (timeline.ticksInPhase() != 1) return;

        ServerWorld world = player.getServerWorld();
        Vec3d center = player.getPos();
        double radius = def.range(); // 5.0m

        // Shroud player
        player.addStatusEffect(new StatusEffectInstance(StatusEffects.INVISIBILITY, 120, 0, false, false, true));
        player.addStatusEffect(new StatusEffectInstance(StatusEffects.SPEED, 120, 1, false, false, true));

        // Disorient nearby enemies
        Box box = new Box(center.subtract(radius, radius, radius), center.add(radius, radius, radius));
        List<LivingEntity> enemies = world.getEntitiesByClass(
                LivingEntity.class, box,
                e -> e != player && e.isAlive() && e.squaredDistanceTo(center) <= radius * radius
        );

        for (LivingEntity enemy : enemies) {
            enemy.addStatusEffect(new StatusEffectInstance(StatusEffects.BLINDNESS, 100, 0));
            enemy.addStatusEffect(new StatusEffectInstance(StatusEffects.SLOWNESS, 100, 1));
        }

        // Dense atmospheric smoke cloud
        world.spawnParticles(ParticleTypes.CAMPFIRE_COSY_SMOKE, center.x, center.y + 0.8, center.z, 60, 2.2, 1.2, 2.2, 0.03);
        world.spawnParticles(ParticleTypes.SQUID_INK, center.x, center.y + 0.8, center.z, 30, 1.8, 1.0, 1.8, 0.05);
        world.spawnParticles(ParticleTypes.POOF, center.x, center.y + 0.8, center.z, 25, 2.0, 1.0, 2.0, 0.08);

        // Sound cues
        world.playSound(null, player.getBlockPos(), SoundEvents.ENTITY_GENERIC_EXPLODE.value(), SoundCategory.PLAYERS, 1.0f, 1.4f);
        world.playSound(null, player.getBlockPos(), SoundEvents.BLOCK_FIRE_EXTINGUISH, SoundCategory.PLAYERS, 1.4f, 0.8f);
    }

    private SmokeBombSkill() {}
}
