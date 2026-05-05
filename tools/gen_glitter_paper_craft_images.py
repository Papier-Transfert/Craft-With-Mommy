#!/usr/bin/env python3
"""Generate all images for glitter-paper-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "glitter-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "glitter-paper-craft.webp",
        "prompt": (
            "A finished handmade rainbow greeting card glitter paper craft displayed "
            "flat on a white craft table. White cardstock card base folded in half. "
            "On the front, a rainbow made of six layered curved arch strips of glitter "
            "paper in red, orange, yellow, green, blue, and purple sparkly cardstock, "
            "stacked from largest at the bottom to smallest at the top. Two fluffy "
            "white cotton ball clouds glued at the bottom ends of the rainbow. "
            "A small pink glitter paper heart sits in the sky next to the rainbow. "
            "The glitter paper sparkles softly in the daylight. Edges are slightly "
            "uneven, clearly cut by a child. Charming and cheerful. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "glitter-paper-craft-mom-child.webp",
        "prompt": (
            "A mom and her young preschool-aged daughter sitting close together at a "
            "white wooden craft table, smiling and excited to start a glitter paper craft. "
            "On the table in front of them: a stack of A4 sized sparkly glitter paper "
            "sheets in red, pink, gold, blue, green, and purple, plus a piece of white "
            "cardstock, kid scissors with red handles, and a purple glue stick. "
            "Mom is gently helping the child pick a sheet of glitter paper. Warm, "
            "cozy family moment. The glitter paper visibly catches the light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "glitter-paper-craft-card-base.webp",
        "prompt": (
            "A single sheet of plain white 8.5 by 11 inch heavy cardstock folded "
            "neatly in half to form a greeting card base. The folded card sits "
            "centered on a white wood craft table. Beside the card on the table: "
            "kid scissors with red handles and a small ruler. No glitter paper yet, "
            "just the clean white folded card base ready to be decorated. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "glitter-paper-craft-cut-arches.webp",
        "prompt": (
            "Six curved rainbow arch strips cut from sparkly glitter cardstock paper, "
            "in the colors red, orange, yellow, green, blue, and purple, arranged in "
            "a stair-stepped row on a white craft table from largest to smallest. "
            "Each arch is a half-moon shape, slightly uneven and clearly cut by hand. "
            "Beside the arches: a folded white cardstock card base, kid scissors "
            "with red handles, and small leftover glitter paper scraps. "
            "The glitter sparkles softly in the natural light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "glitter-paper-craft-glue-rainbow.webp",
        "prompt": (
            "A folded white cardstock greeting card lying flat on a white craft table, "
            "with the rainbow arches now glued onto the front of the card. The largest "
            "red glitter paper arch sits at the bottom, then orange, yellow, green, blue, "
            "and purple arches stacked above it from largest to smallest, forming a "
            "complete rainbow. The arches are glued slightly off-center, clearly handmade. "
            "A small purple glue stick sits next to the card. The glitter paper sparkles. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "glitter-paper-craft-add-clouds.webp",
        "prompt": (
            "The front of a white folded cardstock greeting card on a white craft table "
            "showing a complete six-color rainbow made of red, orange, yellow, green, "
            "blue, and purple sparkly glitter paper arches glued in a stack. Now two "
            "fluffy white cotton ball clouds have been glued onto the card at the "
            "bottom left and bottom right ends of the rainbow, where the arches meet "
            "the card. A purple glue stick sits beside the card. Charming and "
            "clearly handmade, with the glitter sparkling softly. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "glitter-paper-craft-add-heart.webp",
        "prompt": (
            "The front of a white folded cardstock greeting card on a white craft "
            "table showing a complete glittery rainbow made of red, orange, yellow, "
            "green, blue, and purple sparkly glitter paper arches, with two fluffy "
            "white cotton ball clouds at the bottom ends of the rainbow. Now a "
            "small bright pink glitter paper heart shape, about the size of a quarter, "
            "has been glued in the upper right area of the card next to the top of "
            "the rainbow. Tiny scraps of pink glitter paper sit beside the card. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "glitter-paper-craft-finished-card.webp",
        "prompt": (
            "The completely finished handmade rainbow greeting card glitter paper craft "
            "displayed proudly on a white craft table. The white cardstock folded card "
            "now shows the full sparkly six-color rainbow of glittered red, orange, "
            "yellow, green, blue, and purple arches, with two white cotton ball clouds "
            "at the bottom and a small pink glitter heart in the sky. The card has "
            "been opened slightly and stands up on its fold. The glitter paper "
            "sparkles softly in the warm window light. Charmingly imperfect, clearly "
            "made with love by a child. "
            f"{STYLE}"
        ),
    },
]


def generate_image(client, prompt, output_path):
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
