#!/usr/bin/env python3
"""
gen_turtle_why_image.py — Generate the "Why Kids Love" supporting image
for the turtle article.

Saves to:
    blog/images/easy-paper-plate-turtle-craft-for-preschoolers/turtle-craft-kids-love.webp
"""

import io
import os
import sys
import time
import logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR = BASE_DIR / "blog" / "images" / "easy-paper-plate-turtle-craft-for-preschoolers"
OUTPUT_PATH = IMG_DIR / "turtle-craft-kids-love.webp"
MAX_RETRIES = 3

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
log = logging.getLogger(__name__)

load_dotenv(BASE_DIR / ".env")

PHOTO_STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. "
    "Landscape orientation 4:3. "
    "Slightly angled tutorial composition — instructional yet warm."
)

PROMPT = (
    "A warm, joyful scene of a young child (ages 3-5) and a mom sitting together "
    "at a light wood craft table, both smiling and clearly excited to start crafting. "
    "On the table in front of them: a standard white paper plate, "
    "small pots of green washable tempera paint, a couple of round paintbrushes, "
    "a sheet of green cardstock, a glue stick, and a small packet of googly eyes. "
    "No finished turtle visible yet — this is the happy anticipation before starting. "
    "The child looks engaged and delighted. The mom looks relaxed and present. "
    "Mood: warm, cozy, inviting, full of creative energy. "
    f"{PHOTO_STYLE} Aspect ratio: 4:3. Landscape orientation."
)


def generate_image(client, prompt: str, output_path: Path) -> bool:
    try:
        from google.genai import types as genai_types
        from PIL import Image as PILImage
    except ImportError as e:
        log.error(f"Missing dependency: {e}")
        sys.exit(1)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            log.info(f"Attempt {attempt}/{MAX_RETRIES} — generating {output_path.name}")
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
                log.warning(f"Attempt {attempt}: no image data returned")
                if attempt < MAX_RETRIES:
                    time.sleep(2)
                continue

            output_path.parent.mkdir(parents=True, exist_ok=True)
            with PILImage.open(io.BytesIO(image_bytes)) as img:
                resized = img.resize((1200, 900), PILImage.LANCZOS)
                resized.save(output_path, "WEBP", quality=82, method=6)

            size_kb = output_path.stat().st_size // 1024
            log.info(f"Saved: {output_path.name} ({size_kb} KB)")
            return True

        except Exception as exc:
            log.warning(f"Attempt {attempt} error: {exc}")
            if attempt < MAX_RETRIES:
                time.sleep(3)

    log.error(f"All {MAX_RETRIES} attempts failed.")
    return False


def main():
    try:
        from google import genai
    except ImportError:
        log.error("google-genai not installed. Run: pip3 install google-genai")
        sys.exit(1)

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        log.error("GOOGLE_API_KEY not set in .env")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    success = generate_image(client, PROMPT, OUTPUT_PATH)
    if success:
        log.info("Done.")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
