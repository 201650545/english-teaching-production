# -*- coding: utf-8 -*-
import re, json, sys
from playwright.sync_api import sync_playwright

base = r"d:\英语教学\李民宪"
lessons = [6,7,8,9,10]
report = {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for n in lessons:
        path = base + ("\\第%02d课时\\课件成品_网页PPT\\第%02d课时_课件_培优.html" % (n, n))
        page = browser.new_page(viewport={"width":1600,"height":900})
        js_errors = []
        page.on("pageerror", lambda e: js_errors.append(str(e)))
        page.on("console", lambda msg: js_errors.append("console:"+msg.text) if msg.type=="error" else None)
        page.goto("file:///"+path.replace("\\","/"))
        page.wait_for_timeout(800)
        # 1) collect onclick function names from DOM
        fn_names = page.evaluate("""() => {
          const out = new Set();
          document.querySelectorAll('[onclick]').forEach(el=>{
            const m = el.getAttribute('onclick').match(/([A-Za-z_$][A-Za-z0-9_$]*)\\s*\\(/);
            if(m) out.add(m[1]);
          });
          return Array.from(out);
        }""")
        # 2) typeof check
        type_map = page.evaluate("""(fns) => {
          const r={};
          fns.forEach(f=>{ try{r[f]=typeof window[f];}catch(e){r[f]='ERR';} });
          return r;
        }""", fn_names)
        not_functions = {f:t for f,t in type_map.items() if t != 'function'}
        # 3) page count
        n_pages = page.evaluate("document.querySelectorAll('.page').length")
        # 4) navigation: click right half -> active page changes
        nav_ok = True
        try:
            before = page.evaluate("document.querySelector('.page.active') ? document.querySelector('.page.active').id : 'none'")
            page.mouse.click(1400, 500)
            page.wait_for_timeout(200)
            after = page.evaluate("document.querySelector('.page.active') ? document.querySelector('.page.active').id : 'none'")
            nav_ok = (before != after)
        except Exception as e:
            nav_ok = "ERR:"+str(e)
        # 5) fill interaction: click first fill-check-btn
        fill_ok = True
        try:
            page.evaluate("document.querySelectorAll('.page')[0].style.display='block'")
            # jump to reading C page (find page containing fill-check-btn)
            page.evaluate("""() => {
              const pages=document.querySelectorAll('.page');
              for(const pg of pages){ if(pg.querySelector('.fill-check-btn')){ pg.classList.add('active'); pg.style.display='block'; break; } }
            }""")
            page.wait_for_timeout(200)
            if page.evaluate("document.querySelector('.fill-input-box')"):
                page.fill(".fill-input-box", "pollination")
                page.click(".fill-check-btn")
                page.wait_for_timeout(200)
                fill_ok = page.evaluate("document.querySelector('.fill-input-box').classList.contains('correct')")
            else:
                fill_ok = "no-fill-on-page"
        except Exception as e:
            fill_ok = "ERR:"+str(e)
        # 6) check for black/blank: body has visible content
        blank = page.evaluate("document.body.innerText.trim().length")
        report[n] = {
            "pages": n_pages,
            "onclick_fns": fn_names,
            "typeof": type_map,
            "not_functions": not_functions,
            "js_errors": js_errors[:8],
            "nav_ok": nav_ok,
            "fill_ok": fill_ok,
            "body_text_len": blank,
        }
        print("="*60)
        print("L%02d: pages=%d nav_ok=%s fill_ok=%s body_text=%d" % (n, n_pages, nav_ok, fill_ok, blank))
        print("  not_functions(必须空):", not_functions if not_functions else "NONE (all typeof=function)")
        print("  js_errors:", js_errors if js_errors else "NONE")
        print("  typeof[%d fns]:" % len(fn_names), "ALL function" if not not_functions else not_functions)
        page.close()
    browser.close()

json.dump(report, open(r"d:\英语教学\00_工具\_lmx_browser_report.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("\nSaved browser report.")