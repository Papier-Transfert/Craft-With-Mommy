#!/usr/bin/env python3
"""
gen_hero_image.py
Generate the homepage hero lifestyle image and save to images/hero-lifestyle.webp
"""

import io, os, sys, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "images"
OUTPUT_PATH = OUTPUT_DIR / "hero-lifestyle.webp"
TARGET_W, TARGET_H = 1400, 933   # ~3:2, wide landscape for hero

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

PROMPT = (
    "A warm, natural lifestyle photograph. A young American mother, early 30s, casual style, "
    "hair loosely pulled back in a bun, wearing a soft grey or cream knit sweater, sitting at "
    "a rustic light wooden dining table with her two young children: a boy around 5-6 years old "
    "and a girl around 3-4 years old. They are all doing a simple paper craft together — making "
    "small felt shapes and simple paper animals using felt pieces, glue sticks, foam stickers, "
    "and a few colorful paper sheets. The children are smiling and laughing naturally, genuinely "
    "engaged and happy. The mother is leaning in warmly, looking at the craft with a big genuine "
    "smile, emotionally present and connected, not posed. The crafts on the table include colorful "
    "felt shapes, a few completed cute felt animal pieces, glue sticks, and simple craft supplies "
    "— the table is clean, tidy, and inviting, not messy or chaotic. Background: warm, softly "
    "blurred cozy home interior with light wooden shelves in the background holding books and a "
    "few small handmade decorative objects, nothing distracting. Lighting: soft, golden natural "
    "daylight from a window to the right, warm color temperature around 5000K, gentle soft "
    "shadows, no harsh flash. The overall mood is cozy, joyful, low-stress, premium lifestyle "
    "photography. Composition: the family and table activity fill the right two-thirds of the "
    "frame; the left edge of the image is calmer and less busy, softly out of focus. Wide "
    "landscape orientation, 3:2 ratio. No AI artifacts, no distorted fingers or hands, no fake "
    "plastic skin texture, no hyper-processed look. True photographic realism, premium quality, "
    "natural facial expressions, authentic family moment."
)


def generate_image(client, prompt: str, output_path: Path) -> bool:
    try:
        from google.genai import types as genai_types
        from PIL import Image as PILImage

        full_prompt = f"{prompt} Aspect ratio 3:2. Wide rectangular landscape orientation."
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
            log.warning("No image data returned.")
            return False
        with PILImage.open(io.BytesIO(image_bytes)) as img:
            resized = img.resize((TARGET_W, TARGET_H), PILImage.LANCZOS)
            resized.save(output_path, "WEBP", quality=85, method=6)
        size_kb = output_path.stat().st_size // 1024
        log.info(f"Saved: {output_path} ({TARGET_W}x{TARGET_H}px, {size_kb}KB)")
        return True
    except Exception as exc:
        log.warning(f"Failed: {exc}")
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

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    client = genai.Client(api_key=api_key)

    log.info("Generating hero lifestyle image...")
    for attempt in range(1, 4):
        if attempt > 1:
            log.info(f"Retry {attempt}/3...")
            time.sleep(4)
        if generate_image(client, PROMPT, OUTPUT_PATH):
            log.info("Done.")
            return
    log.error("All attempts failed.")
    sys.exit(1)


if __name__ == "__main__":
    main()
