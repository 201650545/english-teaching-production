import re
b=r'D:\英语教学\邓兴华'
h=open(b+r'\第20课时\课件成品_网页PPT\第20课时_课件_中等.html',encoding='utf-8').read()
# items = elements with data-interaction-item="1" OR data-question-id
from collections import Counter
its=Counter(); acts=Counter()
items=[]
for m in re.finditer(r'<([a-z][a-z0-9]*)[^>]*(?:data-interaction-item="1"|data-question-id=")[^>]*>',h):
    tag=m.group(0); t=m.group(1)
    def ga(n):
        mm=re.search(n+r'="([^"]*)"',tag); return mm.group(1) if mm else '?'
    it=ga('data-interaction-type'); ac=ga('data-action-type')
    its[it]+=1; acts[ac]+=1
    items.append((t,it,ac))
total=len(items)
choices=sum(v for k,v in its.items() if k in ('single_choice','multiple_choice','true_false','choice'))
print('total items',total,'choices',choices,'ratio %.1f%%'%(100*choices/total))
print('interaction types',dict(its))
print('action types',dict(acts))