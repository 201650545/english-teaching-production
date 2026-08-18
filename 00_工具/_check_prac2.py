import json, os
base = r'D:\英语教学\00_工具'
d = json.load(open(os.path.join(base, 'practice_content_DXH_L20.json'), encoding='utf-8'))
print('=== _doc ===')
print(json.dumps(d['_doc'], ensure_ascii=False, indent=1)[:800])
print('=== reading_a keys ===')
ra = d['reading_a']
print(type(ra))
if isinstance(ra, dict):
    print('keys:', list(ra.keys()))
    print(json.dumps(ra, ensure_ascii=False, indent=1)[:1200])
elif isinstance(ra, list):
    print(json.dumps(ra, ensure_ascii=False, indent=1)[:1200])
print('=== cloze ===')
print(json.dumps(d['cloze'], ensure_ascii=False, indent=1)[:900])