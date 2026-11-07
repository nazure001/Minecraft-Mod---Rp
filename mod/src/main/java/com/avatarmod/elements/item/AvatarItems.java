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

    public static final Item AIR_STAFF = new Item(new Item.Settings().maxCount(1));

    public static final ItemGroup MAIN_GROUP = FabricItemGroup.builder()
            .icon(() -> new ItemStack(AIR_STAFF))
            .displayName(Text.translatable("itemGroup.avatar_elements.main"))
            .entries((ctx, entries) -> entries.add(AIR_STAFF))
            .build();

    public static void register() {
        Registry.register(Registries.ITEM,
                Identifier.of(AvatarElementsMod.MOD_ID, "air_staff"), AIR_STAFF);
        Registry.register(Registries.ITEM_GROUP,
                Identifier.of(AvatarElementsMod.MOD_ID, "main"), MAIN_GROUP);
    }

    private AvatarItems() {}
}
