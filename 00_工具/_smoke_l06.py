# -*- coding: utf-8 -*-
import asyncio, json
from playwright.async_api import async_playwright

URL = "file:///d:/英语教学/李民宪/第06课时/课件成品_网页PPT/第06课时_课件_培优.html"

async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page(viewport={"width":1600,"height":900})
        console_errors = []
        page.on("console", lambda m: console_errors.append(m.text) if m.type=="error" else None)
        page.on("pageerror", lambda e: console_errors.append("[pageerror] "+str(e)))
        await page.goto(URL)
        await page.wait_for_timeout(1500)

        # 1. 无黑屏：body 有内容
        body_len = await page.evaluate("document.getElementById('pagesContainer').textContent.length")
        print("body内容长度:", body_len)

        # 2. 页数 & 当前页
        total = await page.evaluate("totalPages")
        cur = await page.evaluate("currentPage")
        print("totalPages=%d currentPage=%d" % (total, cur))

        # 3. 翻页：右半点击 → 前进
        await page.mouse.click(1200, 450)
        await page.wait_for_timeout(400)
        cur2 = await page.evaluate("currentPage")
        print("右半点击后 currentPage=%d (应为2)" % cur2)

        # 4. 左半点击 → 后退
        await page.mouse.click(200, 450)
        await page.wait_for_timeout(400)
        cur3 = await page.evaluate("currentPage")
        print("左半点击后 currentPage=%d (应为1)" % cur3)

        # 5. 答题落 IndexedDB：跳到第3页（热身quiz），点 quiz-opt
        await page.evaluate("goToPage(3)")
        await page.wait_for_timeout(400)
        before = await page.evaluate("""async () => {
            return new Promise(res=>{
                var r=indexedDB.open('EnglishCoursewareDB');
                r.onsuccess=e=>{
                    var db=e.target.result; var tx=db.transaction('answerRecords','readonly');
                    var st=tx.objectStore('answerRecords'); var c=st.count();
                    c.onsuccess=()=>res(c.result); c.onerror=()=>res(-1);
                }; r.onerror=()=>res(-1);
            });
        }""")
        # 点第3页第一个 quiz-opt（真实鼠标点击，落库）
        clicked = await page.evaluate("""() => {
            var qs = document.querySelectorAll('#page3 .quiz-opt');
            if(!qs.length) return 0;
            var r = qs[0].getBoundingClientRect();
            return {x: r.x + r.width/2, y: r.y + r.height/2, n: qs.length, qid: qs[0].closest('[data-qid]')?.getAttribute('data-qid')};
        }""")
        if clicked:
            await page.mouse.click(clicked['x'], clicked['y'])
        await page.wait_for_timeout(1500)
        after = await page.evaluate("""async () => {
            return new Promise(res=>{
                var r=indexedDB.open('EnglishCoursewareDB');
                r.onsuccess=e=>{
                    var db=e.target.result; var tx=db.transaction('answerRecords','readonly');
                    var st=tx.objectStore('answerRecords'); var all=st.getAll();
                    all.onsuccess=()=>res({count:all.result.length, sample: all.result.length? all.result[0]: null});
                    all.onerror=()=>res({count:-2});
                }; r.onerror=()=>res({count:-1});
            });
        }""")
        print("答题IndexedDB: 点击(按钮信息)=%s 后=%s" % (clicked, after))

        # 6. 思维导图存在
        mm = await page.evaluate("""() => {
            var html = document.body.innerHTML;
            return {mm: (html.indexOf('思维导图')>=0), map: (html.indexOf('eco-map')>=0 || html.indexOf('mind')>=0)};
        }""")
        print("思维导图存在:", mm)

        # 7. 双击撤销：点一个错误选项后双击该题
        go_res = await page.evaluate("goToPage(3)")
        await page.wait_for_timeout(400)
        wr = await page.evaluate("""() => {
            var q = document.querySelector('#page3 .quiz-q');
            if(!q) return 'no q';
            var correct = q.querySelector('.quiz-opt[data-correct="true"], .quiz-opt[data-correct="1"]');
            var opts = q.querySelectorAll('.quiz-opt');
            var wrong = null;
            for(var i=0;i<opts.length;i++){ if(opts[i]!==correct){ wrong=opts[i]; break; } }
            if(!wrong) return 'no wrong';
            wrong.click();
            return 'clicked wrong';
        }""")
        await page.wait_for_timeout(600)
        dbl = await page.evaluate("""() => {
            var q = document.querySelector('#page3 .quiz-q[data-done]');
            if(q && q.dataset.done==='1' && q.dataset.wrong==='1'){
                q.dispatchEvent(new MouseEvent('dblclick',{bubbles:true}));
                return {was_done:q.dataset.done, was_wrong:q.dataset.wrong, after_done:q.dataset.done};
            }
            return {info:'state', raw: q? {done:q.dataset.done, wrong:q.dataset.wrong}: 'no q'};
        }""")
        print("双击撤销测试:", wr, dbl)

        print("console错误数:", len(console_errors))
        if console_errors:
            print("console错误:", console_errors[:10])
        await browser.close()

asyncio.run(main())