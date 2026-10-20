import asyncio, os, sys, json
from playwright.async_api import async_playwright

DIST = "/workspace/dist"
OUT = "/workspace/shots"
os.makedirs(OUT, exist_ok=True)
PAGES = ["index.html", "products.html", "customise.html", "process.html",
         "works.html", "industries.html", "contact.html", "design-system.html"]
BASE = "http://127.0.0.1:8899"

async def main():
    errors = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/root/.cache/ms-playwright/chromium-1243/chrome-linux/chrome", args=["--no-sandbox", "--disable-dev-shm-usage", "--headless=new"])
        for w, tag in [(1440, "desk"), (390, "mob")]:
            ctx = await b.new_context(viewport={"width": w, "height": 900},
                                      device_scale_factor=1 if w == 1440 else 2)
            page = await ctx.new_page()
            msgs = []
            page.on("console", lambda m: msgs.append(f"[{m.type}] {m.text}") if m.type in ("error", "warning") else None)
            page.on("pageerror", lambda e: msgs.append(f"[pageerror] {e}"))
            page.on("requestfailed", lambda r: msgs.append(f"[404] {r.url}"))
            for name in PAGES:
                msgs.clear()
                await page.goto(f"{BASE}/{name}", wait_until="networkidle", timeout=45000)
                await page.wait_for_timeout(1200)
                # trigger all reveals
                await page.evaluate("""() => {
                    document.querySelectorAll('[data-reveal]').forEach(e => e.classList.add('is-in'));
                    window.scrollTo(0, document.body.scrollHeight);
                }""")
                await page.wait_for_timeout(900)
                await page.evaluate("() => window.scrollTo(0,0)")
                await page.wait_for_timeout(500)
                await page.screenshot(path=f"{OUT}/{name.replace('.html','')}-{tag}.png", full_page=True)
                if msgs:
                    errors[f"{name} [{tag}]"] = list(msgs)
            await ctx.close()
        await b.close()
    print(json.dumps(errors, indent=1) if errors else "NO CONSOLE ERRORS")

asyncio.run(main())
