give @s minecraft:warped_fungus_on_a_stick[custom_model_data=5005,custom_data={avatar_item:true,avatar_skill:"avatar"},item_name='{"text":"Cosmic Avatar Relic","color":"gold","bold":true}',lore=['{"text":"The sacred conduit of Raava","color":"yellow"}','{"text":"Right-Click: Four-Element Orbital Sphere","color":"aqua"}','{"text":"Shift + Right-Click: Enter Avatar State!","color":"light_purple"}']]
scoreboard players set @s av_mast_fire 1
scoreboard players set @s av_mast_water 1
scoreboard players set @s av_mast_earth 1
scoreboard players set @s av_mast_air 1
scoreboard players set @s av_mast_all 1
advancement grant @s only avatar_skills:avatar/state
