# -*- coding: utf-8 -*-
p=r'D:\英语教学\邓兴华\第20课时\课件成品_网页PPT\第20课时_课件_中等.html'
data=open(p,encoding='utf-8').read()
print("total len:", len(data))
i1=data.find('<script>')
print("first <script> at", i1)
print("HEAD (first 200):", data[:200].replace('\n',' '))
i2=data.find('<script>', i1+8)
print("second <script> at", i2)
print("HEAD len to first script:", i1)
print("between first and second script (len):", i2-(i1+8))
print("tail after second script (len):", len(data)-(i2+8))
print("LAST 300 chars:", data[-300:].replace('\n',' '))
# check if </body>/</html> exist anywhere
print("has </body>:", '</body>' in data, " has </html>:", '</html>' in data)
print("count <script>:", data.count('<script>'), " count </script>:", data.count('</script>'))