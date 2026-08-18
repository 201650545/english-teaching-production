# -*- coding: utf-8 -*-
"""L16/L17/L20 verify_interaction 剩余修复（收尾）。
- L16: 加 e.target.closest 守卫(VIS-614) + 转2单选(VIS-601)
- L17: 移除 link-container 的 data-interaction-item(VIS-615) + 补 order-container 元数据(VIS-610/603)
       + 加 e.target.closest 守卫(VIS-614) + 转2单选(VIS-601)
- L20: 转8单选 -> fill_in(VIS-601)
不改知识点/答案/阅读原文；选择转填空仅保留正确项文本为 data-correct。
"""
import re, importlib.util, os
BASE=r'D:\英语教学\邓兴华'
spec=importlib.util.spec_from_file_location("fi", r'D:\英语教学\00_工具\_fix_interaction.py')
fi=importlib.util.module_from_spec(spec); spec.loader.exec_module(fi)

def add_etarget_guard(h):
    if "e.target.closest('.drag-container')" in h:
        return h, False
    anchor="if (e.clientX > window.innerWidth / 2) nextPage();"
    guard=("if (e.target.closest('.drag-container') || e.target.closest('.link-container') "
           "|| e.target.closest('.order-container')) return;\n  ")
    if anchor in h:
        h=h.replace(anchor, guard+anchor, 1)
        return h, True
    return h, False

def fix_l17_vis615(h):
    h2=re.sub(r'(<div class="link-container[^>]*?)\s+data-interaction-item="1"', r'\1', h)
    return h2, h2!=h

def fix_l17_order_meta(h):
    pat=re.compile(r'(<div class="order-container"[^>]*?data-question-id="[^"]*")(>)')
    def repl(m):
        tag=m.group(1)
        if 'data-interaction-type' in tag:
            return m.group(0)
        return ('%s data-knowledge-id="GEN" data-section="core" data-template-id="C-INTERACT" '
                'data-interaction-type="order" data-action-type="order" data-cognitive-level="application" '
                'data-scorable="true">' % tag)
    h2=pat.sub(repl, h)
    return h2, h2!=h

def process(lesson, label, convert_need, do_guard, do_l17_vis615, do_l17_ordermeta):
    p=os.path.join(BASE,'第%02d课时'%lesson,'课件成品_网页PPT',label+'.html')
    h=open(p,encoding='utf-8').read()
    log=[]
    if do_guard:
        h,g=add_etarget_guard(h); log.append("guard=%d"%g)
    if do_l17_vis615:
        h,a=fix_l17_vis615(h); log.append("link615=%d"%a)
    if do_l17_ordermeta:
        h,b=fix_l17_order_meta(h); log.append("ordermeta=%d"%b)
    h,c=fi.convert_choice_to_fill(h, convert_need, lesson); log.append("convert=%d"%c)
    open(p,'w',encoding='utf-8').write(h)
    print("L%d %s: %s"%(lesson,label,", ".join(log)))

process(16,'第16课时_课件_中等',2,True,False,False)
process(17,'第17课时_课件_中等',2,True,True,True)
process(20,'第20课时_课件_中等',8,False,False,False)
print("DONE")