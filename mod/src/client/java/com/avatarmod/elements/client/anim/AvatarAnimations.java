package com.avatarmod.elements.client.anim;

import com.zigythebird.playeranim.animation.PlayerAnimationController;
import com.zigythebird.playeranim.api.PlayerAnimationAccess;
import com.zigythebird.playeranim.api.PlayerAnimationFactory;
import com.zigythebird.playeranimcore.animation.AnimationController;
import com.zigythebird.playeranimcore.animation.AnimationController.AnimationSetter;
import com.zigythebird.playeranimcore.animation.AnimationData;
import com.zigythebird.playeranimcore.enums.PlayState;
import net.minecraft.client.network.AbstractClientPlayerEntity;
import net.minecraft.util.Identifier;

/**
 * PAL (Player Animation Library) registration and trigger helpers.
 *
 * Layer priority 1000 — below PAL's own PlayerModelMixin (2001) but above vanilla.
 * State handler returns STOP by default; animations fire only via triggerFireJab().
 */
public final class AvatarAnimations {

    public static final Identifier FIRE_JAB_LAYER_ID =
            Identifier.of("avatar_elements", "fire_jab_layer");

    // Identifier matches namespace + animation name key inside the JSON file
    private static final Identifier FIRE_JAB_ANIM_ID =
            Identifier.of("avatar_elements", "fire_jab_test");

    public static void register() {
        PlayerAnimationFactory.ANIMATION_DATA_FACTORY.registerFactory(
                FIRE_JAB_LAYER_ID,
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

    /** Call on the client thread when a fire_jab cast is confirmed by the server. */
    public static void triggerFireJab(AbstractClientPlayerEntity player) {
        var layer = PlayerAnimationAccess.getPlayerAnimationLayer(player, FIRE_JAB_LAYER_ID);
        if (layer instanceof PlayerAnimationController controller) {
            controller.triggerAnimation(FIRE_JAB_ANIM_ID);
        }
    }

    private AvatarAnimations() {}
}
