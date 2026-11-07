# Give All Avatar Skills
function avatar_skills:setup
function avatar_skills:tree/init_player
function avatar_skills:give/fire
function avatar_skills:give/water
function avatar_skills:give/earth
function avatar_skills:give/air
function avatar_skills:give/avatar_relic
function avatar_skills:give/mastery
function avatar_skills:give/chi_orbs
function avatar_skills:give/sub_bending_foci
tellraw @s [{"text":"[Avatar System] ","color":"gold","bold":true},{"text":"All Avatar Scrolls, Relics, and Sub-bending Foci have been granted!","color":"green"}]
tellraw @s [{"text":"[Controls Guide] ","color":"aqua","bold":true},{"text":"Right-Click (Mouse Klik Kanan) to cast primary bending. Shift + Right-Click to cast defensive/mobility bending. (Make sure you are in Survival/Adventure mode).","color":"yellow"}]
