#!/usr/bin/env python3
"""
regen_turtle_images.py — Regenerate step images for the turtle article
with accurate, continuity-preserving prompts.

Usage:
    python3 /var/www/craft-with-mommy/tools/regen_turtle_images.py

Overwrites the 6 existing WebP files in:
    /var/www/craft-with-mommy/blog/images/easy-paper-plate-turtle-craft-for-preschoolers/
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
SLUG = "easy-paper-plate-turtle-craft-for-preschoolers"
IMG_DIR = BASE_DIR / "blog" / "images" / SLUG
MAX_RETRIES = 3

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
log = logging.getLogger(__name__)

load_dotenv(BASE_DIR / ".env")

# ---------------------------------------------------------------------------
# Visual consistency anchor (shared across all prompts)
# ---------------------------------------------------------------------------
CRAFT_ANCHOR = (
    "The craft throughout all steps uses these exact consistent elements: "
    "a standard white 9-inch paper plate (dome side = turtle shell, painted solid light green), "
    "four small stubby paddle-shaped legs cut from green cardstock (~1.5 inches each), "
    "one small green cardstock teardrop tail, "
    "one green cardstock oval head (~2-3 inches), "
    "two plastic googly eyes on the head, "
    "a black marker curved smile on the head, "
    "and a black marker hexagon shell pattern on the green dome. "
    "All pieces are the same shade of medium leaf green throughout every step."
)

PHOTO_STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. "
    "Landscape orientation 4:3. "
    "Slightly angled tutorial composition — instructional yet warm."
)

# ---------------------------------------------------------------------------
# Image definitions: filename → prompt
# ---------------------------------------------------------------------------
IMAGES = [
    {
        "filename": "paper-plate-turtle-craft.webp",
        "label": "Featured / Main image",
        "prompt": (
            "A finished paper plate turtle craft displayed attractively on a white craft table. "
            "The turtle is a standard white 9-inch paper plate with the dome side facing up, "
            "painted solid light green. Four small stubby paddle-shaped green cardstock legs "
            "extend from the four sides of the plate. A small green cardstock teardrop tail "
            "peeks out at the bottom edge. A green cardstock oval head sits at the top edge "
            "with two plastic googly eyes and a black marker curved smile. "
            "The green dome shell has a black marker hexagon pattern drawn on it. "
            "The turtle is centered on the table, well-lit, slightly angled view from above. "
            "The photo looks like a beautiful Pinterest-worthy craft result — "
            "attractive but 100% realistic, no cartoon elements. "
            f"{PHOTO_STYLE}"
        ),
    },
    {
        "filename": "child-painting-bottom.webp",
        "label": "Step 1 — Paint the turtle shell",
        "prompt": (
            "Close-up of a young child's hands (ages 3-5) actively painting a paper plate "
            "with a wide paintbrush loaded with bright green washable tempera paint. "
            "CRITICAL: The paper plate is upside down — the dome/rounded bottom side is facing UP "
            "and the child is painting that dome surface green. The concave inner side faces down. "
            "The plate is about half painted green already, with the brush mid-stroke showing active painting. "
            "A small cup or tray of light green tempera paint sits nearby on the table. "
            "No other craft pieces are visible yet — this is the very first step, just plate and paint. "
            f"{PHOTO_STYLE}"
        ),
    },
    {
        "filename": "mom-helping-child.webp",
        "label": "Step 2 — Cut out the body parts",
        "prompt": (
            "A mom's hands guiding a young child's hands (ages 3-5) using child safety scissors "
            "to cut shapes from a sheet of medium green cardstock/construction paper. "
            "On the white table, already cut pieces are visible nearby: "
            "two small stubby paddle-shaped green leg pieces (~1.5 inches) "
            "and one small green teardrop-shaped tail piece. "
            "The child is currently cutting another leg shape. "
            "The painted green paper plate (dome side up, now dry and fully green) "
            "sits to the side on the table, visibly waiting for the next step. "
            "A green oval head shape (~2-3 inches) is also cut and sitting on the table. "
            "Warm collaborative scene — mom and child working together. "
            f"{PHOTO_STYLE}"
        ),
    },
    {
        "filename": "child-gluing-four.webp",
        "label": "Step 3 — Assemble the turtle",
        "prompt": (
            "Close-up of a young child's hands pressing a small stubby green cardstock leg "
            "onto the edge of the green-painted paper plate. "
            "The paper plate is right-side up with the green painted dome facing UP (this is the shell). "
            "Two green cardstock legs are already glued on the left side of the plate, visible. "
            "One leg is already glued on the right side. "
            "The child is pressing down a fourth leg on the lower right edge. "
            "A small green oval head piece and a small green tail piece sit nearby on the table, "
            "not yet glued. A glue stick lies on the table. "
            "The turtle is clearly taking shape with legs around the green dome shell. "
            f"{CRAFT_ANCHOR} "
            f"{PHOTO_STYLE}"
        ),
    },
    {
        "filename": "child-cutting-out.webp",
        "label": "Step 4 — Add the shell details",
        "prompt": (
            "Close-up of a young child's hands holding a black washable marker, "
            "drawing a hexagon shell pattern on the green-painted dome of the paper plate turtle. "
            "The assembled turtle is on the table: green painted dome shell facing up, "
            "four small green cardstock legs extending from the sides, "
            "a small green teardrop tail at the bottom, "
            "and a green oval head piece glued at the top. "
            "The head already has two googly eyes on it. "
            "The child is actively drawing black hexagon outlines on the green shell surface. "
            "Some hexagons are already drawn on part of the shell, others still plain green. "
            "Black marker lies nearby. "
            f"{CRAFT_ANCHOR} "
            f"{PHOTO_STYLE}"
        ),
    },
    {
        "filename": "child-gluing-finished.webp",
        "label": "Step 5 — Give the turtle a face",
        "prompt": (
            "Close-up of a young child's fingers pressing a plastic googly eye "
            "onto a green cardstock oval head shape. "
            "The full assembled turtle is visible on the table: "
            "green painted dome shell (facing up) with black hexagon pattern drawn on it, "
            "four green cardstock legs at the sides, small green tail at bottom, "
            "and the oval head at the top — the other googly eye is already stuck on the head. "
            "A black marker sits nearby for drawing the smile. "
            "The turtle is nearly complete — just the final face details being added. "
            "Child's expression shows delight and focus. "
            "Warm, joyful, cozy family craft atmosphere. "
            f"{CRAFT_ANCHOR} "
            f"{PHOTO_STYLE}"
        ),
    },
]

# ---------------------------------------------------------------------------
# Image generation
# ---------------------------------------------------------------------------

def generate_image(client, prompt: str, output_path: Path) -> bool:
    """Generate one image, save as WebP. Returns True on success."""
    try:
        from google.genai import types as genai_types
        from PIL import Image as PILImage

        full_prompt = f"{prompt} Aspect ratio: 4:3. Landscape orientation."

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
            img.save(output_path, "WEBP", quality=75, method=6)

        size_kb = output_path.stat().st_size // 1024
        log.info(f"  Saved: {output_path.name} ({size_kb} KB)")
        return True

    except Exception as exc:
        log.warning(f"  Generation failed: {exc}")
        return False


def main():
    # Validate dependencies
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
    log.info(f"Output directory: {IMG_DIR}")
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
            log.error(f"  FAILED after {MAX_RETRIES} attempts — keeping original file")
            results["failed"] += 1

        log.info("")
        time.sleep(2)  # Rate limiting between images

    log.info("=" * 50)
    log.info(f"Done: {results['success']} succeeded, {results['failed']} failed")
    if results["failed"] == 0:
        log.info("All images regenerated successfully!")
        log.info(f"View article at: https://craft-with-mommy.com/blog/{SLUG}.html")
    else:
        log.warning("Some images failed — originals preserved for failed ones.")


if __name__ == "__main__":
    main()
