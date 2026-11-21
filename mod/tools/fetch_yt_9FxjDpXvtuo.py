import urllib.request
import re

url = 'https://www.youtube.com/watch?v=9FxjDpXvtuo'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    
    title_m = re.search(r'<title>(.*?)</title>', html)
    if title_m:
        print('Title:', title_m.group(1))

    desc_m = re.search(r'"shortDescription":"(.*?)"', html)
    if desc_m:
        print('\nFull Description:\n', desc_m.group(1).replace(r'\n', '\n'))

    m = re.search(r'("captionTracks":\s*\[.*?\])', html)
    if m:
        import json
        captions_str = '{' + m.group(1) + '}'
        data = json.loads(captions_str)
        t_url = data['captionTracks'][0]['baseUrl']
        print('\nBase URL:\n', t_url)
        
        req2 = urllib.request.Request(t_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req2) as resp2:
            content = resp2.read().decode('utf-8', errors='ignore')
            print('Content length:', len(content))
            print('Content snippet:', content[:500])
            with open(r'd:\repo\Minecraft Mod & Rp\mod\tools\raw_captions.txt', 'w', encoding='utf-8') as out:
                out.write(content)
except Exception as e:
    import traceback
    traceback.print_exc()
