# Place single wall block and register marker for cleanup
execute if block ~ ~ ~ #minecraft:replaceable run summon marker ~ ~ ~ {Tags:["avatar_wall_marker"],Age:0}
execute if block ~ ~ ~ #minecraft:replaceable run setblock ~ ~ ~ stone
