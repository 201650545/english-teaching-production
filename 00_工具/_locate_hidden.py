# -*- coding: utf-8 -*-
import re
p=r'D:\英语教学\邓兴华\第20课时\课件成品_网页PPT\第20课时_课件_中等.html'
data=open(p,encoding='utf-8').read()
i_script=data.find('<script>')
HEAD=data[:i_script]
print("HEAD len:", len(HEAD), "div opens/closes:", len(re.findall(r'<div\b',HEAD)), len(re.findall(r'</div>',HEAD)))
# where is aria-hidden in corrupted file?
for m in re.finditer(r'aria-hidden', data):
    print("aria-hidden at", m.start())
# find L20_ITM_065 (hidden area quiz)
print("L20_ITM_065 in HEAD:", 'L20_ITM_065' in HEAD)
# find hidden area string
idx=data.find('aria-hidden')
print("context around first aria-hidden:", data[idx-100:idx+200].replace('\n',' '))
# page count in HEAD
print("pages in HEAD:", len(re.findall(r'id="page\d+"',HEAD)))
# check the second HEAD (HEAD2) also
i_head2=data.find('<head>', i_script+8)
print("HEAD2 starts at", i_head2)
# find aria-hidden occurrences relative to HEAD2
print("aria-hidden between script and head2:", len(re.findall(r'aria-hidden', data[i_script:i_head2])))