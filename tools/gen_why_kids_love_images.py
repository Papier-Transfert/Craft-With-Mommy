#!/usr/bin/env python3
"""
gen_why_kids_love_images.py — Generate "Why Kids Love" supporting images for 5 articles.
"""

import io
import os
import sys
import time
import logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

load_dotenv(BASE_DIR / ".env")

IMAGES = [
    {
        "slug": "craft-using-paper",
        "prompt": (
            "A warm, joyful scene of a young child (ages 3-5) and a mom sitting together at a light wood craft table, "
            "both smiling and excited to start crafting. On the table: strips of colorful construction paper, a glue stick, "
            "safety scissors, and googly eyes. Nothing has been made yet — this is the happy anticipation before starting. "
            "Mood: warm, cozy, inviting. Realistic photo style. Warm natural daylight from a window. "
            "White or light wood craft table surface. Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3."
        ),
    },
    {
        "slug": "easy-paper-plate-butterfly-craft-for-preschoolers",
        "prompt": (
            "A warm, joyful scene of a young child (ages 3-5) and a mom sitting together at a light wood craft table, "
            "both smiling and excited to start crafting. On the table: a white paper plate, pots of colorful washable tempera paint, "
            "paintbrushes, tissue paper scraps, and pipe cleaners. Nothing has been made yet — this is the happy anticipation before starting. "
            "Mood: warm, cozy, inviting. Realistic photo style. Warm natural daylight from a window. "
            "White or light wood craft table surface. Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3."
        ),
    },
    {
        "slug": "easy-paper-plate-ladybug-craft-for-toddlers",
        "prompt": (
            "A warm, joyful scene of a young child (ages 2-4) and a mom sitting together at a light wood craft table, "
            "both smiling and excited to start crafting. On the table: a white paper plate, red and black washable tempera paint, "
            "paintbrushes, black cardstock, and a glue stick. Nothing has been made yet — this is the happy anticipation before starting. "
            "Mood: warm, cozy, inviting. Realistic photo style. Warm natural daylight from a window. "
            "White or light wood craft table surface. Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3."
        ),
    },
    {
        "slug": "easy-paper-plate-rainbow-fish-craft-for-toddlers",
        "prompt": (
            "A warm, joyful scene of a young child (ages 2-4) and a mom sitting together at a light wood craft table, "
            "both smiling and excited to start crafting. On the table: a white paper plate, colorful tissue paper squares, "
            "glue, safety scissors, and sequins or shiny stickers. Nothing has been made yet — this is the happy anticipation before starting. "
            "Mood: warm, cozy, inviting. Realistic photo style. Warm natural daylight from a window. "
            "White or light wood craft table surface. Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3."
        ),
    },
    {
        "slug": "paper-flower-craft",
        "prompt": (
            "A warm, joyful scene of a young child (ages 3-6) and a mom sitting together at a light wood craft table, "
            "both smiling and excited to start crafting. On the table: colorful tissue paper squares, green pipe cleaners, "
            "scissors, and a pencil. Nothing has been made yet — this is the happy anticipation before starting. "
            "Mood: warm, cozy, inviting. Realistic photo style. Warm natural daylight from a window. "
            "White or light wood craft table surface. Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3."
        ),
    },
]


def generate_image(client, prompt: str, output_path: Path) -> bool:
    try:
        from google.genai import types as genai_types
        from PIL import Image as PILImage

        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=prompt,
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
            resized = img.resize((1200, 900), PILImage.LANCZOS)
            resized.save(output_path, "WEBP", quality=82, method=6)

        size_kb = output_path.stat().st_size // 1024
        log.info(f"  Saved: {output_path} ({size_kb} KB)")
        return True

    except Exception as exc:
        log.warning(f"  Generation failed: {exc}")
        return False


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
    results = {"success": 0, "failed": 0}

    for img in IMAGES:
        slug = img["slug"]
        output_path = BASE_DIR / "blog" / "images" / slug / f"{slug}-why-kids-love.webp"

        log.info(f"Generating: {output_path.name} for {slug}")
        MAX_RETRIES = 3
        success = False
        for attempt in range(1, MAX_RETRIES + 1):
            if attempt > 1:
                log.info(f"  Retry {attempt}/{MAX_RETRIES}...")
                time.sleep(5)
            success = generate_image(client, img["prompt"], output_path)
            if success:
                break
            time.sleep(3)

        if success:
            results["success"] += 1
        else:
            log.error(f"  FAILED after {MAX_RETRIES} attempts")
            results["failed"] += 1

        time.sleep(3)

    log.info(f"Done: {results['success']} succeeded, {results['failed']} failed")


if __name__ == "__main__":
    main()
