import asyncio, json
from playwright.async_api import async_playwright

PAGES = ["index.html", "products.html", "customise.html", "process.html",
         "works.html", "industries.html", "contact.html", "design-system.html"]
BASE = "http://127.0.0.1:8899"


async def main():
    report = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/root/.cache/ms-playwright/chromium-1243/chrome-linux/chrome",
                                    args=["--no-sandbox", "--headless=new"])
        for w, tag in [(1440, "desk"), (768, "tab"), (390, "mob")]:
            ctx = await b.new_context(viewport={"width": w, "height": 900})
            page = await ctx.new_page()
            for name in PAGES:
                await page.goto(f"{BASE}/{name}", wait_until="networkidle")
                await page.wait_for_timeout(700)
                r = await page.evaluate("""(vw) => {
                    const out = [];
                    document.querySelectorAll('body *').forEach(el => {
                        const b = el.getBoundingClientRect();
                        if (b.width === 0 || b.height === 0) return;
                        if (b.right > vw + 1.5) {
                            out.push({
                                tag: el.tagName.toLowerCase(),
                                cls: (el.className || '').toString().slice(0, 70),
                                right: Math.round(b.right),
                                w: Math.round(b.width),
                                txt: (el.textContent || '').trim().slice(0, 40)
                            });
                        }
                    });
                    return {scrollW: document.documentElement.scrollWidth, over: out.slice(0, 12)};
                }""", w)
                key = f"{name}[{tag}]"
                if r["scrollW"] > w + 1 or r["over"]:
                    report[key] = {"scrollW": r["scrollW"], "vw": w, "elems": r["over"]}
            await ctx.close()
        await b.close()
    if report:
        for k, v in report.items():
            print(f"\n### {k}  scrollW={v['scrollW']} vw={v['vw']}")
            for e in v["elems"]:
                print(f"   {e['tag']}.{e['cls']} right={e['right']} w={e['w']} | {e['txt']}")
    else:
        print("NO OVERFLOW FOUND")


asyncio.run(main())
