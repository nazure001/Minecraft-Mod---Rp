package com.avatarmod.elements.client.camera;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class AvatarCameraDirectorTest {

    @BeforeEach
    void setUp() {
        AvatarCameraDirector.setEnabled(true);
        // Reset state
        for (int i = 0; i < 50; i++) {
            AvatarCameraDirector.tick();
        }
    }

    @Test
    @DisplayName("Verify camera roll triggers and decays back to zero")
    void testCameraRollDecay() {
        assertEquals(0.0f, AvatarCameraDirector.getCurrentRoll(), 1e-4);

        AvatarCameraDirector.triggerRoll(12.0f, 10);
        // Initially at 0 before tick or at target
        AvatarCameraDirector.tick();
        assertTrue(AvatarCameraDirector.getCurrentRoll() > 0.0f, "Roll should be positive during active roll");
        assertTrue(AvatarCameraDirector.getCurrentRoll() <= 12.0f, "Roll should not exceed peak target");

        // Tick past duration
        for (int i = 0; i < 15; i++) {
            AvatarCameraDirector.tick();
        }
        assertEquals(0.0f, AvatarCameraDirector.getCurrentRoll(), 1e-4, "Roll should decay back to 0.0");
    }

    @Test
    @DisplayName("Verify screenshake flag and lifetime decay")
    void testScreenshakeLifetime() {
        assertFalse(AvatarCameraDirector.isShaking());

        AvatarCameraDirector.triggerShake(1.0f, 5);
        assertTrue(AvatarCameraDirector.isShaking(), "Director should be shaking");

        AvatarCameraDirector.tick();
        AvatarCameraDirector.tick();
        assertTrue(AvatarCameraDirector.isShaking());

        // Tick to expiration
        AvatarCameraDirector.tick();
        AvatarCameraDirector.tick();
        AvatarCameraDirector.tick();
        AvatarCameraDirector.tick();
        assertFalse(AvatarCameraDirector.isShaking(), "Shake should expire after duration ticks");
    }

    @Test
    @DisplayName("Verify cinematic orbit activation and duration")
    void testCinematicOrbit() {
        assertFalse(AvatarCameraDirector.isCinematicActive());

        AvatarCameraDirector.triggerCinematicOrbit(5.0f, 8);
        assertTrue(AvatarCameraDirector.isCinematicActive(), "Cinematic orbit should be active");
        assertTrue(AvatarCameraDirector.getCurrentRoll() >= 0.0f);

        for (int i = 0; i < 10; i++) {
            AvatarCameraDirector.tick();
        }
        assertFalse(AvatarCameraDirector.isCinematicActive(), "Cinematic orbit should end after ticks");
    }

    @Test
    @DisplayName("Verify disabled director ignores triggers")
    void testDirectorDisabled() {
        AvatarCameraDirector.setEnabled(false);
        AvatarCameraDirector.triggerRoll(15.0f, 10);
        AvatarCameraDirector.triggerShake(1.0f, 10);
        AvatarCameraDirector.triggerCinematicOrbit(4.0f, 10);

        assertEquals(0.0f, AvatarCameraDirector.getCurrentRoll(), 1e-4);
        assertFalse(AvatarCameraDirector.isShaking());
        assertFalse(AvatarCameraDirector.isCinematicActive());
    }
}
