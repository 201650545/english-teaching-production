# -*- coding: utf-8 -*-
import re

path = r"D:\英语教学\邓兴华\第15课时\课件成品_网页PPT\第15课时_课件_中等.html"
src = open(path, encoding="utf-8").read()

# Global token walk over the ENTIRE file with byte offsets
tokens = list(re.finditer(r'<div\b[^>]*>|</div>', src))
open_count = 0
close_count = 0
depth = 0
# Track unclosed opens: stack of (offset, tag, depth_when_opened)
stack = []
unclosed = []

for m in tokens:
    t = m.group(0)
    if t.startswith('</div>'):
        close_count += 1
        depth -= 1
        if depth < 0:
            # extra close
            pass
        if stack:
            stack.pop()
        else:
            unclosed.append(("EXTRA_CLOSE", m.start()))
    else:
        open_count += 1
        depth += 1
        stack.append((m.start(), t[:70], depth))

print("global opens=%d closes=%d end_depth=%d" % (open_count, close_count, depth))
print("stack size at end:", len(stack))
# The bottom of stack = the earliest unclosed opens
print("=== first 50 unclosed opens (from bottom) ===")
for off, tag, d in stack[:50]:
    ctx = src[max(0, off-50):off+20].replace("\n", " ")
    print("depth_when=%d @%d tag=%s" % (d, off, tag))
    print("   ctx: ...%s" % ctx[-80:])