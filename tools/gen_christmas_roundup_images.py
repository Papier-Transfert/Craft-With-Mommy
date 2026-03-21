#!/usr/bin/env python3
"""
gen_christmas_roundup_images.py
Generate craft-specific images for the 13 Christmas roundup ideas
that currently have no images, then inject them into the HTML.

Ideas already with images: 4, 8, 12, 16, 20, 25 (plus hero at top)
Ideas that need images: 1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17

Usage:
    python3 /var/www/craft-with-mommy/tools/gen_christmas_roundup_images.py
"""

import io, os, re, sys, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR = BASE_DIR / "blog" / "images" / "christmas-paper-crafts"
HTML_FILE = BASE_DIR / "blog" / "christmas-paper-crafts.html"
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
        "filename": "paper-christmas-tree.webp",
        "alt": "Handmade paper Christmas tree made from stacked green construction paper triangles on a craft table",
        "prompt": (
            "A cute handmade paper Christmas tree craft displayed on a white craft table. "
            "Three green construction paper triangles stacked in graduating sizes, glued onto a "
            "short brown rectangle trunk. The tree is decorated with small colorful marker dots "
            "as ornaments and a yellow paper star at the very top. "
            "A child's hands may be visible adding decorations. "
            "Simple, adorable, clearly handmade by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 2,
        "filename": "paper-chain-garland.webp",
        "alt": "Colorful red and green paper chain garland made from construction paper loops",
        "prompt": (
            "A colorful handmade paper chain garland craft on a white craft table. "
            "Alternating red and green construction paper rings linked together in a long chain, "
            "looping and curling across the table in a festive, cheerful way. "
            "Several pre-cut strips of red and green paper sit nearby along with a glue stick. "
            "A child's hands may be visible closing one of the loops. "
            "Festive, vibrant, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 3,
        "filename": "paper-snowflake.webp",
        "alt": "Beautiful handmade white paper snowflake with a symmetrical cut pattern unfolded on a table",
        "prompt": (
            "A beautiful handmade white paper snowflake displayed open on a white craft table. "
            "The snowflake has a delicate symmetrical pattern of triangles and notches cut into it. "
            "Nearby: a pair of child safety scissors, small folded paper squares, "
            "and little bits of cut-away paper scattered around. "
            "The snowflake is the clear hero of the photo, spread open fully. "
            "Delicate, lacy, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 5,
        "filename": "handprint-reindeer-card.webp",
        "alt": "Handmade handprint reindeer Christmas card made from a brown paper handprint with googly eyes and red nose",
        "prompt": (
            "A handmade handprint reindeer Christmas card craft on a white table. "
            "A brown construction paper handprint cutout placed upside-down on a folded cream "
            "cardstock card, so the fingers point up as antlers. "
            "Two googly eyes and a red paper circle nose are glued on the palm area as the face. "
            "The card is open, showing the cute reindeer on the front. "
            "A child's hands may be visible pressing the nose down. "
            "Adorable, heartfelt, handmade keepsake card. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 6,
        "filename": "paper-santa-claus.webp",
        "alt": "Handmade paper Santa Claus figure made from construction paper shapes with cotton ball beard",
        "prompt": (
            "A handmade paper Santa Claus figure displayed on a white craft table. "
            "A large red construction paper triangle as the body, a pink or flesh-toned paper circle "
            "as the face on top, a fluffy white cotton ball beard below the face, "
            "a thin black strip of paper as the belt across the middle, "
            "and a small red paper hat on the head. "
            "The Santa stands or lays flat on the white table, looking festive and charming. "
            "A child's hands may be visible adding the cotton ball beard. "
            "Cute, clearly handmade, festive holiday craft. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 7,
        "filename": "cone-christmas-tree.webp",
        "alt": "Small handmade paper cone Christmas trees decorated with sequins and pom-poms on a craft table",
        "prompt": (
            "Three small handmade paper cone Christmas trees displayed together on a white table. "
            "Each cone is rolled from green cardstock in a different size, "
            "decorated with colorful sequins, tiny pom-poms, and small paper circles as ornaments. "
            "A yellow paper star sits at the very tip of the tallest cone. "
            "The three trees are grouped together as a little family, like a tabletop centerpiece. "
            "Festive, charming, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 9,
        "filename": "paper-roll-santa.webp",
        "alt": "Handmade paper roll Santa Claus craft made from a toilet paper roll wrapped in red paper",
        "prompt": (
            "A handmade paper roll Santa Claus craft on a white table. "
            "A toilet paper roll wrapped in red construction paper, with a white fluffy cotton beard, "
            "a small red paper hat, black marker belt buckle, and a friendly drawn-on smiling face. "
            "Beside it, one or two other paper roll holiday characters (an elf in green or a reindeer). "
            "A child's hands may be visible attaching the hat. "
            "Cute, whimsical, clearly handmade from recycled materials. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 10,
        "filename": "paper-snowman.webp",
        "alt": "Handmade paper snowman made from three white paper circles with a black hat and carrot nose",
        "prompt": (
            "A handmade paper snowman craft displayed on a white craft table. "
            "Three white construction paper circles stacked and glued in graduating sizes (large, medium, small). "
            "A black construction paper top hat on the smallest circle head, "
            "a tiny orange triangle carrot nose, small black dot eyes and button dots along the body. "
            "A colorful scarf strip of paper may be wrapped around the neck. "
            "A child's hands may be visible positioning the hat. "
            "Simple, adorable, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 11,
        "filename": "paper-star-garland.webp",
        "alt": "Handmade paper star garland with gold and silver paper stars threaded on twine",
        "prompt": (
            "A handmade paper star garland craft in progress on a white craft table. "
            "Gold and silver construction paper star cutouts spread across the table, "
            "with several already threaded onto a long piece of natural twine forming a glittery garland. "
            "A single-hole punch, scissors, and remaining unthreaded star shapes are nearby. "
            "A child's hands are visible threading a star shape onto the twine. "
            "Festive, sparkly, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 13,
        "filename": "paper-stocking.webp",
        "alt": "Handmade paper Christmas stocking made from red construction paper with marker decorations",
        "prompt": (
            "A handmade paper Christmas stocking craft on a white craft table. "
            "A large red construction paper stocking shape (two layers glued together at the edges), "
            "decorated with colorful marker patterns, star stickers, and a white strip of paper trim at the top opening. "
            "The stocking hangs flat on the table showing both its festive front side. "
            "A child's hands may be visible adding stickers or drawing decorations. "
            "Cheerful, festive, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 14,
        "filename": "paper-candy-cane.webp",
        "alt": "Handmade paper candy canes made by twisting red and white paper strips together",
        "prompt": (
            "Handmade paper candy cane crafts displayed on a white craft table. "
            "Three completed candy canes: each made from a red paper strip and a white paper strip "
            "twisted together to create alternating stripe pattern, then curved into a classic hook. "
            "The candy canes lean against each other in a small festive bunch. "
            "A child's hands may be visible twisting two strips together in the background. "
            "Festive, fun, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 15,
        "filename": "paper-angel.webp",
        "alt": "Handmade paper angel craft made from white cardstock cone body with accordion-fold wings and gold halo",
        "prompt": (
            "A handmade paper angel craft standing upright on a white craft table. "
            "A white cardstock cone as the body, a small white paper circle as the head, "
            "accordion-folded white paper wings extending on each side, "
            "and a gold paper circle or halo piece above the head. "
            "The angel stands gracefully and looks delicate and pretty. "
            "A child's hands may be visible attaching the wings. "
            "Serene, festive, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "idea_number": 17,
        "filename": "paper-dove.webp",
        "alt": "Handmade paper dove ornament with accordion-fold wings hanging from a white thread",
        "prompt": (
            "A handmade paper dove ornament displayed on a white craft table or hanging gently. "
            "A simple white paper bird silhouette body, with accordion-folded white paper wings "
            "spread open on each side. A fine white thread is attached at the top for hanging. "
            "The dove looks graceful and peaceful, slightly turning in the air if hanging. "
            "A child's hands may be visible holding the thread. "
            "Simple, elegant, clearly handmade, peaceful holiday decoration. "
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
        src = f"../blog/images/christmas-paper-crafts/{filename}"

        fig_html = (
            f'\n<figure class="article-step-img">'
            f'<img src="{src}" alt="{alt}" '
            f'width="{TARGET_W}" height="{TARGET_H}" loading="lazy">'
            f'</figure>'
        )

        # Find the h3 for this idea number, then insert image after the description <p>
        # and before the meta <p><em>Age:...</em></p>
        # Pattern: <h3>N. ...name...</h3> ... <p><em>Age:</em></p>
        # We insert the figure before the <p><em>Age: block that follows this idea's h3.

        # Strategy: find the h3 for idea N, then find the next <p><em>Age: after it
        # and insert the figure just before that line.
        h3_pattern = rf'(<h3>{idea_num}\. [^<]+</h3>)'
        h3_match = re.search(h3_pattern, text)
        if not h3_match:
            log.warning(f"  Could not find h3 for idea {idea_num}")
            continue

        # Find position of this h3 in text
        h3_start = h3_match.start()

        # Find the next <p><em>Age: after the h3
        age_pattern = r'<p><em>Age:'
        age_match = re.search(age_pattern, text[h3_start:])
        if not age_match:
            log.warning(f"  Could not find Age line for idea {idea_num}")
            continue

        # Absolute position of the age line
        insert_pos = h3_start + age_match.start()

        # Insert the figure just before the age meta line
        text = text[:insert_pos] + fig_html + '\n' + text[insert_pos:]
        log.info(f"  Injected image for idea {idea_num}: {filename}")

    if text != original:
        HTML_FILE.write_text(text, encoding="utf-8")
        log.info(f"HTML updated: {HTML_FILE.name}")
    else:
        log.warning("No changes made to HTML.")


def add_final_thoughts():
    """Add Final Thoughts section before the closing </article> tag."""
    text = HTML_FILE.read_text(encoding="utf-8")

    # Check if Final Thoughts already exists
    if '<h2>Final Thoughts</h2>' in text:
        log.info("Final Thoughts section already present -- skipping.")
        return

    final_thoughts_html = """
<h2>Final Thoughts</h2>

<p>These <strong>Christmas paper crafts</strong> are proof that some of the sweetest holiday moments happen around a kitchen table with a stack of construction paper and a glue stick. Whether you try one idea this week or work your way through the whole list together, we hope it brings a little extra joy and warmth to your December. Happy crafting, friend!</p>
"""

    # Insert before More Crafts You'll Love or before </article>
    if '<h2>More Crafts You' in text:
        text = text.replace('<h2>More Crafts You', final_thoughts_html + '\n<h2>More Crafts You', 1)
    else:
        text = text.replace('</article>', final_thoughts_html + '\n    </article>', 1)

    HTML_FILE.write_text(text, encoding="utf-8")
    log.info("Final Thoughts section added.")


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

        # Skip if already exists
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

    # Inject images into HTML
    log.info("\nInjecting images into HTML...")
    inject_images_into_html(successfully_generated)

    # Add Final Thoughts section
    log.info("\nAdding Final Thoughts section...")
    add_final_thoughts()

    log.info("\nDone.")


if __name__ == "__main__":
    main()
