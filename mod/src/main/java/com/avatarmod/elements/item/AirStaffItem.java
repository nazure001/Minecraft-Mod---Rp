package com.avatarmod.elements.item;

import com.avatarmod.elements.particle.AvatarParticles;
import net.minecraft.entity.Entity;
import net.minecraft.entity.LivingEntity;
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
 * Air Nomad Glider Staff — canonical kinetic mobility & sweep combat weapon.
 * Attack Damage: 6.0 (Attack speed 2.0/s).
 *
 * Gameplay Mechanics:
 * 1. Glider Flight & Aerodynamics (Airborne Passive):
 *    When held in mid-air, deploys authentic glider wings providing smooth forward gliding,
 *    controlled slow falling, thermal lift when pitching up, and total fall damage immunity.
 * 2. Left Click (Sweep Strike):
 *    Kinetic strike launching target upward with concussive air blast.
 * 3. Right Click:
 *    - On Ground: "Air Vault" launching player high into the air.
 *    - In Mid-Air: "Thermal Updraft Burst" projecting player forward and upward into sustained flight!
 */
public class AirStaffItem extends SwordItem {

    public AirStaffItem() {
        super(ToolMaterials.IRON, new Item.Settings()
                .maxCount(1)
                .attributeModifiers(SwordItem.createAttributeModifiers(ToolMaterials.IRON, 3, -2.0f)));
    }

    @Override
    public void inventoryTick(ItemStack stack, World world, Entity entity, int slot, boolean selected) {
        if (!(entity instanceof PlayerEntity player)) return;
        boolean isHolding = selected || player.getOffHandStack().isOf(this);
        if (!isHolding) return;

        // Glider flight mechanics: active while in mid-air
        boolean midAir = !player.isOnGround() && !player.isTouchingWater() && !player.isClimbing() && !player.isInLava();
        if (midAir) {
            Vec3d look = player.getRotationVec(1.0f);
            Vec3d vel = player.getVelocity();

            // Aerodynamic forward glide and slow descent
            double forwardSpeed = 0.72;
            double vy = Math.max(vel.y * 0.82, -0.12);

            // Pitching up converts forward air velocity into thermal updraft climb
            if (look.y > 0.15) {
                vy = Math.min(vy + 0.05, 0.22);
            }

            player.setVelocity(look.x * forwardSpeed, vy, look.z * forwardSpeed);
            player.velocityModified = true;
            player.fallDistance = 0.0f;

            if (!world.isClient() && world instanceof ServerWorld serverWorld && player.age % 4 == 0) {
                Vec3d pos = player.getPos().add(0, 0.4, 0);
                serverWorld.spawnParticles(ParticleTypes.CLOUD, pos.x, pos.y, pos.z, 2, 0.3, 0.1, 0.3, 0.02);
                serverWorld.spawnParticles(AvatarParticles.GUST_CURL, pos.x, pos.y, pos.z, 1, 0.2, 0.1, 0.2, 0.04);
                if (player.age % 14 == 0) {
                    serverWorld.playSound(null, player.getBlockPos(),
                            SoundEvents.ITEM_ELYTRA_FLYING, SoundCategory.PLAYERS, 0.65f, 1.4f);
                }
            }
        }
    }

    @Override
    public boolean postHit(ItemStack stack, LivingEntity target, LivingEntity attacker) {
        target.addVelocity(0, 0.40, 0); // Extra upward air lift
        target.velocityModified = true;

        if (attacker.getWorld() instanceof ServerWorld serverWorld) {
            Vec3d pos = target.getPos().add(0, target.getHeight() * 0.5, 0);
            serverWorld.spawnParticles(ParticleTypes.CLOUD, pos.x, pos.y, pos.z, 12, 0.25, 0.25, 0.25, 0.08);
            serverWorld.spawnParticles(ParticleTypes.POOF, pos.x, pos.y, pos.z, 6, 0.1, 0.1, 0.1, 0.03);
            serverWorld.playSound(null, target.getX(), target.getY(), target.getZ(),
                    SoundEvents.ENTITY_PLAYER_ATTACK_KNOCKBACK, SoundCategory.PLAYERS, 1.0f, 1.3f);
        }

        return super.postHit(stack, target, attacker);
    }

    @Override
    public TypedActionResult<ItemStack> use(World world, PlayerEntity user, Hand hand) {
        ItemStack stack = user.getStackInHand(hand);
        user.swingHand(hand, true);

        Vec3d look = user.getRotationVec(1.0f);
        boolean midAir = !user.isOnGround() && !user.isTouchingWater() && !user.isClimbing();

        if (midAir) {
            // Thermal Updraft Burst in flight
            user.setVelocity(look.x * 0.95, 0.65, look.z * 0.95);
            user.velocityModified = true;
            user.fallDistance = 0.0f;

            if (!world.isClient() && world instanceof ServerWorld serverWorld) {
                Vec3d pos = user.getPos().add(0, 0.3, 0);
                serverWorld.spawnParticles(AvatarParticles.GUST_CURL, pos.x, pos.y, pos.z, 12, 0.3, 0.3, 0.3, 0.08);
                serverWorld.spawnParticles(ParticleTypes.CLOUD, pos.x, pos.y, pos.z, 10, 0.3, 0.2, 0.3, 0.05);
                serverWorld.playSound(null, user.getX(), user.getY(), user.getZ(),
                        SoundEvents.ITEM_ELYTRA_FLYING, SoundCategory.PLAYERS, 1.2f, 1.5f);
                serverWorld.playSound(null, user.getX(), user.getY(), user.getZ(),
                        SoundEvents.ENTITY_PHANTOM_FLAP, SoundCategory.PLAYERS, 1.0f, 1.4f);
            }
        } else {
            // Ground Air Vault: launch player upward and forward
            user.setVelocity(look.x * 0.80, 0.85, look.z * 0.80);
            user.velocityModified = true;

            if (!world.isClient() && world instanceof ServerWorld serverWorld) {
                Vec3d feet = user.getPos();
                serverWorld.spawnParticles(ParticleTypes.CLOUD, feet.x, feet.y + 0.1, feet.z,
                        16, 0.4, 0.1, 0.4, 0.08);
                serverWorld.spawnParticles(ParticleTypes.POOF, feet.x, feet.y + 0.2, feet.z,
                        10, 0.3, 0.1, 0.3, 0.04);
                serverWorld.playSound(null, user.getX(), user.getY(), user.getZ(),
                        SoundEvents.ENTITY_PHANTOM_FLAP, SoundCategory.PLAYERS, 1.1f, 1.4f);
            }
        }

        user.getItemCooldownManager().set(this, 20);
        return TypedActionResult.success(stack);
    }
}
