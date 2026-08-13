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

## Adding a new collection's slugs, or new designs to an existing one

Don't hand-edit `redirects.json` — use `add_collection.py`:

```
python add_collection.py path/to/source.json
```

The source file (one per collection, lives alongside that collection's designs in the [ShanezShertz](https://github.com/dangerousdan99/ShanezShertz) repo, e.g. `designs/Daily Coping Co/source.json`) lists each design's filename, Teepublic title, Teepublic URL, and **slug**, plus the collection's own slug and album URL. Every design must already have a slug — run `ShanezShertz/scripts/gen_design_index.py` first; it assigns permanent slugs (never renumbering existing ones, even when a new design is added later) and writes them back into `source.json`. This script then just copies `slug → url` into `redirects.json` and rebuilds. Re-running it with an unchanged source file is a no-op — safe to run again after editing. Pass `--dry-run` to preview without writing.

This repo contains no brand copy, designs, or other Shanez Shertz IP — just the slug → URL mapping and the static pages that serve it, which is why it's public while the main [ShanezShertz](https://github.com/dangerousdan99/ShanezShertz) repo stays private.
