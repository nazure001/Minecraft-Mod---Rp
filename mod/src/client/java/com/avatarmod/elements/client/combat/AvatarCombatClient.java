package com.avatarmod.elements.client.combat;

import com.avatarmod.elements.client.anim.AvatarAnimations;
import com.avatarmod.elements.client.camera.AvatarCameraDirector;
import com.avatarmod.elements.client.vfx.CinematicVfxController;
import com.avatarmod.elements.client.vfx.VfxType;
import com.avatarmod.elements.item.AirStaffItem;
import com.avatarmod.elements.item.DualSwordsItem;
import com.avatarmod.elements.item.EarthHammerItem;
import com.avatarmod.elements.item.WarFanItem;
import com.avatarmod.elements.item.WaterSpearItem;
import com.avatarmod.elements.network.SkillPackets;
import com.avatarmod.elements.sound.AvatarSounds;
import com.zigythebird.playeranimcore.easing.EasingType;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.minecraft.client.MinecraftClient;
import net.minecraft.item.Item;
import net.minecraft.item.ItemStack;
import net.minecraft.sound.SoundEvents;
import net.minecraft.util.Hand;
import net.minecraft.util.Identifier;
import net.minecraft.util.math.Vec3d;

/**
 * Client Combat Controller for Fluid Elemental Martial Arts & Weapon Choreography.
 *
 * Implements ergonomic, weapon-specific natural swing mechanics, alternating arm motions,
 * distinct impact audio, micro-trauma camera rolls, screenshake, and authoritative server packets.
 */
public final class AvatarCombatClient {

    private static int currentStep = 0;
    private static long lastGroundAttackTime = 0L;
    private static long lastDiveKickTime = 0L;

    private AvatarCombatClient() {}

    public static boolean tryHandleAttack(MinecraftClient client) {
        if (client.player == null || client.world == null) return false;
        if (client.currentScreen != null) return false;

        ItemStack held = client.player.getMainHandStack();
        if (!isCombatHandEligible(held)) {
            return false;
        }

        // If player is interacting with an Earth Pillar, let pillar interaction take precedence
        if (CinematicVfxController.hasNearbyPillarClient(client.player.getPos(), 5.5)) {
            return false;
        }

        boolean midAir = !client.player.isOnGround() && !client.player.isTouchingWater() && !client.player.isClimbing();
        long now = System.currentTimeMillis();

        if (midAir) {
            if (now - lastDiveKickTime < 750L) {
                return false;
            }
            lastDiveKickTime = now;
            executeAerialPlunge(client, held);
            return true;
        } else {
            executeGroundCombo(client, held, now);
            return true;
        }
    }

    private static boolean isCombatHandEligible(ItemStack stack) {
        if (stack.isEmpty()) return true;
        Item item = stack.getItem();
        return item instanceof DualSwordsItem
                || item instanceof WarFanItem
                || item instanceof WaterSpearItem
                || item instanceof EarthHammerItem
                || item instanceof AirStaffItem;
    }

    private static void executeAerialPlunge(MinecraftClient client, ItemStack held) {
        Item item = held.getItem();
        Vec3d look = client.player.getRotationVec(1.0f);

        if (item instanceof EarthHammerItem) {
            // Heavy downward hammer plunge
            client.player.setVelocity(look.x * 0.35, -1.40, look.z * 0.35);
            client.player.velocityModified = true;
            AvatarAnimations.triggerComboAnimation(
                    client.player,
                    Identifier.of("avatar_elements", "earth_hammer"),
                    2,
                    EasingType.EASE_OUT_CUBIC
            );
            client.player.swingHand(Hand.MAIN_HAND);
            AvatarCameraDirector.triggerRoll(0.0f, 15);
            AvatarCameraDirector.triggerShake(0.95f, 14);
            client.player.playSound(SoundEvents.BLOCK_ANVIL_LAND, 1.0f, 0.8f);
            client.player.playSound(AvatarSounds.MARTIAL_DIVE, 1.3f, 0.9f);
        } else if (item instanceof DualSwordsItem) {
            // Twin dao fiery plunge
            client.player.setVelocity(look.x * 0.55, -1.25, look.z * 0.55);
            client.player.velocityModified = true;
            AvatarAnimations.triggerComboAnimation(
                    client.player,
                    Identifier.of("avatar_elements", "dual_swords"),
                    2,
                    EasingType.EASE_OUT_CUBIC
            );
            client.player.swingHand(Hand.MAIN_HAND);
            client.player.swingHand(Hand.OFF_HAND);
            AvatarCameraDirector.triggerRoll(12.0f, 15);
            AvatarCameraDirector.triggerShake(0.75f, 12);
            client.player.playSound(SoundEvents.ITEM_FIRECHARGE_USE, 1.1f, 1.2f);
            client.player.playSound(AvatarSounds.MARTIAL_DIVE, 1.2f, 1.0f);
        } else if (item instanceof WaterSpearItem) {
            // Streamlined harpoon torpedo dive
            client.player.setVelocity(look.x * 0.50, -1.30, look.z * 0.50);
            client.player.velocityModified = true;
            AvatarAnimations.triggerComboAnimation(
                    client.player,
                    Identifier.of("avatar_elements", "water_spear"),
                    2,
                    EasingType.EASE_OUT_CUBIC
            );
            client.player.swingHand(Hand.MAIN_HAND);
            AvatarCameraDirector.triggerRoll(-8.0f, 14);
            AvatarCameraDirector.triggerShake(0.70f, 12);
            client.player.playSound(SoundEvents.ENTITY_PLAYER_SPLASH_HIGH_SPEED, 1.0f, 1.2f);
            client.player.playSound(AvatarSounds.MARTIAL_DIVE, 1.2f, 1.1f);
        } else if (item instanceof WarFanItem) {
            // Gale glide aerial dive
            client.player.setVelocity(look.x * 0.60, -1.15, look.z * 0.60);
            client.player.velocityModified = true;
            AvatarAnimations.triggerComboAnimation(
                    client.player,
                    Identifier.of("avatar_elements", "war_fan"),
                    2,
                    EasingType.EASE_OUT_CUBIC
            );
            client.player.swingHand(Hand.MAIN_HAND);
            AvatarCameraDirector.triggerRoll(10.0f, 14);
            AvatarCameraDirector.triggerShake(0.60f, 10);
            client.player.playSound(SoundEvents.ITEM_ELYTRA_FLYING, 0.9f, 1.5f);
            client.player.playSound(AvatarSounds.MARTIAL_DIVE, 1.1f, 1.2f);
        } else if (item instanceof AirStaffItem) {
            // Staff air vault plunge
            client.player.setVelocity(look.x * 0.50, -1.25, look.z * 0.50);
            client.player.velocityModified = true;
            AvatarAnimations.triggerComboAnimation(
                    client.player,
                    Identifier.of("avatar_elements", "air_staff_attack"),
                    2,
                    EasingType.EASE_OUT_CUBIC
            );
            client.player.swingHand(Hand.MAIN_HAND);
            AvatarCameraDirector.triggerRoll(8.0f, 14);
            AvatarCameraDirector.triggerShake(0.65f, 11);
            client.player.playSound(AvatarSounds.AIR_STAFF_SWING, 1.2f, 1.1f);
            client.player.playSound(AvatarSounds.MARTIAL_DIVE, 1.2f, 1.1f);
        } else {
            // Unarmed martial dive kick
            client.player.setVelocity(look.x * 0.45, -1.25, look.z * 0.45);
            client.player.velocityModified = true;
            AvatarAnimations.triggerComboAnimation(
                    client.player,
                    Identifier.of("avatar_elements", "martial_dive_kick"),
                    2,
                    EasingType.EASE_OUT_CUBIC
            );
            client.player.swingHand(Hand.MAIN_HAND);
            AvatarCameraDirector.triggerRoll(10.0f, 15);
            AvatarCameraDirector.triggerShake(0.70f, 12);
            client.player.playSound(AvatarSounds.MARTIAL_DIVE, 1.2f, 1.0f);
        }

        CinematicVfxController.spawnTransientVfx(
                VfxType.DIVE_KICK_TRAIL,
                client.player.getPos(),
                client.player.getYaw(),
                client.player.getPitch()
        );

        ClientPlayNetworking.send(new SkillPackets.C2SMartialAttack(0, true));
    }

    private static void executeGroundCombo(MinecraftClient client, ItemStack held, long now) {
        Item item = held.getItem();
        if (item instanceof DualSwordsItem) {
            executeDualSwordsCombo(client, now);
        } else if (item instanceof EarthHammerItem) {
            executeEarthHammerCombo(client, now);
        } else if (item instanceof WarFanItem) {
            executeWarFanCombo(client, now);
        } else if (item instanceof WaterSpearItem) {
            executeWaterSpearCombo(client, now);
        } else if (item instanceof AirStaffItem) {
            executeAirStaffCombo(client, now);
        } else {
            executeUnarmedMartialCombo(client, now);
        }
    }

    private static void executeDualSwordsCombo(MinecraftClient client, long now) {
        long resetWindow = 1300L;
        currentStep = (now - lastGroundAttackTime < resetWindow) ? (currentStep + 1) % 4 : 0;
        lastGroundAttackTime = now;

        AvatarAnimations.triggerComboAnimation(
                client.player,
                Identifier.of("avatar_elements", "dual_swords"),
                2,
                EasingType.EASE_IN_OUT_CUBIC
        );

        switch (currentStep) {
            case 0 -> {
                // Right hand downward slash
                client.player.swingHand(Hand.MAIN_HAND);
                client.player.playSound(SoundEvents.ENTITY_PLAYER_ATTACK_SWEEP, 1.0f, 1.15f);
                AvatarCameraDirector.triggerRoll(3.5f, 8);
                AvatarCameraDirector.triggerShake(0.20f, 5);
            }
            case 1 -> {
                // Left hand rising slash (activates 1st & 3rd person offhand swing)
                client.player.swingHand(Hand.OFF_HAND);
                client.player.playSound(SoundEvents.ENTITY_PLAYER_ATTACK_SWEEP, 1.0f, 1.35f);
                AvatarCameraDirector.triggerRoll(-4.0f, 8);
                AvatarCameraDirector.triggerShake(0.25f, 6);
            }
            case 2 -> {
                // Dual cross slash
                client.player.swingHand(Hand.MAIN_HAND);
                client.player.playSound(SoundEvents.ENTITY_PLAYER_ATTACK_CRIT, 1.1f, 1.25f);
                client.player.playSound(SoundEvents.ITEM_ARMOR_EQUIP_IRON.value(), 0.9f, 1.4f);
                AvatarCameraDirector.triggerRoll(6.0f, 9);
                AvatarCameraDirector.triggerShake(0.40f, 7);
            }
            case 3 -> {
                // 360 Whirlwind finisher
                client.player.swingHand(Hand.MAIN_HAND);
                client.player.swingHand(Hand.OFF_HAND);
                client.player.playSound(AvatarSounds.FLAME_SWEEP_SLASH, 1.2f, 1.0f);
                client.player.playSound(AvatarSounds.HITSTOP_IMPACT, 1.2f, 1.35f);
                AvatarCameraDirector.triggerRoll(-10.0f, 12);
                AvatarCameraDirector.triggerShake(0.70f, 12);
                spawnImpactVfx(client);
            }
        }

        ClientPlayNetworking.send(new SkillPackets.C2SMartialAttack(currentStep, false));
    }

    private static void executeEarthHammerCombo(MinecraftClient client, long now) {
        long resetWindow = 1600L; // Deliberate heavy rhythm
        currentStep = (now - lastGroundAttackTime < resetWindow) ? (currentStep + 1) % 4 : 0;
        lastGroundAttackTime = now;

        AvatarAnimations.triggerComboAnimation(
                client.player,
                Identifier.of("avatar_elements", "earth_hammer"),
                2,
                EasingType.EASE_IN_OUT_CUBIC
        );

        client.player.swingHand(Hand.MAIN_HAND);

        switch (currentStep) {
            case 0 -> {
                client.player.playSound(SoundEvents.ENTITY_PLAYER_ATTACK_STRONG, 1.0f, 0.8f);
                client.player.playSound(SoundEvents.BLOCK_DEEPSLATE_HIT, 1.1f, 0.9f);
                AvatarCameraDirector.triggerRoll(-3.5f, 8);
                AvatarCameraDirector.triggerShake(0.35f, 6);
            }
            case 1 -> {
                client.player.playSound(SoundEvents.BLOCK_STONE_BREAK, 1.0f, 1.1f);
                client.player.playSound(SoundEvents.ENTITY_PLAYER_ATTACK_KNOCKBACK, 1.0f, 0.9f);
                AvatarCameraDirector.triggerRoll(4.5f, 9);
                AvatarCameraDirector.triggerShake(0.45f, 7);
            }
            case 2 -> {
                client.player.playSound(AvatarSounds.EARTH_BOULDER_LAUNCH, 1.1f, 1.15f);
                AvatarCameraDirector.triggerRoll(-2.0f, 8);
                AvatarCameraDirector.triggerShake(0.50f, 8);
            }
            case 3 -> {
                // Seismic ground slam finisher (massive screen crunch)
                client.player.playSound(AvatarSounds.EARTH_IMPACT_HEAVY, 1.3f, 1.0f);
                client.player.playSound(SoundEvents.BLOCK_ANVIL_LAND, 1.0f, 0.75f);
                client.player.playSound(AvatarSounds.HITSTOP_IMPACT, 1.3f, 0.75f);
                AvatarCameraDirector.triggerRoll(0.0f, 14);
                AvatarCameraDirector.triggerShake(0.95f, 14);
                spawnImpactVfx(client);
            }
        }

        ClientPlayNetworking.send(new SkillPackets.C2SMartialAttack(currentStep, false));
    }

    private static void executeWarFanCombo(MinecraftClient client, long now) {
        long resetWindow = 900L; // Rapid, nimble pace
        currentStep = (now - lastGroundAttackTime < resetWindow) ? (currentStep + 1) % 4 : 0;
        lastGroundAttackTime = now;

        AvatarAnimations.triggerComboAnimation(
                client.player,
                Identifier.of("avatar_elements", "war_fan"),
                2,
                EasingType.EASE_IN_OUT_CUBIC
        );

        switch (currentStep) {
            case 0 -> {
                client.player.swingHand(Hand.MAIN_HAND);
                client.player.playSound(SoundEvents.ENTITY_PLAYER_ATTACK_SWEEP, 0.9f, 1.5f);
                AvatarCameraDirector.triggerRoll(4.0f, 7);
                AvatarCameraDirector.triggerShake(0.15f, 4);
            }
            case 1 -> {
                client.player.swingHand(Hand.OFF_HAND);
                client.player.playSound(SoundEvents.ENTITY_PLAYER_ATTACK_SWEEP, 0.9f, 1.7f);
                AvatarCameraDirector.triggerRoll(-5.0f, 8);
                AvatarCameraDirector.triggerShake(0.20f, 5);
            }
            case 2 -> {
                client.player.swingHand(Hand.MAIN_HAND);
                client.player.playSound(SoundEvents.ENTITY_PLAYER_ATTACK_CRIT, 1.0f, 1.5f);
                AvatarCameraDirector.triggerRoll(6.0f, 8);
                AvatarCameraDirector.triggerShake(0.35f, 6);
            }
            case 3 -> {
                // Cyclone gale spin finisher
                client.player.swingHand(Hand.MAIN_HAND);
                client.player.playSound(AvatarSounds.AIR_STAFF_SWING, 1.2f, 1.6f);
                client.player.playSound(AvatarSounds.HITSTOP_IMPACT, 1.1f, 1.5f);
                AvatarCameraDirector.triggerRoll(-9.0f, 10);
                AvatarCameraDirector.triggerShake(0.55f, 10);
                spawnImpactVfx(client);
            }
        }

        ClientPlayNetworking.send(new SkillPackets.C2SMartialAttack(currentStep, false));
    }

    private static void executeWaterSpearCombo(MinecraftClient client, long now) {
        long resetWindow = 1100L;
        currentStep = (now - lastGroundAttackTime < resetWindow) ? (currentStep + 1) % 4 : 0;
        lastGroundAttackTime = now;

        AvatarAnimations.triggerComboAnimation(
                client.player,
                Identifier.of("avatar_elements", "water_spear"),
                2,
                EasingType.EASE_IN_OUT_CUBIC
        );

        switch (currentStep) {
            case 0 -> {
                client.player.swingHand(Hand.MAIN_HAND);
                client.player.playSound(AvatarSounds.WATER_WHIP_LASH, 1.0f, 1.35f);
                AvatarCameraDirector.triggerRoll(2.5f, 7);
                AvatarCameraDirector.triggerShake(0.20f, 5);
            }
            case 1 -> {
                client.player.swingHand(Hand.MAIN_HAND);
                client.player.playSound(SoundEvents.ENTITY_PLAYER_ATTACK_SWEEP, 0.9f, 1.1f);
                client.player.playSound(AvatarSounds.WATER_SPLASH_IMPACT, 0.9f, 1.4f);
                AvatarCameraDirector.triggerRoll(-4.0f, 8);
                AvatarCameraDirector.triggerShake(0.25f, 6);
            }
            case 2 -> {
                client.player.swingHand(Hand.OFF_HAND);
                client.player.playSound(AvatarSounds.WATER_WHIP_LASH, 1.1f, 1.15f);
                AvatarCameraDirector.triggerRoll(5.0f, 8);
                AvatarCameraDirector.triggerShake(0.35f, 7);
            }
            case 3 -> {
                // Surging tidal burst finisher
                client.player.swingHand(Hand.MAIN_HAND);
                client.player.playSound(AvatarSounds.WATER_SPLASH_IMPACT, 1.2f, 0.9f);
                client.player.playSound(AvatarSounds.HITSTOP_IMPACT, 1.2f, 1.2f);
                AvatarCameraDirector.triggerRoll(-7.5f, 11);
                AvatarCameraDirector.triggerShake(0.65f, 11);
                spawnImpactVfx(client);
            }
        }

        ClientPlayNetworking.send(new SkillPackets.C2SMartialAttack(currentStep, false));
    }

    private static void executeAirStaffCombo(MinecraftClient client, long now) {
        long resetWindow = 1100L;
        currentStep = (now - lastGroundAttackTime < resetWindow) ? (currentStep + 1) % 4 : 0;
        lastGroundAttackTime = now;

        AvatarAnimations.triggerComboAnimation(
                client.player,
                Identifier.of("avatar_elements", "air_staff_attack"),
                2,
                EasingType.EASE_IN_OUT_CUBIC
        );

        switch (currentStep) {
            case 0 -> {
                client.player.swingHand(Hand.MAIN_HAND);
                client.player.playSound(AvatarSounds.AIR_STAFF_SWING, 1.0f, 1.0f);
                AvatarCameraDirector.triggerRoll(-3.5f, 7);
                AvatarCameraDirector.triggerShake(0.20f, 5);
            }
            case 1 -> {
                client.player.swingHand(Hand.OFF_HAND);
                client.player.playSound(AvatarSounds.AIR_STAFF_SWING, 1.0f, 1.25f);
                AvatarCameraDirector.triggerRoll(4.0f, 8);
                AvatarCameraDirector.triggerShake(0.25f, 6);
            }
            case 2 -> {
                client.player.swingHand(Hand.MAIN_HAND);
                client.player.playSound(AvatarSounds.AIR_STAFF_SWING, 1.1f, 1.45f);
                AvatarCameraDirector.triggerRoll(-5.5f, 8);
                AvatarCameraDirector.triggerShake(0.35f, 7);
            }
            case 3 -> {
                // Kinetic air burst finisher
                client.player.swingHand(Hand.MAIN_HAND);
                client.player.playSound(AvatarSounds.AIR_STAFF_SWING, 1.3f, 0.8f);
                client.player.playSound(AvatarSounds.HITSTOP_IMPACT, 1.2f, 1.4f);
                AvatarCameraDirector.triggerRoll(8.5f, 10);
                AvatarCameraDirector.triggerShake(0.60f, 10);
                spawnImpactVfx(client);
            }
        }

        ClientPlayNetworking.send(new SkillPackets.C2SMartialAttack(currentStep, false));
    }

    private static void executeUnarmedMartialCombo(MinecraftClient client, long now) {
        long resetWindow = 1200L;
        currentStep = (now - lastGroundAttackTime < resetWindow) ? (currentStep + 1) % 4 : 0;
        lastGroundAttackTime = now;

        String animName = switch (currentStep) {
            case 1 -> "martial_cross";
            case 2 -> "martial_lowkick";
            case 3 -> "martial_roundhouse";
            default -> "martial_jab";
        };

        AvatarAnimations.triggerComboAnimation(
                client.player,
                Identifier.of("avatar_elements", animName),
                2,
                EasingType.EASE_IN_OUT_CUBIC
        );

        if (currentStep % 2 == 0) {
            client.player.swingHand(Hand.MAIN_HAND);
        } else {
            client.player.swingHand(Hand.OFF_HAND);
        }

        if (currentStep == 3) {
            client.player.playSound(AvatarSounds.MARTIAL_KICK, 1.1f, 1.0f);
            client.player.playSound(AvatarSounds.HITSTOP_IMPACT, 1.2f, 1.4f);
            AvatarCameraDirector.triggerRoll(-8.0f, 10);
            AvatarCameraDirector.triggerShake(0.50f, 8);
            spawnImpactVfx(client);
        } else if (currentStep == 2) {
            client.player.playSound(AvatarSounds.MARTIAL_KICK, 1.0f, 1.2f);
            AvatarCameraDirector.triggerRoll(-5.0f, 8);
            AvatarCameraDirector.triggerShake(0.25f, 5);
        } else if (currentStep == 1) {
            client.player.playSound(AvatarSounds.MARTIAL_PUNCH, 0.9f, 1.3f);
            AvatarCameraDirector.triggerRoll(4.0f, 7);
            AvatarCameraDirector.triggerShake(0.20f, 5);
        } else {
            client.player.playSound(AvatarSounds.MARTIAL_PUNCH, 0.9f, 1.2f);
            AvatarCameraDirector.triggerRoll(2.5f, 6);
            AvatarCameraDirector.triggerShake(0.15f, 4);
        }

        ClientPlayNetworking.send(new SkillPackets.C2SMartialAttack(currentStep, false));
    }

    private static void spawnImpactVfx(MinecraftClient client) {
        Vec3d look = client.player.getRotationVec(1.0f);
        Vec3d impactPos = client.player.getPos().add(look.multiply(1.5));
        CinematicVfxController.spawnTransientVfx(
                VfxType.MARTIAL_SHOCKWAVE,
                impactPos,
                client.player.getYaw(),
                client.player.getPitch()
        );
        CinematicVfxController.spawnTransientVfx(
                VfxType.HITSTOP_FLASH,
                impactPos.add(0, 1.0, 0),
                client.player.getYaw(),
                client.player.getPitch()
        );
    }
}
