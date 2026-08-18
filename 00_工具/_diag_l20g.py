import re
b=r'D:\英语教学\邓兴华'
h=open(b+r'\第20课时\课件成品_网页PPT\第20课时_课件_中等.html',encoding='utf-8').read()
# link-container
for m in re.finditer(r'class="[^"]*\blink-container\b',h):
    print('=== link-container @',m.start(),'===')
    print(h[m.start()-250:m.start()+700].replace('\n','\\n'))
    print()
# order-container
for m in re.finditer(r'class="[^"]*\border-container\b',h):
    print('=== order-container @',m.start(),'===')
    print(h[m.start()-250:m.start()+700].replace('\n','\\n'))
    print()
# order-chunks
for m in re.finditer(r'class="[^"]*\border-chunks\b',h):
    print('=== order-chunks @',m.start(),'===')
    print(h[m.start()-250:m.start()+500].replace('\n','\\n'))
    print()