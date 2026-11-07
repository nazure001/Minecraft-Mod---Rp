damage @s 7 minecraft:in_fire
execute at @s if block ~ ~ ~ air run setblock ~ ~ ~ fire
playsound minecraft:entity.generic.burn player @a ~ ~ ~ 0.8 1.0
