package com.avatarmod.elements.skill;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonNull;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import org.junit.jupiter.api.Test;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class SkillConfigParserTest {

    @Test
    void bundledDefinitionsAndSlotsAreValidAndResolve() throws Exception {
        JsonElement skillsJson = readResource("data/avatar_elements/skill_definitions.json");
        JsonElement slotsJson = readResource("data/avatar_elements/element_slots.json");

        List<SkillDefinition> skills =
                SkillConfigParser.parseSkills("bundled skills", skillsJson);
        Map<String, List<String>> slots =
                SkillConfigParser.parseSlots("bundled slots", slotsJson);

        assertEquals(25, skills.size());
        assertDoesNotThrow(() ->
                SkillConfigParser.validateSlotReferences("bundled slots", slots, skills));

        assertEquals(List.of("avatar:fire_jab", "avatar:fire_blast", "avatar:flame_sweep",
                "avatar:lightning_strike", "avatar:fire_jet"), slots.get("FIRE"));
        assertEquals(List.of("avatar:air_palm", "avatar:air_blast", "avatar:air_staff_attack",
                "avatar:air_vortex", "avatar:air_scooter"), slots.get("AIR"));
        assertEquals("avatar:water_whip", slots.get("WATER").get(0));
        assertEquals("avatar:water_jet", slots.get("WATER").get(1));
        assertEquals("avatar:octopus_form", slots.get("WATER").get(2));
        assertNull(slots.get("WATER").get(3));
        assertEquals("avatar:water_surf", slots.get("WATER").get(4));
        assertEquals(List.of("avatar:earth_boulder", "avatar:boulder_launch",
                "avatar:earth_pillar", "avatar:earth_wall", "avatar:earth_tunnel"), slots.get("EARTH"));
        assertEquals(List.of("avatar:chi_strike", "avatar:acrobatic_dodge", "avatar:grapple_wire",
                "avatar:smoke_bomb", "avatar:nerve_strike"), slots.get("NON_BENDER"));
    }

    @Test
    void rejectsMissingFieldsWithSourceAndJsonPath() {
        JsonObject skill = validSkill("avatar:test");
        skill.remove("chiCost");

        IllegalArgumentException error = assertThrows(IllegalArgumentException.class,
                () -> SkillConfigParser.parseSkills("config/custom.json", rootWith(skill)));

        assertTrue(error.getMessage().contains("config/custom.json"));
        assertTrue(error.getMessage().contains("$.skills[0].chiCost"));
    }

    @Test
    void rejectsDuplicateSkillIds() {
        IllegalArgumentException error = assertThrows(IllegalArgumentException.class,
                () -> SkillConfigParser.parseSkills("test", rootWith(
                        validSkill("avatar:test"), validSkill("avatar:test"))));

        assertTrue(error.getMessage().contains("duplicate skill id"));
        assertTrue(error.getMessage().contains("$.skills[0].id"));
    }

    @Test
    void rejectsUnknownPropertiesAndInvalidEnums() {
        JsonObject unknownProperty = validSkill("avatar:test");
        unknownProperty.addProperty("projectile_speed", 1.0);
        assertThrows(IllegalArgumentException.class,
                () -> SkillConfigParser.parseSkills("test", rootWith(unknownProperty)));

        JsonObject invalidEnum = validSkill("avatar:test");
        invalidEnum.addProperty("hitboxShape", "CIRCLE");
        IllegalArgumentException error = assertThrows(IllegalArgumentException.class,
                () -> SkillConfigParser.parseSkills("test", rootWith(invalidEnum)));
        assertTrue(error.getMessage().contains("unknown value 'CIRCLE'"));
    }

    @Test
    void rejectsInvalidNumericValuesAndTypes() {
        JsonObject negativeCost = validSkill("avatar:test");
        negativeCost.addProperty("chiCost", -1);
        assertThrows(IllegalArgumentException.class,
                () -> SkillConfigParser.parseSkills("test", rootWith(negativeCost)));

        JsonObject fractionalCooldown = validSkill("avatar:test");
        fractionalCooldown.addProperty("cooldownTicks", 1.5);
        IllegalArgumentException error = assertThrows(IllegalArgumentException.class,
                () -> SkillConfigParser.parseSkills("test", rootWith(fractionalCooldown)));
        assertTrue(error.getMessage().contains("$.skills[0].cooldownTicks"));
    }

    @Test
    void acceptsSnakeCaseAliasesForHoldReleaseFields() {
        JsonObject skill = validSkill("avatar:test");
        skill.addProperty("cast_type", "HOLD_RELEASE");
        skill.addProperty("max_charge_ticks", 20);

        SkillDefinition parsed = SkillConfigParser
                .parseSkills("test", rootWith(skill)).getFirst();

        assertEquals(SkillDefinition.CastType.HOLD_RELEASE, parsed.castType());
        assertEquals(20, parsed.maxChargeTicks());
    }

    @Test
    void rejectsAmbiguousAliasesAndUnsupportedCastTypes() {
        JsonObject ambiguous = validSkill("avatar:test");
        ambiguous.addProperty("castType", "INSTANT");
        ambiguous.addProperty("cast_type", "INSTANT");
        assertThrows(IllegalArgumentException.class,
                () -> SkillConfigParser.parseSkills("test", rootWith(ambiguous)));

        for (String castType : List.of("CHANNEL", "TOGGLE")) {
            JsonObject unsupported = validSkill("avatar:test");
            unsupported.addProperty("castType", castType);
            IllegalArgumentException error = assertThrows(IllegalArgumentException.class,
                    () -> SkillConfigParser.parseSkills("test", rootWith(unsupported)));
            assertTrue(error.getMessage().contains("not supported by the current runtime"));
        }
    }

    @Test
    void rejectsNonZeroSustainCostUntilTheRuntimeSupportsIt() {
        JsonObject skill = validSkill("avatar:test");
        skill.addProperty("chiPerTick", 2);

        IllegalArgumentException error = assertThrows(IllegalArgumentException.class,
                () -> SkillConfigParser.parseSkills("test", rootWith(skill)));

        assertTrue(error.getMessage().contains("$.skills[0].chiPerTick"));
        assertTrue(error.getMessage().contains("sustain costs are deferred"));
    }

    @Test
    void rejectsUnknownAndCrossElementSlotReferences() {
        List<SkillDefinition> skills = List.of(
                SkillConfigParser.parseSkills("test", rootWith(validSkill("avatar:test"))).getFirst());

        Map<String, List<String>> unknown = SkillConfigParser.parseSlots("test", slotJson(
                "WATER", "avatar:missing"));
        IllegalArgumentException missingError = assertThrows(IllegalArgumentException.class,
                () -> SkillConfigParser.validateSlotReferences("test slots", unknown, skills));
        assertTrue(missingError.getMessage().contains("references unknown skill id"));

        Map<String, List<String>> wrongElement = SkillConfigParser.parseSlots("test", slotJson(
                "AIR", "avatar:test"));
        IllegalArgumentException elementError = assertThrows(IllegalArgumentException.class,
                () -> SkillConfigParser.validateSlotReferences("test slots", wrongElement, skills));
        assertTrue(elementError.getMessage().contains("in the AIR slots"));
    }

    @Test
    void requiresExactlyFiveSlotsForEveryElement() {
        JsonObject invalidSlots = slotJson("FIRE", "avatar:test");
        invalidSlots.add("FIRE", new JsonArray());

        IllegalArgumentException error = assertThrows(IllegalArgumentException.class,
                () -> SkillConfigParser.parseSlots("test slots", invalidSlots));
        assertTrue(error.getMessage().contains("must contain exactly 5 slots"));
    }

    private static JsonObject validSkill(String id) {
        JsonObject skill = new JsonObject();
        skill.addProperty("id", id);
        skill.addProperty("element", "FIRE");
        skill.addProperty("masteryRequired", 0);
        skill.addProperty("chiCost", 1);
        skill.addProperty("chiPerTick", 0);
        skill.addProperty("cooldownTicks", 1);
        skill.addProperty("windupTicks", 0);
        skill.addProperty("activeTicks", 1);
        skill.addProperty("recoveryTicks", 0);
        skill.addProperty("damage", 1.0);
        skill.addProperty("range", 1.0);
        skill.addProperty("cancelOnHit", false);
        skill.addProperty("comboWindowTicks", 0);
        return skill;
    }

    private static JsonObject rootWith(JsonObject... skills) {
        JsonObject root = new JsonObject();
        JsonArray definitions = new JsonArray();
        for (JsonObject skill : skills) {
            definitions.add(skill);
        }
        root.add("skills", definitions);
        return root;
    }

    private static JsonObject slotJson(String element, String skillId) {
        JsonObject root = new JsonObject();
        for (String current : ElementSlotMap.ELEMENTS) {
            JsonArray slots = new JsonArray();
            for (int i = 0; i < ElementSlotMap.SLOT_COUNT; i++) {
                if (current.equals(element) && i == 0) {
                    slots.add(skillId);
                } else {
                    slots.add(JsonNull.INSTANCE);
                }
            }
            root.add(current, slots);
        }
        return root;
    }

    private static JsonElement readResource(String path) throws Exception {
        try (InputStream stream = SkillConfigParserTest.class.getClassLoader()
                .getResourceAsStream(path)) {
            if (stream == null) {
                throw new IllegalStateException("Missing test resource " + path);
            }
            return JsonParser.parseReader(
                    new InputStreamReader(stream, StandardCharsets.UTF_8));
        }
    }
}
