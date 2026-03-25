#!/usr/bin/env python3
"""
gen_paper_arts_crafts_images.py
Generate all 18 craft-specific images for the paper-arts-and-crafts roundup,
fix badge format to match halloween article style, and inject everything into HTML.

Usage:
    python3 /var/www/craft-with-mommy/tools/gen_paper_arts_crafts_images.py
"""

import io, os, re, sys, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-arts-and-crafts"
HTML_FILE = BASE_DIR / "blog" / "paper-arts-and-crafts.html"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. "
    "Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "The craft is clearly handmade by a child, charming and imperfect. Pinterest-worthy."
)

# ---------------------------------------------------------------------------
# One entry per idea that has a [ROUNDUP_IMAGE_PLACEHOLDER]
# ---------------------------------------------------------------------------
IMAGES = [
    {
        "idea_number": 1,
        "filename": "paper-plate-rainbow.webp",
        "alt": "Handmade paper plate rainbow craft with colorful paper strips glued in an arc on a white craft table",
        "prompt": (
            "A handmade paper plate rainbow craft on a white craft table. "
            "A standard white paper plate with colorful strips of construction paper "
            "(red, orange, yellow, green, blue, purple) glued in an arc across the plate. "
            "White cotton-ball clouds at each end. The plate lies flat on the table. "
            "A glue stick and extra paper strips sit nearby. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 2,
        "filename": "accordion-caterpillar.webp",
        "alt": "Handmade accordion-fold paper caterpillar craft made from two interlocked colorful paper strips with googly eyes and paper antennae",
        "prompt": (
            "A handmade accordion-fold paper caterpillar craft on a white craft table. "
            "Two strips of construction paper in contrasting bright colors (green and yellow) "
            "folded over each other in alternating folds to create a springy body. "
            "Two large googly eyes and two tiny curly paper antennae attached to the front end. "
            "The caterpillar is stretched out gently in a slight curve on the table. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 3,
        "filename": "paper-chain-snake.webp",
        "alt": "Handmade colorful paper chain snake craft with interlocked paper loop rings, a paper tongue, and drawn eyes",
        "prompt": (
            "A handmade paper chain snake craft on a white craft table. "
            "A long chain of interlocked loops of brightly colored construction paper "
            "arranged in a gentle S-curve. The front loop has two marker-drawn dot eyes "
            "and a thin red paper forked tongue glued underneath. "
            "A few spare paper strips and a glue stick lie nearby. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 4,
        "filename": "torn-paper-mosaic.webp",
        "alt": "Handmade torn paper mosaic butterfly craft filled with small pieces of torn colorful paper on white cardstock",
        "prompt": (
            "A handmade torn paper mosaic butterfly craft on a white craft table. "
            "A simple butterfly outline drawn on white cardstock, filled in "
            "with small torn pieces of colorful construction paper (pink, orange, purple, yellow) glued flat. "
            "More torn paper scraps scattered around the table. "
            "A child's small hands press a torn piece down with a glue stick. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 5,
        "filename": "paper-bag-puppet.webp",
        "alt": "Handmade paper bag puppet dog made from a brown lunch bag with construction paper ears and googly eyes, a child's hand inside",
        "prompt": (
            "A handmade paper bag puppet on a white craft table. "
            "A brown paper lunch bag transformed into a friendly dog face: "
            "floppy brown construction paper ears glued to the sides, two large googly eyes, "
            "a red construction paper tongue visible at the fold. "
            "A child's small hand is inserted into the open end of the bag, making the mouth move. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 6,
        "filename": "paper-fan.webp",
        "alt": "Handmade accordion-folded paper fan craft decorated with colorful marker patterns and stickers, held open by a child",
        "prompt": (
            "A handmade accordion-folded paper fan craft on a white craft table. "
            "A rectangular piece of bright paper (decorated with colorful flower doodles and small heart stickers) "
            "folded tightly in even accordion pleats, then fanned open and held at the base with a piece of tape. "
            "The fan is opened to show the full rainbow of folds. "
            "A few markers and stickers sit nearby. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 7,
        "filename": "handprint-flower-bouquet.webp",
        "alt": "Handmade handprint flower bouquet craft with cut-out paper hand shapes as flower heads on green paper stems in a paper cup vase",
        "prompt": (
            "A handmade handprint flower bouquet craft on a white craft table. "
            "Five cut-out child handprint shapes in different bright colors (pink, yellow, orange, purple, red) "
            "each attached to a green construction paper stem, arranged in a small paper cup covered in colorful stickers. "
            "The flowers fan out cheerfully from the cup like a real bouquet. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 8,
        "filename": "paper-strip-jellyfish.webp",
        "alt": "Handmade paper strip jellyfish craft with a paper bowl body and long curly colorful paper tentacles, hung from a string",
        "prompt": (
            "A handmade paper jellyfish craft on a white craft table. "
            "A half-circle paper dome body in light blue or purple, "
            "with long strips of colorful construction paper tentacles curled with a pencil hanging below. "
            "Two marker-drawn dot eyes on the dome. The jellyfish rests on the table "
            "with tentacles spread outward. A thin string is attached to the top. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 10,
        "filename": "paper-crown.webp",
        "alt": "Handmade paper crown made from a golden construction paper strip with zigzag peaks, decorated with crayon jewels and star stickers",
        "prompt": (
            "A handmade paper crown craft on a white craft table. "
            "A long strip of yellow construction paper with tall pointed zigzag peaks "
            "cut along the top edge, decorated with crayon-drawn gem shapes in red, blue, and purple, "
            "and colorful star stickers dotted along the band. "
            "The crown band lies flat and unrolled showing its full design. "
            "A child's hand presses a sticker onto it. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 11,
        "filename": "paper-circle-caterpillar.webp",
        "alt": "Handmade paper circle caterpillar craft made from overlapping colored paper circles in graduating sizes with a smiley face",
        "prompt": (
            "A handmade paper circle caterpillar craft on a white craft table. "
            "A row of overlapping construction paper circles in rainbow colors (red, orange, yellow, green, blue, purple), "
            "each slightly larger than the previous. "
            "The first (largest) circle has a smiling marker face with dot eyes and a big grin. "
            "Tiny marker lines along the bottom edge serve as legs. "
            "The caterpillar stretches across the table from left to right. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 12,
        "filename": "3d-paper-butterfly.webp",
        "alt": "Handmade 3D paper butterfly craft with cut-out wings slightly raised off a blue background paper, decorated with colorful paper dots",
        "prompt": (
            "A handmade 3D paper butterfly craft on a white craft table. "
            "A butterfly shape cut from bright pink and purple construction paper, "
            "with wings folded slightly upward to create a 3D raised effect, "
            "glued at the body only to a sky blue background sheet. "
            "Tiny paper dot circles in yellow and orange decorate each wing. "
            "The butterfly casts a soft shadow showing the dimensional fold. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 13,
        "filename": "paper-ladybug.webp",
        "alt": "Handmade paper ladybug craft with a red folded circle for wings on a black paper body with white dot eyes and black paper spots",
        "prompt": (
            "A handmade paper ladybug craft on a white craft table. "
            "A round red construction paper circle folded in half to form two wings, "
            "placed on an oval black paper body. "
            "Six black paper strip legs extend from the body sides. "
            "White dot sticker eyes and small black paper circle spots decorate the red wings. "
            "The ladybug sits centered on the table, round and charming. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 14,
        "filename": "woven-paper-placemat.webp",
        "alt": "Handmade woven paper placemat craft with colorful paper strips woven over and under slits in a green base sheet",
        "prompt": (
            "A handmade woven paper placemat craft on a white craft table. "
            "A green construction paper base sheet with evenly spaced parallel slits cut across it. "
            "Strips of yellow, orange, and blue paper woven over and under through the slits "
            "in a classic checkerboard weave pattern. "
            "A few unfinished strips still lie beside the mat waiting to be woven in. "
            "Neat, colorful, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 15,
        "filename": "paper-ice-cream-cone.webp",
        "alt": "Handmade paper ice cream cone craft with a rolled brown cone and stacked colorful paper circle scoops decorated with marker sprinkles",
        "prompt": (
            "A handmade paper ice cream cone craft on a white craft table. "
            "A brown construction paper triangle rolled into a cone shape and taped. "
            "Two large colorful paper circles (pink and mint green) stacked on top as scoops. "
            "Tiny colorful marker dots scattered on the scoops as sprinkles. "
            "A small red paper half-circle as a cherry on top. "
            "The cone stands upright propped against a small block, looking delicious. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 17,
        "filename": "curled-paper-flower.webp",
        "alt": "Handmade 3D curled paper flower craft with curled petal shapes layered around a yellow paper center button",
        "prompt": (
            "A handmade 3D curled paper flower craft on a white craft table. "
            "Six pink construction paper petals each curled at the tips with a pencil to curve upward, "
            "layered and glued around a small yellow paper circle center button. "
            "The flower sits flat on the table, petals curled gently upward giving a realistic 3D rose look. "
            "Two green paper leaf shapes flank the sides. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 18,
        "filename": "paper-binoculars.webp",
        "alt": "Handmade paper binoculars craft made from two toilet paper rolls wrapped in blue paper with star stickers and a neck strap",
        "prompt": (
            "A handmade paper binoculars craft on a white craft table. "
            "Two toilet paper roll tubes wrapped in bright blue construction paper, "
            "taped side by side. "
            "Decorated with yellow star stickers and crayon lines. "
            "A strip of colorful paper serves as a neck strap connected to both tubes. "
            "The binoculars are shown from a slight angle so both barrels are visible. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 19,
        "filename": "paper-chain-countdown.webp",
        "alt": "Handmade paper chain countdown craft with a long chain of colorful interlocked paper loops hanging from a table edge",
        "prompt": (
            "A handmade paper chain countdown hanging from the edge of a white craft table. "
            "A long, cheerful chain of interlocked loops in rainbow colors: red, orange, yellow, green, blue, purple. "
            "Each loop has a number or small drawing on it in marker. "
            "The chain hangs in a gentle curve with about 15-20 loops visible. "
            "A few pre-cut paper strips and a glue stick sit on the table above. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 20,
        "filename": "paper-city-skyline.webp",
        "alt": "Handmade paper city skyline craft with colorful paper rectangle buildings of different heights glued in a row on dark blue sky paper",
        "prompt": (
            "A handmade paper city skyline craft on a white craft table. "
            "A row of construction paper rectangles in different heights and colors (orange, red, yellow, blue, green) "
            "glued side by side on a dark blue background sheet to form a city silhouette. "
            "Each building has tiny marker-drawn windows, doors, and details. "
            "Small yellow circle or star stickers dot the dark sky above the buildings. "
            "The completed cityscape lies flat on the table. "
            f"{STYLE}"
        ),
    },
]

# ---------------------------------------------------------------------------
# Metadata for badge conversion (all 20 ideas including those without images)
# ---------------------------------------------------------------------------
IDEA_META = {
    1:  ("2+", "15 min", "Low"),
    2:  ("3+", "10 min", "Low"),
    3:  ("3+", "15 min", "Low"),
    4:  ("2+", "20 min", "Medium"),
    5:  ("3+", "20 min", "Low"),
    6:  ("3+", "10 min", "Low"),
    7:  ("2+", "20 min", "Low"),
    8:  ("3+", "15 min", "Low"),
    9:  ("4+", "15 min", "Low"),
    10: ("3+", "15 min", "Low"),
    11: ("2+", "10 min", "Low"),
    12: ("4+", "20 min", "Low"),
    13: ("3+", "15 min", "Low"),
    14: ("4+", "20 min", "Low"),
    15: ("3+", "15 min", "Medium"),
    16: ("4+", "10 min", "Low"),
    17: ("5+", "20 min", "Low"),
    18: ("3+", "15 min", "Low"),
    19: ("3+", "20 min", "Low"),
    20: ("4+", "25 min", "Low"),
}


# ---------------------------------------------------------------------------
# Image generation helpers
# ---------------------------------------------------------------------------

def generate_image(client, prompt: str, output_path: Path) -> bool:
    try:
        from google.genai import types as genai_types
        from PIL import Image as PILImage

        full_prompt = f"{prompt} Aspect ratio: 4:3. Wide rectangular landscape orientation."
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=full_prompt,
            config=genai_types.GenerateContentConfig(response_modalities=["IMAGE"]),
        )
        image_bytes = None
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_bytes = part.inline_data.data
                break
        if image_bytes is None:
            log.warning(f"No image data for {output_path.name}")
            return False
        from PIL import Image as PILImage
        with PILImage.open(io.BytesIO(image_bytes)) as img:
            resized = img.resize((TARGET_W, TARGET_H), PILImage.LANCZOS)
            resized.save(output_path, "WEBP", quality=82, method=6)
        size_kb = output_path.stat().st_size // 1024
        log.info(f"  Saved: {output_path.name} ({TARGET_W}x{TARGET_H}px, {size_kb}KB)")
        return True
    except Exception as exc:
        log.warning(f"  Failed: {exc}")
        return False


def generate_with_retry(client, prompt: str, output_path: Path) -> bool:
    for attempt in range(1, MAX_RETRIES + 1):
        if attempt > 1:
            log.info(f"  Retry {attempt}/{MAX_RETRIES}...")
            time.sleep(3)
        if generate_image(client, prompt, output_path):
            return True
        time.sleep(2)
    return False


# ---------------------------------------------------------------------------
# CSS patch  — add .idea-meta if missing
# ---------------------------------------------------------------------------

def patch_css(text: str) -> str:
    if ".idea-meta" in text:
        return text
    # Insert after .badge-category line
    old = "    .badge-category { background: #FEF0EC; border-color: #FECDC5; color: #C0503A; }"
    new = old + "\n    .idea-meta { display: flex; gap: 8px; flex-wrap: wrap; margin: 10px 0 18px; }"
    if old in text:
        text = text.replace(old, new)
        log.info("  CSS: .idea-meta added")
    else:
        log.warning("  CSS: could not find .badge-category to insert .idea-meta after")
    return text


# ---------------------------------------------------------------------------
# HTML rewrite  — badges + images
# ---------------------------------------------------------------------------

def build_badge_div(age: str, time: str, mess: str) -> str:
    return (
        f'\n<div class="idea-meta">\n'
        f'<span class="badge">👶 Ages {age}</span>\n'
        f'<span class="badge">⏱ {time}</span>\n'
        f'<span class="badge">💧 Mess: {mess}</span>\n'
        f'</div>'
    )


def build_figure(idea_num: int, filename: str, alt: str) -> str:
    src = f"../blog/images/paper-arts-and-crafts/{filename}"
    return (
        f'\n<figure class="article-step-img">'
        f'<img src="{src}" alt="{alt}" '
        f'width="{TARGET_W}" height="{TARGET_H}" loading="lazy">'
        f'</figure>'
    )


def rewrite_html(generated_images: list):
    text = HTML_FILE.read_text(encoding="utf-8")
    original = text

    # 1. Patch CSS
    text = patch_css(text)

    # Build lookup: idea_number -> image info
    img_by_num = {img["idea_number"]: img for img in generated_images}

    # 2. For each idea block, replace old format with new format
    # Old pattern (placeholder before meta):
    #   [ROUNDUP_IMAGE_PLACEHOLDER]\n<p><em>Age: X | Time: X | Mess: X</em></p>
    # New pattern:
    #   <div class="idea-meta">badges</div>\n<figure>...</figure>
    #
    # Also handle ideas without placeholder:
    #   <p><em>Age: X | Time: X | Mess: X</em></p>
    # → just convert to badge div

    for idea_num, (age, time_str, mess) in IDEA_META.items():
        badge_div = build_badge_div(age, time_str, mess)

        # Pattern A: placeholder + meta paragraph
        pattern_a = (
            r'\[ROUNDUP_IMAGE_PLACEHOLDER\]\n'
            r'<p><em>Age: [^<]+</em></p>'
        )
        # Find match near this idea number
        h3_match = re.search(rf'<h3>{idea_num}\. ', text)
        if not h3_match:
            continue
        search_start = h3_match.end()
        # Look ahead max 600 chars for the pattern
        segment = text[search_start: search_start + 800]

        ma = re.search(pattern_a, segment)
        if ma:
            old_block = ma.group(0)
            if idea_num in img_by_num:
                fig = build_figure(idea_num, img_by_num[idea_num]["filename"], img_by_num[idea_num]["alt"])
                new_block = badge_div + fig
            else:
                new_block = badge_div
            text = text[:search_start] + segment.replace(old_block, new_block, 1) + text[search_start + 800:]
            log.info(f"  Idea {idea_num}: replaced placeholder + meta → badges + figure")
            continue

        # Pattern B: meta paragraph only (no placeholder)
        pattern_b = r'<p><em>Age: [^<]+</em></p>'
        mb = re.search(pattern_b, segment)
        if mb:
            old_block = mb.group(0)
            new_block = badge_div
            text = text[:search_start] + segment.replace(old_block, new_block, 1) + text[search_start + 800:]
            log.info(f"  Idea {idea_num}: replaced meta only → badges")

    if text != original:
        HTML_FILE.write_text(text, encoding="utf-8")
        log.info(f"HTML updated: {HTML_FILE.name}")
    else:
        log.warning("No changes made to HTML.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    try:
        from google import genai
        from PIL import Image
    except ImportError as e:
        log.error(f"Missing dependency: {e}")
        sys.exit(1)

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        log.error("GOOGLE_API_KEY not set in .env")
        sys.exit(1)

    IMG_DIR.mkdir(parents=True, exist_ok=True)
    client = genai.Client(api_key=api_key)

    successfully_generated = []
    total_ok = total_fail = 0

    for img_def in IMAGES:
        filename = img_def["filename"]
        output_path = IMG_DIR / filename

        if output_path.exists():
            log.info(f"Already exists, skipping: {filename}")
            successfully_generated.append(img_def)
            continue

        log.info(f"\n[Idea {img_def['idea_number']}] Generating: {filename}")
        ok = generate_with_retry(client, img_def["prompt"], output_path)
        if ok:
            successfully_generated.append(img_def)
            total_ok += 1
        else:
            total_fail += 1
            log.error(f"  FAILED after {MAX_RETRIES} retries: {filename}")
        time.sleep(2)

    log.info(f"\nGenerated: {total_ok} new, {total_fail} failed")
    log.info("\nRewriting HTML (badges + figures)...")
    rewrite_html(successfully_generated)
    log.info("\nDone.")


if __name__ == "__main__":
    main()
