package com.avatarmod.elements.skill;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/**
 * Maps element → 4 skill IDs loaded from element_slots.json.
 * Null slot entries mean "empty — no cast".
 */
public final class ElementSlotMap {

    public static final int SLOT_COUNT = 4;
    public static final String[] ELEMENTS = {"FIRE", "AIR", "WATER", "EARTH"};

    // element → String[4] (null = empty slot)
    private static final Map<String, String[]> MAP = new HashMap<>();

    static {
        load();
    }

    private static void load() {
        try (InputStream in = ElementSlotMap.class.getResourceAsStream(
                "/data/avatar_elements/element_slots.json")) {
            if (in == null) {
                defaultFallback();
                return;
            }
            JsonObject root = JsonParser.parseReader(new InputStreamReader(in, StandardCharsets.UTF_8))
                    .getAsJsonObject();
            for (String element : ELEMENTS) {
                String[] slots = new String[SLOT_COUNT];
                if (root.has(element)) {
                    JsonArray arr = root.getAsJsonArray(element);
                    for (int i = 0; i < Math.min(arr.size(), SLOT_COUNT); i++) {
                        JsonElement e = arr.get(i);
                        slots[i] = (e.isJsonNull()) ? null : e.getAsString();
                    }
                }
                MAP.put(element, slots);
            }
        } catch (Exception e) {
            defaultFallback();
        }
    }

    private static void defaultFallback() {
        MAP.put("FIRE",  new String[]{"avatar:fire_jab", "avatar:flame_sweep", "avatar:fire_guard", "avatar:fire_jet"});
        MAP.put("AIR",   new String[]{"avatar:air_staff_attack", "avatar:air_vortex", null, null});
        MAP.put("WATER", new String[]{"avatar:water_whip", null, null, null});
        MAP.put("EARTH", new String[]{"avatar:earth_boulder", null, null, null});
    }

    /** Returns the skill ID for the given element and slot (0–3), or null if empty. */
    public static String getSkillId(String element, int slot) {
        String[] slots = MAP.getOrDefault(element, new String[SLOT_COUNT]);
        if (slot < 0 || slot >= SLOT_COUNT) return null;
        return slots[slot];
    }

    /** Returns a copy of the 4 slots for HUD display. */
    public static String[] getSlots(String element) {
        return Arrays.copyOf(MAP.getOrDefault(element, new String[SLOT_COUNT]), SLOT_COUNT);
    }

    private ElementSlotMap() {}
}
