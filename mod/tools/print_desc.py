import urllib.request
import re

url = 'https://www.youtube.com/watch?v=9FxjDpXvtuo'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

desc_m = re.search(r'"shortDescription":"(.*?)"', html)
if desc_m:
    raw = desc_m.group(1)
    # decode escapes
    cleaned = raw.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
    print('FULL DESCRIPTION:')
    print(cleaned)
