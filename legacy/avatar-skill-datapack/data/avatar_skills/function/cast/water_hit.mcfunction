damage @s 6 minecraft:magic
effect give @s minecraft:slowness 3 1 true
# Pull target towards player
execute facing entity @p feet run tp @s ^ ^ ^0.8
playsound minecraft:entity.player.attack.sweep player @a ~ ~ ~ 0.8 1.5
