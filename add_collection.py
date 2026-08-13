"""Adds (or updates) a collection's redirect slugs in redirects.json from a
source file, then rebuilds the static redirect pages.

Usage:
    python add_collection.py path/to/source.json
    python add_collection.py path/to/source.json --dry-run

source.json schema (see ShanezShertz/designs/<Collection>/source.json for
real examples):
{
  "prefix": "dc",
  "collection_slug": "daily-coping-co",
  "album_url": "https://www.teepublic.com/user/shanezshertz/albums?album=...",
  "designs": [
    {"slug": "dc-001", "file": "some_design.png", "title": "Some Design", "url": "https://www.teepublic.com/t-shirt/..."},
    ...
  ]
}

Every design must already have a "slug" — this script does not assign
them. Run ShanezShertz/scripts/gen_design_index.py first; it assigns a
permanent slug to any new design (never renumbering existing ones) and
writes it back into source.json. This script then just copies
slug -> url pairs into redirects.json. Re-running with an unchanged
source file is a no-op (idempotent): it overwrites only this prefix's own
keys, so it's always safe to re-run after edits.
"""

import argparse
import json
from pathlib import Path

import build as build_module

ROOT = Path(__file__).parent
REDIRECTS_PATH = ROOT / "redirects.json"


def compute_entries(source: dict) -> dict:
    missing = [d["title"] for d in source["designs"] if not d.get("slug")]
    if missing:
        raise ValueError(
            f"{len(missing)} design(s) have no slug yet: {', '.join(missing)}. "
            f"Run ShanezShertz/scripts/gen_design_index.py on this collection "
            f"first to assign slugs, then re-run this script."
        )
    entries = {d["slug"]: d["url"] for d in source["designs"]}
    entries[source["collection_slug"]] = source["album_url"]
    return entries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_file", type=Path)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print what would change without writing redirects.json or rebuilding",
    )
    args = parser.parse_args()

    source = json.loads(args.source_file.read_text(encoding="utf-8"))
    new_entries = compute_entries(source)

    redirects = json.loads(REDIRECTS_PATH.read_text(encoding="utf-8"))
    before = dict(redirects)
    redirects.update(new_entries)

    changed = {
        k: v for k, v in new_entries.items() if before.get(k) != v
    }
    removed_stale = [
        k
        for k in before
        if k.startswith(f"{source['prefix']}-") and k not in new_entries
    ]

    print(f"{len(new_entries)} entries for prefix {source['prefix']!r} "
          f"({len(changed)} new or changed)")
    for k in sorted(changed):
        print(f"  {k}: {new_entries[k]}")
    if removed_stale:
        print(f"WARNING: {len(removed_stale)} existing {source['prefix']}-* "
              f"entries are not in this source file and were left untouched "
              f"(remove manually from redirects.json if they're stale): "
              f"{', '.join(sorted(removed_stale))}")

    if args.dry_run:
        print("(dry run — nothing written)")
        return

    if not changed:
        print("redirects.json already up to date, skipping rebuild")
        return

    REDIRECTS_PATH.write_text(
        json.dumps(redirects, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    build_module.build()


if __name__ == "__main__":
    main()
