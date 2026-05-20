#!/usr/bin/env python3
"""Generate all images for gift-paper-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "gift-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy. "
    "The craft must visually fill the frame edge to edge. No padding, no letterboxing, no blank borders."
)

CRAFT_DESCRIPTION = (
    "A handmade greeting card shaped like a wrapped present. "
    "The base is a white folded cardstock rectangle. "
    "Glued onto the center of the front is a smaller bright pink patterned paper rectangle "
    "(the wrapping paper), with a clean white border showing all around. "
    "Two thin yellow paper strips cross the wrapping in a plus sign shape (the ribbon). "
    "A small soft yellow paper bow with two looped sides and a center band is glued where the ribbon strips meet. "
    "A few tiny red heart stickers and small marker dots are scattered around the white border."
)

IMAGES = [
    {
        "filename": "gift-paper-craft.webp",
        "prompt": (
            f"{CRAFT_DESCRIPTION} The finished card sits flat on a light wood craft table, "
            "viewed from slightly above. A few paper scraps and a glue stick lie naturally nearby. "
            "Hero photo for a blog tutorial. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "gift-paper-craft-mom-child.webp",
        "prompt": (
            "A young American mom in her early thirties and her four-year-old child "
            "sitting together at a light wood craft table, smiling warmly. "
            "Spread out in front of them: a sheet of white cardstock, a sheet of bright pink "
            "patterned paper, thin yellow paper strips, a pair of blunt-tip kid scissors, "
            "a glue stick, a few colored markers, and a small sheet of red heart stickers. "
            "They are just starting to make a gift paper craft together. "
            "Sunlight streams through a kitchen window behind them. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "gift-paper-craft-fold-base.webp",
        "prompt": (
            "Step 1 of a paper card craft. A piece of white cardstock has been freshly folded "
            "in half to form a clean rectangular card base, with the fold along the left side. "
            "The card lies flat on a light wood craft table. Beside it, a closed glue stick "
            "and a pair of kid scissors with blue handles. No decoration on the card yet. "
            "Top-down view. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "gift-paper-craft-glue-wrapping.webp",
        "prompt": (
            "Step 2 of a paper card craft. A folded white cardstock card lies flat on a light "
            "wood craft table. A smaller rectangle of bright pink patterned paper has just been "
            "glued onto the center of the front of the card, leaving a clean white border of "
            "about half an inch all the way around. The wrapping rectangle is pressed down smoothly. "
            "An open glue stick lies beside the card. No ribbon strips and no bow yet. "
            "Top-down view. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "gift-paper-craft-add-ribbon.webp",
        "prompt": (
            "Step 3 of a paper card craft. The folded white cardstock card lies on a light wood "
            "craft table with the bright pink patterned wrapping rectangle already glued in the "
            "center of the front. Two thin yellow paper strips have just been glued onto the "
            "wrapping in a plus sign shape: one vertical strip from top to bottom, and one "
            "horizontal strip from left to right, crossing at the center of the wrapping. "
            "Paper scraps and kid scissors lie nearby. No bow yet. Top-down view. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "gift-paper-craft-make-bow.webp",
        "prompt": (
            "Step 4 of a paper card craft. The folded white cardstock card lies on a light wood "
            "craft table. The bright pink patterned wrapping rectangle is glued in the center "
            "of the front, with two thin yellow paper strips crossed in a plus shape across it. "
            "A small soft yellow paper bow with two looped sides and a tiny center band has "
            "just been glued where the two ribbon strips meet at the center. The bow is clearly "
            "handmade from paper. A glue stick and small paper scraps lie beside the card. "
            "No heart stickers yet. Top-down view. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "gift-paper-craft-finished-front.webp",
        "prompt": (
            f"Step 5 of a paper card craft. {CRAFT_DESCRIPTION} The completed front of the card "
            "lies flat on a light wood craft table, viewed from directly above. The decorations "
            "are clearly handmade by a child. Top-down view. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "gift-paper-craft-message-inside.webp",
        "prompt": (
            "Step 6 of a paper card craft. A finished gift paper craft card lies open on a light "
            "wood craft table. The right inner panel of the card is decorated with a young "
            "child's hand-drawn marker message: a colorful rainbow arc, a big red heart, the "
            "words 'I love you' written in wobbly crayon letters, and a small stick figure drawing. "
            "On the left, the wrapped present front cover is just visible at the edge, showing "
            "the bright pink patterned wrapping with crossed yellow ribbons and the small yellow "
            "paper bow. A few colored markers lie open beside the card. Top-down view. "
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
