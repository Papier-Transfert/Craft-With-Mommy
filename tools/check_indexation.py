#!/usr/bin/env python3
"""
Daily indexation tracking agent for craft-with-mommy.com.

Reads sitemap.xml, picks up to 10 URLs per run by priority, performs technical
checks (HTTP/noindex/canonical), pushes eligible URLs to Google Indexing API
(cap 5/day) and IndexNow (no cap), then updates state.json and report.md.

Usage:
    python3 tools/check_indexation.py            # normal run
    python3 tools/check_indexation.py --dry-run  # no API calls, no writes
"""

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

ROOT = Path(__file__).resolve().parent.parent
SITEMAP_PATH = ROOT / "sitemap.xml"
INDEXATION_DIR = ROOT / "indexation"
STATE_PATH = INDEXATION_DIR / "state.json"
REPORT_PATH = INDEXATION_DIR / "report.md"
INDEXNOW_KEY_PATH = INDEXATION_DIR / "indexnow.key"
CREDENTIALS_PATH = ROOT / "tools" / "gsc-credentials.json"

SITE_URL = "https://www.craft-with-mommy.com"
SITE_HOST = "www.craft-with-mommy.com"
URLS_PER_RUN = 10
INDEXING_API_DAILY_CAP = 5
RECHECK_DAYS_NOT_INDEXED = 7
RECHECK_DAYS_INDEXED = 60
USER_AGENT = "CraftWithMommy-IndexationBot/1.0 (+https://www.craft-with-mommy.com)"
HTTP_TIMEOUT = 15
INDEXING_SCOPES = ["https://www.googleapis.com/auth/indexing"]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def now_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def days_since(iso_str):
    if not iso_str:
        return 9999
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - dt).days
    except Exception:
        return 9999


def load_state():
    if not STATE_PATH.exists():
        return {"last_run": None, "stats": {}, "articles": {}}
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    INDEXATION_DIR.mkdir(parents=True, exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
        f.write("\n")


def read_sitemap_urls():
    tree = ET.parse(SITEMAP_PATH)
    root = tree.getroot()
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = []
    for url_elem in root.findall("sm:url", ns):
        loc = url_elem.find("sm:loc", ns)
        if loc is None or not loc.text:
            continue
        u = loc.text.strip()
        if "/blog/" in u:
            urls.append(u)
    return urls


def check_url(url):
    result = {
        "url": url,
        "http_status": None,
        "title": None,
        "noindex": None,
        "canonical_ok": None,
        "canonical_url": None,
        "problem": None,
    }
    try:
        r = requests.get(url, headers={"User-Agent": USER_AGENT},
                         timeout=HTTP_TIMEOUT, allow_redirects=True)
        result["http_status"] = r.status_code
        if r.status_code != 200:
            result["problem"] = f"http_status={r.status_code}"
            return result
        soup = BeautifulSoup(r.text, "html.parser")
        title_tag = soup.find("title")
        if title_tag and title_tag.string:
            result["title"] = title_tag.string.strip()
        robots = soup.find("meta", attrs={"name": "robots"})
        if robots and "noindex" in (robots.get("content") or "").lower():
            result["noindex"] = True
            result["problem"] = "noindex"
        else:
            result["noindex"] = False
        canonical = soup.find("link", attrs={"rel": "canonical"})
        if canonical and canonical.get("href"):
            href = canonical["href"].strip()
            result["canonical_url"] = href
            result["canonical_ok"] = href.rstrip("/") == url.rstrip("/")
            if not result["canonical_ok"] and not result["problem"]:
                result["problem"] = f"canonical_mismatch: {href}"
        else:
            result["canonical_ok"] = False
            if not result["problem"]:
                result["problem"] = "no_canonical_tag"
    except Exception as e:
        result["problem"] = f"fetch_error: {type(e).__name__}: {e}"
    return result


def submit_indexing_api(url, credentials, dry_run=False):
    if dry_run:
        return {"ok": True, "dry_run": True}
    try:
        service = build("indexing", "v3", credentials=credentials, cache_discovery=False)
        response = service.urlNotifications().publish(
            body={"url": url, "type": "URL_UPDATED"}
        ).execute()
        return {"ok": True, "response": response}
    except HttpError as e:
        return {"ok": False, "error": f"HttpError {e.resp.status}: {e._get_reason() or str(e)[:200]}"}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {str(e)[:200]}"}


def submit_indexnow(url, key, dry_run=False):
    if dry_run:
        return {"ok": True, "dry_run": True}
    try:
        r = requests.post(
            "https://api.indexnow.org/indexnow",
            json={
                "host": SITE_HOST,
                "key": key,
                "keyLocation": f"{SITE_URL}/{key}.txt",
                "urlList": [url],
            },
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=HTTP_TIMEOUT,
        )
        if r.status_code in (200, 202):
            return {"ok": True, "status": r.status_code}
        return {"ok": False, "error": f"HTTP {r.status_code}: {r.text[:200]}"}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {str(e)[:200]}"}


def select_urls_to_process(sitemap_urls, state):
    selected = []
    seen = set()
    articles = state.get("articles", {})

    never_seen = sorted(u for u in sitemap_urls if u not in articles)
    for u in never_seen:
        if len(selected) >= URLS_PER_RUN:
            break
        selected.append(u)
        seen.add(u)

    if len(selected) < URLS_PER_RUN:
        candidates = []
        for u in sitemap_urls:
            if u in seen:
                continue
            art = articles.get(u)
            if not art:
                continue
            if art.get("gsc_indexed") in ("no", "unknown"):
                last = art.get("last_checked")
                if days_since(last) >= RECHECK_DAYS_NOT_INDEXED:
                    candidates.append((days_since(last), u))
        candidates.sort(reverse=True)
        for _, u in candidates:
            if len(selected) >= URLS_PER_RUN:
                break
            selected.append(u)
            seen.add(u)

    if len(selected) < URLS_PER_RUN:
        candidates = []
        for u in sitemap_urls:
            if u in seen:
                continue
            art = articles.get(u)
            if not art:
                continue
            if art.get("gsc_indexed") == "yes":
                last = art.get("last_checked")
                if days_since(last) >= RECHECK_DAYS_INDEXED:
                    candidates.append((days_since(last), u))
        candidates.sort(reverse=True)
        for _, u in candidates:
            if len(selected) >= URLS_PER_RUN:
                break
            selected.append(u)

    return selected


def update_article_state(state, url, check, indexing_pushed, indexnow_pushed):
    articles = state.setdefault("articles", {})
    art = articles.setdefault(url, {})
    art.setdefault("first_seen", now_date())
    art["title"] = check.get("title") or art.get("title") or ""
    art["last_checked"] = now_iso()
    art["http_status"] = check["http_status"]
    art["noindex"] = check["noindex"]
    art["canonical_ok"] = check["canonical_ok"]
    art["canonical_url"] = check.get("canonical_url")
    art["in_sitemap"] = True
    art.setdefault("gsc_indexed", "unknown")
    art["problem"] = check.get("problem")
    if indexing_pushed:
        art["indexing_api_last_push"] = now_date()
    if indexnow_pushed:
        art["indexnow_last_push"] = now_date()


def compute_stats(state, total_sitemap):
    articles = state.get("articles", {})
    return {
        "total_sitemap_urls": total_sitemap,
        "total_seen": len(articles),
        "indexed": sum(1 for a in articles.values() if a.get("gsc_indexed") == "yes"),
        "not_indexed": sum(1 for a in articles.values() if a.get("gsc_indexed") == "no"),
        "unknown": sum(1 for a in articles.values() if a.get("gsc_indexed") == "unknown"),
        "with_problems": sum(1 for a in articles.values() if a.get("problem")),
    }


def gsc_inspect_link(url):
    return (f"https://search.google.com/search-console/inspect"
            f"?resource_id={quote(SITE_URL + '/', safe='')}"
            f"&id={quote(url, safe='')}")


def write_report(state, urls_processed_today, summary):
    INDEXATION_DIR.mkdir(parents=True, exist_ok=True)
    today = now_date()
    stats = state.get("stats", {})
    articles = state.get("articles", {})

    lines = [
        f"# Indexation Report — {today}",
        "",
        f"**Last run:** `{state.get('last_run')}`",
        "",
        "## Stats globales",
        "",
        f"- Total URLs sitemap : **{stats.get('total_sitemap_urls', 0)}**",
        f"- URLs déjà traitées (au moins une fois) : **{stats.get('total_seen', 0)}**",
        f"- Indexées (à vérifier manuellement dans GSC) : {stats.get('indexed', 0)}",
        f"- Non indexées : {stats.get('not_indexed', 0)}",
        f"- État inconnu : {stats.get('unknown', 0)}",
        f"- Avec problème technique : **{stats.get('with_problems', 0)}**",
        "",
        f"## Run du jour — {summary.get('urls_processed', 0)} URLs traitées",
        "",
        f"- Soumises à Indexing API : **{summary.get('indexing_api_pushed', 0)}** "
        f"(cap {INDEXING_API_DAILY_CAP}/jour)",
        f"- Soumises à IndexNow : **{summary.get('indexnow_pushed', 0)}**",
        "",
        "## URLs traitées aujourd'hui",
        "",
        "| URL | Titre | HTTP | Tech | Indexing API | IndexNow | Problème | GSC |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for url in urls_processed_today:
        art = articles.get(url, {})
        title = (art.get("title") or "")[:50]
        http = art.get("http_status") or "?"
        tech_ok = "✅" if (
            art.get("http_status") == 200
            and not art.get("noindex")
            and art.get("canonical_ok")
        ) else "❌"
        ix_api = art.get("indexing_api_last_push") or "–"
        if ix_api == today:
            ix_api = "✅ today"
        idxnow = art.get("indexnow_last_push") or "–"
        if idxnow == today:
            idxnow = "✅ today"
        problem = art.get("problem") or "–"
        short_url = url.replace(SITE_URL, "")
        gsc = f"[Inspect]({gsc_inspect_link(url)})"
        lines.append(
            f"| [{short_url}]({url}) | {title} | {http} | {tech_ok} | "
            f"{ix_api} | {idxnow} | {problem} | {gsc} |"
        )

    problem_articles = [(u, a) for u, a in articles.items() if a.get("problem")]
    if problem_articles:
        lines.append("")
        lines.append("## ⚠️ URLs avec problèmes techniques")
        lines.append("")
        lines.append("| URL | Problème | Last checked |")
        lines.append("|---|---|---|")
        for u, a in problem_articles[:50]:
            short = u.replace(SITE_URL, "")
            last = (a.get("last_checked") or "–")[:10]
            lines.append(f"| [{short}]({u}) | {a.get('problem')} | {last} |")

    not_indexed = [(u, a) for u, a in articles.items()
                   if a.get("gsc_indexed") in ("no", "unknown")
                   and not a.get("problem")]
    if not_indexed:
        not_indexed.sort(key=lambda x: x[1].get("first_seen", ""))
        lines.append("")
        lines.append("## 🔍 URLs à inspecter manuellement dans GSC (priorité)")
        lines.append("")
        lines.append("Clique sur le lien GSC pour voir l'état d'indexation Google et "
                     "demander l'indexation manuelle si nécessaire.")
        lines.append("")
        lines.append("| URL | Premier vu | Dernière push Indexing API | GSC |")
        lines.append("|---|---|---|---|")
        for u, a in not_indexed[:20]:
            short = u.replace(SITE_URL, "")
            first = a.get("first_seen", "–")
            last_push = a.get("indexing_api_last_push", "–")
            gsc = f"[Inspect]({gsc_inspect_link(u)})"
            lines.append(f"| [{short}]({u}) | {first} | {last_push} | {gsc} |")

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="No API calls, no state/report writes (just print).")
    parser.add_argument("--limit", type=int, default=None,
                        help="Override URLS_PER_RUN for this run.")
    args = parser.parse_args()

    urls_per_run = args.limit if args.limit else URLS_PER_RUN

    print(f"[{now_iso()}] Indexation agent starting"
          + (" [DRY-RUN]" if args.dry_run else ""))

    state = load_state()
    sitemap_urls = read_sitemap_urls()
    print(f"  Sitemap blog URLs: {len(sitemap_urls)}")

    if not INDEXNOW_KEY_PATH.exists():
        print(f"  ERROR: IndexNow key missing at {INDEXNOW_KEY_PATH}", file=sys.stderr)
        sys.exit(1)
    indexnow_key = INDEXNOW_KEY_PATH.read_text().strip()

    if not CREDENTIALS_PATH.exists():
        print(f"  ERROR: SA credentials missing at {CREDENTIALS_PATH}", file=sys.stderr)
        sys.exit(1)
    credentials = service_account.Credentials.from_service_account_file(
        str(CREDENTIALS_PATH), scopes=INDEXING_SCOPES
    )

    to_process = select_urls_to_process(sitemap_urls, state)
    if args.limit:
        to_process = to_process[:urls_per_run]
    print(f"  URLs selected for this run: {len(to_process)}")

    indexing_pushed_count = 0
    indexnow_pushed_count = 0

    for url in to_process:
        print(f"  → {url}")
        check = check_url(url)
        print(f"    HTTP={check['http_status']} noindex={check['noindex']} "
              f"canonical_ok={check['canonical_ok']} problem={check['problem']}")
        tech_clean = (
            check["http_status"] == 200
            and not check["noindex"]
            and check["canonical_ok"]
        )

        indexing_pushed = False
        if tech_clean and indexing_pushed_count < INDEXING_API_DAILY_CAP:
            res = submit_indexing_api(url, credentials, dry_run=args.dry_run)
            if res["ok"]:
                indexing_pushed = True
                indexing_pushed_count += 1
                print(f"    Indexing API: ✅"
                      + (" (dry-run)" if res.get("dry_run") else ""))
            else:
                print(f"    Indexing API: ❌ {res.get('error')}")

        indexnow_pushed = False
        if tech_clean:
            res = submit_indexnow(url, indexnow_key, dry_run=args.dry_run)
            if res["ok"]:
                indexnow_pushed = True
                indexnow_pushed_count += 1
                print(f"    IndexNow: ✅"
                      + (" (dry-run)" if res.get("dry_run") else ""))
            else:
                print(f"    IndexNow: ❌ {res.get('error')}")

        update_article_state(state, url, check, indexing_pushed, indexnow_pushed)

    state["last_run"] = now_iso()
    state["stats"] = compute_stats(state, len(sitemap_urls))

    summary = {
        "urls_processed": len(to_process),
        "indexing_api_pushed": indexing_pushed_count,
        "indexnow_pushed": indexnow_pushed_count,
    }

    if args.dry_run:
        print(f"[{now_iso()}] DRY-RUN done. Would push: "
              f"{indexing_pushed_count} to Indexing API, "
              f"{indexnow_pushed_count} to IndexNow. State/report NOT written.")
    else:
        save_state(state)
        write_report(state, to_process, summary)
        print(f"[{now_iso()}] Done. Indexing API: {indexing_pushed_count}/"
              f"{INDEXING_API_DAILY_CAP} | IndexNow: {indexnow_pushed_count} | "
              f"Total checked: {len(to_process)}")
        print(f"  state.json: {STATE_PATH}")
        print(f"  report.md:  {REPORT_PATH}")


if __name__ == "__main__":
    main()
