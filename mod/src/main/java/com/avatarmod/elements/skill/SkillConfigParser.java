package com.avatarmod.elements.skill;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonPrimitive;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Pattern;

final class SkillConfigParser {

    private static final int SLOT_COUNT = 5;
    private static final List<String> ELEMENTS = List.of("FIRE", "AIR", "WATER", "EARTH");
    private static final Pattern SKILL_ID_PATTERN =
            Pattern.compile("[a-z0-9_.-]+:[a-z0-9/._-]+");
    private static final Set<String> ROOT_KEYS = Set.of("skills");
    private static final Set<String> SKILL_KEYS = Set.of(
            "id", "element", "masteryRequired", "chiCost", "chiPerTick", "cooldownTicks",
            "windupTicks", "activeTicks", "recoveryTicks", "damage", "range", "knockback",
            "hitboxShape", "cancelOnHit", "comboWindowTicks", "castType", "cast_type",
            "maxChargeTicks", "max_charge_ticks");

    static List<SkillDefinition> parseSkills(String source, JsonElement root) {
        JsonObject rootObject = objectAt(source, "$", root);
        rejectUnknownKeys(source, "$", rootObject, ROOT_KEYS);
        JsonArray definitions = arrayAt(source, "$.skills", rootObject.get("skills"));
        if (definitions.isEmpty()) {
            throw invalid(source, "$.skills", "must contain at least one skill definition");
        }

        List<SkillDefinition> skills = new ArrayList<>(definitions.size());
        Map<String, Integer> firstSeen = new HashMap<>();
        for (int i = 0; i < definitions.size(); i++) {
            String path = "$.skills[" + i + "]";
            SkillDefinition skill = parseSkill(source, path, definitions.get(i));
            Integer firstIndex = firstSeen.putIfAbsent(skill.id(), i);
            if (firstIndex != null) {
                throw invalid(source, path + ".id",
                        "duplicate skill id '" + skill.id() + "' (first declared at $.skills["
                                + firstIndex + "].id)");
            }
            skills.add(skill);
        }
        return List.copyOf(skills);
    }

    static Map<String, List<String>> parseSlots(String source, JsonElement root) {
        JsonObject rootObject = objectAt(source, "$", root);
        rejectUnknownKeys(source, "$", rootObject, Set.copyOf(ELEMENTS));
        Map<String, List<String>> slotsByElement = new LinkedHashMap<>();

        for (String element : ELEMENTS) {
            JsonArray slots = arrayAt(source, "$." + element, rootObject.get(element));
            if (slots.size() != SLOT_COUNT) {
                throw invalid(source, "$." + element,
                        "must contain exactly " + SLOT_COUNT + " slots, found " + slots.size());
            }
            List<String> skillIds = new ArrayList<>(SLOT_COUNT);
            for (int i = 0; i < SLOT_COUNT; i++) {
                JsonElement slot = slots.get(i);
                String path = "$." + element + "[" + i + "]";
                if (slot == null || slot.isJsonNull()) {
                    skillIds.add(null);
                } else {
                    String skillId = stringAt(source, path, slot);
                    if (!SKILL_ID_PATTERN.matcher(skillId).matches()) {
                        throw invalid(source, path, "invalid namespaced skill id '" + skillId + "'");
                    }
                    skillIds.add(skillId);
                }
            }
            slotsByElement.put(element, Collections.unmodifiableList(skillIds));
        }
        return Collections.unmodifiableMap(slotsByElement);
    }

    static void validateSlotReferences(
            String source,
            Map<String, List<String>> slotsByElement,
            List<SkillDefinition> skills
    ) {
        Map<String, SkillDefinition> skillsById = new HashMap<>();
        for (SkillDefinition skill : skills) {
            skillsById.put(skill.id(), skill);
        }

        for (String element : ELEMENTS) {
            List<String> slots = slotsByElement.get(element);
            if (slots == null || slots.size() != SLOT_COUNT) {
                throw invalid(source, "$." + element,
                        "must contain exactly " + SLOT_COUNT + " slots");
            }
            for (int i = 0; i < slots.size(); i++) {
                String skillId = slots.get(i);
                if (skillId == null) {
                    continue;
                }
                String path = "$." + element + "[" + i + "]";
                SkillDefinition skill = skillsById.get(skillId);
                if (skill == null) {
                    throw invalid(source, path, "references unknown skill id '" + skillId + "'");
                }
                if (!skill.element().name().equals(element)) {
                    throw invalid(source, path, "references " + skill.element()
                            + " skill '" + skillId + "' in the " + element + " slots");
                }
            }
        }
    }

    private static SkillDefinition parseSkill(String source, String path, JsonElement value) {
        JsonObject object = objectAt(source, path, value);
        rejectUnknownKeys(source, path, object, SKILL_KEYS);

        String id = stringField(source, path, object, "id");
        if (!SKILL_ID_PATTERN.matcher(id).matches()) {
            throw invalid(source, path + ".id", "must be a valid namespaced identifier");
        }
        SkillDefinition.Element element = enumField(
                source, path, object, "element", SkillDefinition.Element.class);
        int masteryRequired = nonNegativeIntField(source, path, object, "masteryRequired");
        int chiCost = nonNegativeIntField(source, path, object, "chiCost");
        int chiPerTick = nonNegativeIntField(source, path, object, "chiPerTick");
        if (chiPerTick != 0) {
            throw invalid(source, path + ".chiPerTick",
                    "sustain costs are deferred; the current runtime requires 0");
        }
        int cooldownTicks = nonNegativeIntField(source, path, object, "cooldownTicks");
        int windupTicks = nonNegativeIntField(source, path, object, "windupTicks");
        int activeTicks = intField(source, path, object, "activeTicks", 1);
        int recoveryTicks = nonNegativeIntField(source, path, object, "recoveryTicks");
        float damage = nonNegativeFloatField(source, path, object, "damage");
        float range = nonNegativeFloatField(source, path, object, "range");
        float knockback = object.has("knockback")
                ? nonNegativeFloatField(source, path, object, "knockback") : 0f;
        SkillDefinition.HitboxShape hitboxShape = object.has("hitboxShape")
                ? enumField(source, path, object, "hitboxShape", SkillDefinition.HitboxShape.class)
                : SkillDefinition.HitboxShape.SPHERE;
        boolean cancelOnHit = booleanField(source, path, object, "cancelOnHit");
        int comboWindowTicks = nonNegativeIntField(source, path, object, "comboWindowTicks");

        rejectAliasConflict(source, path, object, "castType", "cast_type");
        SkillDefinition.CastType castType = object.has("castType") || object.has("cast_type")
                ? enumAliasField(source, path, object, "castType", "cast_type",
                        SkillDefinition.CastType.class)
                : SkillDefinition.CastType.INSTANT;
        if (castType == SkillDefinition.CastType.CHANNEL
                || castType == SkillDefinition.CastType.TOGGLE) {
            throw invalid(source, path + ".castType",
                    castType + " is not supported by the current runtime");
        }

        rejectAliasConflict(source, path, object, "maxChargeTicks", "max_charge_ticks");
        int maxChargeTicks = object.has("maxChargeTicks") || object.has("max_charge_ticks")
                ? nonNegativeIntAliasField(source, path, object,
                        "maxChargeTicks", "max_charge_ticks")
                : 0;
        if (castType == SkillDefinition.CastType.HOLD_RELEASE && maxChargeTicks == 0) {
            throw invalid(source, path + ".maxChargeTicks",
                    "must be greater than zero for HOLD_RELEASE skills");
        }
        if (castType != SkillDefinition.CastType.HOLD_RELEASE && maxChargeTicks != 0) {
            throw invalid(source, path + ".maxChargeTicks",
                    "is only valid for HOLD_RELEASE skills");
        }

        return new SkillDefinition(id, element, masteryRequired, chiCost, chiPerTick,
                cooldownTicks, windupTicks, activeTicks, recoveryTicks, damage, range,
                knockback, hitboxShape, cancelOnHit, comboWindowTicks, castType, maxChargeTicks);
    }

    private static void rejectAliasConflict(
            String source, String path, JsonObject object, String canonical, String alias
    ) {
        if (object.has(canonical) && object.has(alias)) {
            throw invalid(source, path, "must not contain both '" + canonical
                    + "' and its alias '" + alias + "'");
        }
    }

    private static int nonNegativeIntAliasField(
            String source, String path, JsonObject object, String canonical, String alias
    ) {
        String key = object.has(canonical) ? canonical : alias;
        return nonNegativeIntField(source, path, object, key);
    }

    private static <T extends Enum<T>> T enumAliasField(
            String source,
            String path,
            JsonObject object,
            String canonical,
            String alias,
            Class<T> enumType
    ) {
        return enumField(source, path, object,
                object.has(canonical) ? canonical : alias, enumType);
    }

    private static <T extends Enum<T>> T enumField(
            String source, String path, JsonObject object, String key, Class<T> enumType
    ) {
        String value = stringField(source, path, object, key);
        try {
            return Enum.valueOf(enumType, value);
        } catch (IllegalArgumentException e) {
            throw invalid(source, path + "." + key, "unknown value '" + value
                    + "'; expected one of " + String.join(", ", enumNames(enumType)));
        }
    }

    private static <T extends Enum<T>> List<String> enumNames(Class<T> enumType) {
        List<String> names = new ArrayList<>();
        for (T value : enumType.getEnumConstants()) {
            names.add(value.name());
        }
        return names;
    }

    private static String stringField(String source, String path, JsonObject object, String key) {
        return stringAt(source, path + "." + key, object.get(key));
    }

    private static String stringAt(String source, String path, JsonElement value) {
        JsonPrimitive primitive = primitiveAt(source, path, value);
        if (!primitive.isString()) {
            throw invalid(source, path, "must be a string");
        }
        return primitive.getAsString();
    }

    private static int nonNegativeIntField(
            String source, String path, JsonObject object, String key
    ) {
        return intField(source, path, object, key, 0);
    }

    private static int intField(
            String source, String path, JsonObject object, String key, int minimum
    ) {
        String fieldPath = path + "." + key;
        JsonPrimitive primitive = primitiveAt(source, fieldPath, object.get(key));
        if (!primitive.isNumber()) {
            throw invalid(source, fieldPath, "must be an integer");
        }
        try {
            BigDecimal number = new BigDecimal(primitive.getAsString());
            int value = number.intValueExact();
            if (value < minimum) {
                throw invalid(source, fieldPath, "must be at least " + minimum);
            }
            return value;
        } catch (NumberFormatException | ArithmeticException e) {
            throw invalid(source, fieldPath, "must be an integer in the supported range");
        }
    }

    private static float nonNegativeFloatField(
            String source, String path, JsonObject object, String key
    ) {
        String fieldPath = path + "." + key;
        JsonPrimitive primitive = primitiveAt(source, fieldPath, object.get(key));
        if (!primitive.isNumber()) {
            throw invalid(source, fieldPath, "must be a finite non-negative number");
        }
        float value;
        try {
            value = primitive.getAsFloat();
        } catch (NumberFormatException e) {
            throw invalid(source, fieldPath, "must be a finite non-negative number");
        }
        if (!Float.isFinite(value) || value < 0f) {
            throw invalid(source, fieldPath, "must be a finite non-negative number");
        }
        return value;
    }

    private static boolean booleanField(
            String source, String path, JsonObject object, String key
    ) {
        String fieldPath = path + "." + key;
        JsonPrimitive primitive = primitiveAt(source, fieldPath, object.get(key));
        if (!primitive.isBoolean()) {
            throw invalid(source, fieldPath, "must be a boolean");
        }
        return primitive.getAsBoolean();
    }

    private static JsonObject objectAt(String source, String path, JsonElement value) {
        if (value == null || !value.isJsonObject()) {
            throw invalid(source, path, "must be an object");
        }
        return value.getAsJsonObject();
    }

    private static JsonArray arrayAt(String source, String path, JsonElement value) {
        if (value == null || !value.isJsonArray()) {
            throw invalid(source, path, "must be an array");
        }
        return value.getAsJsonArray();
    }

    private static JsonPrimitive primitiveAt(String source, String path, JsonElement value) {
        if (value == null || !value.isJsonPrimitive()) {
            throw invalid(source, path, "is required and must be a JSON primitive");
        }
        return value.getAsJsonPrimitive();
    }

    private static void rejectUnknownKeys(
            String source, String path, JsonObject object, Set<String> allowed
    ) {
        for (String key : object.keySet()) {
            if (!allowed.contains(key)) {
                throw invalid(source, path + "." + key, "is not a supported property");
            }
        }
    }

    private static IllegalArgumentException invalid(String source, String path, String message) {
        return new IllegalArgumentException(source + " " + path + ": " + message);
    }

    private SkillConfigParser() {}
}
