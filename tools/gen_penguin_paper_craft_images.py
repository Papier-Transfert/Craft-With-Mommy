#!/usr/bin/env python3
"""Generate all images for penguin-paper-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "penguin-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3, fills the frame edge to edge with no white borders or padding. "
    "No cartoon elements. Real construction paper craft materials only. "
    "Charming and slightly imperfect, clearly handmade by a young child. Pinterest-worthy."
)

PENGUIN_DESC = (
    "The penguin is a flat paper collage with a tall chubby black construction paper oval body, "
    "a smaller white construction paper oval glued onto the lower front as the belly, "
    "a small orange triangle beak above the white belly, two googly eyes above the beak, "
    "two soft pink marker cheek dots, two narrow black oval flippers on the sides of the body, "
    "and two small orange feet at the bottom."
)

IMAGES = [
    {
        "filename": "penguin-paper-craft.webp",
        "prompt": (
            "A finished handmade flat paper penguin craft glued onto a light blue construction paper background. "
            f"{PENGUIN_DESC} "
            "A tiny red paper scarf is glued around the penguin's neck. "
            "Several small white paper snowflake shapes are scattered around the blue background. "
            "Top-down flat lay photograph centered on the penguin scene, the entire blue paper fills the photo. "
            "Bright, cheerful, cozy winter feel. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "penguin-paper-craft-why-kids-love.webp",
        "prompt": (
            "A warm scene of a young American mother in her early thirties and her smiling child "
            "around 4 years old sitting together at a white craft table. On the table are sheets of black, white, "
            "orange, and light blue construction paper, a pair of kid scissors, a glue stick, and a small "
            "container of self-adhesive googly eyes. The mother is gently helping the child pick up a black "
            "paper oval to start the penguin paper craft. Both look happy and engaged. "
            "Cozy kitchen lighting. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "penguin-paper-craft-blue-background.webp",
        "prompt": (
            "A single full sheet of light blue construction paper laid flat in portrait orientation on a "
            "white craft table, completely empty and ready to be the snowy background for a penguin paper craft. "
            "A pencil, a pair of kid scissors, and a glue stick lie next to the blue paper on the side. "
            "Clean overhead photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "penguin-paper-craft-black-body.webp",
        "prompt": (
            "A tall chubby black construction paper oval, freshly cut to be the body of a paper penguin, "
            "lying flat on a white craft table next to a pair of kid scissors and a pencil. "
            "Some leftover black construction paper scraps lie at the edges. "
            "Just the black oval body and tools, no other penguin parts yet. "
            "Clean overhead photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "penguin-paper-craft-white-belly.webp",
        "prompt": (
            "A flat paper penguin in progress: a tall black construction paper oval body lying flat on a white "
            "craft table, with a smaller white construction paper oval freshly glued onto the lower front of "
            "the black body to form the rounded belly. No beak, no eyes, no flippers, no feet yet. "
            "Just the black body with the white belly attached. A glue stick is visible nearby. "
            "Clean overhead photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "penguin-paper-craft-orange-beak.webp",
        "prompt": (
            "A flat paper penguin in progress on a white craft table: a tall black construction paper oval "
            "body with a smaller white oval belly glued on, plus a small orange paper triangle beak now glued "
            "on the upper part of the body just above the white belly, pointing slightly downward. "
            "No eyes, no cheeks, no flippers, no feet yet. Just the black body, white belly, and orange beak. "
            "Clean overhead photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "penguin-paper-craft-googly-eyes-cheeks.webp",
        "prompt": (
            "A flat paper penguin in progress on a white craft table: a tall black oval body with white "
            "oval belly, an orange paper triangle beak, two googly eyes pressed onto the body above the beak "
            "with a small gap between them, and two soft pink marker cheek dots drawn just below and to the "
            "sides of the beak. No flippers, no feet yet. The penguin face now looks alive and friendly. "
            "Clean overhead photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "penguin-paper-craft-flippers-feet.webp",
        "prompt": (
            "A flat paper penguin almost finished on a white craft table: a tall black oval body with white "
            "oval belly, orange triangle beak, two googly eyes, pink cheek dots, two narrow black paper oval "
            "flippers glued to the sides of the body, and two small orange paper feet glued at the bottom of "
            "the body, peeking out side by side. No scarf, no snowflakes yet. Just the full penguin silhouette. "
            "Clean overhead photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "penguin-paper-craft-finished-scarf-snowflakes.webp",
        "prompt": (
            "A finished handmade flat paper penguin craft glued in the middle of a light blue construction "
            f"paper background. {PENGUIN_DESC} "
            "A tiny red paper scarf with gently fringed ends is glued around the penguin's neck. "
            "Six or seven small white paper snowflake shapes are scattered around the blue background. "
            "The light blue background paper fills the entire photo from edge to edge. Bright cozy winter mood. "
            f"{STYLE}"
        ),
    },
]


def generate_image(client, prompt, output_path):
    from google.genai import types as genai_types
    from PIL import Image as PILImage
    full_prompt = f"{prompt} Aspect ratio: 4:3. Wide rectangular landscape orientation, fills the frame, no white borders."
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
        w, h = img.size
        target_ratio = TARGET_W / TARGET_H
        current_ratio = w / h
        if current_ratio > target_ratio:
            new_w = int(h * target_ratio)
            left = (w - new_w) // 2
            img = img.crop((left, 0, left + new_w, h))
        elif current_ratio < target_ratio:
            new_h = int(w / target_ratio)
            top = (h - new_h) // 2
            img = img.crop((0, top, w, top + new_h))
        resized = img.resize((TARGET_W, TARGET_H), PILImage.LANCZOS)
        resized.save(output_path, "WEBP", quality=82, method=6)

    size_kb = output_path.stat().st_size // 1024
    log.info(f"  Saved: {output_path.name} ({TARGET_W}x{TARGET_H}px, {size_kb}KB)")
    return True


def main():
    import google.genai as genai
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        log.error("GOOGLE_API_KEY not set")
        return

    IMG_DIR.mkdir(parents=True, exist_ok=True)
    client = genai.Client(api_key=api_key)

    for img in IMAGES:
        out = IMG_DIR / img["filename"]
        if out.exists():
            log.info(f"SKIP (exists): {img['filename']}")
            continue
        log.info(f"Generating {img['filename']}...")
        success = False
        for attempt in range(1, MAX_RETRIES + 1):
            if attempt > 1:
                log.info(f"  Retry {attempt}/{MAX_RETRIES}...")
                time.sleep(3)
            try:
                if generate_image(client, img["prompt"], out):
                    success = True
                    break
            except Exception as e:
                log.warning(f"  Error: {e}")
            time.sleep(2)
        if not success:
            log.error(f"  FAILED after {MAX_RETRIES} attempts: {img['filename']}")
        time.sleep(2)

    log.info("All done.")


if __name__ == "__main__":
    main()
