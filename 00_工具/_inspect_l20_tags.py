# -*- coding: utf-8 -*-
import re
p=r'D:\英语教学\邓兴华\第20课时\课件成品_网页PPT\第20课时_课件_中等.html'
data=open(p,encoding='utf-8').read()
for m in re.finditer(r'<script>|</script>|<style>|</style>|<body>|<head>|</head>|</body>|</html>', data):
    print("%8d  %s"%(m.start(), m.group(0)))
print("TOTAL:", len(data))