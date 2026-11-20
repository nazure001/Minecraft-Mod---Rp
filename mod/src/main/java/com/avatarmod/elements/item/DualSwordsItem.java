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
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;
import net.minecraft.world.World;

import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Zuko Dual Dao Broadswords — fast twin-blade combat weapon.
 * - Auto-Dual Wield: Visually renders in both hands when held in main hand.
 * - Alternating Attack Combo:
 *     Hit 1: Main hand fire slash (Right arm).
 *     Hit 2: Offhand fire slash (Left arm).
 *     Hit 3: Twin blade cross-slash.
 *     Hit 4: 360-degree Fire Whirlwind finisher (+AoE damage and ignition).
 * - Right click: Twin Dao Cross-Sweep arc attack (6.0 damage, ignites, knocks back).
 */
public class DualSwordsItem extends SwordItem {

    private static final Map<UUID, Integer> COMBO_STEP = new ConcurrentHashMap<>();
    private static final Map<UUID, Long> LAST_HIT_TIME = new ConcurrentHashMap<>();
    private static final long COMBO_TIMEOUT_MS = 1500; // 1.5s combo reset window

    public DualSwordsItem() {
        super(ToolMaterials.IRON, new Item.Settings()
                .maxCount(1)
                .attributeModifiers(SwordItem.createAttributeModifiers(ToolMaterials.IRON, 3, -1.8f)));
    }

    @Override
    public boolean postHit(ItemStack stack, LivingEntity target, LivingEntity attacker) {
        target.setOnFireForTicks(50); // 2.5s fire burn

        if (attacker instanceof PlayerEntity player) {
            UUID id = player.getUuid();
            long now = System.currentTimeMillis();
            long last = LAST_HIT_TIME.getOrDefault(id, 0L);
            int step = (now - last < COMBO_TIMEOUT_MS) ? (COMBO_STEP.getOrDefault(id, 0) + 1) % 4 : 0;
            COMBO_STEP.put(id, step);
            LAST_HIT_TIME.put(id, now);

            // Alternating arm swing
            if (step == 1) {
                player.swingHand(Hand.OFF_HAND, true);
            } else if (step == 2) {
                player.swingHand(Hand.MAIN_HAND, true);
            } else if (step == 3) {
                // Finisher 360 whirlwind
                player.swingHand(Hand.MAIN_HAND, true);
                player.swingHand(Hand.OFF_HAND, true);
                if (player.getWorld() instanceof ServerWorld serverWorld) {
                    Vec3d pPos = player.getPos();
                    // Spawn 360 fire ring
                    for (int i = 0; i < 16; i++) {
                        double angle = (i / 16.0) * Math.PI * 2;
                        double dx = Math.cos(angle) * 2.2;
                        double dz = Math.sin(angle) * 2.2;
                        serverWorld.spawnParticles(ParticleTypes.FLAME, pPos.x + dx, pPos.y + 0.8, pPos.z + dz, 2, 0.05, 0.05, 0.05, 0.02);
                        serverWorld.spawnParticles(ParticleTypes.SWEEP_ATTACK, pPos.x + dx * 0.5, pPos.y + 0.8, pPos.z + dz * 0.5, 1, 0, 0, 0, 0);
                    }
                    // Additional damage to nearby enemies
                    Box aoe = Box.of(pPos, 5.0, 3.0, 5.0);
                    List<LivingEntity> nearby = serverWorld.getEntitiesByClass(LivingEntity.class, aoe,
                            e -> e != player && e.isAlive() && e.squaredDistanceTo(player) <= 9.0);
                    DamageSource src = serverWorld.getDamageSources().playerAttack(player);
                    for (LivingEntity e : nearby) {
                        e.damage(src, 3.5f);
                        e.setOnFireForTicks(60);
                        e.takeKnockback(0.6, -(e.getX() - player.getX()), -(e.getZ() - player.getZ()));
                    }
                    serverWorld.playSound(null, player.getX(), player.getY(), player.getZ(),
                            SoundEvents.ENTITY_PLAYER_ATTACK_CRIT, SoundCategory.PLAYERS, 1.0f, 1.3f);
                }
            }
        }

        if (attacker.getWorld() instanceof ServerWorld serverWorld) {
            Vec3d pos = target.getPos().add(0, target.getHeight() * 0.5, 0);
            serverWorld.spawnParticles(ParticleTypes.FLAME, pos.x, pos.y, pos.z, 8, 0.25, 0.25, 0.25, 0.05);
            serverWorld.spawnParticles(ParticleTypes.SWEEP_ATTACK, pos.x, pos.y, pos.z, 1, 0, 0, 0, 0);
            serverWorld.playSound(null, target.getX(), target.getY(), target.getZ(),
                    SoundEvents.ITEM_FIRECHARGE_USE, SoundCategory.PLAYERS, 0.8f, 1.2f);
        }

        return super.postHit(stack, target, attacker);
    }

    @Override
    public TypedActionResult<ItemStack> use(World world, PlayerEntity user, Hand hand) {
        ItemStack stack = user.getStackInHand(hand);

        // Visual arm swing for offhand (or opposite hand)
        Hand swingHand = (hand == Hand.MAIN_HAND) ? Hand.OFF_HAND : Hand.MAIN_HAND;
        user.swingHand(swingHand, true);

        if (!world.isClient() && world instanceof ServerWorld serverWorld) {
            Vec3d eyePos = user.getEyePos();
            Vec3d look = user.getRotationVec(1.0f);
            Vec3d forward = eyePos.add(look.multiply(2.5));

            Box hitBox = Box.of(forward, 3.5, 2.5, 3.5);
            List<LivingEntity> targets = world.getEntitiesByClass(
                    LivingEntity.class, hitBox,
                    e -> e != user && e.isAlive() && e.squaredDistanceTo(user) <= 12.0
            );

            DamageSource dmgSource = world.getDamageSources().playerAttack(user);
            for (LivingEntity target : targets) {
                target.damage(dmgSource, 6.0f);
                target.setOnFireForTicks(40);
                target.takeKnockback(0.4, -look.x, -look.z);

                serverWorld.spawnParticles(ParticleTypes.FLAME, target.getX(), target.getBodyY(0.5), target.getZ(),
                        6, 0.2, 0.2, 0.2, 0.04);
            }

            // Fire slash sweep particles in front
            Vec3d particlePos = eyePos.add(look.multiply(1.5));
            serverWorld.spawnParticles(ParticleTypes.SWEEP_ATTACK, particlePos.x, particlePos.y - 0.2, particlePos.z,
                    1, 0.1, 0.1, 0.1, 0.0);
            serverWorld.spawnParticles(ParticleTypes.FLAME, particlePos.x, particlePos.y, particlePos.z,
                    10, 0.4, 0.2, 0.4, 0.05);

            serverWorld.playSound(null, user.getX(), user.getY(), user.getZ(),
                    SoundEvents.ENTITY_PLAYER_ATTACK_SWEEP, SoundCategory.PLAYERS, 1.0f, 1.1f);
        }

        user.getItemCooldownManager().set(this, 12);
        return TypedActionResult.success(stack);
    }
}
