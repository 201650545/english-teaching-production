import re, zipfile, glob, os
b=r'D:\英语教学\邓兴华'
past_verbs=['was','were','went','came','had','did','said','saw','took','ate','drank','bought','taught','climbed','walked','played','visited','enjoyed','realized','remained','stayed','watched','started','finished','wanted','looked','helped','arrived','left','forgot','talked','asked','answered','studied','lived','worked','returned','remembered','stopped','tried','happened','called','opened','closed','decided','showed','told','felt','thought','knew','made','gave','got','found','met','ran','swam','sat','stood','wrote','read','became','began','broke','brought','built','caught','chose','cut','drove','fell','flew','grew','heard','held','kept','led','lost','paid','put','sent','spent','told','wore','won']
def docx_text(p):
    try:
        z=zipfile.ZipFile(p)
        xml=z.read('word/document.xml').decode('utf-8')
        text=re.sub(r'<[^>]+>','',xml)
        return text
    except Exception as e:
        return 'ERROR:'+str(e)
for L in (16,17,18,19,20):
    p=os.path.join(b,'第%d课时'%L,'第%d课时_配套练习_中等.docx'%L)
    if not os.path.exists(p):
        print('L%d: MISSING'%L); continue
    t=docx_text(p)
    if t.startswith('ERROR'):
        print('L%d:%s'%(L,t[:80])); continue
    has_src = '溯源ID' in t or '溯源' in t or 'SOURCE' in t.upper() or '母本' in t or '改编' in t
    # count past tense verbs
    words=re.findall(r'[A-Za-z]+',t.lower())
    past=[w for w in words if w in past_verbs]
    past_set=set(past)
    print('L%d: len=%d 溯源标记=%s 过去时词=%s'%(L,len(t),has_src, sorted(past_set)[:25] if past_set else '无'))
print('done')