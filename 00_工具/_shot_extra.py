import sys, os, asyncio
sys.path.insert(0, "D:/英语教学/00_工具")
from playwright.async_api import async_playwright

BASE = "D:/英语教学/许颖嘉"
HTML_DIR = "课件成品_网页PPT"
OUT = "D:/英语教学/00_工具/_diff_shots"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe")
        page = await browser.new_page(viewport={"width":1280,"height":720})
        for lesson in [17, 26]:
            fn = f"第{lesson:02d}课时_课件_基础.html"
            path = os.path.join(BASE, f"第{lesson:02d}课时", HTML_DIR, fn)
            await page.goto(f"file://{path}", wait_until="networkidle")
            await asyncio.sleep(1)
            await page.screenshot(path=os.path.join(OUT, f"L{lesson:02d}_封面.png"))
            print(f"L{lesson} 封面截图完成")
        # 验证 L05 封面渲染（DOM 检查）
        path = os.path.join(BASE, "第05课时", HTML_DIR, "第05课时_课件_基础.html")
        await page.goto(f"file://{path}", wait_until="networkidle")
        await asyncio.sleep(1)
        c = await page.evaluate("""() => {
          const w = document.querySelector('.cover-wrap');
          if (!w) return 'no cover-wrap';
          const bg = getComputedStyle(w).backgroundImage;
          const title = document.querySelector('.cover-title');
          const t = title ? title.textContent : 'no title';
          const badge = document.querySelector('.cover-badge');
          const b = badge ? getComputedStyle(badge).backgroundColor : 'no badge';
          return {bg: bg.slice(0,80), title: t, badgeBg: b};
        }""")
        print(f"L05 R3: {c}")
        await browser.close()

asyncio.run(main())
