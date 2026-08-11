# shanezshertz-go

Redirect service for Shanez Shertz product and collection links, per the brand bible's rule that outbound links must never point straight at a marketplace (they change; our links don't).

Live at `go.shanezshertz.shop` via GitHub Pages. `go.shanezshertz.shop/wt-014` redirects to product `wt-014`, and `go.shanezshertz.shop/wilderness-therapy-group` redirects to the collection.

## How it works

- `redirects.json` — the source of truth: slug → current target URL.
- `build.py` — generates `docs/<slug>/index.html` (a tiny redirect page) for every entry, plus `docs/CNAME` for the custom domain. GitHub Pages serves the `docs/` folder.

## Updating a link

1. Edit `redirects.json`.
2. Run `python build.py`.
3. Commit and push `redirects.json` and the regenerated `docs/`.

This repo contains no brand copy, designs, or other Shanez Shertz IP — just the slug → URL mapping and the static pages that serve it, which is why it's public while the main [ShanezShertz](https://github.com/dangerousdan99/ShanezShertz) repo stays private.
