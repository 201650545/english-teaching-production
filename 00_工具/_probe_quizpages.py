# -*- coding: utf-8 -*-
import asyncio
from playwright.async_api import async_playwright
URL = "file:///d:/英语教学/李民宪/第06课时/课件成品_网页PPT/第06课时_课件_培优.html"
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        p = await b.new_page()
        await p.goto(URL); await p.wait_for_timeout(1200)
        res = await p.evaluate("""() => {
            var out=[];
            for(var i=1;i<=totalPages;i++){
                var el=document.getElementById('page'+i);
                if(!el) continue;
                var q=el.querySelectorAll('.quiz-opt').length;
                var fill=el.querySelectorAll('.fill-input-box').length;
                var title=el.querySelector('.page-title')?el.querySelector('.page-title').textContent.trim():'';
                if(q>0||fill>0) out.push({page:i,quiz:q,fill:fill,title:title});
            }
            return out;
        }""")
        for r in res:
            print(r)
        await b.close()
asyncio.run(main())