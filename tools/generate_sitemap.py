"""
generate_sitemap.py
Génère sitemap.xml à la racine du repo.
Utilise les dates de commit Git pour lastmod (fiable).
À appeler depuis la racine : python tools/generate_sitemap.py
"""
import os
import glob
import subprocess
from datetime import datetime

BASE_URL = "https://www.craft-with-mommy.com"
BLOG_DIR = "blog"
OUTPUT = "sitemap.xml"

# Pages statiques (sans lastmod — contenu stable)
STATIC_PAGES = [
    "/",
    "/blog/",
    "/about.html",
    "/legal.html",
    "/privacy.html",
    "/blog/paper-crafts.html",
    "/blog/paper-plate-crafts.html",
    "/blog/handprint-crafts.html",
    "/blog/recycled-crafts.html",
]

# Pages de collection à exclure du scan automatique des articles
COLLECTION_PAGES = {
    "index.html",
    "paper-crafts.html",
    "paper-plate-crafts.html",
    "handprint-crafts.html",
    "recycled-crafts.html",
}


def git_lastmod(filepath):
    """Retourne la date du dernier commit Git pour ce fichier (YYYY-MM-DD)."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%aI", "--", filepath],
            capture_output=True, text=True, check=True
        )
        iso = result.stdout.strip()
        if iso:
            return datetime.fromisoformat(iso).strftime("%Y-%m-%d")
    except Exception:
        pass
    return None


def get_blog_articles():
    entries = []
    for filepath in sorted(glob.glob(f"{BLOG_DIR}/*.html")):
        filename = os.path.basename(filepath)
        if filename in COLLECTION_PAGES:
            continue
        lastmod = git_lastmod(filepath)
        entries.append((f"/blog/{filename}", lastmod))
    # Trier par lastmod décroissant (plus récent en premier)
    entries.sort(key=lambda x: x[1] or "", reverse=True)
    return entries


def generate_sitemap():
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        "",
    ]

    for path in STATIC_PAGES:
        lines.append(f"  <url><loc>{BASE_URL}{path}</loc></url>")

    lines.append("")

    for path, lastmod in get_blog_articles():
        if lastmod:
            lines.append(f"  <url>")
            lines.append(f"    <loc>{BASE_URL}{path}</loc>")
            lines.append(f"    <lastmod>{lastmod}</lastmod>")
            lines.append(f"  </url>")
        else:
            lines.append(f"  <url><loc>{BASE_URL}{path}</loc></url>")

    lines += ["", "</urlset>", ""]

    content = "\n".join(lines)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(content)

    total = len(STATIC_PAGES) + len(get_blog_articles())
    print(f"sitemap.xml généré ({total} URLs)")


if __name__ == "__main__":
    generate_sitemap()
