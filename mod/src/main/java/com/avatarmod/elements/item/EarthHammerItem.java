package com.avatarmod.elements.item;

import com.avatarmod.elements.skill.ElementalInteractions;
import net.minecraft.block.Blocks;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.entity.effect.StatusEffectInstance;
import net.minecraft.entity.effect.StatusEffects;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.item.Item;
import net.minecraft.item.ItemStack;
import net.minecraft.item.SwordItem;
import net.minecraft.item.ToolMaterials;
import net.minecraft.particle.BlockStateParticleEffect;
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
 * Earth Kingdom Warhammer — heavy crushing blunt weapon.
 * Attack Damage: 9.5 (Heavy swings).
 * Left click: Crushing strike + Seismic stumble (Slowness II) + stone shock particles.
 * Right click: Earth Ground Slam (shockwave knocks nearby enemies into air, clears vegetation).
 */
public class EarthHammerItem extends SwordItem {

    public EarthHammerItem() {
        super(ToolMaterials.DIAMOND, new Item.Settings()
                .maxCount(1)
                .attributeModifiers(SwordItem.createAttributeModifiers(ToolMaterials.DIAMOND, 5, -3.0f)));
    }

    @Override
    public boolean postHit(ItemStack stack, LivingEntity target, LivingEntity attacker) {
        target.addStatusEffect(new StatusEffectInstance(StatusEffects.SLOWNESS, 60, 1)); // 3s Slowness II

        if (attacker.getWorld() instanceof ServerWorld serverWorld) {
            Vec3d pos = target.getPos().add(0, 0.2, 0);
            serverWorld.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, Blocks.DEEPSLATE.getDefaultState()),
                    pos.x, pos.y, pos.z, 20, 0.3, 0.2, 0.3, 0.15);
            serverWorld.playSound(null, target.getX(), target.getY(), target.getZ(),
                    SoundEvents.BLOCK_ANVIL_LAND, SoundCategory.PLAYERS, 0.6f, 1.4f);
        }

        return super.postHit(stack, target, attacker);
    }

    @Override
    public TypedActionResult<ItemStack> use(World world, PlayerEntity user, Hand hand) {
        ItemStack stack = user.getStackInHand(hand);
        user.swingHand(hand, true);

        if (!world.isClient() && world instanceof ServerWorld serverWorld) {
            Vec3d origin = user.getPos();
            double radius = 3.5;

            // Clear surface grass/flowers in radius
            ElementalInteractions.clearVegetation(serverWorld, origin, radius);

            Box box = Box.of(origin, radius * 2, 2.5, radius * 2);
            List<LivingEntity> targets = world.getEntitiesByClass(
                    LivingEntity.class, box,
                    e -> e != user && e.isAlive() && e.squaredDistanceTo(user) <= radius * radius
            );

            DamageSource dmgSource = world.getDamageSources().playerAttack(user);
            for (LivingEntity target : targets) {
                target.damage(dmgSource, 8.0f);
                target.addVelocity(0, 0.45, 0); // Knocks enemies up into the air
                target.velocityModified = true;
                target.addStatusEffect(new StatusEffectInstance(StatusEffects.SLOWNESS, 80, 1));
            }

            // Shockwave particles
            serverWorld.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, Blocks.STONE.getDefaultState()),
                    origin.x, origin.y + 0.1, origin.z, 40, 1.5, 0.2, 1.5, 0.2);
            serverWorld.spawnParticles(ParticleTypes.CAMPFIRE_COSY_SMOKE,
                    origin.x, origin.y + 0.2, origin.z, 15, 1.0, 0.1, 1.0, 0.05);

            serverWorld.playSound(null, origin.x, origin.y, origin.z,
                    SoundEvents.ENTITY_GENERIC_EXPLODE.value(), SoundCategory.PLAYERS, 0.9f, 1.6f);
        }

        user.getItemCooldownManager().set(this, 30);
        return TypedActionResult.success(stack);
    }
}
