package com.avatarmod.elements.combat;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.particle.AvatarParticles;
import com.avatarmod.elements.skill.ElementalInteractions;
import com.avatarmod.elements.sound.AvatarSounds;
import net.minecraft.block.BlockState;
import net.minecraft.block.Blocks;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.entity.effect.StatusEffectInstance;
import net.minecraft.entity.effect.StatusEffects;
import net.minecraft.particle.BlockStateParticleEffect;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;

import java.util.List;

/**
 * Authoritative Server-Side Logic for 4-Hit Elemental Martial Combos and Aerial Dive-Kicks.
 */
public final class MartialCombatServer {

    private MartialCombatServer() {}

    public static void handleMartialAttack(ServerPlayerEntity player, int comboStep, boolean isAerial) {
        if (player == null || !player.isAlive()) return;
        ServerWorld world = player.getServerWorld();
        PlayerBendingData data = PlayerBendingData.get(player);
        String element = data.getActiveElement();
        if (element == null || element.isEmpty()) {
            element = "FIRE";
        }

        if (isAerial) {
            executeAerialDiveKick(player, world, data, element);
        } else {
            executeGroundCombo(player, world, data, element, comboStep);
        }
    }

    private static void executeAerialDiveKick(ServerPlayerEntity player, ServerWorld world, PlayerBendingData data, String element) {
        Vec3d pos = player.getPos();
        Vec3d look = player.getRotationVec(1.0f);
        double aoe = 3.5;
        Box hitBox = Box.of(pos, aoe * 2, 2.5, aoe * 2);

        List<LivingEntity> targets = world.getEntitiesByClass(
                LivingEntity.class, hitBox,
                e -> e != player && e.isAlive() && e.squaredDistanceTo(pos) <= (aoe * aoe)
        );

        float baseDmg = 6.5f;
        DamageSource src = world.getDamageSources().playerAttack(player);

        for (LivingEntity target : targets) {
            float dmg = baseDmg;
            if ("EARTH".equals(element)) {
                BlockPos groundPos = BlockPos.ofFloored(target.getPos().subtract(0, 0.5, 0));
                dmg = ElementalInteractions.calculateEarthHardnessDamage(world, groundPos, baseDmg);
                ElementalInteractions.applySeismicStagger(target, 40);
            } else if ("FIRE".equals(element)) {
                target.setOnFireForTicks(60); // 3s burn
            } else if ("WATER".equals(element)) {
                target.addStatusEffect(new StatusEffectInstance(StatusEffects.SLOWNESS, 40, 1));
            } else if ("AIR".equals(element)) {
                Vec3d diff = target.getPos().subtract(pos).normalize();
                target.takeKnockback(1.5, -diff.x, -diff.z);
                target.addVelocity(0, 0.45, 0);
                target.velocityModified = true;
            }

            target.damage(src, dmg);
        }

        // Environmental clear & particles
        ElementalInteractions.clearVegetation(world, pos, (float) aoe);

        // Sound & Particle bursts
        world.playSound(null, player.getX(), player.getY(), player.getZ(),
                AvatarSounds.MARTIAL_DIVE, SoundCategory.PLAYERS, 1.4f, 1.0f);

        spawnDiveImpactParticles(world, pos, element);
    }

    private static void executeGroundCombo(ServerPlayerEntity player, ServerWorld world, PlayerBendingData data, String element, int step) {
        Vec3d origin = player.getEyePos();
        Vec3d look = player.getRotationVec(1.0f);

        float damage;
        double range;
        int chiCost;

        switch (step) {
            case 1 -> { // Cross
                damage = 4.0f;
                range = 3.2;
                chiCost = 1;
                // Forward momentum
                player.addVelocity(look.x * 0.15, 0.05, look.z * 0.15);
                player.velocityModified = true;
            }
            case 2 -> { // Low Kick
                damage = 4.5f;
                range = 2.8;
                chiCost = 1;
            }
            case 3 -> { // Roundhouse Finisher
                damage = 7.0f;
                range = 3.5;
                chiCost = 2;
            }
            default -> { // Jab
                damage = 3.0f;
                range = 2.8;
                chiCost = 0;
            }
        }

        if (chiCost > 0) {
            data.trySpendChi(chiCost);
        }

        Vec3d reachPoint = origin.add(look.multiply(range * 0.6));
        Box hitBox = Box.of(reachPoint, range * 1.5, 2.0, range * 1.5);

        List<LivingEntity> targets = world.getEntitiesByClass(
                LivingEntity.class, hitBox,
                e -> e != player && e.isAlive() && origin.squaredDistanceTo(e.getBoundingBox().getCenter()) <= (range * range)
        );

        DamageSource src = world.getDamageSources().playerAttack(player);

        for (LivingEntity target : targets) {
            float finalDmg = damage;
            if ("EARTH".equals(element)) {
                BlockPos gPos = BlockPos.ofFloored(target.getPos().subtract(0, 0.5, 0));
                finalDmg = ElementalInteractions.calculateEarthHardnessDamage(world, gPos, damage);
                if (step == 3) {
                    ElementalInteractions.applySeismicStagger(target, 35);
                }
            } else if ("FIRE".equals(element)) {
                if (step == 3) target.setOnFireForTicks(50);
                else target.setOnFireForTicks(20);
            } else if ("WATER".equals(element)) {
                if (step == 2 || step == 3) {
                    target.addStatusEffect(new StatusEffectInstance(StatusEffects.SLOWNESS, 30, 0));
                }
            } else if ("AIR".equals(element)) {
                if (step == 3) {
                    target.addVelocity(0, 0.4, 0);
                }
            }

            if (step == 3) {
                target.takeKnockback(1.0, -look.x, -look.z);
            } else {
                target.takeKnockback(0.2, -look.x, -look.z);
            }

            target.damage(src, finalDmg);
            spawnTargetHitParticles(world, target.getPos().add(0, target.getHeight() * 0.5, 0), element, step);
        }

        // Sounds
        if (step == 3) {
            world.playSound(null, player.getX(), player.getY(), player.getZ(),
                    AvatarSounds.MARTIAL_KICK, SoundCategory.PLAYERS, 1.1f, 1.0f);
            world.playSound(null, player.getX(), player.getY(), player.getZ(),
                    AvatarSounds.HITSTOP_IMPACT, SoundCategory.PLAYERS, 1.2f, 1.4f);
        } else if (step == 2) {
            world.playSound(null, player.getX(), player.getY(), player.getZ(),
                    AvatarSounds.MARTIAL_KICK, SoundCategory.PLAYERS, 1.0f, 1.2f);
        } else {
            world.playSound(null, player.getX(), player.getY(), player.getZ(),
                    AvatarSounds.MARTIAL_PUNCH, SoundCategory.PLAYERS, 0.9f, 1.2f + (step * 0.1f));
        }
    }

    private static void spawnTargetHitParticles(ServerWorld world, Vec3d pos, String element, int step) {
        switch (element) {
            case "FIRE" -> {
                world.spawnParticles(ParticleTypes.FLAME, pos.x, pos.y, pos.z, 6 + step * 2, 0.2, 0.2, 0.2, 0.04);
                world.spawnParticles(AvatarParticles.SPARK, pos.x, pos.y, pos.z, 4, 0.15, 0.15, 0.15, 0.05);
            }
            case "WATER" -> {
                world.spawnParticles(AvatarParticles.DROPLET, pos.x, pos.y, pos.z, 8 + step * 2, 0.2, 0.2, 0.2, 0.05);
                world.spawnParticles(AvatarParticles.SPLASH, pos.x, pos.y, pos.z, 4, 0.15, 0.15, 0.15, 0.03);
            }
            case "EARTH" -> {
                world.spawnParticles(AvatarParticles.STONE_CHIP, pos.x, pos.y, pos.z, 6 + step * 3, 0.2, 0.2, 0.2, 0.08);
                world.spawnParticles(AvatarParticles.DUST, pos.x, pos.y, pos.z, 5, 0.2, 0.1, 0.2, 0.02);
            }
            case "AIR" -> {
                world.spawnParticles(AvatarParticles.GUST_CURL, pos.x, pos.y, pos.z, 3 + step, 0.2, 0.2, 0.2, 0.04);
                world.spawnParticles(AvatarParticles.SMOKE_PUFF, pos.x, pos.y, pos.z, 4, 0.15, 0.15, 0.15, 0.02);
            }
        }
    }

    private static void spawnDiveImpactParticles(ServerWorld world, Vec3d pos, String element) {
        world.spawnParticles(ParticleTypes.EXPLOSION, pos.x, pos.y + 0.1, pos.z, 1, 0.1, 0.1, 0.1, 0.0);
        switch (element) {
            case "FIRE" -> {
                for (int i = 0; i < 16; i++) {
                    double angle = (i / 16.0) * Math.PI * 2;
                    double dx = Math.cos(angle) * 2.5;
                    double dz = Math.sin(angle) * 2.5;
                    world.spawnParticles(ParticleTypes.FLAME, pos.x + dx, pos.y + 0.2, pos.z + dz, 2, 0.1, 0.1, 0.1, 0.03);
                }
            }
            case "WATER" -> {
                world.spawnParticles(AvatarParticles.SPLASH, pos.x, pos.y + 0.2, pos.z, 30, 1.2, 0.3, 1.2, 0.1);
                world.spawnParticles(AvatarParticles.DROPLET, pos.x, pos.y + 0.3, pos.z, 25, 1.0, 0.4, 1.0, 0.08);
            }
            case "EARTH" -> {
                world.spawnParticles(AvatarParticles.STONE_CHIP, pos.x, pos.y + 0.2, pos.z, 40, 1.2, 0.4, 1.2, 0.15);
                world.spawnParticles(AvatarParticles.DUST, pos.x, pos.y + 0.1, pos.z, 35, 1.5, 0.3, 1.5, 0.05);
            }
            case "AIR" -> {
                world.spawnParticles(AvatarParticles.GUST_CURL, pos.x, pos.y + 0.2, pos.z, 18, 1.5, 0.2, 1.5, 0.1);
                world.spawnParticles(ParticleTypes.POOF, pos.x, pos.y + 0.2, pos.z, 20, 1.2, 0.2, 1.2, 0.05);
            }
        }
    }
}
