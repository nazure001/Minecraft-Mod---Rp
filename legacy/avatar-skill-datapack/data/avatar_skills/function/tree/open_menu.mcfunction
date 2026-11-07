# Open Interactive Skill Tree
tellraw @s ""
tellraw @s [{"text":"==================== ","color":"gold","bold":true},{"text":"AVATAR MASTERY SHRINE","color":"yellow","bold":true},{"text":" ====================","color":"gold","bold":true}]
tellraw @s [{"text":"Available Skill Points: ","color":"gray"},{"score":{"name":"@s","objective":"av_chi_points"},"color":"aqua","bold":true},{"text":" (Earn +1 point every time you level up!)","color":"yellow"}]
tellraw @s ""
tellraw @s [{"text":"--- PASSIVE CULTIVATION TREE ---","color":"gold","bold":true}]
tellraw @s [{"text":"[🏃 AGILITY] ","color":"green","bold":true},{"text":"Level: ","color":"gray"},{"score":{"name":"@s","objective":"av_stat_agi"},"color":"white"},{"text":"/5  "},{"text":"[+] UPGRADE","color":"gold","bold":true,"clickEvent":{"action":"run_command","value":"/function avatar_skills:tree/upgrade_agi"},"hoverEvent":{"action":"show_text","value":"Costs 1 Point. Boosts Speed & Safe Fall Distance."}}]
tellraw @s [{"text":"[🧘 CHI MASTERY] ","color":"aqua","bold":true},{"text":"Level: ","color":"gray"},{"score":{"name":"@s","objective":"av_stat_chi"},"color":"white"},{"text":"/5  "},{"text":"[+] UPGRADE","color":"gold","bold":true,"clickEvent":{"action":"run_command","value":"/function avatar_skills:tree/upgrade_chi"},"hoverEvent":{"action":"show_text","value":"Costs 1 Point. Boosts Max Chi & Regeneration Speed."}}]
tellraw @s [{"text":"[🛡️ RESILIENCE] ","color":"red","bold":true},{"text":"Level: ","color":"gray"},{"score":{"name":"@s","objective":"av_stat_res"},"color":"white"},{"text":"/5  "},{"text":"[+] UPGRADE","color":"gold","bold":true,"clickEvent":{"action":"run_command","value":"/function avatar_skills:tree/upgrade_res"},"hoverEvent":{"action":"show_text","value":"Costs 1 Point. Permanently grants Extra Hearts (up to 40 HP)."}}]
tellraw @s [{"text":"[⚡ ELEMENTAL POTENCY] ","color":"light_purple","bold":true},{"text":"Level: ","color":"gray"},{"score":{"name":"@s","objective":"av_stat_pot"},"color":"white"},{"text":"/5  "},{"text":"[+] UPGRADE","color":"gold","bold":true,"clickEvent":{"action":"run_command","value":"/function avatar_skills:tree/upgrade_pot"},"hoverEvent":{"action":"show_text","value":"Costs 1 Point. Amplifies damage and blast radius of all bending skills."}}]
tellraw @s ""
tellraw @s [{"text":"--- ACTIVE ELEMENTAL DISCIPLINES ---","color":"gold","bold":true}]
tellraw @s [{"text":"• Fire: "},{"score":{"name":"@s","objective":"av_mast_fire"},"color":"red"},{"text":" | Water: "},{"score":{"name":"@s","objective":"av_mast_water"},"color":"blue"},{"text":" | Earth: "},{"score":{"name":"@s","objective":"av_mast_earth"},"color":"dark_green"},{"text":" | Air: "},{"score":{"name":"@s","objective":"av_mast_air"},"color":"yellow"}]
tellraw @s [{"text":"💡 Press 'L' to inspect your full Avatar Advancement Skill Tree!","color":"yellow","italic":true}]
tellraw @s [{"text":"=====================================================","color":"gold","bold":true}]
