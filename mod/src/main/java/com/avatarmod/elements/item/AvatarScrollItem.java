package com.avatarmod.elements.item;

import com.avatarmod.elements.network.AvatarServerEvents;
import com.avatarmod.elements.particle.AvatarParticles;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.item.Item;
import net.minecraft.item.ItemStack;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.util.Hand;
import net.minecraft.util.Rarity;
import net.minecraft.util.TypedActionResult;
import net.minecraft.util.UseAction;
import net.minecraft.util.math.Vec3d;
import net.minecraft.world.World;

/**
 * Ancient Avatar Scroll — sacred relic containing the ancestral memories and katas of past Avatars.
 *
 * Holding Right-Click channels elemental cosmic energy (30 ticks / 1.5s):
 * - Draws converging 4-element energy motes inward from surrounding space.
 * - Levitation ascendance lifting the player gently above the earth.
 * - When channeled to completion, unleashes the transcendent AVATAR STATE with cataclysmic 4-element shockwave!
 */
public class AvatarScrollItem extends Item {

    public static final int CHANNEL_TICKS = 30; // 1.5s channel time
    public static final int COOLDOWN_TICKS = 2400; // 2 minutes cooldown

    public AvatarScrollItem() {
        super(new Item.Settings().maxCount(1).rarity(Rarity.EPIC));
    }

    @Override
    public int getMaxUseTime(ItemStack stack, LivingEntity user) {
        return CHANNEL_TICKS;
    }

    @Override
    public UseAction getUseAction(ItemStack stack) {
        return UseAction.BOW;
    }

    @Override
    public TypedActionResult<ItemStack> use(World world, PlayerEntity user, Hand hand) {
        ItemStack stack = user.getStackInHand(hand);
        user.setCurrentHand(hand);
        world.playSound(null, user.getBlockPos(),
                SoundEvents.BLOCK_ENCHANTMENT_TABLE_USE, SoundCategory.PLAYERS, 1.2f, 1.0f);
        return TypedActionResult.consume(stack);
    }

    @Override
    public void usageTick(World world, LivingEntity user, ItemStack stack, int remainingUseTicks) {
        if (!world.isClient() && world instanceof ServerWorld serverWorld) {
            Vec3d center = user.getEyePos();
            int elapsed = CHANNEL_TICKS - remainingUseTicks;
            double radius = Math.max(0.6, 3.0 - (elapsed * 0.08));

            // Converging elemental energy vortex into the scroll
            double theta = elapsed * 0.45;
            serverWorld.spawnParticles(ParticleTypes.FLAME,
                    center.x + radius * Math.cos(theta), center.y + 0.3 * Math.sin(theta), center.z + radius * Math.sin(theta),
                    2, 0, 0, 0, 0.02);
            serverWorld.spawnParticles(ParticleTypes.SPLASH,
                    center.x + radius * Math.cos(theta + Math.PI * 0.5), center.y, center.z + radius * Math.sin(theta + Math.PI * 0.5),
                    3, 0, 0, 0, 0.05);
            serverWorld.spawnParticles(AvatarParticles.STONE_CHIP,
                    center.x + radius * Math.cos(theta + Math.PI), center.y - 0.2, center.z + radius * Math.sin(theta + Math.PI),
                    2, 0, 0, 0, 0.03);
            serverWorld.spawnParticles(AvatarParticles.GUST_CURL,
                    center.x + radius * Math.cos(theta + Math.PI * 1.5), center.y + 0.1, center.z + radius * Math.sin(theta + Math.PI * 1.5),
                    2, 0, 0, 0, 0.05);

            // Gentle ascending levitation
            if (user.getVelocity().y < 0.12) {
                user.setVelocity(user.getVelocity().x * 0.8, 0.06, user.getVelocity().z * 0.8);
                user.velocityModified = true;
            }

            if (elapsed % 6 == 0) {
                serverWorld.playSound(null, user.getBlockPos(),
                        SoundEvents.BLOCK_BEACON_AMBIENT, SoundCategory.PLAYERS, 0.8f, 1.0f + elapsed * 0.02f);
            }
        }
    }

    @Override
    public ItemStack finishUsing(ItemStack stack, World world, LivingEntity user) {
        if (!world.isClient() && user instanceof ServerPlayerEntity serverPlayer) {
            // Trigger 35-second Avatar State with full cataclysmic visual spectacle
            AvatarServerEvents.triggerAvatarState(serverPlayer, 700, false);
            serverPlayer.getItemCooldownManager().set(this, COOLDOWN_TICKS);
        }
        return stack;
    }
}
