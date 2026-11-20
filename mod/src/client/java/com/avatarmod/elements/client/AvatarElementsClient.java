package com.avatarmod.elements.client;

import com.avatarmod.elements.AvatarElementsMod;
import com.avatarmod.elements.client.anim.AvatarAnimations;
import com.avatarmod.elements.client.hud.AvatarHudRenderer;
import com.avatarmod.elements.client.hud.ElementWheelRenderer;
import com.avatarmod.elements.client.input.AvatarKeyBindings;
import com.avatarmod.elements.client.network.ClientNetworkHandler;
import com.avatarmod.elements.client.network.SkillClientHandler;
import com.avatarmod.elements.client.screen.ElementSelectorScreen;
import com.avatarmod.elements.client.orb.ChargeOrbClientState;
import com.avatarmod.elements.client.orb.ChargeOrbRenderer;
import com.avatarmod.elements.client.orb.FirstPersonOrbRenderer;
import com.avatarmod.elements.client.particle.AvatarClientParticles;
import com.avatarmod.elements.client.vfx.CinematicVfxController;
import com.avatarmod.elements.skill.ElementSlotMap;
import com.avatarmod.elements.skill.SkillRegistry;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayConnectionEvents;
import com.avatarmod.elements.network.SkillPackets;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientWorldEvents;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.minecraft.client.option.KeyBinding;

public class AvatarElementsClient implements ClientModInitializer {

    @Override
    public void onInitializeClient() {
        AvatarElementsMod.LOGGER.info("Avatar: Elements initializing (client)");
        AvatarAnimations.register();
        AvatarKeyBindings.register();
        ClientNetworkHandler.register();
        SkillClientHandler.register();
        AvatarHudRenderer.register();
        ChargeOrbRenderer.register();
        FirstPersonOrbRenderer.register();
        AvatarClientParticles.registerClientFactories();

        net.fabricmc.fabric.api.client.rendering.v1.EntityRendererRegistry.register(
                AvatarElementsMod.FIRE_BLAST_PROJECTILE,
                context -> new net.minecraft.client.render.entity.EntityRenderer<com.avatarmod.elements.entity.FireBlastProjectileEntity>(context) {
                    @Override
                    public net.minecraft.util.Identifier getTexture(com.avatarmod.elements.entity.FireBlastProjectileEntity entity) {
                        return null;
                    }
                });

        // Clear orb state on disconnect or world change to avoid stale visuals
        ClientPlayConnectionEvents.DISCONNECT.register((handler, client) -> {
            ChargeOrbClientState.clear();
            CinematicVfxController.clear();
            java.util.Arrays.fill(slotHolding, false);
            java.util.Arrays.fill(slotHoldTicks, 0);
            java.util.Arrays.fill(slotHeldSkillId, null);
        });
        // JOIN clears stale state from a previous session/world
        ClientPlayConnectionEvents.JOIN.register((handler, sender, client) -> {
            ChargeOrbClientState.clear();
            CinematicVfxController.clear();
            java.util.Arrays.fill(slotHolding, false);
            java.util.Arrays.fill(slotHoldTicks, 0);
            java.util.Arrays.fill(slotHeldSkillId, null);
        });
        // Dimension / world transition cleanup: wipe stale orbs from previous world
        ClientWorldEvents.AFTER_CLIENT_WORLD_CHANGE.register((client, world) -> {
            ChargeOrbClientState.clear();
            CinematicVfxController.clear();
            java.util.Arrays.fill(slotHolding, false);
            java.util.Arrays.fill(slotHoldTicks, 0);
            java.util.Arrays.fill(slotHeldSkillId, null);
        });

        ClientTickEvents.END_CLIENT_TICK.register(client -> {
            CinematicVfxController.tick(client);
            com.avatarmod.elements.client.camera.AvatarCameraDirector.tick();

            if (client.player == null) return;

            while (AvatarKeyBindings.ELEMENT_SELECTOR.wasPressed()) {
                if (client.currentScreen == null) {
                    client.setScreen(new ElementSelectorScreen());
                }
            }

            // --- Element wheel: cycle to next element with debounce ---
            // Continuously drain buffered presses so queued keys (from typing in chat or opening menus) never fire later
            while (AvatarKeyBindings.ELEMENT_WHEEL.wasPressed()) {}

            if (elementCycleCooldown > 0) {
                elementCycleCooldown--;
            }

            int wheelCode = getKeyCode(AvatarKeyBindings.ELEMENT_WHEEL);
            boolean wheelDown = (client.currentScreen == null) && (wheelCode > 0)
                    && net.minecraft.client.util.InputUtil.isKeyPressed(client.getWindow().getHandle(), wheelCode);

            if (wheelDown && !wheelWasDown && elementCycleCooldown == 0) {
                elementCycleCooldown = 6; // 300ms debounce
                ClientPlayNetworking.send(new SkillPackets.C2SCycleElement());
            }
            wheelWasDown = wheelDown;

            // --- Skill slot keys (Z/X/C/V/B) ---
            handleSlotKey(client, 0, AvatarKeyBindings.SLOT_1);
            handleSlotKey(client, 1, AvatarKeyBindings.SLOT_2);
            handleSlotKey(client, 2, AvatarKeyBindings.SLOT_3);
            handleSlotKey(client, 3, AvatarKeyBindings.SLOT_4);
            handleSlotKey(client, 4, AvatarKeyBindings.SLOT_5);

            // --- Attack key interaction with Earth Pillar (Left Click) ---
            if (client.currentScreen == null && client.options.attackKey.wasPressed()) {
                if (CinematicVfxController.hasNearbyPillarClient(client.player.getPos(), 5.5)) {
                    int action = (client.player.isSneaking() || client.player.isSprinting()) ? 0 : 1;
                    SkillClientHandler.sendPillarInteract(action);
                    client.player.swingHand(net.minecraft.util.Hand.MAIN_HAND);
                    if (action == 0) {
                        var animId = AvatarAnimations.getAnimationForSkill("earth_boulder");
                        if (animId != null) AvatarAnimations.triggerComboAnimation(client.player, animId);
                    } else {
                        var animId = AvatarAnimations.getAnimationForSkill("fire_jab");
                        if (animId != null) AvatarAnimations.triggerComboAnimation(client.player, animId);
                    }
                }
            }
        });
    }

    private static boolean wheelWasDown = false;
    private static int elementCycleCooldown = 0;
    private static final boolean[] slotHolding = new boolean[5];
    private static final int[] slotHoldTicks = new int[5];
    private static final String[] slotHeldSkillId = new String[5];
    private static final boolean[] slotWasDown = new boolean[5];

    private static int getKeyCode(KeyBinding key) {
        try {
            int code = net.minecraft.client.util.InputUtil.fromTranslationKey(key.getBoundKeyTranslationKey()).getCode();
            if (code > 0) return code;
        } catch (Exception ignored) {}
        return key.getDefaultKey().getCode();
    }

    private static boolean isSlotKeyDown(net.minecraft.client.MinecraftClient client, KeyBinding key) {
        if (client.currentScreen != null) return false;
        long windowHandle = client.getWindow().getHandle();
        int code = getKeyCode(key);
        boolean glfwPressed = (code > 0) && net.minecraft.client.util.InputUtil.isKeyPressed(windowHandle, code);
        return glfwPressed || key.isPressed();
    }

    private static void handleSlotKey(net.minecraft.client.MinecraftClient client, int slot, KeyBinding key) {
        String activeElement = ElementWheelRenderer.getCurrentElement();
        String skillId = ElementSlotMap.getSkillId(activeElement, slot);
        boolean isHoldSkill = false;
        if (skillId != null) {
            var optDef = SkillRegistry.get(skillId);
            if (optDef.isPresent() && optDef.get().isHoldRelease()) {
                isHoldSkill = true;
            }
        }

        // Guard: Cancel holds immediately when a GUI screen is opened
        if (client.currentScreen != null) {
            if (slotHolding[slot]) {
                slotHolding[slot] = false;
                String heldId = slotHeldSkillId[slot];
                slotHeldSkillId[slot] = null;
                SkillClientHandler.sendHoldRelease(slot, heldId != null ? heldId : "");
                slotHoldTicks[slot] = 0;
            }
            slotWasDown[slot] = false;
            while (key.wasPressed()) {}
            return;
        }

        boolean isDown = isSlotKeyDown(client, key);
        boolean tapped = drainPressed(key);
        boolean justPressed = (isDown && !slotWasDown[slot]) || tapped;
        boolean justReleased = (!isDown && slotWasDown[slot]);
        slotWasDown[slot] = isDown;

        // Interactive Earth Pillar manipulation via Earth slots (Z=Strike, X/C=Kick)
        if ("EARTH".equals(activeElement) && client.player != null
                && CinematicVfxController.hasNearbyPillarClient(client.player.getPos(), 5.5)) {
            if ((slot == 1 || slot == 2) && justPressed) {
                SkillClientHandler.sendPillarInteract(0);
                client.player.swingHand(net.minecraft.util.Hand.MAIN_HAND);
                var animId = AvatarAnimations.getAnimationForSkill("earth_boulder");
                if (animId != null) AvatarAnimations.triggerComboAnimation(client.player, animId);
                return;
            } else if (slot == 0 && justPressed) {
                SkillClientHandler.sendPillarInteract(1);
                client.player.swingHand(net.minecraft.util.Hand.MAIN_HAND);
                var animId = AvatarAnimations.getAnimationForSkill("fire_jab");
                if (animId != null) AvatarAnimations.triggerComboAnimation(client.player, animId);
                return;
            }
        }

        if (isHoldSkill) {
            if (justPressed) {
                if (!slotHolding[slot]) {
                    // Rising edge
                    slotHolding[slot] = true;
                    slotHoldTicks[slot] = 1;
                    slotHeldSkillId[slot] = skillId;
                    SkillClientHandler.sendHoldStart(slot, skillId);

                    // Sub-tick quick tap (< 50ms): key was tapped and released before tick
                    if (!isDown) {
                        slotHolding[slot] = false;
                        slotHeldSkillId[slot] = null;
                        SkillClientHandler.sendHoldRelease(slot, skillId);
                        slotHoldTicks[slot] = 0;
                    }
                }
            } else if (isDown && slotHolding[slot]) {
                slotHoldTicks[slot]++;
            } else if (justReleased) {
                // Falling edge: key released
                if (slotHolding[slot]) {
                    slotHolding[slot] = false;
                    String heldId = slotHeldSkillId[slot] != null ? slotHeldSkillId[slot] : skillId;
                    slotHeldSkillId[slot] = null;
                    SkillClientHandler.sendHoldRelease(slot, heldId);
                    slotHoldTicks[slot] = 0;
                }
            }
        } else {
            // Instant cast
            if (slotHolding[slot]) {
                slotHolding[slot] = false;
                String heldId = slotHeldSkillId[slot] != null ? slotHeldSkillId[slot] : skillId;
                slotHeldSkillId[slot] = null;
                SkillClientHandler.sendHoldRelease(slot, heldId);
                slotHoldTicks[slot] = 0;
            }
            if (justPressed) {
                SkillClientHandler.sendSlotCast(slot);
            }
        }
    }

    /** Drain all queued key-press events; return true if at least one was queued. */
    private static boolean drainPressed(KeyBinding key) {
        boolean any = false;
        while (key.wasPressed()) any = true;
        return any;
    }

}
