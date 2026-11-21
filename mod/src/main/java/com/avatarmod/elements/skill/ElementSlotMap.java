package com.avatarmod.elements.skill;

import com.avatarmod.elements.AvatarElementsMod;
import com.google.gson.JsonIOException;
import com.google.gson.JsonParseException;
import com.google.gson.JsonParser;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Maps elements to skill IDs loaded from element_slots.json.
 * Null slot entries mean "empty — no cast".
 */
public final class ElementSlotMap {

    public static final int SLOT_COUNT = 5;
    public static final String[] ELEMENTS = {"FIRE", "AIR", "WATER", "EARTH", "NON_BENDER"};

    private static final String RESOURCE_PATH = "/data/avatar_elements/element_slots.json";
    private static final Map<String, String[]> MAP = new HashMap<>();

    static {
        load();
    }

    private static void load() {
        try (InputStream in = ElementSlotMap.class.getResourceAsStream(RESOURCE_PATH)) {
            if (in == null) {
                throw new IllegalStateException(
                        "Bundled element slot resource not found at " + RESOURCE_PATH);
            }
            Map<String, List<String>> parsed = SkillConfigParser.parseSlots(
                    "bundled resource " + RESOURCE_PATH,
                    JsonParser.parseReader(new InputStreamReader(in, StandardCharsets.UTF_8)));
            for (String element : ELEMENTS) {
                MAP.put(element, parsed.get(element).toArray(new String[SLOT_COUNT]));
            }
        } catch (JsonIOException e) {
            AvatarElementsMod.LOGGER.error("[Avatar] Failed to read bundled element slots at {}",
                    RESOURCE_PATH, e);
            throw new IllegalStateException(
                    "Failed to read bundled element slots from " + RESOURCE_PATH, e);
        } catch (IOException e) {
            throw new IllegalStateException(
                    "Failed to read bundled element slots from " + RESOURCE_PATH, e);
        } catch (IllegalArgumentException | JsonParseException e) {
            AvatarElementsMod.LOGGER.error("[Avatar] Invalid bundled element slots: {}",
                    e.getMessage());
            throw new IllegalStateException(
                    "Invalid bundled element slots at " + RESOURCE_PATH + ": " + e.getMessage(), e);
        }
    }

    static void validateSkillReferences(List<SkillDefinition> skills) {
        Map<String, List<String>> slots = new HashMap<>();
        for (String element : ELEMENTS) {
            slots.put(element, new ArrayList<>(Arrays.asList(MAP.get(element).clone())));
        }
        try {
            SkillConfigParser.validateSlotReferences(
                    "bundled resource " + RESOURCE_PATH, slots, skills);
        } catch (IllegalArgumentException e) {
            AvatarElementsMod.LOGGER.error("[Avatar] Invalid bundled element slots: {}",
                    e.getMessage());
            throw new IllegalStateException(
                    "Invalid bundled element slots at " + RESOURCE_PATH + ": " + e.getMessage(), e);
        }
    }

    /** Returns the skill ID for the given element and slot (0–4), or null if empty. */
    public static String getSkillId(String element, int slot) {
        String[] slots = MAP.getOrDefault(element, new String[SLOT_COUNT]);
        if (slot < 0 || slot >= SLOT_COUNT) return null;
        return slots[slot];
    }

    /** Returns the next element in the configured selector order. */
    public static String nextElement(String element) {
        for (int i = 0; i < ELEMENTS.length; i++) {
            if (ELEMENTS[i].equals(element)) {
                return ELEMENTS[(i + 1) % ELEMENTS.length];
            }
        }
        return ELEMENTS[0];
    }

    /** Returns whether the value is one of the configured runtime elements. */
    public static boolean isElement(String element) {
        for (String configuredElement : ELEMENTS) {
            if (configuredElement.equals(element)) return true;
        }
        return false;
    }

    /** Returns a copy of the five slots for HUD display. */
    public static String[] getSlots(String element) {
        return Arrays.copyOf(MAP.getOrDefault(element, new String[SLOT_COUNT]), SLOT_COUNT);
    }

    private ElementSlotMap() {}
}
