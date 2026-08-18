# -*- coding: utf-8 -*-
"""L26-L30 浏览器实测：L21 逐页点测 + L22-25 抽查新题型，验证无黑屏/函数定义/答题落 IndexedDB"""
import json
from playwright.sync_api import sync_playwright

base = r"D:\英语教学\邓兴华"
lessons = [26, 27, 28, 29, 30]
report = {}

def _all_pages_ok(page):
    total = page.evaluate("document.querySelectorAll('.page').length")
    blank = []
    for i in range(total):
        page.evaluate("""i => {
          const pages=document.querySelectorAll('.page');
          pages.forEach(p=>p.classList.remove('active'));
          pages[i].classList.add('active');
          pages[i].style.display='block';
        }""", i)
        page.wait_for_timeout(25)
        txt = page.evaluate("document.querySelectorAll('.page')[%d].innerText.trim().length" % i)
        if txt < 5:
            blank.append(i)
    return (len(blank) == 0), blank, total

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for n in lessons:
        path = base + ("\\第%02d课时\\课件成品_网页PPT\\第%02d课时_课件_中等.html" % (n, n))
        ctx = browser.new_context(viewport={"width":1600,"height":900})
        page = ctx.new_page()
        js_errors = []
        page.on("pageerror", lambda e: js_errors.append("pageerror:"+str(e)))
        page.on("console", lambda msg: js_errors.append("console:"+msg.text) if msg.type=="error" else None)
        page.goto("file:///"+path.replace("\\","/"))
        page.wait_for_timeout(900)

        fn_names = page.evaluate("""() => {
          const out = new Set();
          document.querySelectorAll('[onclick]').forEach(el=>{
            const a = el.getAttribute('onclick');
            if(a){ const m=a.match(/([A-Za-z_$][A-Za-z0-9_$]*)\\s*\\(/); if(m) out.add(m[1]); }
          });
          return Array.from(out);
        }""")
        type_map = page.evaluate("""(fns)=>{const r={};fns.forEach(f=>{try{r[f]=typeof window[f];}catch(e){r[f]='ERR';}});return r;}""", fn_names)
        not_functions = {f:t for f,t in type_map.items() if t != 'function'}
        func_ok = (len(not_functions) == 0)

        pages_ok, blank_pages, total = _all_pages_ok(page)

        idb_before = page.evaluate("""() => new Promise(res=>{
          const req=indexedDB.open('EnglishCoursewareDB',1);
          req.onsuccess=e=>{const db=e.target.result; try{
            const st=db.transaction('answerRecords','readonly').objectStore('answerRecords').count();
            st.onsuccess=()=>res(st.result); st.onerror=()=>res(-1);
          }catch(err){res(-2);}};
          req.onerror=()=>res(-3);
        })""")
        idb_after = idb_before
        idb_ok = False
        try:
            # 激活含 quiz-opt 的内容页，程序化 .click() 触发 checkOpt 并落 IndexedDB
            clicked = page.evaluate("""() => {
              const pages=document.querySelectorAll('.page');
              for(const pg of pages){
                if(pg.querySelector('.quiz-opt')){
                  pages.forEach(x=>x.classList.remove('active'));
                  pg.classList.add('active'); pg.style.display='block';
                  const opt = pg.querySelector('.quiz-opt');
                  opt.click();
                  return true;
                }
              }
              return false;
            }""")
            page.wait_for_timeout(500)
            idb_after = page.evaluate("""() => new Promise(res=>{
              const req=indexedDB.open('EnglishCoursewareDB',1);
              req.onsuccess=e=>{const db=e.target.result; try{
                const st=db.transaction('answerRecords','readonly').objectStore('answerRecords').count();
                st.onsuccess=()=>res(st.result); st.onerror=()=>res(-1);
              }catch(err){res(-2);}};
              req.onerror=()=>res(-3);
            })""")
            idb_ok = (clicked and isinstance(idb_after,int) and isinstance(idb_before,int) and idb_after > idb_before)
        except Exception as ex:
            idb_ok = "ERR:"+str(ex)

        report[n] = {
            "totalPages": total,
            "onclick_fns": fn_names,
            "not_functions": not_functions,
            "func_ok": func_ok,
            "blank_pages": blank_pages,
            "pages_ok": pages_ok,
            "idb_before": idb_before,
            "idb_after": idb_after,
            "idb_ok": idb_ok,
            "js_errors": js_errors[:10],
        }
        print("="*60)
        print("L%02d: pages=%d func_ok=%s pages_ok=%s blank=%s idb_ok=%s (%s->%s)" %
              (n, total, func_ok, pages_ok, blank_pages, idb_ok, idb_before, idb_after))
        print("  not_functions:", not_functions if not_functions else "NONE (all typeof=function)")
        print("  js_errors:", js_errors if js_errors else "NONE")
        ctx.close()
    browser.close()

json.dump(report, open(r"D:\英语教学\00_工具\_browser_L26_30_report.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("\nSaved browser report to D:\\英语教学\\00_工具\\_browser_L26_30_report.json")