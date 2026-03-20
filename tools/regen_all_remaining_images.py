#!/usr/bin/env python3
"""
regen_all_remaining_images.py
Regenerate images for 4 articles using step-accurate prompts and 1200x900px output.
Also updates HTML files: replaces placeholders with <img> tags and fixes dimensions.

Articles:
  1. craft-using-paper       (paper chain caterpillar)
  2. rainbow-fish            (paper plate rainbow fish — images missing, placeholders in HTML)
  3. butterfly               (paper plate butterfly — images missing, placeholders in HTML)
  4. ladybug                 (paper plate ladybug)

Usage:
    python3 /var/www/craft-with-mommy/tools/regen_all_remaining_images.py
"""

import io, os, re, sys, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

# ---------------------------------------------------------------------------
# Shared style injected into every prompt
# ---------------------------------------------------------------------------
STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. "
    "Landscape orientation 4:3. "
    "Slightly angled tutorial composition — instructional yet warm. "
    "No cartoon elements. Real craft materials only."
)

# ===========================================================================
# ARTICLE DEFINITIONS
# Each article = slug, image directory, list of image dicts
# ===========================================================================

ARTICLES = []

# ---------------------------------------------------------------------------
# 1. PAPER CHAIN CATERPILLAR  (craft-using-paper)
# ---------------------------------------------------------------------------
CATERPILLAR_ANCHOR = (
    "VISUAL CONSISTENCY: The craft is a colorful paper chain caterpillar. "
    "Body: 8-10 round paper loops (each from a 1-inch-wide, 6-inch strip) in rainbow colors "
    "(red, orange, yellow, green, blue, purple) all linked in a row. "
    "Head: a 3-inch green construction paper circle with two googly eyes, a black marker smile, "
    "and two pipe cleaner antennae with small pom-pom tips. "
    "Tiny black marker feet may be drawn below each loop. "
    "Keep the same colors and design in every step image."
)

ARTICLES.append({
    "slug": "craft-using-paper",
    "html_file": BASE_DIR / "blog" / "craft-using-paper.html",
    "has_placeholders": False,
    "main_img_src": "../blog/images/craft-using-paper/craft-paper.webp",
    "images": [
        {
            "filename": "craft-paper.webp",
            "label": "Featured — finished caterpillar",
            "prompt": (
                "A beautifully presented completed paper chain caterpillar craft on a white table. "
                "The caterpillar body is a chain of 8-10 round paper loops in bright rainbow colors "
                "(red, orange, yellow, green, blue, purple), all linked together in a gentle curve. "
                "The green paper circle head has two googly eyes, a black marker smile, and two pipe "
                "cleaner antennae with small colorful pom-poms at the tips. "
                "Tiny black marker feet are visible below each body loop. "
                "The craft looks charming and handmade. A child's hand may gently touch it. "
                f"{STYLE}"
            ),
        },
        {
            "filename": "mom-child-gathering.webp",
            "label": "Step 1 — Cut paper strips",
            "prompt": (
                "Tutorial step 1: cutting colorful construction paper into strips. "
                "A child's hands (age 3-5) using child safety scissors to cut a strip of "
                "bright orange construction paper. The strip is about 1 inch wide and 6 inches long. "
                "On the white table: sheets of colorful construction paper (red, orange, yellow, green, "
                "blue, purple), several already-cut strips laid out in rainbow order, scissors, glue stick. "
                "No loops or caterpillar assembled yet — only flat strips and paper sheets. "
                "A mom's hands are visible nearby, guiding the child. "
                f"{STYLE}"
            ),
        },
        {
            "filename": "small-child-hands.webp",
            "label": "Step 2 — Make body loops",
            "prompt": (
                "Tutorial step 2: curling paper strips into loops. "
                "Close-up of a child's hands curling one bright yellow construction paper strip "
                "into a circle/loop, with the ends overlapping. "
                "Child is pressing a glue stick along the overlapping ends to seal the loop. "
                "On the white table: 5-6 already-completed colorful loops (red, orange, green, blue) "
                "sitting separately, not yet linked. More flat strips nearby. "
                "No caterpillar chain assembled yet — only loose individual loops. "
                f"{STYLE}"
            ),
        },
        {
            "filename": "child-gluing-layered.webp",
            "label": "Step 3 — Connect the body",
            "prompt": (
                "Tutorial step 3: linking paper loops into a chain. "
                "Child's hands threading a new orange loop through an already-linked chain of "
                "4-5 colorful paper loops (red, yellow, green, blue, purple) and pressing the ends "
                "together with a glue stick to seal. "
                "The rainbow chain stretches across the white table in a gentle curve. "
                "The glue stick is in the child's other hand. No head attached yet. "
                f"{CATERPILLAR_ANCHOR} {STYLE}"
            ),
        },
        {
            "filename": "child-markers-crayons.webp",
            "label": "Step 4 — Make the head",
            "prompt": (
                "Tutorial step 4: making the caterpillar's head. "
                "A child's hands tracing a 3-inch circle onto green construction paper "
                "using a small cup or jar lid as a template and a pencil. "
                "On the white table: the completed rainbow loop chain is visible to the side, "
                "two googly eyes, a black washable marker, two pipe cleaner pieces with curled ends, "
                "and two small colorful pom-poms. "
                "Head not assembled yet — just the tracing step happening now. "
                f"{CATERPILLAR_ANCHOR} {STYLE}"
            ),
        },
        {
            "filename": "proud-toddler-holding.webp",
            "label": "Step 5 — Attach head and details",
            "prompt": (
                "Tutorial step 5: final assembly of the paper caterpillar. "
                "A smiling child (age 3-5) proudly holding up or displaying the completed "
                "paper chain caterpillar. "
                "The caterpillar has a chain of 8-10 colorful loops (red, orange, yellow, green, "
                "blue, purple), a green circle head with two googly eyes, a black marker smile, "
                "and two pipe cleaner antennae with pom-pom tips. "
                "Tiny black marker feet are drawn along the bottom of the body loops. "
                "Child's face shows joy and pride. Warm, cozy home setting. "
                f"{CATERPILLAR_ANCHOR} {STYLE}"
            ),
        },
    ],
})

# ---------------------------------------------------------------------------
# 2. RAINBOW FISH  (easy-paper-plate-rainbow-fish-craft-for-toddlers)
# ---------------------------------------------------------------------------
FISH_ANCHOR = (
    "VISUAL CONSISTENCY: The craft is a paper plate rainbow fish. "
    "The plate is a standard 9-inch white paper plate. A triangular wedge has been "
    "cut from one edge (creating the mouth opening), and that same triangle is glued "
    "to the opposite side as the tail fin. "
    "The fish body is covered in small pieces of rainbow-colored tissue paper "
    "arranged in stripes: red at the top, then orange, yellow, green, blue, purple at the bottom. "
    "A large googly eye is placed near the mouth. "
    "Keep the same fish shape, same tissue paper rainbow stripes, same googly eye in every image."
)

FISH_SLUG = "easy-paper-plate-rainbow-fish-craft-for-toddlers"
ARTICLES.append({
    "slug": FISH_SLUG,
    "html_file": BASE_DIR / "blog" / f"{FISH_SLUG}.html",
    "has_placeholders": True,
    "main_img_src": f"../blog/images/{FISH_SLUG}/rainbow-fish-craft.webp",
    "images": [
        {
            "filename": "rainbow-fish-craft.webp",
            "label": "Featured — finished rainbow fish",
            "prompt": (
                "A beautifully presented completed paper plate rainbow fish craft on a white table. "
                "The paper plate fish has a triangular wedge cut from one side as the mouth, "
                "the same triangle glued to the opposite side as the tail fin. "
                "The entire fish body is covered in small colorful tissue paper pieces arranged "
                "in rainbow stripes: red at the top, then orange, yellow, green, blue, purple. "
                "A large googly eye is near the mouth. "
                "The fish looks vibrant, cheerful, and clearly handmade. "
                "A young child's hands may be gently holding it up. Pinterest-worthy. "
                f"{STYLE}"
            ),
        },
        {
            "filename": "cutting-mouth-shape.webp",
            "label": "Step 1 — Prep the fish shape",
            "prompt": (
                "Tutorial step 1: cutting the fish mouth from a paper plate. "
                "An adult's hands using scissors to cut a triangular wedge from the edge "
                "of a plain white paper plate. The triangle is being removed from one side. "
                "The cut triangle piece sits nearby on the white table, ready to be reused as the tail. "
                "The plate now shows the V-shaped mouth opening on one side. "
                "No tissue paper, no paint yet — just the plain white plate being cut. "
                f"{STYLE}"
            ),
        },
        {
            "filename": "tearing-tissue-paper.webp",
            "label": "Step 2 — Tear tissue paper",
            "prompt": (
                "Tutorial step 2: tearing tissue paper into small pieces. "
                "A toddler's hands (age 2-4) tearing a small piece of bright red tissue paper. "
                "On the white table: small piles of already-torn tissue paper pieces in "
                "rainbow colors: red, orange, yellow, green, blue, purple — each color in its own pile. "
                "The paper plate fish shape (with mouth notch and the triangle attached on the opposite "
                "side as tail) is visible nearby, still plain white with no tissue paper on it yet. "
                "Warm, cozy, active toddler craft scene. "
                f"{STYLE}"
            ),
        },
        {
            "filename": "gluing-tissue-scales.webp",
            "label": "Step 3 — Glue tissue paper scales",
            "prompt": (
                "Tutorial step 3: gluing rainbow tissue paper onto the paper plate fish. "
                "A toddler's hands pressing colorful tissue paper pieces onto the paper plate fish body. "
                "The plate is fish-shaped (triangular mouth notch on one side, triangle tail on the other). "
                "The top half of the fish is already covered in red and orange tissue paper. "
                "The child is now pressing yellow tissue paper pieces onto the middle section. "
                "Green, blue, purple tissue paper pieces are sorted in piles nearby waiting to be glued. "
                "A glue stick is on the table. "
                f"{FISH_ANCHOR} {STYLE}"
            ),
        },
        {
            "filename": "adding-googly-eye.webp",
            "label": "Step 4 — Add the eye and details",
            "prompt": (
                "Tutorial step 4: adding the googly eye to the finished rainbow fish. "
                "A toddler's fingers pressing a large googly eye onto the paper plate fish, "
                "near the mouth opening on the left side. "
                "The fish body is now fully covered in rainbow tissue paper stripes "
                "(red, orange, yellow, green, blue, purple from top to bottom). "
                "The triangular tail is visible on the right side. "
                "A black marker is nearby for adding detail lines. "
                f"{FISH_ANCHOR} {STYLE}"
            ),
        },
        {
            "filename": "finished-rainbow-fish.webp",
            "label": "Step 5 — Show it off",
            "prompt": (
                "Tutorial step 5: the completed rainbow fish being proudly displayed. "
                "A smiling toddler (age 2-4) proudly holding up the finished rainbow fish craft. "
                "The fish is the complete paper plate with rainbow tissue paper stripes "
                "(red at top through purple at bottom), a triangular tail, mouth opening, "
                "and a large googly eye. "
                "Child's face shows pure delight and pride. "
                "Warm, joyful, cozy family craft moment. "
                f"{FISH_ANCHOR} {STYLE}"
            ),
        },
    ],
})

# ---------------------------------------------------------------------------
# 3. BUTTERFLY  (easy-paper-plate-butterfly-craft-for-preschoolers)
# ---------------------------------------------------------------------------
BUTTERFLY_ANCHOR = (
    "VISUAL CONSISTENCY: The craft is a paper plate butterfly. "
    "The wings are a single standard 9-inch white paper plate with both halves painted "
    "in a symmetrical pattern (same blobs and swirls on each side, mirror image) in "
    "bright colors: pink, purple, and blue. "
    "The body is a wooden clothespin painted black, clipped onto the folded center edge. "
    "Two pipe cleaner antennae (curled at the tips) and two googly eyes are on the clothespin. "
    "Keep the same wing colors, same symmetry, same clothespin body in every image."
)

BUTTERFLY_SLUG = "easy-paper-plate-butterfly-craft-for-preschoolers"
ARTICLES.append({
    "slug": BUTTERFLY_SLUG,
    "html_file": BASE_DIR / "blog" / f"{BUTTERFLY_SLUG}.html",
    "has_placeholders": True,
    "main_img_src": f"../blog/images/{BUTTERFLY_SLUG}/butterfly-craft.webp",
    "images": [
        {
            "filename": "butterfly-craft.webp",
            "label": "Featured — finished butterfly",
            "prompt": (
                "A beautifully presented completed paper plate butterfly craft on a white table. "
                "The butterfly wings are a single paper plate with symmetrical painted patterns "
                "on both halves: pink, purple, and blue blobs and swirls, identical mirror image. "
                "A black clothespin is clipped to the center fold as the body, with two googly eyes "
                "and two pipe cleaner antennae with curled tips at the top. "
                "The wings are spread open showing the beautiful symmetrical design. "
                "Charming, colorful, clearly handmade. Child's hands may hold it up. "
                f"{STYLE}"
            ),
        },
        {
            "filename": "folding-paper-plate.webp",
            "label": "Step 1 — Fold the paper plate",
            "prompt": (
                "Tutorial step 1: folding a white paper plate in half. "
                "A child's hands (age 4-6) pressing a plain white paper plate firmly in half "
                "along the center crease, creating two equal wing-shaped halves. "
                "The plate is being held with both hands pressing the fold. "
                "The table shows paint supplies (pink, purple, blue tempera paint in cups) "
                "waiting nearby, but no paint applied yet. "
                "Plate is still perfectly white and clean — this is the very first step. "
                f"{STYLE}"
            ),
        },
        {
            "filename": "painting-wings.webp",
            "label": "Step 2 — Paint one wing",
            "prompt": (
                "Tutorial step 2: painting one half of the unfolded paper plate. "
                "A child (age 4-6) using a chunky paintbrush to add bright blobs of pink, "
                "purple, and blue paint on ONE half of the unfolded paper plate. "
                "The plate is fully open and flat. The left half has colorful paint blobs, "
                "dots, and swirls in pink, purple, and blue. The right half is still plain white. "
                "Cups of pink, purple, blue paint and other brushes on the white table. "
                "Child is actively painting, mid-stroke. "
                f"{STYLE}"
            ),
        },
        {
            "filename": "symmetrical-print-reveal.webp",
            "label": "Step 3 — Symmetrical print reveal",
            "prompt": (
                "Tutorial step 3: the magical symmetrical print reveal. "
                "A child opening the folded paper plate to reveal a beautiful symmetrical "
                "butterfly wing pattern. "
                "The plate is being held open, both halves now visible with identical mirrored "
                "paint patterns in pink, purple, and blue on both sides — same blobs and swirls, "
                "perfectly mirrored. "
                "Child's expression shows pure delight and amazement at the reveal. "
                "Wet paint visible, shiny and fresh. No clothespin or antennae yet. "
                f"{STYLE}"
            ),
        },
        {
            "filename": "clothespin-body-antennae.webp",
            "label": "Step 4 — Prep the clothespin body",
            "prompt": (
                "Tutorial step 4: preparing the butterfly's clothespin body. "
                "A child's hands holding a wooden clothespin that has been painted black. "
                "Two pipe cleaner pieces with curled/spiral tips are attached at the top of "
                "the clothespin as antennae. Two googly eyes are glued onto the flat face of "
                "the clothespin. "
                "On the white table: the dried symmetrically-painted paper plate wings are "
                "visible in the background (pink, purple, blue pattern on both halves). "
                "The clothespin face looks cute and bug-like. "
                f"{STYLE}"
            ),
        },
        {
            "filename": "finished-butterfly.webp",
            "label": "Step 5 — Assemble and display",
            "prompt": (
                "Tutorial step 5: the completed paper plate butterfly being proudly displayed. "
                "A smiling child (age 4-6) holding up or displaying the finished butterfly. "
                "The butterfly has: two wings from the paper plate (symmetrical pink, purple, "
                "blue painted patterns on both halves, plate folded so wings spread open), "
                "a black clothespin clipped to the center fold as the body, two googly eyes "
                "on the clothespin, and two pipe cleaner antennae with curled tips at the top. "
                "Child is beaming with pride. Warm, joyful, family-friendly scene. "
                f"{BUTTERFLY_ANCHOR} {STYLE}"
            ),
        },
    ],
})

# ---------------------------------------------------------------------------
# 4. LADYBUG  (easy-paper-plate-ladybug-craft-for-toddlers)
# ---------------------------------------------------------------------------
LADYBUG_ANCHOR = (
    "VISUAL CONSISTENCY: The craft is a paper plate ladybug. "
    "The plate is a standard 9-inch white paper plate, dome side painted solid bright red. "
    "A black construction paper half-circle (about 1/3 of the plate's diameter) is glued "
    "to the top edge as the head, with two googly eyes. "
    "6-8 black circular spots are on the red wing area. "
    "A black marker line runs down the center of the red plate dividing the wings. "
    "Two short black paper antennae curve up from behind the head. "
    "Keep the same red, same black head, same spots in every image."
)

LADYBUG_SLUG = "easy-paper-plate-ladybug-craft-for-toddlers"
ARTICLES.append({
    "slug": LADYBUG_SLUG,
    "html_file": BASE_DIR / "blog" / f"{LADYBUG_SLUG}.html",
    "has_placeholders": False,
    "main_img_src": f"../blog/images/{LADYBUG_SLUG}/paper-plate-ladybug-craft.webp",
    "images": [
        {
            "filename": "paper-plate-ladybug-craft.webp",
            "label": "Featured — finished ladybug",
            "prompt": (
                "A beautifully presented completed paper plate ladybug craft on a white table. "
                "The ladybug is a 9-inch paper plate (dome side up) painted solid bright red. "
                "A black construction paper half-circle is glued to the top as the head, "
                "with two large googly eyes. 6-8 black circle spots decorate the red wings. "
                "A black marker line runs down the center dividing the wings. "
                "Two short black paper antennae curve upward from behind the head. "
                "Charming, clearly handmade, warm natural light. Pinterest-worthy. "
                f"{STYLE}"
            ),
        },
        {
            "filename": "toddler-painting-bottom.webp",
            "label": "Step 1 — Paint the plate red",
            "prompt": (
                "Tutorial step 1: painting the back of a paper plate red. "
                "A toddler (age 2-4) using a chunky paintbrush to paint the DOME/BOTTOM side "
                "of a white paper plate bright red. The plate is UPSIDE DOWN (dome facing up). "
                "About half the plate is painted red already, brush mid-stroke. "
                "A cup of bright red washable paint sits nearby. "
                "No spots, no head, no details yet — just the plate and red paint. "
                "Toddler is focused and engaged. "
                f"{STYLE}"
            ),
        },
        {
            "filename": "mom-helping-toddler.webp",
            "label": "Step 2 — Cut the black head",
            "prompt": (
                "Tutorial step 2: cutting the black construction paper head. "
                "An adult's hands using scissors to cut a half-circle shape from black "
                "construction paper. The half-circle is roughly 1/3 the diameter of the plate. "
                "The fully dried, solid bright red paper plate (dome side up, no spots yet) "
                "is visible beside it on the white table. "
                "Black construction paper and scissors are the main focus. "
                "Head not yet glued — this is just the cutting step. "
                f"{STYLE}"
            ),
        },
        {
            "filename": "toddler-sticking-precut.webp",
            "label": "Step 3 — Add the spots",
            "prompt": (
                "Tutorial step 3: adding black spots to the red ladybug wings. "
                "A toddler's fingers pressing a black circle sticker or small black paper circle "
                "onto the bright red dome of the paper plate. "
                "4-5 black circles are already stuck on the red surface as spots. "
                "The red plate (dome up) is clearly the main focus. "
                "The black head half-circle is nearby on the table, not yet glued on. "
                "A sheet of black circle stickers or pre-cut black circles sit nearby. "
                f"{LADYBUG_ANCHOR} {STYLE}"
            ),
        },
        {
            "filename": "toddler-gluing-small.webp",
            "label": "Step 4 — Attach head and eyes",
            "prompt": (
                "Tutorial step 4: gluing the black head onto the ladybug. "
                "A toddler's hands pressing the black construction paper half-circle head "
                "onto the top edge of the red paper plate. "
                "A glue stick is being used. "
                "The red plate below clearly shows 6-8 black circle spots on the red surface. "
                "Two large googly eyes are already on the black head piece, staring forward. "
                "The ladybug is taking shape — red spotted body, black head with eyes. "
                f"{LADYBUG_ANCHOR} {STYLE}"
            ),
        },
        {
            "filename": "toddler-gluing-two.webp",
            "label": "Step 5 — Finishing touches",
            "prompt": (
                "Tutorial step 5: finishing the ladybug and showing it off. "
                "A happy, smiling toddler (age 2-4) proudly holding up the completed "
                "paper plate ladybug. "
                "The ladybug shows: bright red dome with 6-8 black circle spots, "
                "black construction paper half-circle head with two googly eyes, "
                "a black marker line down the center of the red body, "
                "and two short black paper antennae curving up from behind the head. "
                "Toddler's face radiates joy and pride. Warm, cozy, family-friendly. "
                f"{LADYBUG_ANCHOR} {STYLE}"
            ),
        },
    ],
})


# ===========================================================================
# Image generation
# ===========================================================================

def generate_image(client, prompt: str, output_path: Path) -> bool:
    try:
        from google.genai import types as genai_types
        from PIL import Image as PILImage

        full_prompt = (f"{prompt} Aspect ratio: 4:3. Wide rectangular landscape orientation.")
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


# ===========================================================================
# HTML updates
# ===========================================================================

def update_html_dimensions(html_path: Path):
    """Replace width="800" height="600" with 1200x900 in img tags."""
    text = html_path.read_text(encoding="utf-8")
    updated = text.replace('width="800" height="600"', 'width="1200" height="900"')
    if updated != text:
        html_path.write_text(updated, encoding="utf-8")
        log.info(f"  Updated image dimensions in {html_path.name}")


def inject_images_into_html(html_path: Path, article: dict, generated: dict):
    """
    For articles with placeholder divs, replace them with real <img> tags.
    Also injects the main featured image.
    """
    text = html_path.read_text(encoding="utf-8")

    # Inject main image (replace img-placeholder--main or insert after <article>)
    main_info = generated.get("main")
    if main_info and main_info.get("ok"):
        main_src = article["main_img_src"]
        main_alt = f"Completed {article['slug'].replace('-', ' ')} craft"
        main_fig = (
            f'<figure class="article-main-img">'
            f'<img src="{main_src}" alt="{main_alt}" '
            f'width="{TARGET_W}" height="{TARGET_H}" loading="eager">'
            f'</figure>'
        )
        # If there's already a main-img figure, replace it
        if 'class="article-main-img"' in text:
            text = re.sub(
                r'<figure class="article-main-img">.*?</figure>',
                main_fig,
                text, flags=re.DOTALL
            )
        else:
            # Insert after opening <article ...> tag
            text = re.sub(
                r'(<article\b[^>]*>)',
                r'\1\n      ' + main_fig + '\n',
                text, count=1
            )

    # Replace placeholder divs for each step
    images = article["images"][1:]  # skip main, steps are index 1-5
    for i, img_def in enumerate(images, start=1):
        step_info = generated.get(f"step_{i}")
        if not step_info or not step_info.get("ok"):
            continue
        src = f"../blog/images/{article['slug']}/{img_def['filename']}"
        alt = img_def["label"].replace('"', "&quot;")
        fig_html = (
            f'<figure class="article-step-img">'
            f'<img src="{src}" alt="{alt}" '
            f'width="{TARGET_W}" height="{TARGET_H}" loading="lazy">'
            f'</figure>'
        )
        # Replace: <div class="img-placeholder img-placeholder--step" ...>Step N 🖐️</div>
        pattern = (
            r'<div class="img-placeholder img-placeholder--step"[^>]*>'
            rf'Step\s+{i}\s*🖐️</div>'
        )
        new_text = re.sub(pattern, fig_html, text, count=1)
        if new_text != text:
            text = new_text
        else:
            log.warning(f"  Could not find placeholder for step {i}")

    html_path.write_text(text, encoding="utf-8")
    log.info(f"  HTML updated: {html_path.name}")


# ===========================================================================
# Main
# ===========================================================================

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

    client = genai.Client(api_key=api_key)
    total_ok = total_fail = 0

    for article in ARTICLES:
        slug = article["slug"]
        img_dir = BASE_DIR / "blog" / "images" / slug
        img_dir.mkdir(parents=True, exist_ok=True)
        images = article["images"]

        log.info("")
        log.info(f"{'='*60}")
        log.info(f"ARTICLE: {slug}")
        log.info(f"{'='*60}")

        generated = {}  # key → {ok: bool}

        for idx, img_def in enumerate(images):
            key = "main" if idx == 0 else f"step_{idx}"
            label = img_def["label"]
            filename = img_def["filename"]
            output_path = img_dir / filename

            log.info(f"\n[{label}]  →  {filename}")
            ok = generate_with_retry(client, img_def["prompt"], output_path)
            generated[key] = {"ok": ok}
            if ok:
                total_ok += 1
            else:
                total_fail += 1
                log.error(f"  FAILED after {MAX_RETRIES} retries")

            time.sleep(2)

        # Update HTML
        log.info(f"\n  Updating HTML for {slug}...")
        html_path = article["html_file"]
        if article["has_placeholders"]:
            inject_images_into_html(html_path, article, generated)
        else:
            update_html_dimensions(html_path)

    log.info("")
    log.info("=" * 60)
    log.info(f"DONE: {total_ok} images saved, {total_fail} failed")


if __name__ == "__main__":
    main()
