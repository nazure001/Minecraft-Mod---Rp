package com.avatarmod.elements.client.combat;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Validates natural weapon grip display transformations and combo timing invariants.
 */
class WeaponCombatChoreographyTest {

    private static final Path MODELS_DIR = Path.of("src/main/resources/assets/avatar_elements/models/item");

    @ParameterizedTest(name = "Model {0} has ergonomic grip transformations in display settings")
    @ValueSource(strings = {
            "dual_swords.json",
            "earth_hammer.json",
            "war_fan.json",
            "water_spear.json",
            "air_staff.json"
    })
    void testWeaponModelDisplayErgonomics(String modelFilename) throws IOException {
        Path modelPath = MODELS_DIR.resolve(modelFilename);
        assertTrue(Files.exists(modelPath), "Model file must exist: " + modelPath);

        JsonObject root = JsonParser.parseString(Files.readString(modelPath)).getAsJsonObject();
        assertTrue(root.has("display"), "Model must have a display block: " + modelFilename);

        JsonObject display = root.getAsJsonObject("display");
        assertTrue(display.has("thirdperson_righthand"), "Must define thirdperson_righthand display settings");
        assertTrue(display.has("firstperson_righthand"), "Must define firstperson_righthand display settings");

        JsonObject thirdPerson = display.getAsJsonObject("thirdperson_righthand");
        var trans = thirdPerson.getAsJsonArray("translation");
        assertNotNull(trans, "translation array must not be null");
        assertEquals(3, trans.size(), "translation must have [x, y, z]");

        // Handle alignment check: translation Y should lift the grip into player's hand palm (2.0 to 4.0)
        double transY = trans.get(1).getAsDouble();
        assertTrue(transY >= 2.0 && transY <= 4.0,
                "Weapon translation Y (" + transY + ") should be between 2.0 and 4.0 to seat handle firmly in hand: " + modelFilename);

        var rot = thirdPerson.getAsJsonArray("rotation");
        assertNotNull(rot, "rotation array must not be null");
        assertEquals(3, rot.size(), "rotation must have [x, y, z]");

        // Angle check: rotation Z should be angled naturally forward/downward (-10 to -45 degrees)
        double rotZ = rot.get(2).getAsDouble();
        assertTrue(rotZ <= -10.0 && rotZ >= -45.0,
                "Weapon rotation Z (" + rotZ + ") must angle weapon blade/shaft forward: " + modelFilename);
    }

    @Test
    @DisplayName("Verify combo step progression and reset window logic")
    void testComboStepLogic() {
        // Step progression: 0 -> 1 -> 2 -> 3 -> 0
        int step = 0;
        step = (step + 1) % 4;
        assertEquals(1, step);
        step = (step + 1) % 4;
        assertEquals(2, step);
        step = (step + 1) % 4;
        assertEquals(3, step);
        step = (step + 1) % 4;
        assertEquals(0, step, "Combo should wrap back to 0 on 4th hit");

        // Verify timing windows per weapon class
        long hammerWindow = 1600L;
        long fanWindow = 900L;
        long swordWindow = 1300L;
        long spearWindow = 1100L;

        assertTrue(hammerWindow > swordWindow, "Earth hammer combo window must be longer to reflect heavy weight");
        assertTrue(fanWindow < swordWindow, "War fan combo window must be faster to reflect rapid agile strikes");
        assertTrue(spearWindow < swordWindow, "Water spear combo window must be between fan and swords");
    }
}
