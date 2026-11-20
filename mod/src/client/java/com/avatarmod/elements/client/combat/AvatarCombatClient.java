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
import net.minecraft.util.Hand;
import net.minecraft.util.Identifier;
import net.minecraft.util.math.Vec3d;

/**
 * Client Combat Controller for Fluid Elemental Martial Arts Combos & Aerial Dive-Kicks.
 * Intercepts attack input when unarmed or holding an Avatar weapon, triggering authentic
 * PAL animations, alternating swings, directional audio, and authoritative server packets.
 */
public final class AvatarCombatClient {

    private static int currentStep = 0;
    private static long lastGroundAttackTime = 0L;
    private static long lastDiveKickTime = 0L;
    private static final long COMBO_RESET_WINDOW_MS = 1200L;

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
            executeAerialDiveKick(client);
            return true;
        } else {
            executeGroundCombo(client, now);
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

    private static void executeAerialDiveKick(MinecraftClient client) {
        Vec3d look = client.player.getRotationVec(1.0f);
        // Downward plunge velocity
        client.player.setVelocity(look.x * 0.45, -1.25, look.z * 0.45);
        client.player.velocityModified = true;

        AvatarAnimations.triggerComboAnimation(
                client.player,
                Identifier.of("avatar_elements", "martial_dive_kick"),
                2,
                EasingType.EASE_OUT_CUBIC
        );

        AvatarCameraDirector.triggerRoll(10.0f, 15);
        AvatarCameraDirector.triggerShake(0.7f, 12);
        CinematicVfxController.spawnTransientVfx(
                VfxType.DIVE_KICK_TRAIL,
                client.player.getPos(),
                client.player.getYaw(),
                client.player.getPitch()
        );

        client.player.playSound(AvatarSounds.MARTIAL_DIVE, 1.2f, 1.0f);
        ClientPlayNetworking.send(new SkillPackets.C2SMartialAttack(0, true));
    }

    private static void executeGroundCombo(MinecraftClient client, long now) {
        if (now - lastGroundAttackTime < COMBO_RESET_WINDOW_MS) {
            currentStep = (currentStep + 1) % 4;
        } else {
            currentStep = 0;
        }
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

        // Alternating visual arm swing
        if (currentStep % 2 == 0) {
            client.player.swingHand(Hand.MAIN_HAND);
        } else {
            client.player.swingHand(Hand.OFF_HAND);
        }

        // SFX, VFX & Camera Impact
        if (currentStep == 3) {
            client.player.playSound(AvatarSounds.MARTIAL_KICK, 1.1f, 1.0f);
            client.player.playSound(AvatarSounds.HITSTOP_IMPACT, 1.2f, 1.4f);
            AvatarCameraDirector.triggerRoll(-8.0f, 10);
            AvatarCameraDirector.triggerShake(0.5f, 8);

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
        } else if (currentStep == 2) {
            client.player.playSound(AvatarSounds.MARTIAL_KICK, 1.0f, 1.2f);
        } else {
            client.player.playSound(AvatarSounds.MARTIAL_PUNCH, 0.9f, 1.2f + (currentStep * 0.1f));
        }

        ClientPlayNetworking.send(new SkillPackets.C2SMartialAttack(currentStep, false));
    }
}
