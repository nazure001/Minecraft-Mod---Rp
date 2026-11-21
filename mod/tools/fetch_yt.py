import urllib.request
import re

url = 'https://www.youtube.com/watch?v=IphpIUm_F7E'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        
        title_m = re.search(r'<title>(.*?)</title>', html)
        if title_m:
            print('Title:', title_m.group(1))
            
        desc_m = re.search(r'"shortDescription":"(.*?)"', html)
        if desc_m:
            desc = desc_m.group(1).encode('utf-8').decode('unicode_escape')
            print('\nDescription:\n', desc[:1200])
except Exception as e:
    print('Error:', e)
