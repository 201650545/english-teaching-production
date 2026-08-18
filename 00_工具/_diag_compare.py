import re

def dump(path, label, tag, n=2):
    h = open(path, encoding='utf-8').read()
    print('='*30, label, '='*30)
    for i, m in enumerate(re.finditer(tag, h)):
        if i >= n:
            break
        start = m.start()
        # print 400 chars after
        print(h[start:start+500])
        print('-----')

dump(r'D:\英语教学\邓兴华\第19课时\课件成品_网页PPT\第19课时_课件_中等.html', 'L19 quiz-q', r'<div class="quiz-q"')
dump(r'D:\英语教学\邓兴华\第18课时\课件成品_网页PPT\第18课时_课件_中等.html', 'L18 quiz-q', r'<div class="quiz-q"')
dump(r'D:\英语教学\邓兴华\第18课时\课件成品_网页PPT\第18课时_课件_中等.html', 'L18 quiz-container', r'<div class="quiz-container"')