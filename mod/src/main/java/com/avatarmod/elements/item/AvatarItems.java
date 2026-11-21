package com.avatarmod.elements.item;

import com.avatarmod.elements.AvatarElementsMod;
import net.fabricmc.fabric.api.itemgroup.v1.FabricItemGroup;
import net.minecraft.item.Item;
import net.minecraft.item.ItemGroup;
import net.minecraft.item.ItemStack;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.text.Text;
import net.minecraft.util.Identifier;

public final class AvatarItems {

    public static final Item AIR_STAFF = new AirStaffItem();
    public static final Item DUAL_SWORDS = new DualSwordsItem();
    public static final Item EARTH_HAMMER = new EarthHammerItem();
    public static final Item WAR_FAN = new WarFanItem();
    public static final Item WATER_SPEAR = new WaterSpearItem();
    public static final Item AVATAR_SCROLL = new AvatarScrollItem();

    public static final ItemGroup MAIN_GROUP = FabricItemGroup.builder()
            .icon(() -> new ItemStack(AIR_STAFF))
            .displayName(Text.translatable("itemGroup.avatar_elements.main"))
            .entries((ctx, entries) -> {
                entries.add(AIR_STAFF);
                entries.add(DUAL_SWORDS);
                entries.add(EARTH_HAMMER);
                entries.add(WAR_FAN);
                entries.add(WATER_SPEAR);
                entries.add(AVATAR_SCROLL);
            })
            .build();

    public static void register() {
        Registry.register(Registries.ITEM,
                Identifier.of(AvatarElementsMod.MOD_ID, "air_staff"), AIR_STAFF);
        Registry.register(Registries.ITEM,
                Identifier.of(AvatarElementsMod.MOD_ID, "dual_swords"), DUAL_SWORDS);
        Registry.register(Registries.ITEM,
                Identifier.of(AvatarElementsMod.MOD_ID, "earth_hammer"), EARTH_HAMMER);
        Registry.register(Registries.ITEM,
                Identifier.of(AvatarElementsMod.MOD_ID, "war_fan"), WAR_FAN);
        Registry.register(Registries.ITEM,
                Identifier.of(AvatarElementsMod.MOD_ID, "water_spear"), WATER_SPEAR);
        Registry.register(Registries.ITEM,
                Identifier.of(AvatarElementsMod.MOD_ID, "avatar_scroll"), AVATAR_SCROLL);
        Registry.register(Registries.ITEM_GROUP,
                Identifier.of(AvatarElementsMod.MOD_ID, "main"), MAIN_GROUP);
    }

    private AvatarItems() {}
}
