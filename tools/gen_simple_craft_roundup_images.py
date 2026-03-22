#!/usr/bin/env python3
"""
gen_simple_craft_roundup_images.py
Generate craft-specific images for the simple-paper-craft roundup ideas
that currently have no images, then inject them into the HTML.

Ideas already with images: 4, 6, 10, 13, 17, 20 (plus hero at top)
Target: ~15 images in article body (75% of 20 ideas)
Ideas to generate: 1, 3, 5, 7, 8, 9, 11, 14, 16 (9 new images → total 15)

Usage:
    python3 /var/www/craft-with-mommy/tools/gen_simple_craft_roundup_images.py
"""

import io, os, re, sys, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR = BASE_DIR / "blog" / "images" / "simple-paper-craft"
HTML_FILE = BASE_DIR / "blog" / "simple-paper-craft.html"
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
# Images to generate — each maps to one specific craft idea in the article
# ---------------------------------------------------------------------------
IMAGES = [
    {
        "idea_number": 1,
        "filename": "paper-plate-animal-face.webp",
        "alt": "Handmade paper plate cat face craft with construction paper ears, googly eyes, and drawn whiskers on a craft table",
        "prompt": (
            "A cute handmade paper plate animal face craft displayed on a white craft table. "
            "A standard white paper plate turned into a cat face: two orange construction paper "
            "triangle ears glued on top, two large googly eyes, a small pink paper circle nose, "
            "and black marker whiskers and a smiling mouth. "
            "The plate lies flat on the table, clearly made by a young child. "
            "A glue stick and a few paper scraps sit nearby. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 3,
        "filename": "accordion-fold-worm.webp",
        "alt": "Springy handmade paper accordion worm craft made from two interlocked paper strips folded in alternating directions",
        "prompt": (
            "A springy handmade paper accordion worm craft displayed on a white craft table. "
            "Made from two strips of construction paper in contrasting colors (yellow and green) "
            "folded over each other in alternating folds to create a stretchy, zigzag body. "
            "A smiling paper circle face with marker dot eyes is attached at one end. "
            "The worm is stretched out in a gentle S-curve on the table. "
            "A child's hand may be visible holding one end and gently stretching it. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 5,
        "filename": "paper-bag-puppet.webp",
        "alt": "Handmade paper bag puppet made from a brown lunch bag with construction paper dog face, floppy ears, and googly eyes",
        "prompt": (
            "A handmade paper bag puppet craft on a white craft table. "
            "A brown paper lunch bag with a friendly dog face: floppy brown construction paper ears "
            "glued to the sides, two large googly eyes, a round pom-pom nose, "
            "and a big red paper tongue visible at the fold of the bag. "
            "A child's hand is inserted into the bag, making the mouth flap open. "
            "Playful, adorable, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 7,
        "filename": "paper-pinwheel.webp",
        "alt": "Handmade paper pinwheel craft made from a bright colored square of construction paper with a brass brad center and pencil handle",
        "prompt": (
            "A handmade paper pinwheel craft displayed on a white craft table. "
            "A brightly multicolored square of construction paper cut and folded into a pinwheel, "
            "with a brass brad fastener at the center and a pencil as the handle. "
            "The pinwheel is shown from a slight angle so the fan blades are visible. "
            "Several more pre-cut colored paper squares and a few extra brads sit nearby. "
            "Bright, fun, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 8,
        "filename": "paper-crown.webp",
        "alt": "Handmade paper crown made from a gold construction paper strip with pointed peaks, decorated with crayon gems and star stickers",
        "prompt": (
            "A handmade paper crown craft displayed on a white craft table. "
            "A long strip of yellow and gold construction paper with tall pointed triangular peaks "
            "cut along the top edge, decorated with crayon-drawn gem shapes in red and purple "
            "and colorful star stickers across the band. "
            "The crown is unrolled flat on the table showing the full design. "
            "A child's hands are visible pressing a star sticker onto the band. "
            "Regal, cheerful, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 9,
        "filename": "paper-bookmarks.webp",
        "alt": "Three handmade paper bookmarks made from decorated cardstock with paper tassels, displayed on a craft table",
        "prompt": (
            "Three handmade paper bookmarks displayed on a white craft table. "
            "Each rectangular bookmark made from thick cardstock is decorated differently: "
            "one with a rainbow drawn in bright markers, one with a daisy flower, "
            "one with a smiling sun. Each has a small paper tassel at the top. "
            "The three bookmarks fan out side by side on the table in a cheerful arrangement. "
            "A marker and scissors sit nearby. "
            "Clean, colorful, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 11,
        "filename": "torn-paper-mosaic.webp",
        "alt": "Handmade torn paper mosaic sun craft being filled with small pieces of torn yellow and orange construction paper on a white background",
        "prompt": (
            "A handmade torn paper mosaic craft in progress on a white craft table. "
            "A simple sun shape drawn in pencil on white cardstock, being filled in "
            "with small pieces of torn yellow and orange construction paper glued down. "
            "Torn paper scraps in yellow, orange, and red are scattered around the table. "
            "A child's hands are visible pressing torn pieces onto the paper with a glue stick. "
            "Textured, colorful, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 14,
        "filename": "paper-kite.webp",
        "alt": "Handmade paper kite craft made from a diamond of bright red and yellow construction paper with a looping paper loop tail and string",
        "prompt": (
            "A handmade paper kite craft displayed on a white craft table. "
            "A diamond-shaped kite made from bright red and yellow construction paper, "
            "with decorative marker lines drawn from each corner to center. "
            "A cheerful tail of multi-colored looped paper strips attached at the bottom point, "
            "and a piece of white string tied to the center front. "
            "The kite lies flat on the table showing its full design and colorful tail. "
            "Bright, playful, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 16,
        "filename": "paper-bird.webp",
        "alt": "Handmade folded paper bird craft made from blue construction paper with open fanned wings, an orange paper beak, and a hanging thread",
        "prompt": (
            "A handmade folded paper bird craft displayed on a white craft table. "
            "Made from a square of sky blue construction paper folded into a simple bird shape, "
            "with the two wings fanned open on each side to show the full wingspan. "
            "A small orange paper triangle beak and a round black dot eye are glued on the head. "
            "A fine white thread is attached at the top for hanging, visible dangling above. "
            "The bird is balanced upright, appearing to soar. "
            "Simple, elegant, clearly handmade. "
            f"{STYLE}"
        ),
    },
]


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
# HTML injection
# ---------------------------------------------------------------------------

def inject_images_into_html(generated_images: list):
    """Insert <figure> image tags for each successfully generated image."""
    text = HTML_FILE.read_text(encoding="utf-8")
    original = text

    for img in generated_images:
        idea_num = img["idea_number"]
        filename = img["filename"]
        alt = img["alt"]
        src = f"../blog/images/simple-paper-craft/{filename}"

        fig_html = (
            f'\n<figure class="article-step-img">'
            f'<img src="{src}" alt="{alt}" '
            f'width="{TARGET_W}" height="{TARGET_H}" loading="lazy">'
            f'</figure>'
        )

        # Find the h3 for this idea number
        h3_pattern = rf'(<h3>{idea_num}\. [^<]+</h3>)'
        h3_match = re.search(h3_pattern, text)
        if not h3_match:
            log.warning(f"  Could not find h3 for idea {idea_num}")
            continue

        h3_start = h3_match.start()

        # Find the next <p>Age: after the h3
        age_pattern = r'<p>Age:'
        age_match = re.search(age_pattern, text[h3_start:])
        if not age_match:
            log.warning(f"  Could not find Age line for idea {idea_num}")
            continue

        insert_pos = h3_start + age_match.start()
        text = text[:insert_pos] + fig_html + '\n' + text[insert_pos:]
        log.info(f"  Injected image for idea {idea_num}: {filename}")

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
    except ImportError:
        log.error("google-genai not installed.")
        sys.exit(1)
    try:
        from PIL import Image
    except ImportError:
        log.error("Pillow not installed.")
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

    log.info(f"\nGenerated: {total_ok} ok, {total_fail} failed")

    log.info("\nInjecting images into HTML...")
    inject_images_into_html(successfully_generated)

    log.info("\nDone.")


if __name__ == "__main__":
    main()
