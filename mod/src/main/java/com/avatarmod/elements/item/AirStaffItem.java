package com.avatarmod.elements.item;

import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.item.Item;
import net.minecraft.item.ItemStack;
import net.minecraft.item.SwordItem;
import net.minecraft.item.ToolMaterials;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.util.Hand;
import net.minecraft.util.TypedActionResult;
import net.minecraft.util.math.Vec3d;
import net.minecraft.world.World;

/**
 * Air Nomad Glider Staff — kinetic mobility & sweep combat weapon.
 * Attack Damage: 6.0 (Attack speed 2.0/s).
 * Left click: Kinetic strike + upward air lift.
 * Right click: Glider Staff Air Vault (propels player into air/forward with air cushion).
 */
public class AirStaffItem extends SwordItem {

    public AirStaffItem() {
        super(ToolMaterials.IRON, new Item.Settings()
                .maxCount(1)
                .attributeModifiers(SwordItem.createAttributeModifiers(ToolMaterials.IRON, 3, -2.0f)));
    }

    @Override
    public boolean postHit(ItemStack stack, LivingEntity target, LivingEntity attacker) {
        target.addVelocity(0, 0.35, 0); // Extra upward air lift
        target.velocityModified = true;

        if (attacker.getWorld() instanceof ServerWorld serverWorld) {
            Vec3d pos = target.getPos().add(0, target.getHeight() * 0.5, 0);
            serverWorld.spawnParticles(ParticleTypes.CLOUD, pos.x, pos.y, pos.z, 10, 0.25, 0.25, 0.25, 0.08);
            serverWorld.spawnParticles(ParticleTypes.POOF, pos.x, pos.y, pos.z, 5, 0.1, 0.1, 0.1, 0.03);
            serverWorld.playSound(null, target.getX(), target.getY(), target.getZ(),
                    SoundEvents.ENTITY_PLAYER_ATTACK_KNOCKBACK, SoundCategory.PLAYERS, 0.9f, 1.3f);
        }

        return super.postHit(stack, target, attacker);
    }

    @Override
    public TypedActionResult<ItemStack> use(World world, PlayerEntity user, Hand hand) {
        ItemStack stack = user.getStackInHand(hand);
        user.swingHand(hand, true);

        Vec3d look = user.getRotationVec(1.0f);
        // Air Vault: launch player upward and slightly in look direction
        user.addVelocity(look.x * 0.75, 0.75, look.z * 0.75);
        user.velocityModified = true;

        if (!world.isClient() && world instanceof ServerWorld serverWorld) {
            Vec3d feet = user.getPos();
            serverWorld.spawnParticles(ParticleTypes.CLOUD, feet.x, feet.y + 0.1, feet.z,
                    15, 0.4, 0.1, 0.4, 0.08);
            serverWorld.spawnParticles(ParticleTypes.POOF, feet.x, feet.y + 0.2, feet.z,
                    8, 0.3, 0.1, 0.3, 0.04);
            serverWorld.playSound(null, user.getX(), user.getY(), user.getZ(),
                    SoundEvents.ENTITY_PHANTOM_FLAP, SoundCategory.PLAYERS, 1.0f, 1.5f);
        }

        user.getItemCooldownManager().set(this, 25);
        return TypedActionResult.success(stack);
    }
}
