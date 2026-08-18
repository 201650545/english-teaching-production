# -*- coding: utf-8 -*-
import json, os, sys, importlib.util
HERE = r'D:\英语教学\00_工具'
sys.path.insert(0, HERE)
spec=importlib.util.spec_from_file_location("bp", os.path.join(HERE,"build_practice_paper.py"))
bp=importlib.util.module_from_spec(spec); spec.loader.exec_module(bp)
lesson=18
content=json.load(open(os.path.join(HERE,"practice_content_DXH_L%02d.json"%lesson),encoding="utf-8"))
card={"lesson":lesson,"student":"邓兴华","tier":"中等","stage":"S5","type":"normal",
 "grammar":["G46 现在进行时","G47 V-ing变化","G48 标志词"],"theme":"现在进行时·家务",
 "vocab":{"new_count":20,"review_count":0,"theme":"现在进行时·家务"},"phonics":"le /l/","listening":False}
out=os.path.join(r'D:\英语教学\邓兴华','第%02d课时'%lesson,'第%02d课时_配套练习_中等.docx'%lesson)
p=bp.build_practice(card,content,out)
print('L%d 配套练习生成：%s (%d bytes)'%(lesson,p,os.path.getsize(p)))