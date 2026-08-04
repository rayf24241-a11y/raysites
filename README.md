# raysites

Portfolio and demo sites for a freelance web-building service. **Seven pages, one repo, one deploy.**

Every page is a single self-contained HTML file — no build step, no npm install, no framework, no external requests. Two of them render real-time 3D in raw WebGL. The heaviest page on the site is 8.8 KB gzipped.

## Pages

| Path | What it is | Gzipped |
|---|---|---|
| `/` | Portfolio — live embedded previews of every demo, pricing, FAQ | 8.8 KB |
| `/barbershop/` | Demo — Ironside Barber Co. Price menu, booking form, hours that highlight today | 5.5 KB |
| `/landscaping/` | Demo — Cedar & Stone Landscaping. Service pricing, quote form, illustrated projects | 7.0 KB |
| `/detailing/` | Demo — Apex Auto Detailing. **Raymarched 3D paint render**, drag before/after slider | 7.9 KB |
| `/bar/` | Demo — The Ember Room. **Animated smoke shader**, live open/closed status | 7.1 KB |
| `/work/ironside/` | Case study — the barbershop build, decision by decision | 5.3 KB |
| `/work/cedar-stone/` | Case study — the landscaping build, decision by decision | 5.9 KB |

The demo businesses are **concept builds, not real clients** — the case studies say so explicitly. Keep it that way.

## The one thing to edit

In `index.html`, near the bottom:

```js
const CONFIG = {
  email: 'rayf24241@gmail.com'
};
```

That's where every "Email me" button points. The case-study pages have the same address in their own script blocks — search the repo for the address if you change it.

To change the price, search for `$150`.

## Put it on GitHub

Create an empty repo at [github.com/new](https://github.com/new) — name it `raysites`, don't add a README or .gitignore (this repo already has both). Then:

```bash
git remote add origin https://github.com/YOUR-USERNAME/raysites.git
```

```bash
git push -u origin main
```

## Deploy on Vercel

1. [vercel.com/new](https://vercel.com/new) → import the `raysites` repo
2. Framework preset: **Other**
3. Leave build command and output directory **empty** — there's nothing to build
4. Deploy

All seven pages go live at once. Every `git push` after that redeploys automatically.

## Local preview

```bash
python -m http.server 5599
```

Then open <http://localhost:5599>. A plain file server is all this needs.

## Notes

- **`vercel.json` deliberately sets no `X-Frame-Options`.** The portfolio embeds the demo sites in iframes; a frame-blocking header would break every preview on the home page.
- **WebGL init is retried from the render loop**, not run once on load. A backgrounded tab can return a null context, which would otherwise leave a dead grey hero for anyone who opens your link in a new tab.
- **No stock photography anywhere.** Every illustration is inline SVG, so there are no image files and nothing extra to download. On a real client job these get replaced by the client's own photos.
