give @s minecraft:warped_fungus_on_a_stick[custom_model_data=5001,custom_data={avatar_item:true,avatar_skill:"fire"},item_name='{"text":"Scroll of Firebending","color":"red","bold":true}',lore=['{"text":"Discipline of the Sun Warriors","color":"gold"}','{"text":"Right-Click: Fire Blast","color":"yellow"}','{"text":"Shift + Right-Click: Jet Propulsion","color":"yellow"}']]
scoreboard players set @s av_mast_fire 1
advancement grant @s only avatar_skills:fire/root
