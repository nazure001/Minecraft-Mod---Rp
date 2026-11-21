import urllib.request
import re
import json

url = 'https://www.youtube.com/watch?v=IphpIUm_F7E'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        
    m = re.search(r'("captionTracks":\s*\[.*?\])', html)
    if m:
        captions_str = '{' + m.group(1) + '}'
        data = json.loads(captions_str)
        tracks = data.get('captionTracks', [])
        print(f"Found {len(tracks)} caption tracks:")
        for t in tracks:
            print("Language:", t.get('name', {}).get('simpleText'), t.get('baseUrl'))
            # fetch first caption track
            t_url = t.get('baseUrl')
            t_req = urllib.request.Request(t_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(t_req) as t_resp:
                xml = t_resp.read().decode('utf-8', errors='ignore')
                texts = re.findall(r'<text[^>]*>(.*?)</text>', xml)
                print(f"Sample transcript ({len(texts)} lines):")
                print("\n".join(texts[:30]))
                with open(r'd:\repo\Minecraft Mod & Rp\mod\tools\yt_transcript.txt', 'w', encoding='utf-8') as out:
                    out.write("\n".join(texts))
            break
    else:
        print("No captionTracks found")
except Exception as e:
    print('Error:', e)
