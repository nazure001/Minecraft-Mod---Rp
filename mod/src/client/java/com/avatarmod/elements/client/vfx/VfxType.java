package com.avatarmod.elements.client.vfx;

import net.minecraft.component.DataComponentTypes;
import net.minecraft.component.type.CustomModelDataComponent;
import net.minecraft.item.Item;
import net.minecraft.item.ItemStack;
import net.minecraft.item.Items;
import org.joml.Vector3f;

/**
 * Cinematic 3D VFX Preset Definitions.
 * Parameterizes mesh item fallback, CustomModelData value, scale curves, duration, and rotation rate.
 */
public enum VfxType {

    AEGIS_DOME(
            "avatar:fire_guard",
            1001,
            Items.SHIELD,
            15,
            new Vector3f(0.1f, 0.1f, 0.1f),
            new Vector3f(3.0f, 3.0f, 3.0f),
            0.0f,
            true
    ),
    CRESCENT_SLASH(
            "avatar:flame_sweep",
            1002,
            Items.FIRE_CHARGE,
            8,
            new Vector3f(0.5f, 0.5f, 0.5f),
            new Vector3f(2.5f, 2.5f, 2.5f),
            0.0f,
            false
    ),
    RUNE_DISC(
            "avatar:avatar_state",
            1003,
            Items.NETHER_STAR,
            40,
            new Vector3f(2.5f, 2.5f, 0.05f),
            new Vector3f(2.5f, 2.5f, 0.05f),
            18.0f,
            true
    ),
    EARTH_PILLAR(
            "avatar:earth_pillar",
            1005,
            Items.DEEPSLATE,
            25,  // 1.25s = 25 ticks
            new Vector3f(1.0f, 1.0f, 1.0f),
            new Vector3f(1.0f, 1.0f, 1.0f),
            0.0f,
            false  // position fixed at ground, not following caster
    ),
    BOULDER_LAUNCH_MEGALITH(
            "avatar:boulder_launch",
            1006,
            Items.DEEPSLATE,
            25,
            new Vector3f(1.0f, 1.0f, 1.0f),
            new Vector3f(1.2f, 1.2f, 1.2f),
            0.0f,
            false
    ),
    WATER_WHIP_STREAM(
            "avatar:water_whip",
            1007,
            Items.PRISMARINE_SHARD,
            12,
            new Vector3f(2.5f, 2.5f, 2.5f),
            new Vector3f(2.5f, 2.5f, 2.5f),
            0.0f,
            true
    ),
    AIR_VORTEX_FUNNEL(
            "avatar:air_vortex",
            1008,
            Items.FEATHER,
            40,
            new Vector3f(1.0f, 1.0f, 1.0f),
            new Vector3f(1.5f, 1.5f, 1.5f),
            20.0f,
            true
    ),
    CAPTURED_EARTH_SHARDS(
            "avatar:earth_boulder",
            1009,
            Items.DEEPSLATE,
            25,
            new Vector3f(1.0f, 1.0f, 1.0f),
            new Vector3f(1.0f, 1.0f, 1.0f),
            12.0f,
            true
    ),
    EARTH_ARMOR_OVERLAY(
            "avatar:earth_armor",
            1010,
            Items.IRON_CHESTPLATE,
            60,
            new Vector3f(1.0f, 1.0f, 1.0f),
            new Vector3f(1.0f, 1.0f, 1.0f),
            0.0f,
            true
    ),
    // Compatibility aliases
    MAGIC_RUNE_CIRCLE(
            "avatar:avatar_state",
            1003,
            Items.NETHER_STAR,
            40,
            new Vector3f(2.5f, 2.5f, 0.05f),
            new Vector3f(2.5f, 2.5f, 0.05f),
            18.0f,
            true
    ),
    SWIRL_VORTEX(
            "avatar:legacy_air_vortex",
            1004,
            Items.FEATHER,
            20,
            new Vector3f(1.0f, 1.0f, 1.0f),
            new Vector3f(1.5f, 1.5f, 1.5f),
            15.0f,
            true
    ),
    SWIRLING_VORTEX(
            "avatar:legacy_air_vortex",
            1004,
            Items.FEATHER,
            20,
            new Vector3f(1.0f, 1.0f, 1.0f),
            new Vector3f(1.5f, 1.5f, 1.5f),
            15.0f,
            true
    );

    private final String skillId;
    private final int customModelData;
    private final Item fallbackItem;
    private final int durationTicks;
    private final Vector3f baseScale;
    private final Vector3f targetScale;
    private final float rotationSpeed;
    private final boolean followCaster;

    VfxType(
            String skillId,
            int customModelData,
            Item fallbackItem,
            int durationTicks,
            Vector3f baseScale,
            Vector3f targetScale,
            float rotationSpeed,
            boolean followCaster
    ) {
        this.skillId = skillId;
        this.customModelData = customModelData;
        this.fallbackItem = fallbackItem;
        this.durationTicks = durationTicks;
        this.baseScale = baseScale;
        this.targetScale = targetScale;
        this.rotationSpeed = rotationSpeed;
        this.followCaster = followCaster;
    }

    /**
     * Creates an ItemStack backed by the fallback item and configured with the preset's CustomModelData.
     * When resource packs or custom Blockbench models are loaded, this activates custom 3D model geometry.
     */
    public ItemStack createItemStack() {
        ItemStack stack = new ItemStack(fallbackItem);
        stack.set(DataComponentTypes.CUSTOM_MODEL_DATA, new CustomModelDataComponent(customModelData));
        return stack;
    }

    public String skillId() {
        return skillId;
    }

    public int customModelData() {
        return customModelData;
    }

    public Item fallbackItem() {
        return fallbackItem;
    }

    public int durationTicks() {
        return durationTicks;
    }

    public int defaultLifetimeTicks() {
        return durationTicks;
    }

    public Vector3f baseScale() {
        return new Vector3f(baseScale);
    }

    public Vector3f targetScale() {
        return new Vector3f(targetScale);
    }

    public float rotationSpeed() {
        return rotationSpeed;
    }

    public boolean followCaster() {
        return followCaster;
    }

    /**
     * Finds the VFX preset associated with the given skill identifier.
     *
     * @param skillId The skill identifier (e.g. "avatar:fire_guard")
     * @return Matching VfxType, or null if none registered
     */
    public static VfxType fromSkillId(String skillId) {
        if (skillId == null) {
            return null;
        }
        for (VfxType type : values()) {
            if (type.skillId.equals(skillId)) {
                return type;
            }
        }
        return null;
    }
}
