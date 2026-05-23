#!/usr/bin/env python3
"""Generate all images for paper-mosaic-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-mosaic-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "paper-mosaic-craft.webp",
        "prompt": (
            "A finished handmade paper mosaic craft of a colorful rainbow heart shape "
            "on a white cardstock sheet. The heart is filled with small fingernail-sized "
            "construction paper squares arranged in rainbow rows: red at the top, then "
            "orange, yellow, green, blue, and purple at the bottom. Small white gaps "
            "visible between each square creating a classic mosaic look. The background "
            "around the heart is filled with light blue paper squares. The cardstock sits "
            "flat on a light wood craft table with a few leftover colored squares, a glue "
            "stick, and child-safe scissors nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mosaic-craft-why-kids-love.webp",
        "prompt": (
            "A warm, candid photo of an American mom in her thirties and her young child "
            "around age five sitting close together at a light wood craft table. They are "
            "sorting small colorful construction paper squares into separate piles by color "
            "on the table. The child is smiling and reaching for a yellow square. The mom "
            "is watching with a soft smile. A sheet of white cardstock with a pencil heart "
            "outline lies on the table next to them. Glue stick and child scissors visible. "
            "Cozy, joyful family moment, warm natural daylight. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mosaic-craft-outline.webp",
        "prompt": (
            "A close-up flat lay of a single sheet of white cardstock on a light wood craft "
            "table. A large simple heart shape is lightly drawn in pencil in the center of "
            "the cardstock, taking up most of the page. The pencil line is thin and clean. "
            "Nothing else is on the cardstock yet. A sharpened pencil and a stack of colored "
            "construction paper sit at the edge of the frame. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mosaic-craft-cut-squares.webp",
        "prompt": (
            "A close-up flat lay of dozens of small fingernail-sized construction paper "
            "squares in red, orange, yellow, green, blue, and purple, scattered together "
            "in a loose pile in the center of a light wood craft table. Some squares are "
            "slightly uneven, clearly cut by a child. A pair of open child-safe scissors "
            "and a few longer paper strips that have been partially cut into squares are "
            "visible to the side. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mosaic-craft-sort-colors.webp",
        "prompt": (
            "A close-up flat lay of a white twelve-cup muffin tin on a light wood craft "
            "table. Each cup holds a small pile of construction paper squares sorted "
            "by single color: red in one cup, orange in another, yellow, green, blue, "
            "purple, pink, and so on. The squares are small, roughly fingernail-sized. "
            "A sheet of white cardstock with a faint pencil heart outline sits next to "
            "the muffin tin. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mosaic-craft-glue-pieces.webp",
        "prompt": (
            "A close-up of a young child's small hand pressing a yellow construction paper "
            "square inside a pencil-drawn heart outline on white cardstock. The heart is "
            "partially filled in with red, orange, and yellow paper squares arranged in "
            "rows from the top, with tiny white gaps visible between each square. The "
            "lower portion of the heart is still empty pencil outline waiting to be filled. "
            "A purple glue stick lies open next to the cardstock. Light wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mosaic-craft-fill-background.webp",
        "prompt": (
            "A close-up overhead shot of a paper mosaic craft on white cardstock. The "
            "rainbow heart in the center is fully complete: red at the top, then orange, "
            "yellow, green, blue, and purple paper squares. Light blue construction paper "
            "squares are being added around the heart to fill the white background, with "
            "about half the background already filled in. Tiny white gaps visible between "
            "all squares. A small pile of leftover blue squares sits beside the cardstock "
            "on a light wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mosaic-craft-finished.webp",
        "prompt": (
            "A finished handmade paper mosaic craft of a rainbow heart shape on white "
            "cardstock, with the background fully filled in with light blue construction "
            "paper squares. The rainbow heart fills the center: red, orange, yellow, "
            "green, blue, and purple rows from top to bottom. A child's name 'Lily' is "
            "written in small black marker letters in the bottom right corner. The "
            "cardstock sits flat on a light wood craft table next to leftover colored "
            "paper squares and a black marker. Charming and clearly handmade by a child. "
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
