#!/usr/bin/env python3
"""Crop Avatar Elements atlas entries using docs/asset_manifest.json."""
from pathlib import Path
from PIL import Image
import json, argparse
p=argparse.ArgumentParser();p.add_argument('--pack',default='.');p.add_argument('--out',default='cropped');p.add_argument('--name',action='append');a=p.parse_args()
root=Path(a.pack);m=json.loads((root/'docs/asset_manifest.json').read_text());out=root/a.out;out.mkdir(parents=True,exist_ok=True)
for item in m['assets']:
 if a.name and item['name'] not in a.name:continue
 atlas=item.get('atlas_file')
 if not atlas:continue
 im=Image.open(root/'atlases'/atlas).convert('RGBA');x,y,w,h=(item[k] for k in ('x','y','width','height'))
 crop=im.crop((x,y,x+w,y+h));crop.save(out/(item['name']+'.png'))
print('Cropped assets into',out)
