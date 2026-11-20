import json

for path in ['air_staff.json', 'dual_swords.json', 'earth_hammer.json', 'war_fan.json', 'water_spear.json']:
    full = 'd:/repo/Minecraft Mod & Rp/mod/src/main/resources/assets/avatar_elements/models/item/' + path
    data = json.load(open(full, 'r', encoding='utf-8'))
    print(f"=== {path} ===")
    for e in data.get('elements', []):
        name = e.get('name', '').lower()
        if 'grip' in name or 'handle' in name or 'shaft' in name or 'pommel' in name:
            print(f"  {e.get('name')}: from={e['from']} to={e['to']}")
