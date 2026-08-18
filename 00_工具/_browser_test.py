# -*- coding: utf-8 -*-
"""L21-25 浏览器实测：L21 逐页 + L22-25 抽查新题型 + typeof 函数 + IndexedDB 落库"""
import json, re, sys, os
from playwright.sync_api import sync_playwright

BASE = r'D:\英语教学\邓兴华'
def html_path(l):
    return os.path.join(BASE, '第%d课时' % l, '课件成品_网页PPT', '第%d课时_课件_中等.html' % l)

ONCLICK_RE = re.compile(r'onclick="([A-Za-z_$][A-Za-z0-9_$]*)\(', re.S)
EXCLUDE = {'event','window','document','this','alert','console','Array','Math','JSON'}

def get_onclick_names(l):
    s = open(html_path(l), encoding='utf-8').read()
    return sorted(set(ONCLICK_RE.findall(s)) - EXCLUDE)

def run_test():
    result = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for l in [21, 22, 23, 24, 25]:
            page = browser.new_page()
            errors = []
            page.on("console", lambda m: errors.append(m.type+": "+m.text) if m.type in ("error","warning") else None)
            page.on("pageerror", lambda e: errors.append("PAGEERROR: "+str(e)))
            path = html_path(l)
            page.goto("file:///" + path.replace("\\","/"))
            page.wait_for_timeout(800)

            # 1) typeof window[fn]==='function'
            names = get_onclick_names(l)
            fncheck = {}
            for n in names:
                fncheck[n] = page.evaluate("typeof window[%s]" % json.dumps(n))
            missing = [n for n,v in fncheck.items() if v != 'function']

            # 2) 总页数
            total = page.evaluate("document.querySelectorAll('.page').length")

            res = {'total_pages': total, 'fn_types': fncheck, 'missing_fn': missing, 'console_errors': errors[:10]}

            if l == 21:
                # L21 逐页：goToPage 每一页，确认 active
                nav_ok = True
                bad = []
                for i in range(1, total+1):
                    try:
                        page.evaluate("goToPage(%d)" % i)
                        page.wait_for_timeout(120)
                        active = page.evaluate(
                            "document.querySelector('.page.active') ? "
                            "document.querySelector('.page.active').id : 'NONE'")
                        if active != 'page%d' % i:
                            nav_ok = False; bad.append((i, active))
                    except Exception as e:
                        nav_ok = False; bad.append((i, str(e)))
                res['l21_nav_all_pages'] = nav_ok
                res['l21_nav_bad'] = bad
                # 交互落库：翻到含 quiz 的页，点首题
                db_cnt = page.evaluate("""async () => {
                  try {
                    const req = indexedDB.open('EnglishCoursewareDB',1);
                    return await new Promise((resolve)=>{
                      req.onsuccess=e=>{const d=req.result;
                        if(!d.objectStoreNames.contains('answerRecords')){d.close();resolve(-3);}
                        const st=d.transaction('answerRecords','readonly').objectStore('answerRecords');
                        const g=st.getAll(); g.onsuccess=()=>{let a=g.result||[];d.close();resolve(a.length);};
                        g.onerror=()=>{d.close();resolve(-4);};};
                      req.onerror=()=>resolve(-2);
                      req.onupgradeneeded=e=>{const d=req.result;
                        if(!d.objectStoreNames.contains('answerRecords'))d.createObjectStore('answerRecords',{keyPath:'event_id'});
                      };
                    });}catch(err){return -9;}
                }""")
                res['l21_db_exists_cnt_before'] = db_cnt
                # 点第一个可见 quiz-opt
                clicked = page.evaluate("""() => {
                  const vis = document.querySelector('.page.active');
                  if(!vis) return 'no-active';
                  const b = vis.querySelector('.quiz-opt');
                  if(!b) return 'no-opt';
                  b.click(); return 'clicked';
                }""")
                page.wait_for_timeout(400)
                db_cnt2 = page.evaluate("""async () => {
                  try {
                    const req = indexedDB.open('EnglishCoursewareDB',1);
                    return await new Promise((resolve)=>{
                      req.onsuccess=e=>{const d=req.result;
                        const st=d.transaction('answerRecords','readonly').objectStore('answerRecords');
                        const g=st.getAll(); g.onsuccess=()=>{let a=g.result||[];d.close();resolve(a.length);};
                        g.onerror=()=>{d.close();resolve(-4);};};
                      req.onerror=()=>resolve(-2);
                      req.onupgradeneeded=e=>{const d=req.result;
                        if(!d.objectStoreNames.contains('answerRecords'))d.createObjectStore('answerRecords',{keyPath:'event_id'});
                      };
                    });}catch(err){return -9;}
                }""")
                res['l21_interact_click'] = clicked
                res['l21_db_cnt_after_click'] = db_cnt2
                res['l21_db_recorded'] = (db_cnt2 is not None and db_cnt2 > 0)
            else:
                # L22-25 抽查 1 页新题型：找含 drag/order/match/flip 的页，操作并验证落库
                # 找到第一个含 drag-submit 的可见页
                interaction = page.evaluate("""() => {
                  const pages = document.querySelectorAll('.page');
                  for (const pg of pages){
                    const d = pg.querySelector('.drag-submit');
                    if(d) return {type:'drag', page: pg.id};
                  }
                  for (const pg of pages){
                    const o = pg.querySelector('.order-item');
                    if(o) return {type:'order', page: pg.id};
                  }
                  for (const pg of pages){
                    const m = pg.querySelector('.match-item');
                    if(m) return {type:'match', page: pg.id};
                  }
                  return {type:'none', page:''};
                }""")
                res['interaction_found'] = interaction
                db_before = page.evaluate("""async () => {
                  try{w=indexedDB.open('EnglishCoursewareDB',1);
                    return await new Promise(r=>{w.onsuccess=e=>{const d=w.result;
                      const st=d.transaction('answerRecords','readonly').objectStore('answerRecords');
                      const g=st.getAll(); g.onsuccess=()=>{let a=g.result||[];d.close();r(a.length);};g.onerror=()=>{d.close();r(-4);};};
                      w.onerror=()=>r(-2);w.onupgradeneeded=e=>{const d=w.result;if(!d.objectStoreNames.contains('answerRecords'))d.createObjectStore('answerRecords',{keyPath:'event_id'});};});
                  }catch(err){return -9;}
                }""")
                # 跳转到该页
                if interaction['type'] != 'none':
                    pid = int(interaction['page'].replace('page',''))
                    page.evaluate("goToPage(%d)" % pid); page.wait_for_timeout(300)
                    # 操作：点击所有未使用的 drag-word 填满所有槽，再点提交
                    act = page.evaluate("""() => {
                      const vis = document.querySelector('.page.active');
                      if(!vis) return 'no-vis';
                      const words = vis.querySelectorAll('.drag-word:not(.used)');
                      words.forEach(function(w){ w.click(); });
                      const sb = vis.querySelector('.drag-submit');
                      if(sb){ sb.click(); return 'all-dragged-and-submitted'; }
                      return 'no-submit';
                    }""")
                    res['interact_act'] = act
                page.wait_for_timeout(400)
                db_after = page.evaluate("""async () => {
                  try{w=indexedDB.open('EnglishCoursewareDB',1);
                    return await new Promise(r=>{w.onsuccess=e=>{const d=w.result;
                      const st=d.transaction('answerRecords','readonly').objectStore('answerRecords');
                      const g=st.getAll(); g.onsuccess=()=>{let a=g.result||[];d.close();r(a.length);};g.onerror=()=>{d.close();r(-4);};};
                      w.onerror=()=>r(-2);w.onupgradeneeded=e=>{const d=w.result;if(!d.objectStoreNames.contains('answerRecords'))d.createObjectStore('answerRecords',{keyPath:'event_id'});};});
                  }catch(err){return -9;}
                }""")
                res['db_before'] = db_before
                res['db_after'] = db_after
                res['db_recorded'] = (db_after is not None and db_after > 0)
            result[l] = res
            page.close()
        browser.close()
    return result

if __name__ == '__main__':
    r = run_test()
    out = r'D:\英语教学\00_总规划\05_交付与审核记录\_browser_test_tmp.json'
    json.dump(r, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for l, res in r.items():
        print('=== L%d ===' % l)
        print('  总页数=%s' % res.get('total_pages'))
        print('  缺失函数=%s' % res.get('missing_fn'))
        if l == 21:
            print('  逐页导航OK=%s 坏页=%s' % (res.get('l21_nav_all_pages'), res.get('l21_nav_bad')))
            print('  点击=%s 落库前=%s 落库后=%s 已落库=%s' % (res.get('l21_interact_click'), res.get('l21_db_exists_cnt_before'), res.get('l21_db_cnt_after_click'), res.get('l21_db_recorded')))
        else:
            print('  交互类型=%s 操作=%s 落库前=%s 落库后=%s 已落库=%s' % (res.get('interaction_found'), res.get('interact_act'), res.get('db_before'), res.get('db_after'), res.get('db_recorded')))
        if res.get('console_errors'):
            print('  控制台错误=%s' % res.get('console_errors'))
    print('\n结果已保存: ' + out)