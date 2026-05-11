#!/usr/bin/env python3
"""Generate all images for kite-craft-paper.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "kite-craft-paper"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "kite-craft-paper.webp",
        "prompt": (
            "A finished handmade paper kite craft on a light wood craft table. "
            "A bright yellow cardstock diamond shape about 10 inches tall, decorated on the front "
            "with hand-drawn rainbow stripes, hearts, and stars in red, orange, green, blue, and purple marker. "
            "A long rainbow curling ribbon tail flows from the bottom point with three small bright bows tied "
            "along its length. A length of natural jute twine is tied through a punched hole near the top center "
            "to be the kite line. The kite lies flat, viewed from above, slightly angled to show the long tail. "
            "Cheerful spring afternoon mood. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kite-craft-paper-mom-child.webp",
        "prompt": (
            "A warm overhead view of a young American mom and her 5-year-old child sitting together at a light wood "
            "craft table, both smiling, about to start a paper kite craft project. On the table in front of them "
            "are several sheets of colorful cardstock, two thin bamboo skewers, a small roll of rainbow curling ribbon, "
            "a ball of natural jute twine, red kids safety scissors, and a purple glue stick. The mom and child are "
            "leaning in together, both clearly engaged and happy. Soft natural daylight. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kite-craft-paper-cut-diamond.webp",
        "prompt": (
            "A close-up view of a child's small hand using red Fiskars kids safety scissors to cut a folded sheet "
            "of bright yellow cardstock along a faint pencil line. The pencil line traces half of a tall diamond "
            "shape along the folded edge of the paper, with a long bottom point and a shorter top point. "
            "The cardstock fold is clearly visible. A pencil rests beside the paper on a light wood craft table. "
            "No frame or ribbons yet, just the diamond being cut. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kite-craft-paper-decorate.webp",
        "prompt": (
            "An opened-out bright yellow cardstock diamond shape lying flat on a light wood craft table, "
            "the full diamond visible, about 10 inches tall and 8 inches wide. A child's hand is using a "
            "broad-line marker to draw colorful rainbow stripes across the diamond, with red, orange, green, "
            "and blue stripes already drawn and a few hearts and stars in between. A small bundle of Crayola "
            "broad line markers sits next to the diamond. The frame and ribbons are NOT yet attached. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kite-craft-paper-cross-frame.webp",
        "prompt": (
            "A close-up flat lay of two thin natural bamboo skewers laid in a cross shape on a light wood "
            "craft table. The longer vertical skewer is about 9 inches long. The shorter horizontal skewer "
            "is about 7 inches long and crosses the long one near the upper third, not the middle. "
            "A small piece of natural beige string is wrapped a few times around the crossing point and tied "
            "in a neat little knot. No paper kite in this image, just the bare cross frame. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kite-craft-paper-attach-frame.webp",
        "prompt": (
            "The back side of a colorful paper diamond kite craft, lying flat on a light wood craft table. "
            "The back is plain bright yellow cardstock. A bamboo skewer cross is glued flat to the back, "
            "with the long skewer running from top point to bottom point of the diamond and the shorter "
            "skewer reaching to the two side points. The skewers are held in place with a thin line of "
            "dried clear glue along their length. A purple glue stick lies open next to the kite. "
            "The colorful decorated front of the kite is hidden because the back is facing up. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kite-craft-paper-tail-ribbons.webp",
        "prompt": (
            "The back side of a paper diamond kite craft on a light wood craft table, with a long "
            "rainbow curling ribbon tail about 24 inches long taped firmly to the bottom point of the "
            "diamond using a small piece of clear tape. The bamboo skewer cross frame is visible on the back. "
            "The long ribbon tail trails freely off to one side of the kite. No bows tied on the tail yet. "
            "Soft daylight, simple flat lay. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kite-craft-paper-add-bows.webp",
        "prompt": (
            "A finished decorated paper diamond kite craft lying on a light wood craft table, front side up, "
            "with rainbow stripes and stars drawn on the front. The long rainbow curling ribbon tail extends "
            "down from the bottom point of the kite, and three small ribbon bows in bright contrasting colors "
            "(pink, blue, and green) are tied at even spacing along the tail. A pair of red kids safety scissors "
            "rests next to the kite. Cheerful and clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kite-craft-paper-add-string.webp",
        "prompt": (
            "A close-up view of the front of a decorated paper diamond kite craft on a light wood craft table. "
            "Near the top center of the kite, where the two bamboo skewers cross underneath, a small square of "
            "clear tape reinforces the paper, and a single hole has been punched through it. A length of natural "
            "beige jute twine is threaded through the hole and tied in a double knot on the front. "
            "The colorful rainbow stripes and hearts on the kite face are visible. Long tail with bows trails off "
            "the bottom of the frame. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kite-craft-paper-finished.webp",
        "prompt": (
            "A cheerful 5-year-old American child standing in a sunny living room or backyard, holding up a "
            "finished handmade paper kite craft proudly with both hands. The kite is a bright yellow cardstock "
            "diamond about 10 inches tall, decorated with rainbow stripes, hearts and stars, with a long "
            "rainbow curling ribbon tail tied with three small colorful bows trailing down. A length of "
            "natural jute twine is tied to the front of the kite. The child is smiling with sparkly eyes. "
            "Warm natural daylight. "
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
