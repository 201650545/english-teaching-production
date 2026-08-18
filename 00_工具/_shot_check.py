import sys, os, asyncio
sys.path.insert(0, "D:/英语教学/00_工具")
from playwright.async_api import async_playwright

BASE = "D:/英语教学/许颖嘉"
HTML_DIR = "课件成品_网页PPT"
OUT = "D:/英语教学/00_工具/_diff_shots"
os.makedirs(OUT, exist_ok=True)

# 抽查覆盖全部5个recipe的课
LESSONS = {1:"R1", 4:"R5", 5:"R3", 2:"R4", 3:"R2"}  # L01 R1, L04 R5, L05 R3, L02 R4, L03 R2

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe")
        page = await browser.new_page(viewport={"width":1280,"height":720})
        for lesson, recipe in LESSONS.items():
            fn = f"第{lesson:02d}课时_课件_基础.html"
            path = os.path.join(BASE, f"第{lesson:02d}课时", HTML_DIR, fn)
            await page.goto(f"file://{path}", wait_until="networkidle")
            await asyncio.sleep(1)
            # 封面
            await page.screenshot(path=os.path.join(OUT, f"L{lesson:02d}_{recipe}_封面.png"))
            # 跳到讲解页/选择题页
            try:
                await page.evaluate("jumpToSegment(5)")
                await asyncio.sleep(0.8)
                await page.screenshot(path=os.path.join(OUT, f"L{lesson:02d}_{recipe}_内容页.png"))
            except Exception as e:
                print(f"L{lesson} jumpToSegment: {e}")
        # 浏览器实测：L01 答题+翻页+检查
        await page.goto(f"file://{BASE}/第01课时/{HTML_DIR}/第01课时_课件_基础.html", wait_until="networkidle")
        await asyncio.sleep(1)
        # 找第一个 quiz-opt 点击
        r = await page.evaluate("""() => {
          const opt = document.querySelector('.quiz-opt');
          const before = document.body.scrollWidth;
          let clickOk = false, feedback = '';
          if (opt) { opt.click(); clickOk = true; 
            const f = document.querySelector('.fb-bubble, .game-feedback');
            if (f) feedback = f.className;
          }
          return {clickOk, feedback, overflow: document.body.scrollWidth > window.innerWidth};
        }""")
        print("L01 实测:", r)
        await browser.close()

asyncio.run(main())
