# RAY — website service landing page

Single-file static site. Live 3D background is a raymarched gyroid tunnel written in raw WebGL — **no libraries, no build step, no dependencies.**

## Edit before you post it

Open `index.html`, scroll to the `CONFIG` block near the bottom:

```js
const CONFIG = {
  email: 'rayf24241@gmail.com',
  demos: [ 'https://...', 'https://...', 'https://...' ]
};
```

- `email` — where the "Email me" buttons send people.
- The demo sites live in `barbershop/` and `landscaping/` and are wired up already.

Change the price in two places if you ever raise it: search the file for `$150`.

## Put it on GitHub

```bash
gh repo create raysites --public --source=. --push
```

No `gh` CLI? Make an empty repo at github.com/new, then:

```bash
git remote add origin https://github.com/YOUR-USERNAME/raysites.git
git push -u origin main
```

## Deploy on Vercel

1. vercel.com → **Add New** → **Project**
2. Import the `raysites` repo
3. Framework preset: **Other**. Leave build command and output directory empty.
4. **Deploy**

You get `raysites.vercel.app` free. Every `git push` after that redeploys automatically.

## Local preview

```bash
python -m http.server 5599
```

Then open http://localhost:5599
