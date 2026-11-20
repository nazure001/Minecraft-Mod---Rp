package com.avatarmod.elements.combat;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.item.AirStaffItem;
import com.avatarmod.elements.item.DualSwordsItem;
import com.avatarmod.elements.item.EarthHammerItem;
import com.avatarmod.elements.item.WarFanItem;
import com.avatarmod.elements.item.WaterSpearItem;
import com.avatarmod.elements.particle.AvatarParticles;
import com.avatarmod.elements.skill.ElementalInteractions;
import com.avatarmod.elements.sound.AvatarSounds;
import net.minecraft.block.BlockState;
import net.minecraft.block.Blocks;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.entity.effect.StatusEffectInstance;
import net.minecraft.entity.effect.StatusEffects;
import net.minecraft.item.Item;
import net.minecraft.item.ItemStack;
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
 * Authoritative Server-Side Logic for Elemental Martial Combos, Weapon Strikes, and Aerial Plunges.
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

        ItemStack held = player.getMainHandStack();
        if (isAerial) {
            executeAerialDiveKick(player, world, data, element, held);
        } else {
            // If player has an active Earth Pillar nearby, martial attack kicks it!
            if (com.avatarmod.elements.skill.impl.EarthPillarSkill.hasNearbyPillar(player, com.avatarmod.elements.skill.impl.EarthPillarSkill.INTERACTION_RADIUS)) {
                boolean kicked = com.avatarmod.elements.skill.impl.EarthPillarSkill.kickPillar(player);
                if (kicked) {
                    return;
                }
            }
            executeGroundCombo(player, world, data, element, comboStep, held);
        }
    }

    private static void executeAerialDiveKick(ServerPlayerEntity player, ServerWorld world,
                                              PlayerBendingData data, String element, ItemStack held) {
        Vec3d pos = player.getPos();
        Vec3d look = player.getRotationVec(1.0f);
        Item item = held.getItem();

        double aoe = 3.5;
        float baseDmg = 6.5f;

        if (item instanceof EarthHammerItem) {
            baseDmg = 13.0f;
            aoe = 4.2;
        } else if (item instanceof DualSwordsItem) {
            baseDmg = 9.5f;
            aoe = 3.6;
        } else if (item instanceof WaterSpearItem) {
            baseDmg = 10.0f;
            aoe = 3.4;
        } else if (item instanceof WarFanItem) {
            baseDmg = 8.0f;
            aoe = 3.8;
        } else if (item instanceof AirStaffItem) {
            baseDmg = 8.5f;
            aoe = 3.8;
        }

        final double effectiveAoe = aoe;
        final double effectiveAoeSq = effectiveAoe * effectiveAoe;

        Box hitBox = Box.of(pos, effectiveAoe * 2, 2.5, effectiveAoe * 2);
        List<LivingEntity> targets = world.getEntitiesByClass(
                LivingEntity.class, hitBox,
                e -> e != player && e.isAlive() && e.squaredDistanceTo(pos) <= effectiveAoeSq
        );

        DamageSource src = world.getDamageSources().playerAttack(player);

        for (LivingEntity target : targets) {
            float dmg = baseDmg;
            if (item instanceof EarthHammerItem || "EARTH".equals(element)) {
                BlockPos groundPos = BlockPos.ofFloored(target.getPos().subtract(0, 0.5, 0));
                dmg = ElementalInteractions.calculateEarthHardnessDamage(world, groundPos, baseDmg);
                ElementalInteractions.applySeismicStagger(target, 45);
            }
            if (item instanceof DualSwordsItem || "FIRE".equals(element)) {
                target.setOnFireForTicks(70); // 3.5s burn
            }
            if (item instanceof WaterSpearItem || "WATER".equals(element)) {
                target.extinguish();
                target.addStatusEffect(new StatusEffectInstance(StatusEffects.SLOWNESS, 50, 1));
            }
            if (item instanceof AirStaffItem || "AIR".equals(element)) {
                Vec3d diff = target.getPos().subtract(pos).normalize();
                target.takeKnockback(1.6, -diff.x, -diff.z);
                target.addVelocity(0, 0.55, 0);
                target.velocityModified = true;
            }

            target.damage(src, dmg);
        }

        // Environmental clear & particles
        ElementalInteractions.clearVegetation(world, pos, (float) aoe);

        // Sound & Particle bursts
        if (item instanceof EarthHammerItem) {
            world.playSound(null, player.getX(), player.getY(), player.getZ(),
                    AvatarSounds.EARTH_IMPACT_HEAVY, SoundCategory.PLAYERS, 1.4f, 0.9f);
        } else {
            world.playSound(null, player.getX(), player.getY(), player.getZ(),
                    AvatarSounds.MARTIAL_DIVE, SoundCategory.PLAYERS, 1.4f, 1.0f);
        }

        spawnDiveImpactParticles(world, pos, element);
    }

    private static void executeGroundCombo(ServerPlayerEntity player, ServerWorld world,
                                           PlayerBendingData data, String element, int step, ItemStack held) {
        Vec3d origin = player.getEyePos();
        Vec3d look = player.getRotationVec(1.0f);
        Item item = held.getItem();

        float damage;
        double range;
        int chiCost;

        if (item instanceof DualSwordsItem) {
            range = 3.2;
            switch (step) {
                case 1 -> { damage = 6.5f; chiCost = 0; }
                case 2 -> { damage = 7.5f; chiCost = 1; }
                case 3 -> { damage = 10.5f; chiCost = 2; }
                default -> { damage = 5.5f; chiCost = 0; }
            }
        } else if (item instanceof EarthHammerItem) {
            range = 3.2;
            switch (step) {
                case 1 -> { damage = 9.0f; chiCost = 1; }
                case 2 -> { damage = 10.5f; chiCost = 1; }
                case 3 -> { damage = 14.5f; chiCost = 2; }
                default -> { damage = 7.5f; chiCost = 0; }
            }
        } else if (item instanceof WarFanItem) {
            range = 3.0;
            switch (step) {
                case 1 -> { damage = 5.2f; chiCost = 0; }
                case 2 -> { damage = 6.0f; chiCost = 1; }
                case 3 -> { damage = 9.0f; chiCost = 2; }
                default -> { damage = 4.5f; chiCost = 0; }
            }
            // War fan deflects incoming projectiles
            ElementalInteractions.deflectProjectiles(world, player, origin, look, 3.5, 1.2);
        } else if (item instanceof WaterSpearItem) {
            range = 4.2; // Extended piercing reach
            switch (step) {
                case 1 -> { damage = 7.0f; chiCost = 0; }
                case 2 -> { damage = 8.0f; chiCost = 1; }
                case 3 -> { damage = 11.5f; chiCost = 2; }
                default -> { damage = 6.0f; chiCost = 0; }
            }
        } else if (item instanceof AirStaffItem) {
            range = 3.6;
            switch (step) {
                case 1 -> { damage = 6.0f; chiCost = 0; }
                case 2 -> { damage = 7.0f; chiCost = 1; }
                case 3 -> { damage = 9.5f; chiCost = 2; }
                default -> { damage = 5.0f; chiCost = 0; }
            }
        } else {
            // Unarmed martial arts
            switch (step) {
                case 1 -> {
                    damage = 4.0f;
                    range = 3.2;
                    chiCost = 1;
                    player.addVelocity(look.x * 0.15, 0.05, look.z * 0.15);
                    player.velocityModified = true;
                }
                case 2 -> {
                    damage = 4.5f;
                    range = 2.8;
                    chiCost = 1;
                }
                case 3 -> {
                    damage = 7.0f;
                    range = 3.5;
                    chiCost = 2;
                }
                default -> {
                    damage = 3.0f;
                    range = 2.8;
                    chiCost = 0;
                }
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
            if (item instanceof EarthHammerItem || "EARTH".equals(element)) {
                BlockPos gPos = BlockPos.ofFloored(target.getPos().subtract(0, 0.5, 0));
                finalDmg = ElementalInteractions.calculateEarthHardnessDamage(world, gPos, damage);
                if (step == 3) {
                    ElementalInteractions.applySeismicStagger(target, 40);
                }
            }
            if (item instanceof DualSwordsItem || "FIRE".equals(element)) {
                if (step == 3) target.setOnFireForTicks(60);
                else target.setOnFireForTicks(25);
            }
            if (item instanceof WaterSpearItem || "WATER".equals(element)) {
                target.extinguish();
                if (step >= 2) {
                    target.addStatusEffect(new StatusEffectInstance(StatusEffects.SLOWNESS, 40, 0));
                }
                if (item instanceof WaterSpearItem && step == 3) {
                    // Pull target closer
                    Vec3d pull = player.getPos().subtract(target.getPos()).normalize().multiply(0.4);
                    target.addVelocity(pull.x, 0.15, pull.z);
                    target.velocityModified = true;
                }
            }
            if (item instanceof AirStaffItem || "AIR".equals(element)) {
                if (step == 3) {
                    target.addVelocity(0, 0.45, 0);
                    target.velocityModified = true;
                }
            }

            if (step == 3) {
                target.takeKnockback(item instanceof EarthHammerItem ? 1.5 : 1.0, -look.x, -look.z);
            } else {
                target.takeKnockback(0.2, -look.x, -look.z);
            }

            target.damage(src, finalDmg);
            spawnTargetHitParticles(world, target.getPos().add(0, target.getHeight() * 0.5, 0), element, step);
        }

        // Play authoritative server sounds for nearby players
        if (item instanceof EarthHammerItem) {
            if (step == 3) {
                world.playSound(null, player.getX(), player.getY(), player.getZ(),
                        AvatarSounds.EARTH_IMPACT_HEAVY, SoundCategory.PLAYERS, 1.3f, 1.0f);
            } else {
                world.playSound(null, player.getX(), player.getY(), player.getZ(),
                        SoundEvents.BLOCK_DEEPSLATE_HIT, SoundCategory.PLAYERS, 1.0f, 0.9f);
            }
        } else if (item instanceof DualSwordsItem) {
            if (step == 3) {
                world.playSound(null, player.getX(), player.getY(), player.getZ(),
                        AvatarSounds.FLAME_SWEEP_SLASH, SoundCategory.PLAYERS, 1.2f, 1.0f);
            } else {
                world.playSound(null, player.getX(), player.getY(), player.getZ(),
                        SoundEvents.ENTITY_PLAYER_ATTACK_SWEEP, SoundCategory.PLAYERS, 1.0f, 1.2f);
            }
        } else if (item instanceof WaterSpearItem) {
            if (step == 3) {
                world.playSound(null, player.getX(), player.getY(), player.getZ(),
                        AvatarSounds.WATER_SPLASH_IMPACT, SoundCategory.PLAYERS, 1.2f, 0.9f);
            } else {
                world.playSound(null, player.getX(), player.getY(), player.getZ(),
                        AvatarSounds.WATER_WHIP_LASH, SoundCategory.PLAYERS, 1.0f, 1.2f);
            }
        } else if (item instanceof WarFanItem || item instanceof AirStaffItem) {
            if (step == 3) {
                world.playSound(null, player.getX(), player.getY(), player.getZ(),
                        AvatarSounds.AIR_STAFF_SWING, SoundCategory.PLAYERS, 1.2f, 1.5f);
            } else {
                world.playSound(null, player.getX(), player.getY(), player.getZ(),
                        AvatarSounds.AIR_STAFF_SWING, SoundCategory.PLAYERS, 0.9f, 1.2f);
            }
        } else {
            // Unarmed
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
