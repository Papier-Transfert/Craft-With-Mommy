#!/usr/bin/env python3
"""
regen_flower_images.py — Regenerate step images for the paper flower article
with accurate, step-matched prompts and 1200x900px rectangular output.

Usage:
    python3 /var/www/craft-with-mommy/tools/regen_flower_images.py

Overwrites the 6 existing WebP files in:
    /var/www/craft-with-mommy/blog/images/paper-flower-craft/
Output size: 1200x900 px (4:3, rectangular)
"""

import io
import os
import sys
import time
import logging
from pathlib import Path
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
SLUG = "paper-flower-craft"
IMG_DIR = BASE_DIR / "blog" / "images" / SLUG
TARGET_W, TARGET_H = 1200, 900          # New standard: 4:3 rectangular
MAX_RETRIES = 3

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
log = logging.getLogger(__name__)

load_dotenv(BASE_DIR / ".env")

# ---------------------------------------------------------------------------
# Visual consistency anchor — describes the craft design that appears in
# every step so the AI keeps the same materials and colors throughout
# ---------------------------------------------------------------------------
CRAFT_ANCHOR = (
    "VISUAL CONSISTENCY RULE: All step images must show the EXACT SAME craft "
    "evolving step by step. "
    "Each flower in this craft has: "
    "5-7 rounded teardrop-shaped petals (~3 inches tall) cut from bright construction paper "
    "(colors: pink, purple, orange — same colors in every image); "
    "a 2-3 inch yellow paper circle as the flower center; "
    "a 10-12 inch green paper strip stem (~1 inch wide); "
    "and 1-2 small pointed-oval green paper leaf shapes glued to the stem. "
    "The finished bouquet has 3-4 of these flowers together. "
    "Do NOT change petal color, shape, or flower design between images. "
    "Do NOT show elements from future steps too early."
)

PHOTO_STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. "
    "Landscape orientation. "
    "Slightly angled tutorial composition — instructional yet warm and inviting. "
    "No cartoon elements. Real craft materials only."
)

# ---------------------------------------------------------------------------
# Image definitions: filename → prompt
# ---------------------------------------------------------------------------
IMAGES = [
    {
        "filename": "paper-flower-craft.webp",
        "label": "Featured / Main image",
        "prompt": (
            "A beautifully presented completed paper flower bouquet craft displayed on a white craft table. "
            "The bouquet has 3-4 cheerful paper flowers: each flower has 5-7 rounded teardrop petals "
            "in bright colors (pink, purple, orange) fanned out around a small yellow paper circle center. "
            "Each flower has a long green paper strip stem (~10-12 inches) with 1-2 small green paper "
            "leaf shapes attached partway down. The flowers are gathered together as a bouquet. "
            "The photo is Pinterest-worthy — attractive, vibrant, realistic, warm. "
            "A young child's hands may be gently touching or holding the bouquet. "
            "Colorful and joyful — this is the hero image that makes a mom want to make this craft right now. "
            f"{PHOTO_STYLE}"
        ),
    },
    {
        "filename": "childs-hands-tracing.webp",
        "label": "Step 1 — Cut out the petals",
        "prompt": (
            "Tutorial photo for step 1 of a paper flower craft: cutting out petals. "
            "A young child's hands (ages 3-5) are tracing a rounded teardrop/petal shape (~3 inches tall) "
            "onto a folded piece of bright pink construction paper, using a pencil or crayon. "
            "A folded sheet of pink paper is under the child's hands, pencil mid-stroke on the paper. "
            "On the white craft table: sheets of colorful construction paper spread out "
            "(pink, purple, orange, yellow), a pair of child safety scissors, a glue stick. "
            "2-3 already-cut teardrop petal shapes in pink are visible on the table. "
            "NO assembled flower yet — this is the very first step, only loose paper and petals. "
            "The scene looks active and hands-on. "
            f"{PHOTO_STYLE}"
        ),
    },
    {
        "filename": "child-cutting-out.webp",
        "label": "Step 2 — Make the flower center",
        "prompt": (
            "Tutorial photo for step 2 of a paper flower craft: making the flower center circle. "
            "A young child's hands are tracing a small circle (2-3 inches) onto yellow construction paper "
            "using a small cup or jar lid pressed onto the paper as a template. "
            "Child safety scissors lie nearby, about to cut the circle out. "
            "On the white craft table: a small cup/lid being used as the circle template, "
            "yellow construction paper, and a pile of already-cut colorful teardrop petal shapes "
            "in pink, purple, and orange — the petals from step 1. "
            "No assembled flower yet — petals and soon-to-be-cut yellow center are loose on the table. "
            f"{PHOTO_STYLE}"
        ),
    },
    {
        "filename": "small-hands-layering.webp",
        "label": "Step 3 — Assemble the petals",
        "prompt": (
            "Tutorial photo for step 3 of a paper flower craft: assembling the petals around the center. "
            "A young child's small hands are pressing a colorful teardrop-shaped paper petal (pink or purple) "
            "onto the edge of a yellow paper circle (~2-3 inches), gluing it down. "
            "The yellow circle is face-down on the white table surface. "
            "3-4 teardrop petals in pink, purple, and orange are already glued around the circle edge, "
            "fanning outward like a sunburst. Child is adding another petal. "
            "A glue stick is on the table. "
            "Remaining loose petals (pink, orange) sit nearby waiting to be attached. "
            "No stem attached yet — this is just the flower head being assembled. "
            f"{CRAFT_ANCHOR} "
            f"{PHOTO_STYLE}"
        ),
    },
    {
        "filename": "child-gluing-green.webp",
        "label": "Step 4 — Attach the stem",
        "prompt": (
            "Tutorial photo for step 4 of a paper flower craft: attaching the green stem. "
            "A young child's hands are turning a completed paper flower FACE-DOWN on the white table. "
            "The back of the flower is visible: a yellow paper circle center with colorful teardrop petals "
            "(pink, purple, orange) fanned out around it, now seen from behind. "
            "Child is pressing a long green paper strip (~1 inch wide, ~10-12 inches long) "
            "onto the back center of the flower with a glue stick or tape. "
            "The green paper stem is being firmly attached to the back of the flower. "
            "A glue stick and tape dispenser are visible on the table. "
            "No leaves on the stem yet — this is step 4, leaves come in step 5. "
            f"{CRAFT_ANCHOR} "
            f"{PHOTO_STYLE}"
        ),
    },
    {
        "filename": "proud-toddler-holding.webp",
        "label": "Step 5 — Add leaves and display bouquet",
        "prompt": (
            "Tutorial photo for the final step 5 of a paper flower craft: the completed bouquet. "
            "A cheerful, smiling toddler (ages 2-4) is proudly holding up a completed paper flower bouquet. "
            "The bouquet has 3-4 paper flowers: each with 5-7 rounded teardrop petals "
            "in bright colors (pink, purple, orange), a yellow paper circle center, "
            "a long green paper strip stem, and 1-2 small pointed-oval green paper leaf shapes "
            "attached partway down the stem. "
            "The child's face shows pure joy and pride — big smile, eyes bright. "
            "The flowers are vibrant and clearly handmade. "
            "Warm, cozy home background with natural light. "
            "This is the triumphant final image — a happy child, a beautiful bouquet, "
            "a proud mom moment. Emotional and warm. "
            f"{PHOTO_STYLE}"
        ),
    },
]

# ---------------------------------------------------------------------------
# Image generation
# ---------------------------------------------------------------------------

def generate_image(client, prompt: str, output_path: Path,
                   target_w: int = TARGET_W, target_h: int = TARGET_H) -> bool:
    """Generate one image, resize to target dimensions, save as WebP.
    Returns True on success."""
    try:
        from google.genai import types as genai_types
        from PIL import Image as PILImage

        full_prompt = (
            f"{prompt} "
            f"Aspect ratio: 4:3. Landscape orientation. "
            f"Wide rectangular composition."
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=full_prompt,
            config=genai_types.GenerateContentConfig(
                response_modalities=["IMAGE"],
            ),
        )

        image_bytes = None
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_bytes = part.inline_data.data
                break

        if image_bytes is None:
            log.warning(f"No image data returned for {output_path.name}")
            return False

        with PILImage.open(io.BytesIO(image_bytes)) as img:
            # Resize to exact target dimensions (1200x900 = 4:3)
            resized = img.resize((target_w, target_h), PILImage.LANCZOS)
            resized.save(output_path, "WEBP", quality=82, method=6)

        size_kb = output_path.stat().st_size // 1024
        log.info(f"  Saved: {output_path.name} ({target_w}x{target_h}px, {size_kb} KB)")
        return True

    except Exception as exc:
        log.warning(f"  Generation failed: {exc}")
        return False


def main():
    try:
        from google import genai
    except ImportError:
        log.error("google-genai not installed. Run: pip3 install google-genai")
        sys.exit(1)
    try:
        from PIL import Image
    except ImportError:
        log.error("Pillow not installed. Run: pip3 install Pillow")
        sys.exit(1)

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        log.error("GOOGLE_API_KEY not set in .env")
        sys.exit(1)

    IMG_DIR.mkdir(parents=True, exist_ok=True)
    client = genai.Client(api_key=api_key)

    log.info(f"Regenerating {len(IMAGES)} images for: {SLUG}")
    log.info(f"Output: {TARGET_W}x{TARGET_H}px (4:3 rectangular) WebP")
    log.info(f"Directory: {IMG_DIR}")
    log.info("")

    results = {"success": 0, "failed": 0}

    for img in IMAGES:
        filename = img["filename"]
        label = img["label"]
        prompt = img["prompt"]
        output_path = IMG_DIR / filename

        log.info(f"[{label}]")
        log.info(f"  Target: {filename}")

        success = False
        for attempt in range(1, MAX_RETRIES + 1):
            if attempt > 1:
                log.info(f"  Retry {attempt}/{MAX_RETRIES}...")
                time.sleep(3)
            success = generate_image(client, prompt, output_path)
            if success:
                break
            time.sleep(2)

        if success:
            results["success"] += 1
        else:
            log.error(f"  FAILED after {MAX_RETRIES} attempts — original preserved")
            results["failed"] += 1

        log.info("")
        time.sleep(2)

    log.info("=" * 50)
    log.info(f"Done: {results['success']} succeeded, {results['failed']} failed")
    if results["failed"] == 0:
        log.info("All images regenerated successfully!")
        log.info(f"View: https://craft-with-mommy.com/blog/{SLUG}.html")
    else:
        log.warning("Some images failed — originals preserved for failed ones.")


if __name__ == "__main__":
    main()
