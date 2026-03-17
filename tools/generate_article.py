#!/usr/bin/env python3
"""
generate_article.py — Daily blog article generator for craft-with-mommy.com
Runs via cron at 8h every day.
"""

import os
import sys
import json
import re
import time
import logging
import subprocess
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from slugify import slugify
import anthropic
from dotenv import load_dotenv

try:
    from PIL import Image as _PILImage
    _PILLOW_AVAILABLE = True
except ImportError:
    _PILLOW_AVAILABLE = False

try:
    from amazon_paapi import AmazonApi
    _AMAZON_PAAPI_AVAILABLE = True
except ImportError:
    _AMAZON_PAAPI_AVAILABLE = False

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
TOOLS_DIR = BASE_DIR / "tools"
BLOG_DIR = BASE_DIR / "blog"
IMAGES_DIR = BLOG_DIR / "images"
PUBLISHED_KEYWORDS_FILE = TOOLS_DIR / "published_keywords.json"
BLOG_INDEX_FILE = BLOG_DIR / "index.html"
HOME_INDEX_FILE = BASE_DIR / "index.html"

COMPETITOR_SITES = [
    "https://kidsactivitiesblog.com",
    "https://thebestideasforkids.com",
    "https://easypeasyandfun.com",
    "https://iheartcraftythings.com",
    "https://happyhooligans.ca",
    "https://craftymorning.com",
    "https://firefliesandmudpies.com",
    "https://simpleeverydaymom.com",
    "https://messforless.net",
    "https://nontoygifts.com",
]

FALLBACK_TOPICS = [
    "Paper plate animals for toddlers",
    "Easy yarn crafts for kids",
    "Recycled toilet roll crafts",
    "Finger painting ideas for babies",
    "Nature crafts with leaves",
    "Sensory play dough recipes",
    "Rainbow craft activities",
    "Simple butterfly crafts",
    "Cotton ball cloud art",
    "Handprint keepsake craft",
    "Paper bag puppet making",
    "Sticker art for toddlers",
    "Foam sticker collage",
    "Tissue paper flower craft",
    "Egg carton caterpillar",
    "Paper chain decorations",
    "Salt dough ornaments",
    "Painted rock garden",
    "Cardboard box castle",
    "Pipe cleaner animals",
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_env():
    load_dotenv(BASE_DIR / ".env")


def load_published_keywords() -> list:
    if PUBLISHED_KEYWORDS_FILE.exists():
        try:
            return json.loads(PUBLISHED_KEYWORDS_FILE.read_text())
        except Exception:
            pass
    return []


def save_keyword(keyword_data: dict, slug: str, pub_date: str, main_image_filename: str = "") -> None:
    records = load_published_keywords()
    records.append({
        "keyword": keyword_data["primary_keyword"],
        "slug": slug,
        "title": keyword_data["article_title"],
        "date": pub_date,
        "main_image": main_image_filename,
    })
    PUBLISHED_KEYWORDS_FILE.write_text(json.dumps(records, indent=2, ensure_ascii=False))
    log.info("Saved keyword to published_keywords.json")


# ---------------------------------------------------------------------------
# Image helpers — SEO filenames + compression
# ---------------------------------------------------------------------------

_STOP_WORDS = {
    "a", "an", "the", "for", "with", "and", "of", "in", "to", "how",
    "easy", "simple", "fun", "make", "making", "do", "doing", "step",
    "using", "use", "get", "your", "our", "my", "their", "its",
}


def make_seo_filename(text: str, max_words: int = 4) -> str:
    """Return a 3-4 word hyphenated SEO-friendly filename stem.

    Example: "easy paper plate sun craft for toddlers" → "paper-plate-sun-craft"
    """
    cleaned = re.sub(r"[^a-z0-9\s]", "", text.lower())
    words = [w for w in cleaned.split() if w and w not in _STOP_WORDS]
    if not words:
        words = cleaned.split()  # fallback: keep all words
    return "-".join(words[:max_words]) or "craft-image"


def compress_image(path: Path) -> None:
    """Re-save a WebP with Pillow at quality=75 to reduce file size.

    Order: called *after* the raw bytes are written, *before* the file is
    used anywhere — so the final file on disk is both compressed and already
    named with its SEO-friendly filename (no rename needed).
    """
    if not _PILLOW_AVAILABLE:
        log.warning("Pillow not installed — skipping compression (pip install Pillow)")
        return
    try:
        original_size = path.stat().st_size
        with _PILImage.open(path) as img:
            img.save(path, "WEBP", quality=75, method=6)
        new_size = path.stat().st_size
        log.info(
            f"Compressed {path.name}: {original_size // 1024}KB → {new_size // 1024}KB "
            f"(saved {(original_size - new_size) // 1024}KB)"
        )
    except Exception as exc:
        log.warning(f"Compression failed for {path.name}: {exc}")


# ---------------------------------------------------------------------------
# Step 1 — Scrape competitor titles
# ---------------------------------------------------------------------------

def scrape_competitor_titles(sites: list) -> list:
    titles = []
    for site in sites:
        try:
            resp = requests.get(site, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            for tag in soup.find_all(["h2", "h3"]):
                text = tag.get_text(strip=True)
                if 15 < len(text) < 120:
                    titles.append(text)
            log.info(f"Scraped {site} — {len(titles)} titles so far")
        except Exception as exc:
            log.warning(f"Could not scrape {site}: {exc}")

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for t in titles:
        if t not in seen:
            seen.add(t)
            unique.append(t)

    if not unique:
        log.warning("No titles scraped — using fallback topics")
        return FALLBACK_TOPICS

    return unique[:150]


# ---------------------------------------------------------------------------
# Step 2 — Claude: choose keyword + metadata
# ---------------------------------------------------------------------------

def select_keyword_and_variants(titles: list, used_keywords: list) -> dict:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    used_str = ", ".join(used_keywords[-60:]) if used_keywords else "none yet"
    titles_str = "\n".join(f"- {t}" for t in titles[:80])

    prompt = f"""You are a content strategist for craft-with-mommy.com, a US family craft blog targeting moms with children ages 2–8.

Here are recent article titles from competitor craft blogs:
{titles_str}

Keywords already used (do NOT repeat): {used_str}

Choose ONE primary keyword for a new blog article. Requirements:
- Long-tail, SEO-friendly, specific (e.g. "easy paper plate sun craft for toddlers")
- NOT already in the used list
- Highly relevant to the US mom persona
- Craft that can be broken into exactly 5 simple steps
- Must be genuinely fun and feasible for young kids

Return ONLY valid JSON with this exact structure (no markdown, no explanation):
{{
  "primary_keyword": "...",
  "long_tail_variants": ["...", "...", "...", "...", "..."],
  "article_title": "...",
  "category": "Painting|Paper Crafts|Yarn & Weaving|Recycled Crafts|Sensory Play",
  "age_range": "Ages 2+|Ages 3+|Ages 4+|Ages 5+",
  "time_minutes": 15,
  "messiness_scale": "Low|Medium|High",
  "step_descriptions": [
    "Brief description of step 1 (for image prompt)",
    "Brief description of step 2 (for image prompt)",
    "Brief description of step 3 (for image prompt)",
    "Brief description of step 4 (for image prompt)",
    "Brief description of step 5 (for image prompt)"
  ]
}}"""

    for attempt in range(2):
        try:
            msg = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=800,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = msg.content[0].text.strip()
            # Strip markdown code fences if present
            raw = re.sub(r"^```(?:json)?\s*", "", raw)
            raw = re.sub(r"\s*```$", "", raw)
            data = json.loads(raw)
            log.info(f"Keyword selected: {data['primary_keyword']}")
            return data
        except json.JSONDecodeError as exc:
            if attempt == 0:
                log.warning(f"JSON parse error on attempt {attempt+1}: {exc}. Retrying...")
                prompt += "\n\nReturn JSON only, no other text."
            else:
                log.error(f"JSON parse error on attempt 2: {exc}")
                raise
        except Exception as exc:
            log.error(f"Claude keyword selection failed: {exc}")
            raise


# ---------------------------------------------------------------------------
# Step 3 — Claude: generate article HTML body
# ---------------------------------------------------------------------------

def generate_article_html(keyword_data: dict, published_articles: list = None) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    keyword = keyword_data["primary_keyword"]
    title = keyword_data["article_title"]
    variants = ", ".join(keyword_data["long_tail_variants"])
    category = keyword_data["category"]
    age_range = keyword_data["age_range"]
    time_min = keyword_data["time_minutes"]
    messiness = keyword_data["messiness_scale"]

    # Build the "More Crafts You'll Love" instruction based on real published articles
    if published_articles:
        # Use up to 2 most recent articles as internal links
        links_to_use = published_articles[-2:]
        internal_links_instruction = (
            '   - <h2>More Crafts You\'ll Love</h2> — link to these exact published articles '
            '(use the exact URLs and titles provided, do NOT invent other links):\n'
        )
        for art in links_to_use:
            art_url = f"/blog/{art['slug']}.html"
            art_title = art.get("title", art["slug"].replace("-", " ").title())
            internal_links_instruction += f'     <li><a href="{art_url}">{art_title}</a></li>\n'
        internal_links_instruction += (
            '     Write 1 short sentence of intro before the list, '
            'then the list with these 2 links only.'
        )
    else:
        internal_links_instruction = (
            '   - <h2>More Crafts You\'ll Love</h2> — write: '
            '"More fun craft ideas are coming soon — stay tuned!" (no links, no list)'
        )

    prompt = f"""You are writing a craft blog article for craft-with-mommy.com — a warm, friendly US family craft blog for moms with kids ages 2–8.

Primary keyword: {keyword}
LSI/variant keywords to include naturally: {variants}
Article title: {title}
Category: {category} | Age range: {age_range} | Time: {time_min} min | Messiness: {messiness}

Write a complete, engaging article of ~1500 words in HTML format. The article must:

1. Start with a warm, relatable intro paragraph (2–3 sentences, no heading)

2. Use this exact section structure with these HTML headings:
   - <h2>Why Kids Love This Craft</h2> (2 short paragraphs, benefits)

   - <h2>What You'll Need</h2>
     This is the most important section for practical value. Write a detailed <ul> list of EVERY material and tool needed.
     Rules for this section:
     a) Be SPECIFIC — mention exact colors, sizes, quantities when they matter.
        Examples: "6 paper plates (standard 9-inch size)", "washable red and black tempera paint",
        "a medium round paintbrush (#8)", "a low-temp glue gun", "12 googly eyes (10mm)"
     b) For every item that can realistically be purchased on Amazon, wrap the item name in an affiliate link:
        <a href="[AMAZON_LINK_item_slug]" rel="nofollow sponsored" target="_blank">item name</a>
        where item_slug is a short lowercase hyphenated identifier for that item.
        Examples:
          <a href="[AMAZON_LINK_paper_plates]" rel="nofollow sponsored" target="_blank">standard 9-inch paper plates</a>
          <a href="[AMAZON_LINK_washable_tempera_paint]" rel="nofollow sponsored" target="_blank">washable red and black tempera paint</a>
          <a href="[AMAZON_LINK_googly_eyes]" rel="nofollow sponsored" target="_blank">10mm googly eyes</a>
          <a href="[AMAZON_LINK_round_paintbrush]" rel="nofollow sponsored" target="_blank">medium round paintbrush</a>
          <a href="[AMAZON_LINK_glue_stick]" rel="nofollow sponsored" target="_blank">glue stick</a>
     c) Items that do NOT need an affiliate link: things every household has (tap water, a table, paper towels, etc.)
     d) Aim for 6–10 items total. Every item must be on its own <li>.

   - <h2>Step-by-Step Instructions</h2> (5 numbered steps, each with <h3>Step X: [name]</h3>, a paragraph, and an image placeholder: [STEP_IMAGE_PLACEHOLDER_1] through [STEP_IMAGE_PLACEHOLDER_5])

   - <h2>Tips for Success</h2> (3–4 bullet tips for age-appropriate adaptations)

   - <h2>Variations to Try</h2> (2–3 creative variations, 1 short paragraph each)

   - {internal_links_instruction}

   - <h2>Final Thoughts</h2> (1 warm closing paragraph with a call to action to share on Pinterest)

3. Naturally include the primary keyword "{keyword}" at least 4 times
4. Include at least 2 of these variant keywords: {variants}
5. Place [MAIN_IMAGE_PLACEHOLDER] as the very first element (before the intro)
6. Use only these HTML tags: p, ul, ol, li, h2, h3, strong, em, a, div
7. Keep the tone warm, encouraging, and conversational — like a best friend who crafts
8. Do NOT include <html>, <head>, <body>, or any document-level tags
9. Do NOT include the article title as an h1 (it's added by the template)
10. IMPORTANT: Do NOT invent any internal links. Only use the exact URLs provided above.
11. IMPORTANT: Do NOT use generic affiliate links. Each Amazon link must target the specific item it wraps.

Return only the HTML content, no explanation."""

    msg = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    html = msg.content[0].text.strip()
    log.info("Article HTML generated")
    return html


# ---------------------------------------------------------------------------
# Step 4 — Generate images via Google Imagen
# ---------------------------------------------------------------------------

def generate_images(slug: str, article_title: str, step_descriptions: list,
                    primary_keyword: str = "") -> dict:
    """Generate all images for an article.

    Returns a dict where each value is either:
      {"path": "blog/images/{slug}/filename.webp", "filename": "filename.webp", "alt": "..."}
    or the PLACEHOLDER sentinel dict on failure.

    Image pipeline per image:
      1. Generate via Imagen API (landscape 4:3 aspect ratio)
      2. Write raw bytes to disk (SEO-friendly filename already applied)
      3. Compress in-place with Pillow (quality=75)
    """
    try:
        from google import genai
        from google.genai import types as genai_types
    except ImportError:
        log.warning("google-genai not installed — skipping image generation")
        return _placeholder_paths()

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        log.warning("GOOGLE_API_KEY not set — skipping image generation")
        return _placeholder_paths()

    client = genai.Client(api_key=api_key)
    img_dir = IMAGES_DIR / slug
    img_dir.mkdir(parents=True, exist_ok=True)

    paths = {}

    # --- Main image: flat-lay, landscape 4:3 ---
    source_text = primary_keyword or article_title
    main_stem = make_seo_filename(source_text, max_words=4)
    main_filename = f"{main_stem}.webp"
    main_alt = f"Craft supplies for {article_title}"
    main_prompt = (
        f"Flat-lay photo of craft materials for '{article_title}': colorful paper, "
        f"scissors, glue, and other supplies arranged neatly on a white wooden table. "
        f"Bright, natural light. Clean, cheerful aesthetic. No people."
    )
    paths["main"] = _generate_single_image(
        client, main_prompt, img_dir / main_filename,
        alt_text=main_alt, aspect_ratio="4:3",
    )
    time.sleep(1)

    # --- Step images: process shots, landscape 4:3 ---
    for i, desc in enumerate(step_descriptions[:5], start=1):
        step_stem = make_seo_filename(desc, max_words=3)
        step_filename = f"{step_stem}.webp"
        # Descriptive alt: use the step description directly (already natural language)
        step_alt = desc.strip().rstrip(".")
        if len(step_alt) > 120:
            step_alt = step_alt[:117] + "..."
        step_prompt = (
            f"Close-up photo of child's hands doing a craft step: {desc}. "
            f"Bright natural light, white table, colorful craft supplies visible. "
            f"Warm and cheerful kids craft photo style."
        )
        paths[f"step_{i}"] = _generate_single_image(
            client, step_prompt, img_dir / step_filename,
            alt_text=step_alt, aspect_ratio="4:3",
        )
        time.sleep(1)

    return paths


def _generate_single_image(client, prompt: str, output_path: Path,
                            alt_text: str = "", aspect_ratio: str = "4:3") -> dict:
    """Generate one image via Gemini 2.5 Flash Image, convert to WebP, compress, return info dict.

    Uses generateContent with responseModalities=["IMAGE"] — same endpoint as text generation.
    Gemini returns base64-encoded PNG/JPEG; we decode and re-save as WebP via Pillow.
    The compress+convert step replaces the separate compress_image() call.
    """
    try:
        import io
        from google.genai import types as genai_types

        # Include aspect ratio hint in the prompt (no dedicated config param for this model)
        full_prompt = f"{prompt} Aspect ratio: {aspect_ratio}. Landscape orientation."

        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=full_prompt,
            config=genai_types.GenerateContentConfig(
                response_modalities=["IMAGE"],
            ),
        )

        # Extract the first image part from the response
        # Note: inline_data.data is already raw bytes (not base64) in google-genai SDK
        image_bytes = None
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_bytes = part.inline_data.data
                break

        if image_bytes is None:
            raise ValueError("No image data found in Gemini response")

        # Convert from PNG/JPEG → WebP at quality=75 in one Pillow pass (no temp file)
        with _PILImage.open(io.BytesIO(image_bytes)) as img:
            img.save(output_path, "WEBP", quality=75, method=6)

        size_kb = output_path.stat().st_size // 1024
        log.info(f"Image saved & compressed: {output_path.name} ({size_kb}KB)")

        return {
            "path": str(output_path.relative_to(BASE_DIR)),
            "filename": output_path.name,
            "alt": alt_text,
        }
    except Exception as exc:
        log.warning(f"Image generation failed for {output_path.name}: {exc}")
        return {"path": "PLACEHOLDER", "filename": "", "alt": ""}


def _placeholder_paths() -> dict:
    return {k: {"path": "PLACEHOLDER", "filename": "", "alt": ""}
            for k in ["main", "step_1", "step_2", "step_3", "step_4", "step_5"]}


# ---------------------------------------------------------------------------
# Step 5 — Replace image placeholders in article HTML
# ---------------------------------------------------------------------------

def resolve_image_placeholders(article_html: str, image_paths: dict, slug: str) -> str:
    """Replace [MAIN_IMAGE_PLACEHOLDER] and [STEP_IMAGE_PLACEHOLDER_N] with
    real <figure><img> tags using SEO-friendly filenames and descriptive alts,
    or styled placeholder divs when images failed to generate.
    """
    def _get(info, key, default=""):
        return info.get(key, default) if isinstance(info, dict) else default

    # --- Main image ---
    main_info = image_paths.get("main", {})
    main_path = _get(main_info, "path", "PLACEHOLDER")
    if main_path == "PLACEHOLDER":
        main_img_html = '<div class="img-placeholder img-placeholder--main" aria-hidden="true">🎨</div>'
    else:
        filename = _get(main_info, "filename") or "main.webp"
        alt = _get(main_info, "alt") or "Craft materials laid out for the project"
        rel = f"../blog/images/{slug}/{filename}"
        main_img_html = (
            f'<figure class="article-main-img">'
            f'<img src="{rel}" alt="{alt}" '
            f'width="800" height="600" loading="eager">'
            f'</figure>'
        )
    article_html = article_html.replace("[MAIN_IMAGE_PLACEHOLDER]", main_img_html)

    # --- Step images ---
    for i in range(1, 6):
        step_info = image_paths.get(f"step_{i}", {})
        step_path = _get(step_info, "path", "PLACEHOLDER")
        if step_path == "PLACEHOLDER":
            step_img_html = (
                f'<div class="img-placeholder img-placeholder--step" aria-hidden="true">'
                f'Step {i} 🖐️</div>'
            )
        else:
            filename = _get(step_info, "filename") or f"step-{i}.webp"
            alt = _get(step_info, "alt") or f"Step {i} of the craft activity"
            rel = f"../blog/images/{slug}/{filename}"
            step_img_html = (
                f'<figure class="article-step-img">'
                f'<img src="{rel}" alt="{alt}" '
                f'width="800" height="600" loading="lazy">'
                f'</figure>'
            )
        article_html = article_html.replace(f"[STEP_IMAGE_PLACEHOLDER_{i}]", step_img_html)

    return article_html


# ---------------------------------------------------------------------------
# Step 6 — Build full article page HTML
# ---------------------------------------------------------------------------

def build_article_page(slug: str, article_html: str, keyword_data: dict, pub_date: str) -> str:
    title = keyword_data["article_title"]
    category = keyword_data["category"]
    age_range = keyword_data["age_range"]
    time_min = keyword_data["time_minutes"]
    messiness = keyword_data["messiness_scale"]
    keyword = keyword_data["primary_keyword"]
    canonical_url = f"https://craft-with-mommy.com/blog/{slug}.html"

    messiness_emoji = {"Low": "💧", "Medium": "💦", "High": "🌊"}.get(messiness, "💧")
    category_emoji = {
        "Painting": "🎨",
        "Paper Crafts": "✂️",
        "Yarn & Weaving": "🧵",
        "Recycled Crafts": "♻️",
        "Sensory Play": "🌈",
    }.get(category, "🎨")

    # Build JSON-LD HowTo steps
    steps_ld = []
    for i, desc in enumerate(keyword_data.get("step_descriptions", []), start=1):
        steps_ld.append({
            "@type": "HowToStep",
            "name": f"Step {i}",
            "text": desc,
        })

    json_ld = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": title,
        "description": f"Learn how to make {keyword} with your kids — a simple, fun craft for {age_range}.",
        "totalTime": f"PT{time_min}M",
        "step": steps_ld,
    }

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Craft with Mommy</title>
  <meta name="description" content="Learn how to make {keyword} with your kids. A simple, fun {category.lower()} craft for {age_range}. Takes only {time_min} minutes!">
  <link rel="canonical" href="{canonical_url}">

  <!-- Open Graph -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="Easy {keyword} craft for kids — step by step. Perfect for {age_range}, takes {time_min} minutes!">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:site_name" content="Craft with Mommy">

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,400&display=swap" rel="stylesheet">

  <!-- JSON-LD HowTo -->
  <script type="application/ld+json">
  {json.dumps(json_ld, indent=2, ensure_ascii=False)}
  </script>

  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      font-family: 'DM Sans', sans-serif;
      color: #333333;
      background: #FFFFFF;
      line-height: 1.65;
      -webkit-font-smoothing: antialiased;
    }}
    h1, h2, h3, h4, h5 {{ font-family: 'Nunito', sans-serif; line-height: 1.2; }}
    a {{ text-decoration: none; color: inherit; }}
    img {{ max-width: 100%; display: block; }}
    .container {{ max-width: 1140px; margin: 0 auto; padding: 0 24px; }}

    /* Buttons */
    .btn {{
      display: inline-block;
      background: #E8856A;
      color: #FFFFFF;
      font-family: 'Nunito', sans-serif;
      font-weight: 700;
      font-size: 1rem;
      padding: 13px 30px;
      border-radius: 36px;
      border: 2px solid transparent;
      cursor: pointer;
      transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
      white-space: nowrap;
    }}
    .btn:hover {{ background: #D4755C; transform: translateY(-2px); box-shadow: 0 8px 24px rgba(232,133,106,0.3); }}
    .btn-outline {{ background: transparent; border-color: #E8856A; color: #E8856A; }}
    .btn-outline:hover {{ background: #E8856A; color: #FFFFFF; }}
    .btn-sm {{ font-size: 0.88rem; padding: 10px 22px; }}

    /* Header */
    .header {{
      position: sticky; top: 0; z-index: 200;
      background: rgba(255,255,255,0.96);
      backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
      border-bottom: 1px solid #F0ECE7;
    }}
    .header-inner {{ height: 72px; display: flex; align-items: center; justify-content: space-between; gap: 24px; }}
    .logo {{ display: flex; align-items: center; flex-shrink: 0; }}
    .logo img {{ height: 54px; width: auto; }}
    .nav {{ display: flex; align-items: center; gap: 4px; }}
    .nav-item {{ position: relative; }}
    .nav-trigger {{
      font-family: 'Nunito', sans-serif; font-weight: 700; font-size: 0.95rem;
      color: #444; padding: 9px 16px; border-radius: 10px; cursor: pointer;
      display: flex; align-items: center; gap: 6px;
      transition: background 0.15s, color 0.15s;
      background: none; border: none;
    }}
    .nav-trigger:hover {{ background: #FDFBF7; color: #E8856A; }}
    .nav-trigger svg {{ transition: transform 0.25s; flex-shrink: 0; }}
    .nav-item:hover .nav-trigger svg {{ transform: rotate(180deg); }}
    .dropdown {{
      position: absolute; top: calc(100% + 10px); left: 0;
      background: #FFFFFF; border: 1px solid #F0ECE7; border-radius: 18px;
      padding: 8px; min-width: 210px;
      box-shadow: 0 12px 40px rgba(0,0,0,0.09);
      opacity: 0; visibility: hidden; transform: translateY(-6px);
      transition: opacity 0.2s, transform 0.2s, visibility 0.2s; pointer-events: none;
    }}
    .nav-item:hover .dropdown, .nav-item:focus-within .dropdown {{
      opacity: 1; visibility: visible; transform: translateY(0); pointer-events: auto;
    }}
    .dropdown a {{
      display: flex; align-items: center; gap: 11px;
      padding: 10px 13px; border-radius: 11px;
      font-size: 0.91rem; font-weight: 500; color: #555;
      transition: background 0.15s, color 0.15s;
    }}
    .dropdown a:hover {{ background: #FEF0EC; color: #E8856A; }}
    .drop-icon {{ font-size: 1.05rem; line-height: 1; }}
    .hamburger {{ display: none; flex-direction: column; justify-content: center; gap: 5px; padding: 8px; cursor: pointer; background: none; border: none; }}
    .hamburger span {{ display: block; width: 22px; height: 2px; background: #444; border-radius: 2px; transition: transform 0.25s, opacity 0.25s; }}
    .hamburger.open span:nth-child(1) {{ transform: translateY(7px) rotate(45deg); }}
    .hamburger.open span:nth-child(2) {{ opacity: 0; }}
    .hamburger.open span:nth-child(3) {{ transform: translateY(-7px) rotate(-45deg); }}
    .mobile-nav {{ display: none; position: fixed; inset: 72px 0 0 0; background: #FFFFFF; z-index: 190; padding: 24px; overflow-y: auto; }}
    .mobile-nav.open {{ display: block; }}
    .mobile-nav-group {{ margin-bottom: 28px; }}
    .mobile-nav-group h5 {{ font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #E8856A; margin-bottom: 12px; }}
    .mobile-nav-group a {{ display: flex; align-items: center; gap: 12px; padding: 11px 14px; border-radius: 12px; font-size: 0.95rem; font-weight: 500; color: #444; transition: background 0.15s; }}
    .mobile-nav-group a:hover {{ background: #FDFBF7; }}

    /* Breadcrumb */
    .breadcrumb {{ padding: 18px 0 0; }}
    .breadcrumb-list {{ display: flex; align-items: center; gap: 8px; font-size: 0.83rem; color: #aaa; list-style: none; flex-wrap: wrap; }}
    .breadcrumb-list a {{ color: #E8856A; }}
    .breadcrumb-list li:not(:last-child)::after {{ content: "›"; margin-left: 8px; }}

    /* Article hero */
    .article-hero {{ padding: 32px 0 48px; background: #FDFBF7; }}
    .article-meta-badges {{ display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 20px; }}
    .badge {{
      display: inline-flex; align-items: center; gap: 6px;
      background: #FFFFFF; border: 1px solid #F0ECE7; border-radius: 36px;
      padding: 5px 14px; font-size: 0.78rem; font-weight: 600;
      font-family: 'Nunito', sans-serif; color: #666;
    }}
    .badge-category {{ background: #FEF0EC; border-color: #FECDC5; color: #C0503A; }}
    .article-hero h1 {{ font-size: clamp(1.8rem, 3.5vw, 2.8rem); font-weight: 900; color: #333; margin-bottom: 18px; line-height: 1.15; }}
    .article-pub-date {{ font-size: 0.82rem; color: #bbb; }}

    /* Article layout */
    .article-layout {{ max-width: 780px; margin: 0 auto; padding: 48px 24px 80px; }}
    .article-layout h2 {{ font-size: 1.45rem; font-weight: 800; color: #333; margin: 44px 0 16px; }}
    .article-layout h3 {{ font-size: 1.15rem; font-weight: 700; color: #333; margin: 28px 0 10px; }}
    .article-layout p {{ margin-bottom: 18px; font-size: 1rem; line-height: 1.75; color: #444; }}
    .article-layout ul, .article-layout ol {{ padding-left: 24px; margin-bottom: 18px; }}
    .article-layout li {{ margin-bottom: 8px; font-size: 1rem; line-height: 1.65; color: #444; }}
    .article-layout strong {{ font-weight: 700; color: #333; }}
    .article-layout a {{ color: #E8856A; text-decoration: underline; text-underline-offset: 2px; }}
    .article-layout a:hover {{ color: #C0503A; }}

    /* Images */
    .article-main-img {{ margin: 0 0 32px; border-radius: 18px; overflow: hidden; }}
    .article-main-img img {{ width: 100%; object-fit: cover; }}
    .article-step-img {{ margin: 16px 0 24px; border-radius: 14px; overflow: hidden; }}
    .article-step-img img {{ width: 100%; object-fit: cover; }}
    .img-placeholder {{
      border-radius: 18px; background: linear-gradient(135deg, #FECDC5, #FFD8B0);
      display: flex; align-items: center; justify-content: center;
      font-size: 3rem; color: #E8856A;
    }}
    .img-placeholder--main {{ height: 380px; margin-bottom: 32px; }}
    .img-placeholder--step {{ height: 220px; margin: 16px 0 24px; border-radius: 14px; font-size: 2rem; }}

    /* Newsletter */
    .newsletter {{ padding: 72px 0; background: linear-gradient(150deg, #FDFBF7 0%, #FEF0EC 100%); }}
    .newsletter-inner {{ text-align: center; max-width: 540px; margin: 0 auto; }}
    .newsletter-emoji {{ font-size: 2.8rem; margin-bottom: 18px; }}
    .newsletter h2 {{ font-size: clamp(1.8rem, 3vw, 2.3rem); font-weight: 900; color: #333; margin-bottom: 14px; }}
    .newsletter-lead {{ font-size: 1rem; color: #888; line-height: 1.75; margin-bottom: 38px; }}
    .newsletter-form {{ display: flex; gap: 10px; max-width: 460px; margin: 0 auto 16px; }}
    .newsletter-form input {{ flex: 1; min-width: 0; padding: 13px 20px; border: 2px solid #EDE8E3; border-radius: 36px; font-family: 'DM Sans', sans-serif; font-size: 0.95rem; color: #333; background: #FFFFFF; outline: none; transition: border-color 0.2s; }}
    .newsletter-form input:focus {{ border-color: #E8856A; }}
    .newsletter-note {{ font-size: 0.8rem; color: #c5bfba; }}

    /* Footer */
    .footer {{ background: #2E2B28; color: #FFFFFF; padding: 64px 0 32px; }}
    .footer-top {{ display: grid; grid-template-columns: 1.6fr 1fr 1fr; gap: 56px; margin-bottom: 56px; }}
    .footer-brand-name {{ font-family: 'Nunito', sans-serif; font-weight: 900; font-size: 1.25rem; color: #FFFFFF; margin-bottom: 14px; display: flex; align-items: center; gap: 10px; }}
    .footer-brand-name .dot {{ width: 8px; height: 8px; background: #E8856A; border-radius: 50%; flex-shrink: 0; }}
    .footer-tagline {{ font-size: 0.9rem; color: rgba(255,255,255,0.45); line-height: 1.7; max-width: 260px; }}
    .footer-col-title {{ font-family: 'Nunito', sans-serif; font-weight: 800; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.8px; color: rgba(255,255,255,0.7); margin-bottom: 18px; }}
    .footer-links {{ list-style: none; }}
    .footer-links li {{ margin-bottom: 10px; }}
    .footer-links a {{ font-size: 0.9rem; color: rgba(255,255,255,0.4); transition: color 0.2s; }}
    .footer-links a:hover {{ color: #FECDC5; }}
    .footer-bottom {{ border-top: 1px solid rgba(255,255,255,0.08); padding-top: 26px; display: flex; justify-content: space-between; align-items: center; gap: 16px; flex-wrap: wrap; }}
    .footer-copy {{ font-size: 0.82rem; color: rgba(255,255,255,0.3); }}
    .social-row {{ display: flex; gap: 10px; }}
    .social-btn {{ width: 38px; height: 38px; background: rgba(255,255,255,0.07); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.95rem; color: rgba(255,255,255,0.5); transition: background 0.2s, color 0.2s, transform 0.15s; }}
    .social-btn:hover {{ background: #E8856A; color: #FFFFFF; transform: translateY(-2px); }}
    .section-label {{ font-family: 'Nunito', sans-serif; font-weight: 700; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 1.2px; color: #E8856A; margin-bottom: 10px; }}

    /* Responsive */
    @media (max-width: 960px) {{
      .footer-top {{ grid-template-columns: 1fr 1fr; gap: 36px; }}
      .footer-brand-col {{ grid-column: 1 / -1; }}
    }}
    @media (max-width: 640px) {{
      .nav {{ display: none; }}
      .hamburger {{ display: flex; }}
      .newsletter-form {{ flex-direction: column; }}
      .newsletter-form input, .newsletter-form .btn {{ width: 100%; }}
      .footer-top {{ grid-template-columns: 1fr; gap: 28px; }}
      .footer-bottom {{ flex-direction: column; align-items: flex-start; }}
    }}
  </style>
</head>
<body>

  <header class="header">
    <div class="container">
      <div class="header-inner">
        <a href="/" class="logo" aria-label="Craft with Mommy — Home">
          <img src="../brand_assets/Craft with mommy logo.png" alt="Craft with Mommy">
        </a>
        <nav class="nav" aria-label="Main navigation">
          <div class="nav-item">
            <button class="nav-trigger" aria-haspopup="true" aria-expanded="false">
              Activities
              <svg width="13" height="13" viewBox="0 0 13 13" fill="none" aria-hidden="true">
                <path d="M2.5 4.5L6.5 8.5L10.5 4.5" stroke="#666" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
            <div class="dropdown" role="menu">
              <a href="/" role="menuitem"><span class="drop-icon">🎨</span> Painting</a>
              <a href="/" role="menuitem"><span class="drop-icon">✂️</span> Paper Crafts</a>
              <a href="/" role="menuitem"><span class="drop-icon">🧵</span> Yarn &amp; Weaving</a>
              <a href="/" role="menuitem"><span class="drop-icon">♻️</span> Recycled Crafts</a>
              <a href="/" role="menuitem"><span class="drop-icon">🌈</span> Sensory Play</a>
            </div>
          </div>
          <div class="nav-item">
            <button class="nav-trigger" aria-haspopup="true" aria-expanded="false">
              Seasons
              <svg width="13" height="13" viewBox="0 0 13 13" fill="none" aria-hidden="true">
                <path d="M2.5 4.5L6.5 8.5L10.5 4.5" stroke="#666" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
            <div class="dropdown" role="menu">
              <a href="/" role="menuitem"><span class="drop-icon">🌸</span> Spring</a>
              <a href="/" role="menuitem"><span class="drop-icon">☀️</span> Summer</a>
              <a href="/" role="menuitem"><span class="drop-icon">🍂</span> Fall</a>
              <a href="/" role="menuitem"><span class="drop-icon">❄️</span> Winter</a>
            </div>
          </div>
          <a href="/blog/" class="btn btn-sm" style="margin-left:8px;">All Crafts</a>
        </nav>
        <button class="hamburger" id="menuBtn" aria-label="Open menu" aria-expanded="false">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </header>

  <div class="mobile-nav" id="mobileNav" aria-hidden="true">
    <div class="mobile-nav-group">
      <h5>Activities</h5>
      <a href="/"><span class="drop-icon">🎨</span> Painting</a>
      <a href="/"><span class="drop-icon">✂️</span> Paper Crafts</a>
      <a href="/"><span class="drop-icon">🧵</span> Yarn &amp; Weaving</a>
      <a href="/"><span class="drop-icon">♻️</span> Recycled Crafts</a>
      <a href="/"><span class="drop-icon">🌈</span> Sensory Play</a>
    </div>
    <div class="mobile-nav-group">
      <h5>Seasons</h5>
      <a href="/"><span class="drop-icon">🌸</span> Spring</a>
      <a href="/"><span class="drop-icon">☀️</span> Summer</a>
      <a href="/"><span class="drop-icon">🍂</span> Fall</a>
      <a href="/"><span class="drop-icon">❄️</span> Winter</a>
    </div>
  </div>

  <!-- Breadcrumb -->
  <div class="breadcrumb">
    <div class="container">
      <ol class="breadcrumb-list" itemscope itemtype="https://schema.org/BreadcrumbList">
        <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
          <a href="/" itemprop="item"><span itemprop="name">Home</span></a>
          <meta itemprop="position" content="1">
        </li>
        <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
          <a href="/blog/" itemprop="item"><span itemprop="name">Blog</span></a>
          <meta itemprop="position" content="2">
        </li>
        <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
          <span itemprop="name">{title}</span>
          <meta itemprop="position" content="3">
        </li>
      </ol>
    </div>
  </div>

  <!-- Article Hero -->
  <section class="article-hero">
    <div class="container">
      <div class="article-meta-badges">
        <span class="badge badge-category">{category_emoji} {category}</span>
        <span class="badge">👶 {age_range}</span>
        <span class="badge">⏱ {time_min} min</span>
        <span class="badge">{messiness_emoji} Messiness: {messiness}</span>
      </div>
      <h1>{title}</h1>
      <p class="article-pub-date">Published on {pub_date}</p>
    </div>
  </section>

  <!-- Article Content -->
  <main>
    <article class="article-layout" itemscope itemtype="https://schema.org/Article">
      {article_html}
    </article>
  </main>

  <!-- Newsletter -->
  <section class="newsletter">
    <div class="container">
      <div class="newsletter-inner">
        <div class="newsletter-emoji">💌</div>
        <h2>Be the first to create!</h2>
        <p class="newsletter-lead">
          Get fresh foolproof craft ideas delivered to your inbox every week. Simple, cute, and guaranteed to bring smiles — zero chaos included.
        </p>
        <form class="newsletter-form" onsubmit="return false;" aria-label="Newsletter signup">
          <input type="email" placeholder="Your email address" autocomplete="email" aria-label="Email address" required>
          <button type="submit" class="btn">Join us!</button>
        </form>
        <p class="newsletter-note">No spam, ever. Just crafts and happy moments. 🎨</p>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer class="footer">
    <div class="container">
      <div class="footer-top">
        <div class="footer-brand-col">
          <div class="footer-brand-name"><span class="dot"></span> Craft with Mommy</div>
          <p class="footer-tagline">Simple, foolproof crafts for moms and little ones. Creating memories, one project at a time.</p>
        </div>
        <div>
          <div class="footer-col-title">Activities</div>
          <ul class="footer-links">
            <li><a href="/">Painting</a></li>
            <li><a href="/">Paper Crafts</a></li>
            <li><a href="/">Yarn &amp; Weaving</a></li>
            <li><a href="/">Recycled Crafts</a></li>
            <li><a href="/">Sensory Play</a></li>
          </ul>
        </div>
        <div>
          <div class="footer-col-title">Seasons</div>
          <ul class="footer-links">
            <li><a href="/">🌸 Spring</a></li>
            <li><a href="/">☀️ Summer</a></li>
            <li><a href="/">🍂 Fall</a></li>
            <li><a href="/">❄️ Winter</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span class="footer-copy">© 2026 Craft with Mommy. Made with ❤️ for moms &amp; kids.</span>
        <div class="social-row">
          <a href="#" class="social-btn" aria-label="Pinterest">📌</a>
          <a href="#" class="social-btn" aria-label="Instagram">📷</a>
          <a href="#" class="social-btn" aria-label="Facebook">👍</a>
        </div>
      </div>
    </div>
  </footer>

  <script>
    (function () {{
      const btn = document.getElementById('menuBtn');
      const nav = document.getElementById('mobileNav');
      btn.addEventListener('click', function () {{
        const isOpen = nav.classList.toggle('open');
        btn.classList.toggle('open', isOpen);
        btn.setAttribute('aria-expanded', isOpen);
        nav.setAttribute('aria-hidden', !isOpen);
        document.body.style.overflow = isOpen ? 'hidden' : '';
      }});
      nav.querySelectorAll('a').forEach(function (link) {{
        link.addEventListener('click', function () {{
          nav.classList.remove('open');
          btn.classList.remove('open');
          btn.setAttribute('aria-expanded', 'false');
          nav.setAttribute('aria-hidden', 'true');
          document.body.style.overflow = '';
        }});
      }});
      window.addEventListener('resize', function () {{
        if (window.innerWidth > 640) {{
          nav.classList.remove('open');
          btn.classList.remove('open');
          btn.setAttribute('aria-expanded', 'false');
          nav.setAttribute('aria-hidden', 'true');
          document.body.style.overflow = '';
        }}
      }});
    }})();
  </script>

</body>
</html>"""


# ---------------------------------------------------------------------------
# Step 7 — Save article file
# ---------------------------------------------------------------------------

def save_article(slug: str, page_html: str) -> Path:
    BLOG_DIR.mkdir(exist_ok=True)
    path = BLOG_DIR / f"{slug}.html"
    path.write_text(page_html, encoding="utf-8")
    log.info(f"Article saved: {path}")
    return path


# ---------------------------------------------------------------------------
# Step 8 — Update blog/index.html
# ---------------------------------------------------------------------------

BLOG_INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>All Craft Ideas — Craft with Mommy</title>
  <meta name="description" content="Browse all our simple, foolproof craft ideas for moms and kids. New articles published daily!">
  <link rel="canonical" href="https://craft-with-mommy.com/blog/">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,400&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body { font-family: 'DM Sans', sans-serif; color: #333; background: #fff; line-height: 1.65; -webkit-font-smoothing: antialiased; }
    h1, h2, h3, h4, h5 { font-family: 'Nunito', sans-serif; line-height: 1.2; }
    a { text-decoration: none; color: inherit; }
    img { max-width: 100%; display: block; }
    .container { max-width: 1140px; margin: 0 auto; padding: 0 24px; }
    .btn { display: inline-block; background: #E8856A; color: #fff; font-family: 'Nunito', sans-serif; font-weight: 700; font-size: 1rem; padding: 13px 30px; border-radius: 36px; border: 2px solid transparent; cursor: pointer; transition: background 0.2s, transform 0.15s; white-space: nowrap; }
    .btn:hover { background: #D4755C; transform: translateY(-2px); }
    .btn-sm { font-size: 0.88rem; padding: 10px 22px; }
    .header { position: sticky; top: 0; z-index: 200; background: rgba(255,255,255,0.96); backdrop-filter: blur(12px); border-bottom: 1px solid #F0ECE7; }
    .header-inner { height: 72px; display: flex; align-items: center; justify-content: space-between; gap: 24px; }
    .logo { display: flex; align-items: center; flex-shrink: 0; }
    .logo img { height: 54px; width: auto; }
    .nav { display: flex; align-items: center; gap: 4px; }
    .nav-item { position: relative; }
    .nav-trigger { font-family: 'Nunito', sans-serif; font-weight: 700; font-size: 0.95rem; color: #444; padding: 9px 16px; border-radius: 10px; cursor: pointer; display: flex; align-items: center; gap: 6px; transition: background 0.15s, color 0.15s; background: none; border: none; }
    .nav-trigger:hover { background: #FDFBF7; color: #E8856A; }
    .nav-trigger svg { transition: transform 0.25s; flex-shrink: 0; }
    .nav-item:hover .nav-trigger svg { transform: rotate(180deg); }
    .dropdown { position: absolute; top: calc(100% + 10px); left: 0; background: #fff; border: 1px solid #F0ECE7; border-radius: 18px; padding: 8px; min-width: 210px; box-shadow: 0 12px 40px rgba(0,0,0,0.09); opacity: 0; visibility: hidden; transform: translateY(-6px); transition: opacity 0.2s, transform 0.2s, visibility 0.2s; pointer-events: none; }
    .nav-item:hover .dropdown, .nav-item:focus-within .dropdown { opacity: 1; visibility: visible; transform: translateY(0); pointer-events: auto; }
    .dropdown a { display: flex; align-items: center; gap: 11px; padding: 10px 13px; border-radius: 11px; font-size: 0.91rem; font-weight: 500; color: #555; transition: background 0.15s, color 0.15s; }
    .dropdown a:hover { background: #FEF0EC; color: #E8856A; }
    .drop-icon { font-size: 1.05rem; line-height: 1; }
    .hamburger { display: none; flex-direction: column; justify-content: center; gap: 5px; padding: 8px; cursor: pointer; background: none; border: none; }
    .hamburger span { display: block; width: 22px; height: 2px; background: #444; border-radius: 2px; transition: transform 0.25s, opacity 0.25s; }
    .hamburger.open span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
    .hamburger.open span:nth-child(2) { opacity: 0; }
    .hamburger.open span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }
    .mobile-nav { display: none; position: fixed; inset: 72px 0 0 0; background: #fff; z-index: 190; padding: 24px; overflow-y: auto; }
    .mobile-nav.open { display: block; }
    .mobile-nav-group { margin-bottom: 28px; }
    .mobile-nav-group h5 { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #E8856A; margin-bottom: 12px; }
    .mobile-nav-group a { display: flex; align-items: center; gap: 12px; padding: 11px 14px; border-radius: 12px; font-size: 0.95rem; font-weight: 500; color: #444; transition: background 0.15s; }
    .mobile-nav-group a:hover { background: #FDFBF7; }
    .blog-hero { background: #FDFBF7; padding: 72px 0 56px; }
    .section-label { font-family: 'Nunito', sans-serif; font-weight: 700; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 1.2px; color: #E8856A; margin-bottom: 10px; }
    .blog-hero h1 { font-size: clamp(2rem, 4vw, 3rem); font-weight: 900; color: #333; margin-bottom: 14px; }
    .blog-hero p { font-size: 1rem; color: #888; max-width: 520px; }
    .blog-grid-section { padding: 64px 0 96px; }
    .blog-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px; }
    .blog-card { border-radius: 20px; overflow: hidden; background: #fff; border: 1px solid #F0ECE7; transition: transform 0.2s, box-shadow 0.2s; }
    .blog-card:hover { transform: translateY(-5px); box-shadow: 0 18px 48px rgba(0,0,0,0.08); }
    .blog-card-thumb { height: 195px; overflow: hidden; position: relative; background: linear-gradient(135deg, #FECDC5, #FFD8B0); display: flex; align-items: center; justify-content: center; font-size: 4rem; }
    .blog-card-thumb img { width: 100%; height: 100%; object-fit: cover; }
    .blog-card-body { padding: 20px; }
    .blog-card-tag { font-family: 'Nunito', sans-serif; font-size: 0.73rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: #E8856A; margin-bottom: 8px; }
    .blog-card-title { font-family: 'Nunito', sans-serif; font-size: 1rem; font-weight: 800; color: #333; line-height: 1.4; margin-bottom: 12px; }
    .blog-card-meta { display: flex; gap: 14px; font-size: 0.78rem; color: #bbb; }
    .newsletter { padding: 88px 0; background: linear-gradient(150deg, #FDFBF7 0%, #FEF0EC 100%); }
    .newsletter-inner { text-align: center; max-width: 540px; margin: 0 auto; }
    .newsletter-emoji { font-size: 2.8rem; margin-bottom: 18px; }
    .newsletter h2 { font-size: clamp(1.8rem, 3vw, 2.3rem); font-weight: 900; color: #333; margin-bottom: 14px; }
    .newsletter-lead { font-size: 1rem; color: #888; line-height: 1.75; margin-bottom: 38px; }
    .newsletter-form { display: flex; gap: 10px; max-width: 460px; margin: 0 auto 16px; }
    .newsletter-form input { flex: 1; min-width: 0; padding: 13px 20px; border: 2px solid #EDE8E3; border-radius: 36px; font-family: 'DM Sans', sans-serif; font-size: 0.95rem; color: #333; background: #fff; outline: none; transition: border-color 0.2s; }
    .newsletter-form input:focus { border-color: #E8856A; }
    .newsletter-note { font-size: 0.8rem; color: #c5bfba; }
    .footer { background: #2E2B28; color: #fff; padding: 64px 0 32px; }
    .footer-top { display: grid; grid-template-columns: 1.6fr 1fr 1fr; gap: 56px; margin-bottom: 56px; }
    .footer-brand-name { font-family: 'Nunito', sans-serif; font-weight: 900; font-size: 1.25rem; color: #fff; margin-bottom: 14px; display: flex; align-items: center; gap: 10px; }
    .footer-brand-name .dot { width: 8px; height: 8px; background: #E8856A; border-radius: 50%; flex-shrink: 0; }
    .footer-tagline { font-size: 0.9rem; color: rgba(255,255,255,0.45); line-height: 1.7; max-width: 260px; }
    .footer-col-title { font-family: 'Nunito', sans-serif; font-weight: 800; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.8px; color: rgba(255,255,255,0.7); margin-bottom: 18px; }
    .footer-links { list-style: none; }
    .footer-links li { margin-bottom: 10px; }
    .footer-links a { font-size: 0.9rem; color: rgba(255,255,255,0.4); transition: color 0.2s; }
    .footer-links a:hover { color: #FECDC5; }
    .footer-bottom { border-top: 1px solid rgba(255,255,255,0.08); padding-top: 26px; display: flex; justify-content: space-between; align-items: center; gap: 16px; flex-wrap: wrap; }
    .footer-copy { font-size: 0.82rem; color: rgba(255,255,255,0.3); }
    .social-row { display: flex; gap: 10px; }
    .social-btn { width: 38px; height: 38px; background: rgba(255,255,255,0.07); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.95rem; color: rgba(255,255,255,0.5); transition: background 0.2s, color 0.2s, transform 0.15s; }
    .social-btn:hover { background: #E8856A; color: #fff; transform: translateY(-2px); }
    @media (max-width: 960px) {
      .blog-grid { grid-template-columns: 1fr 1fr; }
      .footer-top { grid-template-columns: 1fr 1fr; gap: 36px; }
      .footer-brand-col { grid-column: 1 / -1; }
    }
    @media (max-width: 640px) {
      .nav { display: none; }
      .hamburger { display: flex; }
      .blog-grid { grid-template-columns: 1fr; }
      .newsletter-form { flex-direction: column; }
      .newsletter-form input, .newsletter-form .btn { width: 100%; }
      .footer-top { grid-template-columns: 1fr; gap: 28px; }
      .footer-bottom { flex-direction: column; align-items: flex-start; }
    }
  </style>
</head>
<body>

  <header class="header">
    <div class="container">
      <div class="header-inner">
        <a href="/" class="logo" aria-label="Craft with Mommy — Home">
          <img src="../brand_assets/Craft with mommy logo.png" alt="Craft with Mommy">
        </a>
        <nav class="nav" aria-label="Main navigation">
          <div class="nav-item">
            <button class="nav-trigger" aria-haspopup="true" aria-expanded="false">
              Activities
              <svg width="13" height="13" viewBox="0 0 13 13" fill="none" aria-hidden="true">
                <path d="M2.5 4.5L6.5 8.5L10.5 4.5" stroke="#666" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
            <div class="dropdown" role="menu">
              <a href="/" role="menuitem"><span class="drop-icon">🎨</span> Painting</a>
              <a href="/" role="menuitem"><span class="drop-icon">✂️</span> Paper Crafts</a>
              <a href="/" role="menuitem"><span class="drop-icon">🧵</span> Yarn &amp; Weaving</a>
              <a href="/" role="menuitem"><span class="drop-icon">♻️</span> Recycled Crafts</a>
              <a href="/" role="menuitem"><span class="drop-icon">🌈</span> Sensory Play</a>
            </div>
          </div>
          <div class="nav-item">
            <button class="nav-trigger" aria-haspopup="true" aria-expanded="false">
              Seasons
              <svg width="13" height="13" viewBox="0 0 13 13" fill="none" aria-hidden="true">
                <path d="M2.5 4.5L6.5 8.5L10.5 4.5" stroke="#666" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
            <div class="dropdown" role="menu">
              <a href="/" role="menuitem"><span class="drop-icon">🌸</span> Spring</a>
              <a href="/" role="menuitem"><span class="drop-icon">☀️</span> Summer</a>
              <a href="/" role="menuitem"><span class="drop-icon">🍂</span> Fall</a>
              <a href="/" role="menuitem"><span class="drop-icon">❄️</span> Winter</a>
            </div>
          </div>
          <a href="/blog/" class="btn btn-sm" style="margin-left:8px;">All Crafts</a>
        </nav>
        <button class="hamburger" id="menuBtn" aria-label="Open menu" aria-expanded="false">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </header>

  <div class="mobile-nav" id="mobileNav" aria-hidden="true">
    <div class="mobile-nav-group">
      <h5>Activities</h5>
      <a href="/"><span class="drop-icon">🎨</span> Painting</a>
      <a href="/"><span class="drop-icon">✂️</span> Paper Crafts</a>
      <a href="/"><span class="drop-icon">🧵</span> Yarn &amp; Weaving</a>
      <a href="/"><span class="drop-icon">♻️</span> Recycled Crafts</a>
      <a href="/"><span class="drop-icon">🌈</span> Sensory Play</a>
    </div>
    <div class="mobile-nav-group">
      <h5>Seasons</h5>
      <a href="/"><span class="drop-icon">🌸</span> Spring</a>
      <a href="/"><span class="drop-icon">☀️</span> Summer</a>
      <a href="/"><span class="drop-icon">🍂</span> Fall</a>
      <a href="/"><span class="drop-icon">❄️</span> Winter</a>
    </div>
  </div>

  <section class="blog-hero">
    <div class="container">
      <div class="section-label">All craft ideas</div>
      <h1>Craft with Mommy — All Articles</h1>
      <p>Simple, foolproof craft ideas for moms and little ones. New ideas published every day!</p>
    </div>
  </section>

  <section class="blog-grid-section">
    <div class="container">
      <div class="blog-grid">
        <!-- ARTICLE_CARDS_START -->
        <!-- ARTICLE_CARDS_END -->
      </div>
    </div>
  </section>

  <section class="newsletter">
    <div class="container">
      <div class="newsletter-inner">
        <div class="newsletter-emoji">💌</div>
        <h2>Be the first to create!</h2>
        <p class="newsletter-lead">Get fresh foolproof craft ideas delivered to your inbox every week. Simple, cute, and guaranteed to bring smiles — zero chaos included.</p>
        <form class="newsletter-form" onsubmit="return false;" aria-label="Newsletter signup">
          <input type="email" placeholder="Your email address" autocomplete="email" aria-label="Email address" required>
          <button type="submit" class="btn">Join us!</button>
        </form>
        <p class="newsletter-note">No spam, ever. Just crafts and happy moments. 🎨</p>
      </div>
    </div>
  </section>

  <footer class="footer">
    <div class="container">
      <div class="footer-top">
        <div class="footer-brand-col">
          <div class="footer-brand-name"><span class="dot"></span> Craft with Mommy</div>
          <p class="footer-tagline">Simple, foolproof crafts for moms and little ones. Creating memories, one project at a time.</p>
        </div>
        <div>
          <div class="footer-col-title">Activities</div>
          <ul class="footer-links">
            <li><a href="/">Painting</a></li>
            <li><a href="/">Paper Crafts</a></li>
            <li><a href="/">Yarn &amp; Weaving</a></li>
            <li><a href="/">Recycled Crafts</a></li>
            <li><a href="/">Sensory Play</a></li>
          </ul>
        </div>
        <div>
          <div class="footer-col-title">Seasons</div>
          <ul class="footer-links">
            <li><a href="/">🌸 Spring</a></li>
            <li><a href="/">☀️ Summer</a></li>
            <li><a href="/">🍂 Fall</a></li>
            <li><a href="/">❄️ Winter</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span class="footer-copy">© 2026 Craft with Mommy. Made with ❤️ for moms &amp; kids.</span>
        <div class="social-row">
          <a href="#" class="social-btn" aria-label="Pinterest">📌</a>
          <a href="#" class="social-btn" aria-label="Instagram">📷</a>
          <a href="#" class="social-btn" aria-label="Facebook">👍</a>
        </div>
      </div>
    </div>
  </footer>

  <script>
    (function () {
      const btn = document.getElementById('menuBtn');
      const nav = document.getElementById('mobileNav');
      btn.addEventListener('click', function () {
        const isOpen = nav.classList.toggle('open');
        btn.classList.toggle('open', isOpen);
        btn.setAttribute('aria-expanded', isOpen);
        nav.setAttribute('aria-hidden', !isOpen);
        document.body.style.overflow = isOpen ? 'hidden' : '';
      });
      nav.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', function () {
          nav.classList.remove('open');
          btn.classList.remove('open');
          btn.setAttribute('aria-expanded', 'false');
          nav.setAttribute('aria-hidden', 'true');
          document.body.style.overflow = '';
        });
      });
      window.addEventListener('resize', function () {
        if (window.innerWidth > 640) {
          nav.classList.remove('open');
          btn.classList.remove('open');
          btn.setAttribute('aria-expanded', 'false');
          nav.setAttribute('aria-hidden', 'true');
          document.body.style.overflow = '';
        }
      });
    })();
  </script>

</body>
</html>"""


def _build_blog_card(metadata: dict) -> str:
    slug = metadata["slug"]
    title = metadata["title"]
    category = metadata["category"]
    age_range = metadata["age_range"]
    time_min = metadata["time_minutes"]
    pub_date = metadata["pub_date"]
    has_img = metadata.get("has_main_image", False)

    category_emoji = {
        "Painting": "🎨",
        "Paper Crafts": "✂️",
        "Yarn & Weaving": "🧵",
        "Recycled Crafts": "♻️",
        "Sensory Play": "🌈",
    }.get(category, "🎨")

    main_filename = metadata.get("main_image_filename") or "main.webp"
    thumb_html = ""
    if has_img:
        thumb_html = (
            f'<img src="../blog/images/{slug}/{main_filename}" '
            f'alt="{title}" loading="lazy">'
        )
    else:
        thumb_html = category_emoji

    return f"""        <article class="blog-card">
          <a href="/blog/{slug}.html">
            <div class="blog-card-thumb">
              {thumb_html}
            </div>
            <div class="blog-card-body">
              <div class="blog-card-tag">{category} · {age_range}</div>
              <h3 class="blog-card-title">{title}</h3>
              <div class="blog-card-meta">
                <span>⏱ {time_min} min</span>
                <span>📅 {pub_date}</span>
              </div>
            </div>
          </a>
        </article>"""


def update_blog_index(metadata: dict) -> None:
    if not BLOG_INDEX_FILE.exists():
        BLOG_INDEX_FILE.write_text(BLOG_INDEX_TEMPLATE, encoding="utf-8")
        log.info("Created blog/index.html from template")

    content = BLOG_INDEX_FILE.read_text(encoding="utf-8")
    new_card = _build_blog_card(metadata)
    # Insert new card right after the marker
    content = content.replace(
        "        <!-- ARTICLE_CARDS_START -->",
        f"        <!-- ARTICLE_CARDS_START -->\n{new_card}",
    )
    BLOG_INDEX_FILE.write_text(content, encoding="utf-8")
    log.info(f"blog/index.html updated with card for {metadata['slug']}")


# ---------------------------------------------------------------------------
# Step 9 — Update homepage "Latest Crafts" section
# ---------------------------------------------------------------------------

def update_homepage_latest_crafts(recent_articles: list) -> None:
    content = HOME_INDEX_FILE.read_text(encoding="utf-8")

    cards_html = ""
    for art in recent_articles[:3]:
        slug = art["slug"]
        title = art["title"]
        category = art["category"]
        age_range = art["age_range"]
        time_min = art["time_minutes"]
        has_img = art.get("has_main_image", False)

        if has_img:
            main_filename = art.get("main_image_filename") or "main.webp"
            thumb_inner = (
                f'<img src="blog/images/{slug}/{main_filename}" '
                f'alt="{title}" style="width:100%;height:100%;object-fit:cover;" loading="lazy">'
            )
        else:
            category_emoji = {
                "Painting": "🎨",
                "Paper Crafts": "✂️",
                "Yarn & Weaving": "🧵",
                "Recycled Crafts": "♻️",
                "Sensory Play": "🌈",
            }.get(category, "🎨")
            thumb_inner = category_emoji

        cards_html += f"""
        <article class="craft-card">
          <a href="blog/{slug}.html" style="display:block;color:inherit;">
            <div class="craft-thumb" style="background: linear-gradient(135deg, #FECDC5, #FFB8A0);">
              {thumb_inner}
            </div>
            <div class="craft-body">
              <div class="craft-tag">{category} · {age_range}</div>
              <h3 class="craft-title">{title}</h3>
              <div class="craft-meta">
                <span>⏱ {time_min} min</span>
                <span>⭐ Beginner</span>
              </div>
            </div>
          </a>
        </article>"""

    new_section = f"""<!-- =============================================
       LATEST CRAFTS
  ============================================= -->
  <section class="crafts" id="crafts">
    <div class="container">

      <div class="crafts-header">
        <div>
          <div class="section-label">Fresh from the craft table</div>
          <h2 class="section-title">Latest crafts</h2>
        </div>
        <a href="blog/" class="btn btn-outline btn-sm">View all crafts</a>
      </div>

      <div class="crafts-grid">
        {cards_html}
      </div>
    </div>
  </section>"""

    pattern = r'<!-- =+\s*LATEST CRAFTS.*?</section>'
    new_content = re.sub(pattern, new_section, content, flags=re.DOTALL | re.IGNORECASE)

    if new_content == content:
        log.warning("Could not find LATEST CRAFTS section to replace in index.html")
    else:
        HOME_INDEX_FILE.write_text(new_content, encoding="utf-8")
        log.info("index.html Latest Crafts section updated")


# ---------------------------------------------------------------------------
# Step 10 — Git commit & push
# ---------------------------------------------------------------------------

def git_commit_and_push(slug: str, pub_date: str) -> None:
    def run(cmd):
        result = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Command {cmd} failed:\n{result.stderr}")
        return result.stdout

    run(["git", "add",
         f"blog/{slug}.html",
         f"blog/images/{slug}/",
         "blog/index.html",
         "blog/",
         "index.html",
         "tools/published_keywords.json"])
    run(["git", "commit", "-m", f"blog: publish '{slug}' — {pub_date}"])
    run(["git", "push", "origin", "main"])
    log.info(f"Git commit & push done for {slug}")


# ---------------------------------------------------------------------------
# Step 3b — Resolve Amazon affiliate link placeholders
# ---------------------------------------------------------------------------

_AMAZON_LINK_RE = re.compile(
    r'<a\b([^>]*?)href="\[AMAZON_LINK_([a-z_]+)\]"([^>]*?)>(.*?)</a>',
    re.IGNORECASE | re.DOTALL,
)

_CRAFT_WORDS = {
    "paint", "brush", "glue", "scissors", "paper", "foam", "felt", "yarn",
    "craft", "art", "marker", "crayon", "sticker", "ribbon", "tape", "stamp",
}


def _placeholder_key_to_query(key: str) -> str:
    """Convert a snake_case placeholder key to an Amazon search query."""
    words = key.replace("_", " ")
    if any(w in words.split() for w in _CRAFT_WORDS):
        return f"{words} kids"
    return f"{words} kids craft"


def search_amazon_product(query: str, amazon_api, associate_tag: str) -> dict | None:
    """Search Amazon PA API for a product matching query.

    Returns {"asin": ..., "url": ..., "title": ...} or None.
    Never raises — all errors are caught and logged as warnings.
    """
    try:
        results = amazon_api.search_items(
            keywords=query,
            search_index="Toys",
            item_count=5,
        )
        if not results or not results.items_result or not results.items_result.items:
            log.warning(f"Amazon search: no results for '{query}'")
            return None

        for item in results.items_result.items:
            try:
                reviews = item.customer_reviews
                if reviews is None:
                    continue
                count = getattr(reviews, "count", 0) or 0
                rating = float(getattr(reviews, "star_rating", {}).display_value or 0)
                if count < 50 or rating < 4.0:
                    continue
                asin = item.asin
                url = f"https://www.amazon.com/dp/{asin}?tag={associate_tag}"
                title = (item.item_info.title.display_value
                         if item.item_info and item.item_info.title else query)
                log.info(f"Amazon product found: '{title}' (ASIN={asin}, {count} reviews, {rating}★)")
                return {"asin": asin, "url": url, "title": title}
            except Exception:
                continue

        log.warning(f"Amazon search: no product with ≥50 reviews & ≥4.0★ for '{query}'")
        return None
    except Exception as exc:
        log.warning(f"Amazon PA API call failed for '{query}': {exc}")
        return None


def resolve_amazon_links(article_html: str) -> str:
    """Replace [AMAZON_LINK_*] placeholders with real affiliate links.

    Fallback cascade (in priority order):
      1. Library not installed        → href="#"
      2. Credentials not configured   → Amazon search URL fallback
      3. Product found (≥50 rev, ≥4★) → Real dp/ affiliate link
      4. No qualifying product found  → Strip <a>, keep plain text
      5. API call fails               → Strip <a>, keep plain text
    """
    associate_tag = os.environ.get("AMAZON_ASSOCIATE_TAG", "").strip()
    access_key = os.environ.get("AMAZON_ACCESS_KEY", "").strip()
    secret_key = os.environ.get("AMAZON_SECRET_KEY", "").strip()

    if not _AMAZON_PAAPI_AVAILABLE:
        log.warning("python-amazon-paapi not installed — Amazon links set to '#'")

        def _noop_replace(m):
            pre, _key, post, text = m.group(1), m.group(2), m.group(3), m.group(4)
            return f'<a{pre}href="#"{post}>{text}</a>'

        return _AMAZON_LINK_RE.sub(_noop_replace, article_html)

    credentials_ok = bool(associate_tag and access_key and secret_key)
    if not credentials_ok:
        log.warning("Amazon credentials not configured — using search URL fallback")

    amazon_api = None
    if credentials_ok:
        try:
            amazon_api = AmazonApi(
                access_key, secret_key, associate_tag,
                country="US", throttling=0.5,
            )
        except Exception as exc:
            log.warning(f"Could not initialise AmazonApi: {exc}")
            amazon_api = None

    # Cache: one API call per unique slug
    cache: dict[str, dict | None] = {}

    def _replace(m: re.Match) -> str:
        pre, key, post, text = m.group(1), m.group(2), m.group(3), m.group(4)

        if not credentials_ok:
            query = _placeholder_key_to_query(key)
            safe_q = requests.utils.quote(query, safe="")
            search_url = f"https://www.amazon.com/s?k={safe_q}&tag={associate_tag or 'craftmommy-20'}"
            return f'<a{pre}href="{search_url}"{post}>{text}</a>'

        if key not in cache:
            query = _placeholder_key_to_query(key)
            cache[key] = search_amazon_product(query, amazon_api, associate_tag)

        product = cache[key]
        if product:
            return f'<a{pre}href="{product["url"]}"{post}>{text}</a>'
        # No qualifying product — strip <a>, keep plain text
        return text

    return _AMAZON_LINK_RE.sub(_replace, article_html)


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def main():
    load_env()
    log.info("=== generate_article.py starting ===")

    published = load_published_keywords()
    used_keywords = [r["keyword"] for r in published]

    # Step 1: Scrape
    titles = scrape_competitor_titles(COMPETITOR_SITES)
    log.info(f"Total titles collected: {len(titles)}")

    # Step 2: Select keyword
    try:
        keyword_data = select_keyword_and_variants(titles, used_keywords)
    except Exception as exc:
        log.error(f"Aborting: keyword selection failed — {exc}")
        sys.exit(1)

    slug = slugify(keyword_data["primary_keyword"])
    pub_date = datetime.today().strftime("%B %d, %Y")
    log.info(f"Slug: {slug} | Date: {pub_date}")

    # Step 3: Generate article (pass published articles for real internal links)
    try:
        article_html = generate_article_html(keyword_data, published_articles=published)
    except Exception as exc:
        log.error(f"Aborting: article generation failed — {exc}")
        sys.exit(1)

    # Step 3b: Resolve Amazon affiliate links
    article_html = resolve_amazon_links(article_html)

    # Step 4: Generate images (SEO filenames + landscape 4:3 + compression)
    image_paths = generate_images(
        slug, keyword_data["article_title"],
        keyword_data.get("step_descriptions", []),
        keyword_data["primary_keyword"],
    )
    main_img_info = image_paths.get("main", {})
    has_main_image = isinstance(main_img_info, dict) and main_img_info.get("path", "PLACEHOLDER") != "PLACEHOLDER"
    main_image_filename = main_img_info.get("filename", "") if isinstance(main_img_info, dict) else ""

    # Step 5: Resolve placeholders
    article_html = resolve_image_placeholders(article_html, image_paths, slug)

    # Step 6: Build full page
    page_html = build_article_page(slug, article_html, keyword_data, pub_date)

    # Step 7: Save article
    save_article(slug, page_html)

    # Build metadata for index updates
    metadata = {
        "slug": slug,
        "title": keyword_data["article_title"],
        "category": keyword_data["category"],
        "age_range": keyword_data["age_range"],
        "time_minutes": keyword_data["time_minutes"],
        "pub_date": pub_date,
        "has_main_image": has_main_image,
        "main_image_filename": main_image_filename,
    }

    # Step 8: Update blog index
    update_blog_index(metadata)

    # Step 9: Update homepage — gather last 3 published + this new one
    all_published = published + [{"keyword": keyword_data["primary_keyword"], "slug": slug, "date": pub_date}]
    recent_slugs = [r["slug"] for r in all_published[-3:]]

    # For recent articles metadata we just use what we have
    recent_articles_meta = []
    for r in all_published[-3:]:
        if r["slug"] == slug:
            recent_articles_meta.append(metadata)
        else:
            # Older articles: use stored info from published_keywords.json
            stored_img = r.get("main_image", "")
            recent_articles_meta.append({
                "slug": r["slug"],
                "title": r["slug"].replace("-", " ").title(),
                "category": "Paper Crafts",
                "age_range": "Ages 3+",
                "time_minutes": 15,
                "pub_date": r.get("date", ""),
                "has_main_image": bool(stored_img),
                "main_image_filename": stored_img or "main.webp",
            })

    # Re-order so newest first
    recent_articles_meta.reverse()
    update_homepage_latest_crafts(recent_articles_meta)

    # Step 10: Save keyword record (includes main image filename for future homepage rebuilds)
    save_keyword(keyword_data, slug, pub_date, main_image_filename)

    # Step 11: Git push
    try:
        git_commit_and_push(slug, pub_date)
    except Exception as exc:
        log.error(f"Git push failed (files saved locally): {exc}")
        sys.exit(1)

    log.info("=== Run complete ===")


if __name__ == "__main__":
    main()
