package com.avatarmod.elements.client.anim;

import com.zigythebird.playeranim.animation.PlayerAnimResources;
import com.zigythebird.playeranim.animation.PlayerAnimationController;
import com.zigythebird.playeranim.api.PlayerAnimationAccess;
import com.zigythebird.playeranim.api.PlayerAnimationFactory;
import com.zigythebird.playeranimcore.animation.AnimationController;
import com.zigythebird.playeranimcore.animation.AnimationController.AnimationSetter;
import com.zigythebird.playeranimcore.animation.AnimationData;
import com.zigythebird.playeranimcore.animation.layered.modifier.AbstractFadeModifier;
import com.zigythebird.playeranimcore.easing.EasingType;
import com.zigythebird.playeranimcore.enums.PlayState;
import net.minecraft.client.network.AbstractClientPlayerEntity;
import net.minecraft.util.Identifier;

/**
 * PAL (Player Animation Library) registration and combat choreography helpers.
 *
 * Layer priority 1000 — below PAL's own PlayerModelMixin (2001) but above vanilla.
 * Unified COMBAT_LAYER_ID ensures combat animations chain seamlessly without mid-combo snapping
 * to vanilla idle/T-pose.
 */
public final class AvatarAnimations {

    public static final Identifier COMBAT_LAYER_ID =
            Identifier.of("avatar_elements", "combat_layer");

    // Aliased for backward compatibility with Milestone 1-5 tests and call-sites
    public static final Identifier FIRE_JAB_LAYER_ID = COMBAT_LAYER_ID;

    private static final Identifier FIRE_JAB_ANIM_ID =
            Identifier.of("avatar_elements", "fire_jab_test");

    private static final boolean DEBUG = Boolean.getBoolean("avatar.debug.anim");

    private static void debugLog(String message) {
        if (DEBUG) {
            System.out.println("[Avatar DEBUG] " + message);
        }
    }

    public static void register() {
        PlayerAnimationFactory.ANIMATION_DATA_FACTORY.registerFactory(
                COMBAT_LAYER_ID,
                1000,
                player -> new PlayerAnimationController(
                        player,
                        (AnimationController controller, AnimationData state, AnimationSetter setter) -> {
                            if (controller instanceof PlayerAnimationController pac && pac.isPlayingTriggeredAnimation()) {
                                return PlayState.CONTINUE;
                            }
                            return PlayState.STOP;
                        }
                )
        );
    }

    /**
     * Resolves an animation Identifier, verifying presence in PAL PlayerAnimResources.
     * Checks both exact identifier and namespace-prefixed variants.
     */
    public static Identifier resolveAnimationId(Identifier animId) {
        if (animId == null) {
            return null;
        }
        if (PlayerAnimResources.hasAnimation(animId)) {
            debugLog("resolveAnimationId: exact match " + animId);
            return animId;
        }

        // Check canonical Bedrock full key: animation.avatar_elements.<path>
        Identifier fullId = Identifier.of(animId.getNamespace(), "animation." + animId.getNamespace() + "." + animId.getPath());
        if (PlayerAnimResources.hasAnimation(fullId)) {
            debugLog("resolveAnimationId: full key match " + fullId);
            return fullId;
        }

        // Check short path if animId contains full prefix
        String path = animId.getPath();
        String prefix = "animation." + animId.getNamespace() + ".";
        if (path.startsWith(prefix)) {
            String shortPath = path.substring(prefix.length());
            Identifier shortId = Identifier.of(animId.getNamespace(), shortPath);
            if (PlayerAnimResources.hasAnimation(shortId)) {
                debugLog("resolveAnimationId: short path match " + shortId);
                return shortId;
            }
        }

        // Dynamic match: scan loaded animations for path matching
        debugLog("resolveAnimationId: scanning " + PlayerAnimResources.getAnimations().size() + " loaded animations for " + animId);
        for (Identifier id : PlayerAnimResources.getAnimations().keySet()) {
            if (id.getNamespace().equals(animId.getNamespace())) {
                String p = id.getPath();
                if (p.endsWith(animId.getPath()) || p.contains(animId.getPath())) {
                    debugLog("resolveAnimationId: dynamic match " + id);
                    return id;
                }
            }
        }

        debugLog("resolveAnimationId: NO MATCH for " + animId);
        return null;
    }

    public static boolean hasAnimation(Identifier animId) {
        return resolveAnimationId(animId) != null;
    }

    /**
     * Plays a combo animation on COMBAT_LAYER_ID.
     * If an animation is already running, uses replaceAnimationWithFade and standardFadeIn
     * to cross-fade bone snapshots without snapping to idle/T-pose.
     */
    public static boolean triggerComboAnimation(AbstractClientPlayerEntity player, Identifier animId, int blendTicks, EasingType easing) {
        if (player == null || animId == null) {
            return false;
        }

        Identifier resolved = resolveAnimationId(animId);
        if (resolved == null) {
            // Graceful fallback when asset is not loaded/found, preventing NPE
            debugLog("Failed to resolve animation: " + animId);
            return false;
        }

        var layer = PlayerAnimationAccess.getPlayerAnimationLayer(player, COMBAT_LAYER_ID);
        if (layer instanceof PlayerAnimationController controller) {
            if (blendTicks > 0 && easing != null && controller.isPlayingTriggeredAnimation()) {
                AbstractFadeModifier fadeModifier = AbstractFadeModifier.standardFadeIn(blendTicks, easing);
                boolean result = controller.replaceAnimationWithFade(fadeModifier, resolved);
                debugLog("replaceAnimationWithFade(" + resolved + ") = " + result);
                return result;
            } else {
                boolean result = controller.triggerAnimation(resolved);
                debugLog("triggerAnimation(" + resolved + ") = " + result);
                return result;
            }
        }

        debugLog("Layer not PlayerAnimationController: " + layer);
        return false;
    }

    public static boolean triggerComboAnimation(AbstractClientPlayerEntity player, Identifier animId) {
        return triggerComboAnimation(player, animId, 3, EasingType.EASE_IN_OUT_CUBIC);
    }

    /**
     * Directly triggers an animation for a skill on the client player without phase constraints.
     */
    public static boolean triggerSkill(AbstractClientPlayerEntity player, String skillId) {
        if (player == null || skillId == null) {
            return false;
        }
        if ("avatar:fire_jab".equals(skillId)) {
            triggerFireJab(player);
            return true;
        }
        Identifier animId = getAnimationForSkill(skillId);
        if (animId == null) {
            return false;
        }
        return triggerComboAnimation(player, animId);
    }

    /**
     * Dispatches skill phase to corresponding martial arts animation clip.
     */
    public static boolean triggerSkillAnimation(AbstractClientPlayerEntity player, String skillId, String phase) {
        if (player == null || skillId == null) {
            return false;
        }

        // Trigger animations during WINDUP, HOLD, or ACTIVE phase transitions
        if (!"WINDUP".equals(phase) && !"ACTIVE".equals(phase) && !"HOLD".equals(phase)) {
            return false;
        }

        Identifier animId = getAnimationForSkill(skillId);
        if (animId == null) {
            debugLog("Animation ID null for skill: " + skillId);
            return false;
        }

        boolean result = triggerComboAnimation(player, animId, 3, EasingType.EASE_IN_OUT_CUBIC);
        debugLog("triggerSkillAnimation(" + skillId + ", " + phase + ") -> " + animId + " = " + result);
        return result;
    }

    /**
     * Maps a skill identifier (e.g. "avatar:flame_sweep") to the target PAL animation Identifier.
     */
    public static Identifier getAnimationForSkill(String skillId) {
        if (skillId == null || skillId.isEmpty()) {
            return null;
        }

        String clean = skillId.toLowerCase();
        if (clean.startsWith("avatar:")) {
            clean = clean.substring("avatar:".length());
        } else if (clean.startsWith("avatar_elements:")) {
            clean = clean.substring("avatar_elements:".length());
        }

        if ("fire_jab".equals(clean)) {
            Identifier fullId = Identifier.of("avatar_elements", "fire_jab");
            if (PlayerAnimResources.hasAnimation(fullId)) {
                return fullId;
            }
            Identifier testId = Identifier.of("avatar_elements", "fire_jab_test");
            if (PlayerAnimResources.hasAnimation(testId)) {
                return testId;
            }
            return fullId;
        }

        return Identifier.of("avatar_elements", clean);
    }

    /**
     * Returns the canonical martial arts discipline for a given skill.
     */
    public static String getCanonicalDiscipline(String skillId) {
        if (skillId == null || skillId.isEmpty()) {
            return "Unknown Martial Art";
        }
        String s = skillId.toLowerCase();
        if (s.contains("fire") || s.contains("flame") || s.contains("lightning")) {
            return "Northern Shaolin / Boxing / Capoeira";
        } else if (s.contains("air") || s.contains("vortex") || s.contains("scooter") || s.contains("staff") || s.contains("palm")) {
            return "Baguazhang";
        } else if (s.contains("water") || s.contains("octopus") || s.contains("whip")) {
            return "Tai Chi";
        } else if (s.contains("earth") || s.contains("boulder") || s.contains("wall")) {
            return "Hung Gar / Southern Mantis";
        }
        return "Unknown Martial Art";
    }

    /** Call on the client thread when a fire_jab cast is confirmed or synced by the server. */
    public static void triggerFireJab(AbstractClientPlayerEntity player) {
        if (player == null) return;
        Identifier animId = Identifier.of("avatar_elements", "fire_jab");
        if (!PlayerAnimResources.hasAnimation(animId)) {
            animId = Identifier.of("avatar_elements", "fire_jab_test");
        }
        triggerComboAnimation(player, animId, 0, EasingType.LINEAR);
    }

    /** Checks whether any combat animation is currently playing on the given player. */
    public static boolean isPlayingAnimation(AbstractClientPlayerEntity player) {
        if (player == null) return false;
        var layer = PlayerAnimationAccess.getPlayerAnimationLayer(player, COMBAT_LAYER_ID);
        if (layer instanceof PlayerAnimationController controller) {
            return controller.isPlayingTriggeredAnimation();
        }
        return false;
    }

    /** Checks whether the fire_jab animation is currently playing on the given player. */
    public static boolean isFireJabPlaying(AbstractClientPlayerEntity player) {
        return isPlayingAnimation(player);
    }

    private AvatarAnimations() {}
}
