# Magma cools back to solidified cobblestone
fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 cobblestone replace magma_block
particle minecraft:smoke ~ ~0.5 ~ 1.5 0.3 1.5 0.05 30 normal
playsound minecraft:block.lava.extinguish player @a ~ ~ ~ 1.2 1.2
kill @s
