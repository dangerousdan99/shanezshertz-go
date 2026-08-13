"""Generates static redirect pages from redirects.json into docs/.

Each slug in redirects.json becomes docs/<slug>/index.html, a tiny page
that immediately redirects to its target URL. GitHub Pages serves docs/
on the custom domain go.shanezshertz.shop.
"""

import json
from pathlib import Path

ROOT = Path(__file__).parent
REDIRECTS = json.loads((ROOT / "redirects.json").read_text(encoding="utf-8"))
DOCS = ROOT / "docs"

PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Redirecting...</title>
<meta http-equiv="refresh" content="0; url={target}">
<link rel="canonical" href="{target}">
<script>location.replace({target_json});</script>
</head>
<body>
<p>Redirecting to <a href="{target}">the product page</a>...</p>
</body>
</html>
"""

INDEX_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Shanez Shertz</title>
</head>
<body>
<p>Shanez Shertz</p>
</body>
</html>
"""


def build():
    DOCS.mkdir(exist_ok=True)
    for slug, target in REDIRECTS.items():
        page_dir = DOCS / slug
        page_dir.mkdir(exist_ok=True)
        html = PAGE_TEMPLATE.format(target=target, target_json=json.dumps(target))
        (page_dir / "index.html").write_text(html, encoding="utf-8")

    (DOCS / "index.html").write_text(INDEX_PAGE, encoding="utf-8")
    (DOCS / "CNAME").write_text("go.shanezshertz.shop\n", encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")

    print(f"Built {len(REDIRECTS)} redirect pages into {DOCS}")


if __name__ == "__main__":
    build()
