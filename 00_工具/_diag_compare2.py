import re
def dump(path, label, tags, n=3):
    h = open(path, encoding='utf-8').read()
    print('='*30, label, '='*30)
    for tag in tags:
        cnt = len(re.findall(re.escape(tag), h))
        print('tag', tag, 'count', cnt)
    for i, m in enumerate(re.finditer(r'<div class="quiz-(q|container)"', h)):
        if i >= n:
            break
        start = m.start()
        end = h.find('>', start)
        print(h[start:end+1])
        print('  body:', repr(h[end+1:end+260]))
        print('-----')

dump(r'D:\英语教学\邓兴华\第17课时\课件成品_网页PPT\第17课时_课件_中等.html', 'L17', [r'class="quiz-q"', r'class="quiz-container"'])
dump(r'D:\英语教学\邓兴华\第16课时\课件成品_网页PPT\第16课时_课件_中等.html', 'L16', [r'class="quiz-q"', r'class="quiz-container"'])