import re
h = open(r'D:\英语教学\邓兴华\第16课时\课件成品_网页PPT\第16课时_课件_中等.html', encoding='utf-8').read()
print('### ALL quiz-q AND quiz-container opening tags ###')
for tag in ['quiz-q', 'quiz-container']:
    for m in re.finditer(r'<div class="%s"' % tag, h):
        start = m.start()
        end = h.find('>', start)
        t = h[start:end+1]
        t = t.replace('\n', '\\n')
        print('[' + tag + ' len=' + str(len(t)) + ']', t)
        print('---')