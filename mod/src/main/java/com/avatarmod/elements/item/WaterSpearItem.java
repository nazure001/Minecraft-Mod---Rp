package com.avatarmod.elements.item;

import com.avatarmod.elements.skill.ElementalInteractions;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.entity.effect.StatusEffectInstance;
import net.minecraft.entity.effect.StatusEffects;
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
 * Water Tribe Harpoon Spear — piercing reach weapon.
 * Attack Damage: 7.5 (Attack speed 1.7/s).
 * Left click: Piercing thrust + Water splash + douses fire + Slowness I.
 * Right click: Water Piercing Lunge (reaches 4.5 blocks, pierces multiple enemies, pulls targets).
 */
public class WaterSpearItem extends SwordItem {

    public WaterSpearItem() {
        super(ToolMaterials.DIAMOND, new Item.Settings()
                .maxCount(1)
                .attributeModifiers(SwordItem.createAttributeModifiers(ToolMaterials.DIAMOND, 3, -2.3f)));
    }

    @Override
    public boolean postHit(ItemStack stack, LivingEntity target, LivingEntity attacker) {
        target.extinguish();
        target.addStatusEffect(new StatusEffectInstance(StatusEffects.SLOWNESS, 80, 0)); // 4s Slowness I

        if (attacker.getWorld() instanceof ServerWorld serverWorld) {
            Vec3d pos = target.getPos().add(0, target.getHeight() * 0.5, 0);
            serverWorld.spawnParticles(ParticleTypes.SPLASH, pos.x, pos.y, pos.z, 15, 0.3, 0.3, 0.3, 0.1);
            serverWorld.spawnParticles(ParticleTypes.FALLING_WATER, pos.x, pos.y, pos.z, 8, 0.2, 0.2, 0.2, 0.05);
            serverWorld.playSound(null, target.getX(), target.getY(), target.getZ(),
                    SoundEvents.ENTITY_PLAYER_SPLASH, SoundCategory.PLAYERS, 0.8f, 1.2f);
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

            // Piercing beam line check (4.5 blocks reach)
            Vec3d end = eyePos.add(look.multiply(4.5));
            Box box = new Box(eyePos, end).expand(1.2);

            List<LivingEntity> targets = world.getEntitiesByClass(
                    LivingEntity.class, box,
                    e -> e != user && e.isAlive()
            );

            DamageSource dmgSource = world.getDamageSources().playerAttack(user);
            for (LivingEntity target : targets) {
                target.damage(dmgSource, 7.5f);
                target.extinguish();
                target.addStatusEffect(new StatusEffectInstance(StatusEffects.SLOWNESS, 100, 1));
                // Pull toward user (harpoon catch)
                Vec3d pull = user.getPos().subtract(target.getPos()).normalize().multiply(0.4);
                target.addVelocity(pull.x, 0.15, pull.z);
                target.velocityModified = true;
            }

            // Piercing water line particles
            for (double d = 0.5; d <= 4.5; d += 0.5) {
                Vec3d p = eyePos.add(look.multiply(d));
                serverWorld.spawnParticles(ParticleTypes.SPLASH, p.x, p.y, p.z, 4, 0.1, 0.1, 0.1, 0.05);
                serverWorld.spawnParticles(ParticleTypes.BUBBLE, p.x, p.y, p.z, 3, 0.1, 0.1, 0.1, 0.02);
            }

            // Douse fire blocks
            ElementalInteractions.douseFireBlocks(serverWorld, eyePos.add(look.multiply(3.0)), 2.5);

            serverWorld.playSound(null, user.getX(), user.getY(), user.getZ(),
                    SoundEvents.ENTITY_PLAYER_SPLASH_HIGH_SPEED, SoundCategory.PLAYERS, 0.9f, 1.1f);
        }

        user.getItemCooldownManager().set(this, 25);
        return TypedActionResult.success(stack);
    }
}
