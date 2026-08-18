import sys, os, asyncio
sys.path.insert(0, "D:/英语教学/00_工具")
from playwright.async_api import async_playwright

BASE = "D:/英语教学/许颖嘉"
HTML_DIR = "课件成品_网页PPT"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe")
        page = await browser.new_page(viewport={"width":1280,"height":720})
        for lesson in [1, 5, 2, 3, 4, 17, 26]:
            fn = f"第{lesson:02d}课时_课件_基础.html"
            path = os.path.join(BASE, f"第{lesson:02d}课时", HTML_DIR, fn)
            await page.goto(f"file://{path}", wait_until="networkidle")
            await asyncio.sleep(1)
            c = await page.evaluate("""() => {
              const w = document.querySelector('.cover-wrap');
              const cs = getComputedStyle(w);
              const before = getComputedStyle(w, '::before');
              const after = getComputedStyle(w, '::after');
              return {
                wrapBg: cs.backgroundImage.slice(0,80),
                wrapBgColor: cs.backgroundColor,
                title: document.querySelector('.cover-title')?.textContent || 'no',
                afterDisplay: after.display
              };
            }""")
            status = "✅" if "gradient" in c["wrapBg"] or "#fafafa" in c["wrapBg"] else "❌"
            print(f"L{lesson:02d}: {status} bg={c['wrapBg']} color={c['wrapBgColor']} title={c['title'][:15]} after={c['afterDisplay']}")
        await browser.close()

asyncio.run(main())
