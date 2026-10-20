import asyncio, json, re
from playwright.async_api import async_playwright

PAGES = ["index.html", "products.html", "customise.html", "process.html",
         "works.html", "industries.html", "contact.html", "design-system.html", "404.html"]
BASE = "http://127.0.0.1:8899"


async def main():
    issues = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/root/.cache/ms-playwright/chromium-1243/chrome-linux/chrome",
                                    args=["--no-sandbox", "--headless=new"])
        ctx = await b.new_context(viewport={"width": 1440, "height": 900})
        page = await ctx.new_page()
        all_links = set()
        for name in PAGES:
            await page.goto(f"{BASE}/{name}", wait_until="networkidle")
            await page.wait_for_timeout(400)
            r = await page.evaluate("""() => {
                const q = s => [...document.querySelectorAll(s)];
                const res = {issues: [], links: []};
                // images
                q('img').forEach(i => {
                    if (!i.hasAttribute('alt')) res.issues.push('img missing alt: ' + (i.src||'').split('/').pop());
                    if (!i.getAttribute('width') || !i.getAttribute('height')) res.issues.push('img missing dimensions: ' + (i.src||'').split('/').pop());
                    if (i.loading !== 'lazy' && i.getAttribute('loading') !== null) res.issues.push('img loading attr: ' + i.loading);
                });
                // heading order
                const hs = q('h1,h2,h3,h4,h5,h6').map(h => +h.tagName[1]);
                let prev = 0;
                hs.forEach((lv, i) => { if (prev && lv > prev + 1) res.issues.push(`heading jump h${prev}->h${lv} at #${i}`); prev = lv; });
                if (hs.filter(x => x === 1).length !== 1) res.issues.push('h1 count = ' + hs.filter(x => x === 1).length);
                // form labels
                q('input,select,textarea').forEach(el => {
                    if (el.type === 'hidden') return;
                    const id = el.id;
                    const lab = id && document.querySelector(`label[for="${id}"]`);
                    const wrapped = el.closest('label');
                    if (!lab && !wrapped) res.issues.push('unlabelled field: ' + (id || el.name || el.type));
                });
                // buttons need accessible names
                q('button').forEach(bt => {
                    const t = (bt.textContent||'').trim();
                    if (!t && !bt.getAttribute('aria-label') && !bt.getAttribute('aria-labelledby')) res.issues.push('button without name: ' + bt.className);
                });
                // links
                q('a[href]').forEach(a => {
                    const href = a.getAttribute('href');
                    res.links.push({href, text: (a.textContent||'').trim().slice(0,40)});
                });
                // meta
                const t = document.title, d = document.querySelector('meta[name=description]');
                if (!t || t.length < 10) res.issues.push('weak title');
                if (!d || !d.content || d.content.length < 50) res.issues.push('weak description: ' + (d ? d.content.length : 0));
                if (!document.querySelector('meta[property="og:image"]')) res.issues.push('no og:image');
                if (!document.querySelector('link[rel="icon"]')) res.issues.push('no favicon');
                return res;
            }""")
            for i in r["issues"]:
                issues.setdefault(name, []).append(i)
            for l in r["links"]:
                h = l["href"]
                if h.startswith(("http", "mailto:", "tel:", "#", "data:")):
                    continue
                all_links.add(h.split("#")[0])
            if r["issues"]:
                print(f"--- {name}: {len(r['issues'])} issue(s)")
                for i in r["issues"][:8]:
                    print("   ", i)
        # verify internal links resolve
        print("\n--- internal link targets ---")
        for l in sorted(all_links):
            if not l:
                continue
            resp = await page.goto(f"{BASE}/{l}")
            code = resp.status if resp else "?"
            if code != 200:
                print(f"   BROKEN {code}  {l}")
        print("   all internal links checked:", len([x for x in all_links if x]))
        await b.close()

asyncio.run(main())
