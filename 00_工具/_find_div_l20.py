# -*- coding: utf-8 -*-
import re, sys
p = r'D:\英语教学\邓兴华\第20课时\课件成品_网页PPT\第20课时_课件_中等.html'
h = open(p, encoding='utf-8').read()
tokens = re.finditer(r'<div\b(?![^>]*/)|</div>', h)
stack = []
unmatched = []
def lineno(pos):
    return h.count('\n', 0, pos) + 1
for m in tokens:
    tok = m.group(0)
    pos = m.start()
    context = h[pos:pos+90].replace('\n',' ')
    if tok == '<div':
        stack.append((pos, lineno(pos), context))
    else:
        if stack:
            stack.pop()
        else:
            unmatched.append((pos, lineno(pos), context))
out = []
out.append("Unclosed <div> at end: %d" % len(stack))
for pos, ln, ctx in stack[-15:]:
    out.append("  L%d pos=%d: %s" % (ln, pos, ctx))
out.append("Extra </div> unmatched: %d" % len(unmatched))
for pos, ln, ctx in unmatched[:10]:
    out.append("  L%d pos=%d: %s" % (ln, pos, ctx))
sys.stdout.buffer.write(("\n".join(out)).encode('utf-8', 'replace'))