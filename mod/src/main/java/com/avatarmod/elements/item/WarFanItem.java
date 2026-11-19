package com.avatarmod.elements.item;

import com.avatarmod.elements.skill.ElementalInteractions;
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
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;
import net.minecraft.world.World;

import java.util.List;

/**
 * Kyoshi Warrior War Fan — agile defensive and deflection weapon.
 * Attack Damage: 5.5 (Fast attack speed 2.6/s).
 * Left click: Quick slice + directional knockback.
 * Right click: Fan Gust & Deflection (sweeps wind burst, pushes enemies, deflects projectiles).
 */
public class WarFanItem extends SwordItem {

    public WarFanItem() {
        super(ToolMaterials.IRON, new Item.Settings()
                .maxCount(1)
                .attributeModifiers(SwordItem.createAttributeModifiers(ToolMaterials.IRON, 2, -1.4f)));
    }

    @Override
    public boolean postHit(ItemStack stack, LivingEntity target, LivingEntity attacker) {
        if (attacker.getWorld() instanceof ServerWorld serverWorld) {
            Vec3d pos = target.getPos().add(0, target.getHeight() * 0.5, 0);
            serverWorld.spawnParticles(ParticleTypes.SWEEP_ATTACK, pos.x, pos.y, pos.z, 1, 0, 0, 0, 0);
            serverWorld.spawnParticles(ParticleTypes.CLOUD, pos.x, pos.y, pos.z, 6, 0.2, 0.2, 0.2, 0.05);
            serverWorld.playSound(null, target.getX(), target.getY(), target.getZ(),
                    SoundEvents.ENTITY_PLAYER_ATTACK_SWEEP, SoundCategory.PLAYERS, 0.9f, 1.4f);
        }

        return super.postHit(stack, target, attacker);
    }

    @Override
    public TypedActionResult<ItemStack> use(World world, PlayerEntity user, Hand hand) {
        ItemStack stack = user.getStackInHand(hand);
        user.swingHand(hand, true);

        if (!world.isClient() && world instanceof ServerWorld serverWorld) {
            Vec3d eyePos = user.getEyePos();
            Vec3d look = user.getRotationVec(1.0f);
            Vec3d center = eyePos.add(look.multiply(2.0));

            // 1. Deflect projectiles in front
            if (user instanceof net.minecraft.server.network.ServerPlayerEntity serverPlayer) {
                ElementalInteractions.deflectProjectiles(serverWorld, serverPlayer, eyePos, look, 4.0, 1.5);
            }

            // 2. Clear loose grass
            ElementalInteractions.clearVegetation(serverWorld, eyePos.add(look.multiply(2.0)), 2.0);

            // 3. Push and damage enemies
            Box box = Box.of(center, 4.0, 2.5, 4.0);
            List<LivingEntity> targets = world.getEntitiesByClass(
                    LivingEntity.class, box,
                    e -> e != user && e.isAlive() && e.squaredDistanceTo(user) <= 16.0
            );

            DamageSource dmgSource = world.getDamageSources().playerAttack(user);
            for (LivingEntity target : targets) {
                target.damage(dmgSource, 5.0f);
                target.takeKnockback(1.0, -look.x, -look.z);
            }

            // Wind gust particles
            for (double d = 0.5; d <= 3.5; d += 0.8) {
                Vec3d p = eyePos.add(look.multiply(d));
                serverWorld.spawnParticles(ParticleTypes.CLOUD, p.x, p.y, p.z, 3, 0.3, 0.2, 0.3, 0.05);
                serverWorld.spawnParticles(ParticleTypes.POOF, p.x, p.y, p.z, 2, 0.2, 0.1, 0.2, 0.03);
            }

            serverWorld.playSound(null, user.getX(), user.getY(), user.getZ(),
                    SoundEvents.ITEM_ELYTRA_FLYING, SoundCategory.PLAYERS, 0.8f, 1.6f);
        }

        user.getItemCooldownManager().set(this, 20);
        return TypedActionResult.success(stack);
    }
}
